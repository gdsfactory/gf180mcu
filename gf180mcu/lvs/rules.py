"""gflvs LVS rules for gf180mcu: layers, tracer connectivity, device templates and run config.

Usage::

    import gflvs
    from gf180mcu.lvs.rules import DEFAULT_LVS_CONFIG

    clean, extracted, l2n, report = gflvs.lvs(reference_netlist, gdstk_library, DEFAULT_LVS_CONFIG)

Flip the flags below and call `build_lvs_config()` for a variant config.

Targets the gflvs `dev` API (`gflvs.gflvs_refactor`: `LvsConfig`, `NetlistTracerConfig`,
`ElectricalDeviceExtractionConfig`; protos from `gflvs.gflvs_schema`). gflvs extracts a device only from a
cell's own polygons, so every device PCell must be flat (cap_mim, the diodes and sc_diode call `c.flatten()`).
Templates come from the verified swarm report `templates-gf180mcu.md`.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Iterable, Iterator, Sequence
from itertools import pairwise
from typing import Any

import gdstk
import numpy as np
from gflvs import ElectricalDeviceExtractionConfig, LvsConfig, NetlistTracerConfig
from gflvs.gflvs_schema import (
    DeviceParameterTemplate,
    DeviceTemplate,
    DeviceTerminalTemplate,
    DeviceTerminalType,
    LayerGds,
    LayerOffsetOperation,
    LayerOperation,
    LayerRef,
    LvsRunMode,
)

from gf180mcu.layers import LAYER

# ── Flags ───────────────────────────────────────────────────────────
ENABLE_ELECTRICAL_TRACING = (
    True  # trace metal/via nets; False → tracer galvanic layers empty
)
ENABLE_DEVICE_EXTRACTION = True  # use DEVICE_TEMPLATES; False → connectivity-only LVS
ENABLE_MOSFET_TEMPLATES = True  # nfet/pfet/nfet_06v0_nvt; False → MOSFETs not extracted
ENABLE_MOSCAP_TEMPLATES = True  # cap_mos; False → MOS caps not extracted
ENABLE_MIM_TEMPLATES = True  # cap_mim; False → MIM caps not extracted
ENABLE_DIODE_TEMPLATES = True  # diode_* and sc_diode; False → diodes not extracted
ENABLE_RESISTOR_TEMPLATES = (
    True  # res (metal, poly, diffusion, nwell); False → resistors not extracted
)
ENABLE_PARAMETER_CHECK = True  # False → every template blackboxed (topology only)
HIERARCHICAL_RUN = False  # True → LVS_RUN_MODE_HIERARCHICAL, else FLAT
VERBOSE = False  # True → LvsConfig.verbose=1
PARAMETER_RELATIVE_TOLERANCE = 1e-3  # relative tolerance for parameter comparison

LayerKey = tuple[int, int]
Polygons = list[gdstk.Polygon]

# ── Helpers ─────────────────────────────────────────────────────────
# ponytail: duplicated per PDK repo; move to gflvs when it ships helpers
PIN = DeviceTerminalType.DEVICE_TERMINAL_TYPE_PIN
Op = LayerRef | LayerOperation


def key(layer: Any) -> LayerKey:
    """(layer, datatype) of a PDK LAYER member."""
    return (layer.layer, layer.datatype)


def L(layer: Any) -> LayerRef:
    """LayerRef for a PDK LAYER member."""
    return LayerRef(layer=LayerGds(layer=layer.layer, datatype=layer.datatype))


def op(x: Op) -> LayerOperation:
    """Wrap a bare LayerRef as a LayerOperation."""
    return x if isinstance(x, LayerOperation) else LayerOperation(layer_ref_left=x)


def grow(x: Op, d: float) -> LayerOperation:
    """Isotropic sizing by d µm: confines an op to one device's neighbourhood."""
    return LayerOperation(
        layer_op_left=op(x), offset_op=LayerOffsetOperation(offset_x=d, offset_y=d)
    )


def on(anchor: Op, region: Op) -> LayerOperation:
    """Region geometry keyed on the anchor layer, so it binds to routes on that layer."""
    return op((anchor & region) | region)


def pin(name: str, x: Op) -> DeviceTerminalTemplate:
    """Electrical terminal template."""
    return DeviceTerminalTemplate(
        terminal_name=name, terminal_type=PIN, layer_composed_op=op(x)
    )


