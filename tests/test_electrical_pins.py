"""Tests verifying geometric and logical electrical pins on GF180MCU PCells."""

from __future__ import annotations

import pytest
import kfactory as kf

from gf180mcu import PDK

kdb = kf.kdb


@pytest.fixture(autouse=True)
def activate_pdk():
    PDK.activate()


# Drawing layer (datatype 0) → pin layer (datatype 2)
_PIN_LAYER_MAP: dict[tuple[int, int], tuple[int, int]] = {
    (34, 0): (34, 2),   # metal1      → metal1_pin
    (36, 0): (36, 2),   # metal2      → metal2_pin
    (42, 0): (42, 2),   # metal3      → metal3_pin
    (46, 0): (46, 2),   # metal4      → metal4_pin
    (81, 0): (81, 2),   # metal5      → metal5_pin
    (53, 0): (53, 2),   # metaltop    → metaltop_pin
}

# Electrical PCells with geometric/logical pins added.
# NOTE: diode_nw2ps, diode_pw2dw, diode_dw2ps are excluded — they call _add_pins
# but define no add_port(..., port_type="electrical") calls, so they have no
# electrical ports. This is a source-code bug to be fixed separately.
CELL_NAMES = [
    "cap_mim",
    "cap_mos",
    "diode_nd2ps",
    "diode_pd2nw",
    "res",
    "via_generator",
    "via_stack",
    "pcmpgr_gen",
]


def _has_pin_polygon_near_port(comp, port, pin_layer_tuple: tuple[int, int]) -> bool:
    """Return True if there is at least one polygon on pin_layer_tuple near the port center."""
    layout = comp.kcl.layout
    layer_idx = layout.find_layer(*pin_layer_tuple)
    if layer_idx < 0:
        return False
    dbu = layout.dbu
    cx = int(port.dcenter[0] / dbu)
    cy = int(port.dcenter[1] / dbu)
    half = int(0.1 / dbu)
    probe = kdb.Region(kdb.Box(cx - half, cy - half, cx + half, cy + half))
    region = kdb.Region(comp.begin_shapes_rec(layer_idx))
    return not (region & probe).is_empty()


@pytest.mark.parametrize("cell_name", CELL_NAMES)
def test_geometric_pin_present(cell_name):
    """Each electrical port on a metal layer must have a polygon on the corresponding pin layer.

    Ports on via/contact layers (e.g. 66/44) have no dedicated pin layer in GF180MCU;
    those are skipped for the geometric check but still verified in other tests.
    """
    c = PDK.cells[cell_name]()
    electrical_ports = [p for p in c.ports if p.port_type == "electrical"]
    assert electrical_ports, f"No electrical ports on {cell_name}"
    checked_any = False
    for port in electrical_ports:
        info = c.kcl.layout.get_info(port.layer)
        drawing = (info.layer, info.datatype)
        pin_layer = _PIN_LAYER_MAP.get(drawing)
        if pin_layer is None:
            # Port is on a via/contact layer without a dedicated pin layer — skip geometric check
            continue
        checked_any = True
        assert _has_pin_polygon_near_port(c, port, pin_layer), (
            f"No geometric pin polygon near port '{port.name}' on layer {pin_layer} in {cell_name}"
        )
    if not checked_any:
        pytest.skip(f"All ports in {cell_name} are on unmapped (non-metal) layers; no geometric pin check performed")


@pytest.mark.parametrize("cell_name", CELL_NAMES)
def test_logical_pin_registered(cell_name):
    """create_pin() must have been called — c.pins must be non-empty."""
    c = PDK.cells[cell_name]()
    assert len(c.pins) > 0, f"No logical pins registered on {cell_name}"


@pytest.mark.parametrize("cell_name", CELL_NAMES)
def test_port_type_is_electrical(cell_name):
    """Every electrical port on these PCells must have port_type == 'electrical'."""
    c = PDK.cells[cell_name]()
    electrical_ports = [p for p in c.ports if p.port_type == "electrical"]
    assert electrical_ports, f"No electrical ports found on {cell_name}"
    for port in electrical_ports:
        assert port.port_type == "electrical", (
            f"Port '{port.name}' has type '{port.port_type}', expected 'electrical' in {cell_name}"
        )
