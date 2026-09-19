"""LVS configuration for the GlobalFoundries 180nm MCU PDK.

CONFIDENCE annotations:
  HIGH   — layer stack unambiguous, matches proven patterns
  MEDIUM — layer stack inferred from connectivity; single plausible interpretation
  LOW    — multiple interpretations possible; manual verification required

CRITICAL notes:
  1. No pin/label layers exist for comp, poly2, or contact in the gf180mcu LayerMap.
     Terminal extraction for substrate-connected ports relies on drawing-layer polygon
     overlap only (comp AND contact AND metal1 intersection).
  2. Diode parameter extraction has no clean single encoding layer; guard ring comp
     polygons overlap the active diffusion area.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from gflvs.electrical_device import (
    default_device_parameter_extract_count,
    default_device_parameter_extract_height,
    default_device_parameter_extract_width,
)
from gflvs.gflvs_schema import (
    DeviceParameterTemplate,
    DeviceTemplate,
    LayerBooleanOperation,
    LayerComposedOperation,
    LayerGds,
    LayerRef,
    LvsRunConfig,
    LvsRunMode,
)
from gflvs.gflvs_schema.lvs_config import ConnectivityKeyValuePair
from gflvs.helpers import build_terminal_from_overlapping_layers, lr
from gflvs.lvs import LvsResult, run_lvs

if TYPE_CHECKING:
    from gdsfactory import Component
    from gdstk import Library
    from gflvs.gflvs_schema.circuit import Circuit
    from gflvs.gflvs_schema.layout_to_netlist import Device
    from gflvs.gflvs_schema.layout_to_netlist import Port as SchemaPort
    from gflvs.tech import GdsTable

# ── GDS Layer Table ───────────────────────────────────────────────────────────

GDS_TABLE: dict[str, LayerGds] = {
    "Compdrawing": LayerGds(layer=22, datatype=0),
    "Poly2drawing": LayerGds(layer=30, datatype=0),
    "Contactdrawing": LayerGds(layer=33, datatype=0),
    "Metal1drawing": LayerGds(layer=34, datatype=0),
    "Metal1pin": LayerGds(layer=34, datatype=2),
    "Metal1label": LayerGds(layer=34, datatype=10),
    "Via1drawing": LayerGds(layer=35, datatype=0),
    "Metal2drawing": LayerGds(layer=36, datatype=0),
    "Metal2pin": LayerGds(layer=36, datatype=2),
    "Metal2label": LayerGds(layer=36, datatype=10),
    "Via2drawing": LayerGds(layer=38, datatype=0),
    "Metal3drawing": LayerGds(layer=42, datatype=0),
    "Metal3pin": LayerGds(layer=42, datatype=2),
    "Metal3label": LayerGds(layer=42, datatype=10),
    "Via3drawing": LayerGds(layer=40, datatype=0),
    "Metal4drawing": LayerGds(layer=46, datatype=0),
    "Metal4pin": LayerGds(layer=46, datatype=2),
    "Metal4label": LayerGds(layer=46, datatype=10),
    "Via4drawing": LayerGds(layer=41, datatype=0),
    "Metal5drawing": LayerGds(layer=81, datatype=0),
    "Metal5pin": LayerGds(layer=81, datatype=2),
    "Metal5label": LayerGds(layer=81, datatype=10),
    "Via5drawing": LayerGds(layer=82, datatype=0),
    "Metaltopdrawing": LayerGds(layer=53, datatype=0),
    "Metaltoppin": LayerGds(layer=53, datatype=2),
    "Metaltoplabel": LayerGds(layer=53, datatype=10),
    "Nwelldrawing": LayerGds(layer=21, datatype=0),
    "Lvpwelldrawing": LayerGds(layer=204, datatype=0),
    "Dnwelldrawing": LayerGds(layer=12, datatype=0),
    "Nplusdrawing": LayerGds(layer=32, datatype=0),
    "Pplusdrawing": LayerGds(layer=31, datatype=0),
    "FuseTopdrawing": LayerGds(layer=75, datatype=0),
    "Metal1Resdrawing": LayerGds(layer=110, datatype=11),
    "Metal2Resdrawing": LayerGds(layer=110, datatype=12),
    "Metal3Resdrawing": LayerGds(layer=110, datatype=13),
    "ResMkdrawing": LayerGds(layer=110, datatype=5),
    "Resistordrawing": LayerGds(layer=62, datatype=0),
}

# ── Layer Lists ───────────────────────────────────────────────────────────────

DRAWING_LAYERS: list[str] = [
    "Metal1drawing",
    "Metal2drawing",
    "Metal3drawing",
    "Metal4drawing",
    "Metal5drawing",
    "Metaltopdrawing",
]

VIA_DRAWING_LAYERS: list[str] = [
    "Contactdrawing",
    "Via1drawing",
    "Via2drawing",
    "Via3drawing",
    "Via4drawing",
    "Via5drawing",
]

PIN_LOGIC_LAYERS: list[str] = [
    "Metal1pin",
    "Metal2pin",
    "Metal3pin",
    "Metal4pin",
    "Metal5pin",
    "Metaltoppin",
]

LABEL_LOGIC_LAYERS: list[str] = [
    "Metal1label",
    "Metal2label",
    "Metal3label",
    "Metal4label",
    "Metal5label",
    "Metaltoplabel",
]

# ── Layer Connectivity ────────────────────────────────────────────────────────

LAYER_CONNECTIVITY: dict[str, list[str]] = {
    "Metal1pin": ["Metal1drawing"],
    "Metal1label": ["Metal1drawing"],
    "Metal2pin": ["Metal2drawing"],
    "Metal2label": ["Metal2drawing"],
    "Metal3pin": ["Metal3drawing"],
    "Metal3label": ["Metal3drawing"],
    "Metal4pin": ["Metal4drawing"],
    "Metal4label": ["Metal4drawing"],
    "Metal5pin": ["Metal5drawing"],
    "Metal5label": ["Metal5drawing"],
    "Metaltoppin": ["Metaltopdrawing"],
    "Metaltoplabel": ["Metaltopdrawing"],
    "Compdrawing": ["Contactdrawing"],
    "Poly2drawing": ["Contactdrawing"],
    "Lvpwelldrawing": ["Compdrawing"],
    "Nwelldrawing": ["Compdrawing", "Lvpwelldrawing"],
    "Dnwelldrawing": ["Nwelldrawing"],
    "Nplusdrawing": ["Compdrawing"],
    "Pplusdrawing": ["Compdrawing"],
    "Contactdrawing": ["Metal1drawing"],
    "Metal1drawing": ["Via1drawing"],
    "Via1drawing": ["Metal2drawing"],
    "Metal2drawing": ["Via2drawing"],
    "Via2drawing": ["Metal3drawing"],
    "Metal3drawing": ["Via3drawing"],
    "Via3drawing": ["Metal4drawing"],
    "Metal4drawing": ["Via4drawing"],
    "Via4drawing": ["Metal5drawing"],
    "Metal5drawing": ["Via5drawing"],
    "Via5drawing": ["Metaltopdrawing"],
}

# ── Device Family Switches ────────────────────────────────────────────────────

INCLUDE_FET = True
INCLUDE_RESISTORS = True
INCLUDE_CAPACITORS = True
INCLUDE_DIODES = True
INCLUDE_GUARDRING = True
INCLUDE_VIA_CELLS = True

# ── Shared Layer Operations ───────────────────────────────────────────────────

_gate_overlap_op = LayerComposedOperation(
    layer_a_ref=LayerRef(canonical_layer_name="Compdrawing", layer_gds=GDS_TABLE["Compdrawing"]),
    layer_b_ref=LayerRef(canonical_layer_name="Poly2drawing", layer_gds=GDS_TABLE["Poly2drawing"]),
    bool_op=LayerBooleanOperation.AND,
)
_fusetop_op = LayerComposedOperation(
    layer_a_ref=LayerRef(canonical_layer_name="FuseTopdrawing", layer_gds=GDS_TABLE["FuseTopdrawing"]),
)
_metal1_res_op = LayerComposedOperation(
    layer_a_ref=LayerRef(canonical_layer_name="Metal1Resdrawing", layer_gds=GDS_TABLE["Metal1Resdrawing"]),
)
_metal2_res_op = LayerComposedOperation(
    layer_a_ref=LayerRef(canonical_layer_name="Metal2Resdrawing", layer_gds=GDS_TABLE["Metal2Resdrawing"]),
)
_metal3_res_op = LayerComposedOperation(
    layer_a_ref=LayerRef(canonical_layer_name="Metal3Resdrawing", layer_gds=GDS_TABLE["Metal3Resdrawing"]),
)
_res_mk_op = LayerComposedOperation(
    layer_a_ref=LayerRef(canonical_layer_name="ResMkdrawing", layer_gds=GDS_TABLE["ResMkdrawing"]),
)
_resistor_op = LayerComposedOperation(
    layer_a_ref=LayerRef(canonical_layer_name="Resistordrawing", layer_gds=GDS_TABLE["Resistordrawing"]),
)

# ── Device Templates ──────────────────────────────────────────────────────────

# CONFIDENCE: MEDIUM
NFET_TEMPLATE = DeviceTemplate(
    device_name="nfet",
    device_class_name="nfet",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "SD_terminals", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "Gate_terminals", ["Poly2drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="w", layer_composed_op=[_gate_overlap_op], extract=default_device_parameter_extract_height),
        DeviceParameterTemplate(uid=1, name="l", layer_composed_op=[_gate_overlap_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=2, name="nf", layer_composed_op=[_gate_overlap_op], extract=default_device_parameter_extract_count),
    ],
)

# CONFIDENCE: MEDIUM
PFET_TEMPLATE = DeviceTemplate(
    device_name="pfet",
    device_class_name="pfet",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "SD_terminals", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "Gate_terminals", ["Poly2drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="w", layer_composed_op=[_gate_overlap_op], extract=default_device_parameter_extract_height),
        DeviceParameterTemplate(uid=1, name="l", layer_composed_op=[_gate_overlap_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=2, name="nf", layer_composed_op=[_gate_overlap_op], extract=default_device_parameter_extract_count),
    ],
)

# CONFIDENCE: MEDIUM
NFET_06V0_NVT_TEMPLATE = DeviceTemplate(
    device_name="nfet_06v0_nvt",
    device_class_name="nfet_06v0_nvt",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "SD_terminals", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "Gate_terminals", ["Poly2drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="w", layer_composed_op=[_gate_overlap_op], extract=default_device_parameter_extract_height),
        DeviceParameterTemplate(uid=1, name="l", layer_composed_op=[_gate_overlap_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=2, name="nf", layer_composed_op=[_gate_overlap_op], extract=default_device_parameter_extract_count),
    ],
)

# CONFIDENCE: HIGH
RES_RM1_TEMPLATE = DeviceTemplate(
    device_name="res_rm1",
    device_class_name="res",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "R0_terminal", ["Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "R1_terminal", ["Metal1drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="w_res", layer_composed_op=[_metal1_res_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=1, name="l_res", layer_composed_op=[_metal1_res_op], extract=default_device_parameter_extract_height),
    ],
)

# CONFIDENCE: HIGH
RES_RM2_TEMPLATE = DeviceTemplate(
    device_name="res_rm2",
    device_class_name="res",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "R0_terminal", ["Metal2drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "R1_terminal", ["Metal2drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="w_res", layer_composed_op=[_metal2_res_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=1, name="l_res", layer_composed_op=[_metal2_res_op], extract=default_device_parameter_extract_height),
    ],
)

# CONFIDENCE: HIGH
RES_RM3_TEMPLATE = DeviceTemplate(
    device_name="res_rm3",
    device_class_name="res",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "R0_terminal", ["Metal3drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "R1_terminal", ["Metal3drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="w_res", layer_composed_op=[_metal3_res_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=1, name="l_res", layer_composed_op=[_metal3_res_op], extract=default_device_parameter_extract_height),
    ],
)

# CONFIDENCE: MEDIUM
RES_PPOLYF_U_TEMPLATE = DeviceTemplate(
    device_name="res_ppolyf_u",
    device_class_name="res",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "R0_terminal", ["Poly2drawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "R1_terminal", ["Poly2drawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="w_res", layer_composed_op=[_res_mk_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=1, name="l_res", layer_composed_op=[_res_mk_op], extract=default_device_parameter_extract_height),
    ],
)

# CONFIDENCE: MEDIUM
RES_NPOLYF_U_TEMPLATE = DeviceTemplate(
    device_name="res_npolyf_u",
    device_class_name="res",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "R0_terminal", ["Poly2drawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "R1_terminal", ["Poly2drawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="w_res", layer_composed_op=[_res_mk_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=1, name="l_res", layer_composed_op=[_res_mk_op], extract=default_device_parameter_extract_height),
    ],
)

# CONFIDENCE: MEDIUM
RES_PPOLYF_S_TEMPLATE = DeviceTemplate(
    device_name="res_ppolyf_s",
    device_class_name="res",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "R0_terminal", ["Poly2drawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "R1_terminal", ["Poly2drawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="w_res", layer_composed_op=[_res_mk_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=1, name="l_res", layer_composed_op=[_res_mk_op], extract=default_device_parameter_extract_height),
    ],
)

# CONFIDENCE: MEDIUM
RES_NPOLYF_S_TEMPLATE = DeviceTemplate(
    device_name="res_npolyf_s",
    device_class_name="res",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "R0_terminal", ["Poly2drawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "R1_terminal", ["Poly2drawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="w_res", layer_composed_op=[_res_mk_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=1, name="l_res", layer_composed_op=[_res_mk_op], extract=default_device_parameter_extract_height),
    ],
)

# CONFIDENCE: MEDIUM
RES_NPLUS_U_TEMPLATE = DeviceTemplate(
    device_name="res_nplus_u",
    device_class_name="res",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "R0_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "R1_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="w_res", layer_composed_op=[_res_mk_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=1, name="l_res", layer_composed_op=[_res_mk_op], extract=default_device_parameter_extract_height),
    ],
)

# CONFIDENCE: MEDIUM
RES_PPLUS_U_TEMPLATE = DeviceTemplate(
    device_name="res_pplus_u",
    device_class_name="res",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "R0_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "R1_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="w_res", layer_composed_op=[_res_mk_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=1, name="l_res", layer_composed_op=[_res_mk_op], extract=default_device_parameter_extract_height),
    ],
)

# CONFIDENCE: MEDIUM
RES_NWELL_TEMPLATE = DeviceTemplate(
    device_name="res_nwell",
    device_class_name="res",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "R0_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "R1_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="w_res", layer_composed_op=[_resistor_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=1, name="l_res", layer_composed_op=[_resistor_op], extract=default_device_parameter_extract_height),
    ],
)

# CONFIDENCE: MEDIUM
RES_PPOLYF_U_1K_TEMPLATE = DeviceTemplate(
    device_name="res_ppolyf_u_1k",
    device_class_name="res",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "R0_terminal", ["Poly2drawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "R1_terminal", ["Poly2drawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="w_res", layer_composed_op=[_resistor_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=1, name="l_res", layer_composed_op=[_resistor_op], extract=default_device_parameter_extract_height),
    ],
)

# CONFIDENCE: MEDIUM
RES_PPOLYF_U_1K_6P0_TEMPLATE = DeviceTemplate(
    device_name="res_ppolyf_u_1k_6p0",
    device_class_name="res",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "R0_terminal", ["Poly2drawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "R1_terminal", ["Poly2drawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="w_res", layer_composed_op=[_resistor_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=1, name="l_res", layer_composed_op=[_resistor_op], extract=default_device_parameter_extract_height),
    ],
)

# CONFIDENCE: MEDIUM
# TODO: FuseTopdrawing (75/0) must be present in GDS to enable parameter extraction.
CAP_MIM_TEMPLATE = DeviceTemplate(
    device_name="cap_mim",
    device_class_name="cap_mim",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "Top_terminal", ["Metal3drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "Bottom_terminal", ["Metal2drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="lc", layer_composed_op=[_fusetop_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=1, name="wc", layer_composed_op=[_fusetop_op], extract=default_device_parameter_extract_height),
    ],
)

# CONFIDENCE: MEDIUM
CAP_MOS_TEMPLATE = DeviceTemplate(
    device_name="cap_mos",
    device_class_name="cap_mos",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "Gate_terminal", ["Poly2drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "SD_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
    device_parameter_template=[
        DeviceParameterTemplate(uid=0, name="lc", layer_composed_op=[_gate_overlap_op], extract=default_device_parameter_extract_width),
        DeviceParameterTemplate(uid=1, name="wc", layer_composed_op=[_gate_overlap_op], extract=default_device_parameter_extract_height),
    ],
)

# CONFIDENCE: MEDIUM
# TODO: Parameter extraction for diodes requires distinguishing active from guard ring comp.
DIODE_ND2PS_TEMPLATE = DeviceTemplate(
    device_name="diode_nd2ps",
    device_class_name="diode_nd2ps",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "Anode_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "Cathode_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
)

# CONFIDENCE: MEDIUM
DIODE_PD2NW_TEMPLATE = DeviceTemplate(
    device_name="diode_pd2nw",
    device_class_name="diode_pd2nw",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "Anode_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "Cathode_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
)

# CONFIDENCE: MEDIUM
DIODE_NW2PS_TEMPLATE = DeviceTemplate(
    device_name="diode_nw2ps",
    device_class_name="diode_nw2ps",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "Cathode_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "Anode_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
)

# CONFIDENCE: MEDIUM
DIODE_PW2DW_TEMPLATE = DeviceTemplate(
    device_name="diode_pw2dw",
    device_class_name="diode_pw2dw",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "Anode_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "Cathode_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
)

# CONFIDENCE: MEDIUM
DIODE_DW2PS_TEMPLATE = DeviceTemplate(
    device_name="diode_dw2ps",
    device_class_name="diode_dw2ps",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "Cathode_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "Anode_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
)

# CONFIDENCE: MEDIUM
SC_DIODE_TEMPLATE = DeviceTemplate(
    device_name="sc_diode",
    device_class_name="sc_diode",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "Cathode_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
        build_terminal_from_overlapping_layers(1, "Anode_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
)

# CONFIDENCE: HIGH
PCMPGR_TEMPLATE = DeviceTemplate(
    device_name="pcmpgr_gen",
    device_class_name="guardring",
    device_terminal_template=[
        build_terminal_from_overlapping_layers(0, "Guardring_terminal", ["Compdrawing", "Contactdrawing", "Metal1drawing"], GDS_TABLE),
    ],
)

# CONFIDENCE: HIGH
VIA_GENERATOR_TEMPLATE = DeviceTemplate(device_name="via_generator", device_class_name="via")
VIA_STACK_TEMPLATE = DeviceTemplate(device_name="via_stack", device_class_name="via")

# ── Template Groups ───────────────────────────────────────────────────────────

FET_TEMPLATES: list[DeviceTemplate] = [NFET_TEMPLATE, PFET_TEMPLATE, NFET_06V0_NVT_TEMPLATE]
RESISTOR_TEMPLATES: list[DeviceTemplate] = [
    RES_RM1_TEMPLATE, RES_RM2_TEMPLATE, RES_RM3_TEMPLATE,
    RES_PPOLYF_U_TEMPLATE, RES_NPOLYF_U_TEMPLATE,
    RES_PPOLYF_S_TEMPLATE, RES_NPOLYF_S_TEMPLATE,
    RES_NPLUS_U_TEMPLATE, RES_PPLUS_U_TEMPLATE,
    RES_NWELL_TEMPLATE, RES_PPOLYF_U_1K_TEMPLATE, RES_PPOLYF_U_1K_6P0_TEMPLATE,
]
CAPACITOR_TEMPLATES: list[DeviceTemplate] = [CAP_MIM_TEMPLATE, CAP_MOS_TEMPLATE]
DIODE_TEMPLATES: list[DeviceTemplate] = [
    DIODE_ND2PS_TEMPLATE, DIODE_PD2NW_TEMPLATE, DIODE_NW2PS_TEMPLATE,
    DIODE_PW2DW_TEMPLATE, DIODE_DW2PS_TEMPLATE, SC_DIODE_TEMPLATE,
]
VIA_TEMPLATES: list[DeviceTemplate] = [VIA_GENERATOR_TEMPLATE, VIA_STACK_TEMPLATE]

DEVICE_TEMPLATES: list[DeviceTemplate] = [
    *(FET_TEMPLATES if INCLUDE_FET else []),
    *(RESISTOR_TEMPLATES if INCLUDE_RESISTORS else []),
    *(CAPACITOR_TEMPLATES if INCLUDE_CAPACITORS else []),
    *(DIODE_TEMPLATES if INCLUDE_DIODES else []),
    *([PCMPGR_TEMPLATE] if INCLUDE_GUARDRING else []),
    *(VIA_TEMPLATES if INCLUDE_VIA_CELLS else []),
]

# ── Connectivity Pairs ────────────────────────────────────────────────────────

_CONNECTIVITY_PAIRS: list[ConnectivityKeyValuePair] = [
    ConnectivityKeyValuePair(source_layer=lr(src, GDS_TABLE), to=lr(dst, GDS_TABLE))
    for src, dsts in LAYER_CONNECTIVITY.items()
    for dst in dsts
    if src in GDS_TABLE and dst in GDS_TABLE
]

# ── Default LVS Config ────────────────────────────────────────────────────────

DEFAULT_LVS_CONFIG = LvsRunConfig(
    run_mode=LvsRunMode.HIERARCHICAL,
    drawing_layers=DRAWING_LAYERS,
    via_drawing_layers=VIA_DRAWING_LAYERS,
    pin_logic_layers=PIN_LOGIC_LAYERS,
    label_logic_layers=LABEL_LOGIC_LAYERS,
    layer_connectivity=_CONNECTIVITY_PAIRS,
    device_templates=DEVICE_TEMPLATES,
    dbu=1e3,
    precision=1e-3,
)

# ── Convenience Runner ────────────────────────────────────────────────────────


def run_lvs_gf180mcu(
    lib: Library | Component,
    circuit: Circuit,
    *,
    config: LvsRunConfig | None = None,
    devices: list[Device] | None = None,
    components: list[Component] | None = None,
    device_ports: dict[str, dict[str, SchemaPort]] | None = None,
    tech_gds_table: GdsTable | None = None,
    original_file: str = "",
) -> LvsResult:
    """Run LVS for the GlobalFoundries 180nm MCU PDK with default configuration."""
    return run_lvs(
        lib,
        circuit,
        config or DEFAULT_LVS_CONFIG,
        devices=devices,
        components=components,
        device_ports=device_ports,
        tech_gds_table=tech_gds_table or GDS_TABLE,
        original_file=original_file,
    )