def par(name: str, x: Op, extractor: str) -> DeviceParameterTemplate:
    """Parameter template; extractor is a gflvs built-in or a PARAMETER_EXTRACTORS name."""
    return DeviceParameterTemplate(
        name=name, layer_composed_op=op(x), properties={"extractor": extractor}
    )


def tpl(
    name: str,
    cls: str,
    terms: Sequence[DeviceTerminalTemplate],
    params: Sequence[DeviceParameterTemplate],
) -> DeviceTemplate:
    """Device template."""
    return DeviceTemplate(
        device_name=name,
        device_class_name=cls,
        device_terminal_template=list(terms),
        device_parameter_template=list(params),
    )


def _points(polygons: Polygons) -> np.ndarray[Any, Any]:
    return np.vstack([p.points for p in polygons])


def bbox_x(polygons: Polygons) -> float:
    """X extent of the region (nan if empty)."""
    return float(np.ptp(_points(polygons)[:, 0])) if polygons else float("nan")


def bbox_y(polygons: Polygons) -> float:
    """Y extent of the region (nan if empty)."""
    return float(np.ptp(_points(polygons)[:, 1])) if polygons else float("nan")


def sum_bbox_y(polygons: Polygons) -> float:
    """Summed y extent of the region's polygons, e.g. total MOS gate width w_gate*nf (nan if empty)."""
    return (
        sum(float(np.ptp(_points([p])[:, 1])) for p in polygons)
        if polygons
        else float("nan")
    )


def area(polygons: Polygons) -> float:
    """Total area of the region (nan if empty)."""
    return float(sum(p.area() for p in polygons)) if polygons else float("nan")


def perimeter(polygons: Polygons) -> float:
    """Total perimeter of the region (nan if empty)."""
    return float(sum(p.perimeter() for p in polygons)) if polygons else float("nan")


def _leaf_layers(operation: LayerOperation) -> Iterator[LayerKey]:
    """Every layer an op reads."""
    for side in ("left", "right"):
        match operation.WhichOneof(f"layer_{side}"):
            case None:
                continue
            case name if name == f"layer_ref_{side}":
                layer = getattr(operation, name).layer
                yield (layer.layer, layer.datatype)
            case name:
                yield from _leaf_layers(getattr(operation, name))


def connectivity(chains: Iterable[Sequence[Any]]) -> dict[LayerKey, list[LayerKey]]:
    """Symmetric layer adjacency from chains of PDK layers, e.g. (metal1, via1, metal2)."""
    neighbours: defaultdict[LayerKey, set[LayerKey]] = defaultdict(set)
    for chain in chains:
        for a, b in pairwise(map(key, chain)):
            neighbours[a].add(b)
            neighbours[b].add(a)
    return {layer: sorted(adjacent) for layer, adjacent in neighbours.items()}


# ── Layers ──────────────────────────────────────────────────────────
comp, poly2, metal1, metal2, metal3 = (
    L(LAYER.comp),
    L(LAYER.poly2),
    L(LAYER.metal1),
    L(LAYER.metal2),
    L(LAYER.metal3),
)
nplus, pplus, nwell, lvpwell, dnwell = (
    L(LAYER.nplus),
    L(LAYER.pplus),
    L(LAYER.nwell),
    L(LAYER.lvpwell),
    L(LAYER.dnwell),
)
dualgate, nat, sab, res_mk, resistor = (
    L(LAYER.dualgate),
    L(LAYER.nat),
    L(LAYER.sab),
    L(LAYER.res_mk),
    L(LAYER.resistor),
)
diode_mk, mos_cap_mk, cap_mk, fusetop = (
    L(LAYER.diode_mk),
    L(LAYER.mos_cap_mk),
    L(LAYER.cap_mk),
    L(LAYER.fusetop),
)
schottky = L(LAYER.schottky_diode)

MARKER_LAYERS: frozenset[LayerKey] = frozenset(
    key(layer)
    for layer in (
        LAYER.res_mk,
        LAYER.diode_mk,
        LAYER.mos_cap_mk,
        LAYER.cap_mk,
        LAYER.schottky_diode,
        LAYER.dualgate,
        LAYER.nat,
        *(getattr(LAYER, f"metal{i}_res") for i in range(1, 7)),
    )
)  # add_electrical_pins draws no pin geometry, so no pin layers here
NO_MARKER_TEMPLATES: frozenset[str] = frozenset(
    {
        "nmos_3p3",  # 3.3 V MOS has no recognition layer (dualgate/nat only mark 6 V/native); gated on poly2&comp
        "pmos_3p3",  # same
    }
)

