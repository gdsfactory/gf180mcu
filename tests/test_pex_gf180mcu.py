"""Consistency checks for the gfpex default PEX rules of GF180MCU."""

from __future__ import annotations

from itertools import pairwise

import pytest

pytest.importorskip(
    "gfpex.gfpex"
)  # not bare "gfpex": a folder named gfpex on sys.path would satisfy it

from gfpex.gfpex import Contact, Techfile

from gf180mcu.layers import LAYER
from gf180mcu.pex.rules import DEFAULT_PEX_RULES_CONFIG as CFG

# Carried over unchanged from KPEX (gf-pex gfpexconfg/gf180mcuD.py): the capacitance tables use LVPWELL,
# which has no LayerInfo. Remove it from here once a LVPWELL layer is added.
KNOWN_UNRESOLVED = {"LVPWELL"}


def _contacts() -> list[Contact]:
    found = []
    for s in CFG.process_stack.layers:
        for layer in (s.metal_layer, s.diffusion_layer, s.nwell_layer):
            if layer is not None and layer.contact_above is not None:
                found.append(layer.contact_above)
    return found


def test_round_trip() -> None:
    assert isinstance(CFG, Techfile)
    assert Techfile.model_validate_json(CFG.to_json()) == CFG


def test_names_resolve() -> None:
    layers = {layer.name for layer in CFG.layers}
    contacts = _contacts()
    stack_names = {
        s.name
        for s in CFG.process_stack.layers
        if s.metal_layer or s.diffusion_layer or s.nwell_layer
    }
    assert stack_names <= layers
    for c in contacts:
        assert {c.layer_below, c.metal_above} <= layers, c.name

    # Contacts keep their KPEX names (M1-Nplus, Via1_con, ...), so contact and via
    # resistances may refer to a stack contact instead of a LayerInfo.
    known = layers | {c.name for c in contacts}
    r = CFG.process_parasitics.resistance
    cap = CFG.process_parasitics.capacitance
    used = (
        {x.layer_name for x in r.layers}
        | {
            n
            for x in r.contacts
            for n in (x.contact_name, x.device_layer_name, x.layer_above)
        }
        | {x.via_name for x in r.vias}
        | {x.layer_name for x in cap.substrates}
        | {n for x in cap.overlaps for n in (x.top_layer_name, x.bottom_layer_name)}
        | {x.layer_name for x in cap.sidewalls}
        | {n for x in cap.sideoverlaps for n in (x.in_layer_name, x.out_layer_name)}
    )
    assert used - known == KNOWN_UNRESOLVED


def test_gds_pairs_match_layer_map() -> None:
    for layer in CFG.layers:
        expected = getattr(LAYER, layer.name.lower())
        pair = layer.drw_gds_pair
        assert (pair.layer, pair.datatype) == tuple(expected), layer.name
        if layer.label_gds_pair is not None:
            label = getattr(LAYER, f"{layer.name.lower()}_label")
            pair = layer.label_gds_pair
            assert (pair.layer, pair.datatype) == tuple(label), layer.name


def test_metal_z_increases() -> None:
    metals = [s.metal_layer for s in CFG.process_stack.layers if s.metal_layer]
    assert len(metals) > 1
    for below, above in pairwise(metals):
        assert above.z_bottom >= below.z_top


def test_z_lookup_covers_contacts() -> None:
    z = CFG.build_layer_z_lookup()
    contacts = _contacts()
    assert contacts
    assert all(c.name in z for c in contacts)
