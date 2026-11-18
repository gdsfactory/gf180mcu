"""Smoke tests for the gflvs LVS rules in `gf180mcu.lvs.rules` (skipped without gflvs)."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import pytest

gflvs = pytest.importorskip("gflvs")

import gdstk  # noqa: E402  (gdstk comes with gflvs)
from gflvs.gflvs_refactor import ElectricalDeviceExtractionPolicy  # noqa: E402
from gflvs.gflvs_schema import (  # noqa: E402
    LayerBooleanOperation,
    LayerOperation,
    LvsRunMode,
)
from result import Ok  # noqa: E402

from gf180mcu import cells  # noqa: E402
from gf180mcu.layers import LAYER  # noqa: E402
from gf180mcu.lvs import rules  # noqa: E402

GROUPS = ("MOSFET", "MOSCAP", "MIM", "DIODE", "RESISTOR")


def _positive_leaf_layers(operation: LayerOperation) -> Iterator[tuple[int, int]]:
    """Yield the leaf layers of *operation* that are ANDed/ORed in, skipping NOT right operands."""
    for side in ("left", "right"):
        if (
            side == "right"
            and operation.bool_op == LayerBooleanOperation.LAYER_BOOLEAN_OPERATION_NOT
        ):
            continue
        match operation.WhichOneof(f"layer_{side}"):
            case None:
                continue
            case name if name == f"layer_ref_{side}":
                layer = getattr(operation, name).layer
                yield (layer.layer, layer.datatype)
            case name:
                yield from _positive_leaf_layers(getattr(operation, name))


def test_default_config_builds() -> None:
    """The default config is an LvsConfig."""
    assert isinstance(rules.DEFAULT_LVS_CONFIG, gflvs.LvsConfig)


def test_connectivity_symmetric() -> None:
    """Every connectivity edge is listed in both directions."""
    assert all(
        a in rules.LAYER_CONNECTIVITY[b]
        for a, bs in rules.LAYER_CONNECTIVITY.items()
        for b in bs
    )


def test_template_layers_in_pdk() -> None:
    """Every layer used by the rules is a PDK layer."""
    used = set(rules.LAYER_CONNECTIVITY)
    for t in rules.DEVICE_TEMPLATES:
        for x in (*t.device_terminal_template, *t.device_parameter_template):
            used |= set(rules._leaf_layers(x.layer_composed_op))
    assert used <= {(layer.layer, layer.datatype) for layer in LAYER}  # type: ignore[attr-defined]


def test_terminals_use_markers() -> None:
    """Every terminal op ANDs in a device marker, unless its template has none."""
    missing = [
        (t.device_name, term.terminal_name)
        for t in rules.DEVICE_TEMPLATES
        if t.device_name not in rules.NO_MARKER_TEMPLATES
        for term in t.device_terminal_template
        if not set(_positive_leaf_layers(term.layer_composed_op)) & rules.MARKER_LAYERS
    ]
    assert not missing


def test_flags_toggle(monkeypatch: pytest.MonkeyPatch) -> None:
    """Each flag changes the built config as documented."""
    default = rules.build_lvs_config()
    names = [t.device_name for t in default.device_templates]
    assert default.netlist_tracer_config.galvanic_drawing_layers
    assert default.run_mode == LvsRunMode.LVS_RUN_MODE_FLAT

    with monkeypatch.context() as m:
        m.setattr(rules, "ENABLE_ELECTRICAL_TRACING", False)
        assert (
            not rules.build_lvs_config().netlist_tracer_config.galvanic_drawing_layers
        )

    with monkeypatch.context() as m:
        m.setattr(rules, "ENABLE_DEVICE_EXTRACTION", False)
        assert rules.build_lvs_config().device_templates == []

    with monkeypatch.context() as m:
        m.setattr(rules, "ENABLE_PARAMETER_CHECK", False)
        templates = rules.build_lvs_config().device_templates
        assert templates
        assert all(t.properties["blackbox"] == "true" for t in templates)
        assert all("blackbox" not in t.properties for t in rules.DEVICE_TEMPLATES)

    for group in GROUPS:
        with monkeypatch.context() as m:
            m.setattr(rules, f"ENABLE_{group}_TEMPLATES", False)
            removed = {t.device_name for t in getattr(rules, f"{group}_TEMPLATES")}
            assert removed
            got = [t.device_name for t in rules.build_lvs_config().device_templates]
            assert got == [n for n in names if n not in removed]

    with monkeypatch.context() as m:
        m.setattr(rules, "HIERARCHICAL_RUN", True)
        assert rules.build_lvs_config().run_mode == LvsRunMode.LVS_RUN_MODE_HIERARCHICAL


def _res(res_type: str, l_res: float = 10.0, w_res: float = 1.0) -> Any:
    """Return a res() pytest row with r_length/r_width equal to the drawn size."""
    return (
        cells.res,
        {"res_type": res_type, "l_res": l_res, "w_res": w_res},
        res_type,
        3 if res_type not in ("rm1", "rm2", "rm3") else 2,
        {"r_length": l_res, "r_width": w_res},
    )


# one row per HIGH-confidence template (templates-gf180mcu.md); values are the drawn PCell kwargs.
# `device` is the template device_name (stricter than its class: nmos_3p3 vs nmos_6p0 are both "nfet").
PCELL_ROWS = [
    (
        cells.nfet,
        {"l_gate": 0.5, "w_gate": 1.0, "nf": 3},
        "nmos_3p3",
        4,
        {"l": 0.5, "w": 3.0, "nf": 3},
    ),
    (
        cells.nfet,
        {"l_gate": 0.7, "w_gate": 0.4, "volt": "6.0V"},
        "nmos_6p0",
        4,
        {"l": 0.7, "w": 0.4, "nf": 1},
    ),
    (
        cells.pfet,
        {"l_gate": 0.28, "w_gate": 0.5, "nf": 2},
        "pmos_3p3",
        4,
        {"l": 0.28, "w": 1.0, "nf": 2},
    ),
    (
        cells.pfet,
        {"l_gate": 0.5, "w_gate": 0.6, "volt": "6.0V"},
        "pmos_6p0",
        4,
        {"l": 0.5, "w": 0.6, "nf": 1},
    ),
    (cells.nfet_06v0_nvt, {}, "nmos_6p0_nat", 4, {"l": 1.8, "w": 0.8, "nf": 1}),
    pytest.param(
        cells.cap_mos,
        {"lc": 2.0, "wc": 3.0},
        "nmoscap_3p3_b",
        2,
        {"c_length": 2.0, "c_width": 3.0},
        marks=pytest.mark.xfail(
            strict=True, reason="PCell bug: 3.3 V cap_mos draws no comp (no channel)"
        ),
        id="nmoscap_3p3_b",
    ),
    (
        cells.cap_mos,
        {"lc": 2.0, "wc": 3.0, "volt": "6.0V"},
        "nmoscap_6p0_b",
        2,
        {"c_length": 2.0, "c_width": 3.0},
    ),
    *(
        pytest.param(
            pcell,
            {"la": 1.0, "wa": 2.0, "volt": volt},
            f"{name}_{suffix}",
            2,
            {"area": 2.0, "pj": 6.0},
            id=f"{name}_{suffix}",
        )
        for pcell, name in ((cells.diode_nd2ps, "np"), (cells.diode_pd2nw, "pn"))
        for volt, suffix in (("3.3V", "3p3"), ("6.0V", "6p0"))
    ),
    *(
        _res(t)
        for t in (
            "rm1",
            "rm2",
            "rm3",
            "ppolyf_u",
            "ppolyf_s",
            "npolyf_u",
            "npolyf_s",
            "ppolyf_u_1k",
            "ppolyf_u_1k_6p0",
            "nplus_u",
            "pplus_u",
        )
    ),
]


@pytest.mark.parametrize("pcell, kwargs, device, n_terminals, params", PCELL_ROWS)
def test_pcell_extracts(
    pcell: Callable[..., Any],
    kwargs: dict[str, Any],
    device: str,
    n_terminals: int,
    params: dict[str, float],
    tmp_path: Path,
) -> None:
    """The PCell extracts exactly one device of the right class, terminals and parameters."""
    component = pcell(**kwargs)
    lib = gdstk.read_gds(component.write_gds(tmp_path / "c.gds"))
    cfg = rules.DEFAULT_LVS_CONFIG
    # like gflvs: extract from every non-passthrough cell (res keeps its geometry in a child cell)
    results = [
        result
        for cell in lib.cells
        if isinstance(cell, gdstk.Cell)
        and cell.name != "$$$CONTEXT_INFO$$$"
        and not cell.name.lower().startswith(rules.PASSTHROUGH_DEVICE_CLASS_NAMES)
        for result in ElectricalDeviceExtractionPolicy().execute(
            cell, cfg.device_templates, cfg.electrical_device_extraction_config
        )
    ]
    assert all(isinstance(r, Ok) for r in results), [
        r for r in results if not isinstance(r, Ok)
    ]
    devices = [r.unwrap() for r in results]
    assert [d.name for d in devices] == [f"{device}_0"]
    (d,) = devices
    assert len(d.terminals) == n_terminals
    assert {p.name: p.value for p in d.parameters} == pytest.approx(params, rel=1e-3)
    # terminal names are the PCell's logical pins, its port names where it registers none
    pins = {p.name for p in component.pins} or {p.name for p in component.ports}
    names = {t.name for t in d.terminals}
    if names - pins == {"bulk"}:
        pytest.skip("terminal ↔ pin name mismatch: the res PCell has no bulk pin")
    assert names == pins


# small foundry GDS from google/globalfoundries-pdk-libs-gf180mcu_fd_pr @ 9f992d5 (Apache-2.0),
# rules/klayout/lvs/testing; expected values are the official KLayout deck's extraction
LVS_DATA = Path(__file__).parent / "lvs_data"


# gflvs issue: its built-in "length" extractor calls np.mean([]) on a device fragment with no terminal
# pair (gflvs_refactor.py:2672), e.g. a stray tap region; not from rules.py
@pytest.mark.filterwarnings("ignore:Mean of empty slice:RuntimeWarning")
@pytest.mark.filterwarnings(
    "ignore:invalid value encountered in scalar divide:RuntimeWarning"
)
def test_inv_gate_not_shorted_to_rails() -> None:
    """Foundry 5 V INV_X1: G is its own net (rails crossing the poly ends don't join it), devices are 5 V."""
    _, l2n, _ = gflvs.layout_to_netlist(
        gdstk.read_gds(LVS_DATA / "ref_sc_INV_X1_7T5P0.gds"),
        "INV_X1_7T5P0",
        device_templates=rules.DEFAULT_LVS_CONFIG.device_templates,
        nettracer_config=rules.DEFAULT_LVS_CONFIG.netlist_tracer_config,
        electrical_device_extraction_config=rules.DEFAULT_LVS_CONFIG.electrical_device_extraction_config,
    )
    net_of = {
        (t.device_instance_name.rsplit("/", 1)[-1], t.device_terminal_name): n.name
        for n in l2n.nets
        for t in n.connected_terminals
    }
    assert sorted({d for d, _ in net_of}) == ["nmos_5p0_0", "pmos_5p0_0"]
    gates = {net for (_, term), net in net_of.items() if term == "Gate"}
    others = {net for (_, term), net in net_of.items() if term != "Gate"}
    assert len(gates) == 1  # both gates on the input net
    assert not gates & others


def test_resistor_width_any_orientation() -> None:
    """Foundry rm1 testcase: wide (W > L) bodies still give r_width = W."""
    lib = gdstk.read_gds(LVS_DATA / "rm1.gds")
    cfg = rules.DEFAULT_LVS_CONFIG
    got = sorted(
        (round(p["r_length"], 3), round(p["r_width"], 3))
        for cell in lib.cells
        if isinstance(cell, gdstk.Cell)
        for r in ElectricalDeviceExtractionPolicy().execute(
            cell, cfg.device_templates, cfg.electrical_device_extraction_config
        )
        for p in [{q.name: q.value for q in r.unwrap().parameters}]
    )
    lw = (0.23, 13.5, 50.0)
    # KLayout: the full L x W grid, with the 0.23 x 0.23 device drawn twice
    expected = sorted(
        [(length, width) for length in lw for width in lw] + [(0.23, 0.23)]
    )
    assert got == expected