# Grow distances (µm). ponytail: tuned on PCell geometry; re-measure if PCell rules change
GATE_REACH = 1.0  # gate → its poly2 and metal1 gate pads
SD_REACH = 2.0  # gate → S/D comp
TAP_REACH = 3.0  # gate → bulk tap comp
MOSCAP_REACH = 1.0  # mos_cap_mk → gate poly2/pads and S/D comp
MIM_BOTTOM_REACH = 4.0  # cap_mk → metal2 bottom-plate route
DIODE_TAP_REACH = 2.0  # nd2ps/pd2nw junction → opposite tap comp
WELL_DIODE_REACH = 1.0  # nw2ps/pw2dw marker key → taps and well body
TAP_TO_WELL = 0.5  # tap grown to the well edge so the terminal and body bboxes touch
DW_GUARD_REACH = 4.0  # dw2ps key → p+ guard ring comp
DW_BODY_REACH = 2.0  # dw2ps key → dnwell body
SC_ANODE_GAP = 0.1  # sc_diode: cathode region excludes the anode comp grown by this
RES_HEAD_REACH = 1.0  # resistor body → its head contacts region
RES_RING_REACH = 3.0  # resistor body → guard-ring comp
METAL_RES_HEAD = 0.5  # metal*_res marker → metal head beyond it

# Tracer connectivity. The PDK has no Python `connectivity`; chains come from the gf180mcu KLayout LVS deck
# (gf180mcu.lvs:1061-1084, 1256-1266).
# TODO(issue: pending): gf180mcu PDK lacks a Python `connectivity` list.
LAYER_CONNECTIVITY: dict[LayerKey, list[LayerKey]] = connectivity(
    [
        # comp/poly2 not traced: device bodies, would short S/D and resistor heads in any parent cell
        (LAYER.contact, LAYER.metal1),
        (LAYER.metal1, LAYER.via1, LAYER.metal2),
        (LAYER.metal2, LAYER.via2, LAYER.metal3),
        (LAYER.metal3, LAYER.via3, LAYER.metal4),
        (LAYER.metal4, LAYER.via4, LAYER.metal5),
        (LAYER.metal5, LAYER.via5, LAYER.metaltop),
        # fusetop–via2–metal3 (deck MIM-A) not traced: fusetop is a cap plate; the MIM top terminal binds on metal3
    ]
)


# ── Templates ───────────────────────────────────────────────────────
# python precedence: `-` binds tighter than `&`, `&` tighter than `|`: every step is parenthesised


def mos(name: str, cls: str, gate: Op, sd_imp: Op, tap_imp: Op) -> DeviceTemplate:
    """MOSFET (SPICE D G S B); w = w_gate*nf, D/S alternate left to right."""
    sd = ((comp & sd_imp) & grow(gate, SD_REACH)) - poly2
    tap = (comp & tap_imp) & grow(gate, TAP_REACH)
    return tpl(
        name,
        cls,
        [
            pin("D/S", on(metal1, sd)),
            pin(
                "G", (metal1 & poly2) & grow(gate, GATE_REACH)
            ),  # metal1 gate pads; poly2 gates aren't traced
            pin("B", on(metal1, tap)),
        ],
        [
            par("l", poly2 & grow(gate, GATE_REACH), "length"),
            par(
                "w", gate, "sum_bbox_y"
            ),  # schematic w = w_gate*nf (report used the per-finger mean)
            par("nf", gate, "count"),
        ],
    )


ngate = (poly2 & comp) & nplus
pgate = ((poly2 & comp) & pplus) & nwell
MOSFET_TEMPLATES = [
    # CONFIDENCE: HIGH
    mos(
        "nmos_3p3",
        "nfet",
        (((ngate - nwell) - dualgate) - nat) - mos_cap_mk,
        nplus,
        pplus,
    ),
    # CONFIDENCE: HIGH
    mos(
        "nmos_6p0",
        "nfet",
        (((ngate & dualgate) - nwell) - nat) - mos_cap_mk,
        nplus,
        pplus,
    ),
    # CONFIDENCE: HIGH
    mos("pmos_3p3", "pfet", (pgate - dualgate) - mos_cap_mk, pplus, nplus),
    # CONFIDENCE: HIGH
    mos("pmos_6p0", "pfet", (pgate & dualgate) - mos_cap_mk, pplus, nplus),
    # CONFIDENCE: HIGH
    mos(
        "nmos_6p0_nat",
        "nfet_06v0_nvt",
        ((ngate & nat) & dualgate) - nwell,
        nplus,
        pplus,
    ),
]


def moscap(name: str, body: Op) -> DeviceTemplate:
    """MOS capacitor (SPICE gate source_drain)."""
    sd = ((comp & nplus) & grow(body, MOSCAP_REACH)) - poly2
    return tpl(
        name,
        "cap_mos",
        [
            pin("gate", (metal1 & poly2) & grow(body, MOSCAP_REACH)),
            pin("source_drain", on(metal1, sd)),
        ],
        [
            par("c_length", poly2 & grow(body, MOSCAP_REACH), "bbox_x"),
            par("c_width", body, "bbox_y"),
        ],
    )


# TODO(issue: pending): cap_mos(type="cap_pmos") draws the nmos layers, so it extracts as nmoscap_3p3.
# TODO(issue: pending): cap_mos draws poly 0.36 wide when lc < 0.36, so c_length extracts as 0.36.
MOSCAP_TEMPLATES = [
    # CONFIDENCE: HIGH for lc >= 0.36
    moscap("nmoscap_3p3", ((mos_cap_mk & nplus) & nwell) - dualgate),
    # CONFIDENCE: HIGH for lc >= 0.36
    moscap("nmoscap_6p0", ((mos_cap_mk & nplus) & nwell) & dualgate),
]

# CONFIDENCE: MEDIUM (verified only after flattening)
# TODO(issue: pending): cap_mim has no metal2 bottom plate under fusetop, the bottom port sits in that hole,
# and MIM-B is not implemented.
MIM_TEMPLATES = [
    tpl(
        "mim_2p0fF",
        "cap_mim",
        [
            pin("top", (metal3 & fusetop) & cap_mk),
            pin("bottom", metal2 & grow(cap_mk, MIM_BOTTOM_REACH)),
        ],
        [
            par("c_length", fusetop & cap_mk, "bbox_y"),
            par("c_width", fusetop & cap_mk, "bbox_x"),
        ],
    )
]


def diode(name: str, cls: str, anode: Op, cathode: Op, body: Op) -> DeviceTemplate:
    """Diode (SPICE anode cathode); area in µm², pj in µm."""
    return tpl(
        name,
        cls,
        [pin("anode", on(metal1, anode)), pin("cathode", on(metal1, cathode))],
        [par("area", body, "area"), par("pj", body, "perimeter")],
    )


def tap_to(tap: Op, well: Op) -> LayerOperation:
    """Tap grown to the well edge, so the tap and body bboxes touch."""
    return grow(tap, TAP_TO_WELL) - well


np_k = (((comp & nplus) & diode_mk) - nwell) - dnwell
pn_a = ((comp & pplus) & diode_mk) & nwell
nwp_key = (diode_mk & nplus) & nwell
dnwpw_key = ((diode_mk & pplus) & lvpwell) & dnwell
dnwps_key = ((diode_mk & nplus) & dnwell) - lvpwell
sc_key = schottky & dnwell
sc_a = (comp & sc_key) - nplus
DIODE_TEMPLATES = [
    # CONFIDENCE: HIGH (flattened PCell)
    diode(
        "np_3p3",
        "diode_nd2ps",
        ((comp & pplus) & grow(np_k - dualgate, DIODE_TAP_REACH)) - nwell,
        np_k - dualgate,
        np_k - dualgate,
    ),
    # CONFIDENCE: HIGH (flattened PCell)
    diode(
        "np_6p0",
        "diode_nd2ps",
        ((comp & pplus) & grow(np_k & dualgate, DIODE_TAP_REACH)) - nwell,
        np_k & dualgate,
        np_k & dualgate,
    ),
    # CONFIDENCE: HIGH (flattened PCell)
    diode(
        "pn_3p3",
        "diode_pd2nw",
        pn_a - dualgate,
        ((comp & nplus) & nwell) & grow(pn_a - dualgate, DIODE_TAP_REACH),
        pn_a - dualgate,
    ),
    # CONFIDENCE: HIGH (flattened PCell)
    diode(
        "pn_6p0",
        "diode_pd2nw",
        pn_a & dualgate,
        ((comp & nplus) & nwell) & grow(pn_a & dualgate, DIODE_TAP_REACH),
        pn_a & dualgate,
    ),
    # CONFIDENCE: MEDIUM (no metal1 at the ports: comp+implant+well only)
    diode(
        "nwp_3p3",
        "diode_nw2ps",
        tap_to(((comp & pplus) & grow(nwp_key, WELL_DIODE_REACH)) - nwell, nwell),
        ((comp & nplus) & nwell) & grow(nwp_key, WELL_DIODE_REACH),
        nwell & grow(nwp_key, WELL_DIODE_REACH),
    ),
    # CONFIDENCE: MEDIUM (no metal1 at the ports: comp+implant+well only)
    diode(
        "dnwpw",
        "diode_pw2dw",
        ((comp & pplus) & lvpwell) & grow(dnwpw_key, WELL_DIODE_REACH),
        tap_to(
            (((comp & nplus) & dnwell) & grow(dnwpw_key, WELL_DIODE_REACH)) - lvpwell,
            lvpwell,
        ),
        lvpwell & grow(dnwpw_key, WELL_DIODE_REACH),
    ),
    # CONFIDENCE: LOW (anode only when pcmpgr=True)
    # TODO(issue: pending): diode_dw2ps guard-ring comp is 0.1 wide with contacts outside it; anode port off comp.
    diode(
        "dnwps",
        "diode_dw2ps",
        ((comp & pplus) & grow(dnwps_key, DW_GUARD_REACH)) - dnwell,
        (comp & nplus) & dnwps_key,
        (dnwell & diode_mk) & grow(dnwps_key, DW_BODY_REACH),
    ),
    # CONFIDENCE: LOW (static check only, at la=wa=cw=1)
    # TODO(issue: pending): sc_diode metal1 straps miss the contacts and the ports are off the terminals.
    diode("sc_diode", "sc_diode", sc_a, sc_key - grow(sc_a, SC_ANODE_GAP), sc_a),
]


def res(name: str, body: Op, head: Op, ring_imp: Op) -> DeviceTemplate:
    """Poly/diffusion/well resistor (SPICE r0 r1 bulk); PCell frame: length along y, r0 on top."""
    heads = (head & grow(body, RES_HEAD_REACH)) - res_mk
    return tpl(
        name,
        "res",
        [
            pin("r1/r0", on(metal1, heads)),
            pin("bulk", on(metal1, (comp & ring_imp) & grow(body, RES_RING_REACH))),
        ],
        [par("r_length", body, "length"), par("r_width", body, "bbox_x")],
    )


def metal_res(name: str, metal: Any, marker: Any) -> DeviceTemplate:
    """Metal resistor (SPICE r0 r1) under a metal*_res marker."""
    m, mk = L(metal), L(marker)
    return tpl(
        name,
        "res",
        [pin("r1/r0", (m & grow(mk, METAL_RES_HEAD)) - mk)],
        [par("r_length", m & mk, "length"), par("r_width", m & mk, "bbox_x")],
    )


poly_body = poly2 & res_mk
RESISTOR_TEMPLATES = [
    # CONFIDENCE: HIGH
    metal_res("rm1", LAYER.metal1, LAYER.metal1_res),
    # CONFIDENCE: HIGH
    metal_res("rm2", LAYER.metal2, LAYER.metal2_res),
    # CONFIDENCE: HIGH
    metal_res("rm3", LAYER.metal3, LAYER.metal3_res),
    # CONFIDENCE: HIGH
    res("ppolyf_u", (((poly_body & pplus) & sab) - resistor) - dualgate, poly2, nplus),
    # CONFIDENCE: HIGH
    res("ppolyf_s", ((poly_body & pplus) - sab) - resistor, poly2, nplus),
    # CONFIDENCE: HIGH
    res("npolyf_u", (((poly_body & nplus) & sab) - resistor) - dualgate, poly2, pplus),
    # CONFIDENCE: HIGH
    res("npolyf_s", ((poly_body & nplus) - sab) - resistor, poly2, nplus),
    # CONFIDENCE: HIGH
    res("ppolyf_u_1k", ((poly_body & sab) & resistor) - dualgate, poly2, pplus),
    # CONFIDENCE: HIGH
    res("ppolyf_u_1k_6p0", ((poly_body & sab) & resistor) & dualgate, poly2, pplus),
    # CONFIDENCE: HIGH
    res("nplus_u", (((comp & res_mk) & nplus) & sab) & lvpwell, comp & nplus, pplus),
    # CONFIDENCE: HIGH
    res("pplus_u", (((comp & res_mk) & pplus) & sab) & nwell, comp & pplus, nplus),
    # CONFIDENCE: LOW (blocked: never fires as drawn)
    # TODO(issue: pending): the nwell resistor PCell draws no res_mk, which the deck needs (nwell & res_mk).
    res("nwell", ((nwell & res_mk) - comp) - poly2, nwell, pplus),
]

DEVICE_TEMPLATES: list[DeviceTemplate] = [
    *MOSFET_TEMPLATES,
    *MOSCAP_TEMPLATES,
    *MIM_TEMPLATES,
    *DIODE_TEMPLATES,
    *RESISTOR_TEMPLATES,
]

_EXTRACTORS: dict[str, Callable[[Polygons], float]] = {
    "bbox_x": bbox_x,
    "bbox_y": bbox_y,
    "sum_bbox_y": sum_bbox_y,
    "area": area,
    "perimeter": perimeter,
}
# the built-in "width" picks the long side edges of long terminals, so widths use bbox extractors instead
PARAMETER_EXTRACTORS: dict[tuple[str, str], Callable[[Polygons], float]] = {
    (t.device_name, p.name): _EXTRACTORS[p.properties["extractor"]]
    for t in DEVICE_TEMPLATES
    for p in t.device_parameter_template
    if p.properties["extractor"] in _EXTRACTORS
}

# lowercase cell-name prefixes traced through, never device-extracted (gflvs default; no straight_heater here)
PASSTHROUGH_DEVICE_CLASS_NAMES: tuple[str, ...] = ("via", "straight", "bend")


# ── Config ──────────────────────────────────────────────────────────
def _blackbox(template: DeviceTemplate) -> DeviceTemplate:
    copy = DeviceTemplate()
    copy.CopyFrom(template)
    copy.properties["blackbox"] = "true"
    return copy


def build_lvs_config() -> LvsConfig:
    """LvsConfig from the module flags, read at call time."""
    groups = (
        (ENABLE_MOSFET_TEMPLATES, MOSFET_TEMPLATES),
        (ENABLE_MOSCAP_TEMPLATES, MOSCAP_TEMPLATES),
        (ENABLE_MIM_TEMPLATES, MIM_TEMPLATES),
        (ENABLE_DIODE_TEMPLATES, DIODE_TEMPLATES),
        (ENABLE_RESISTOR_TEMPLATES, RESISTOR_TEMPLATES),
    )
    templates = (
        [t for enabled, group in groups if enabled for t in group]
        if ENABLE_DEVICE_EXTRACTION
        else []
    )
    if not ENABLE_PARAMETER_CHECK:
        templates = [_blackbox(t) for t in templates]
    extraction_layers = frozenset(
        layer
        for t in templates
        for x in (*t.device_terminal_template, *t.device_parameter_template)
        for layer in _leaf_layers(x.layer_composed_op)
    )
    return LvsConfig(
        device_templates=templates,
        netlist_tracer_config=NetlistTracerConfig(
            layer_connectivity=LAYER_CONNECTIVITY,
            # routing metals, contact and vias only: comp/poly2/fusetop are device bodies
            galvanic_drawing_layers=frozenset(LAYER_CONNECTIVITY)
            if ENABLE_ELECTRICAL_TRACING
            else frozenset(),
            passthrough_device_class_names=PASSTHROUGH_DEVICE_CLASS_NAMES,
        ),
        electrical_device_extraction_config=ElectricalDeviceExtractionConfig(
            galvanic_drawing_layers=extraction_layers,
            parameter_extractors=PARAMETER_EXTRACTORS,
        ),
        parameter_relative_tolerance=PARAMETER_RELATIVE_TOLERANCE,
        run_mode=LvsRunMode.LVS_RUN_MODE_HIERARCHICAL
        if HIERARCHICAL_RUN
        else LvsRunMode.LVS_RUN_MODE_FLAT,
        verbose=int(VERBOSE),
    )


DEFAULT_LVS_CONFIG = build_lvs_config()
