"""Tests for the via_stack PCell across all metal levels."""

import gdsfactory as gf
import pytest

import klayout.db as kdb
from gf180mcu.cells.via_generator import via_stack
from gf180mcu.layers import layer

# (cut layer, metal below, metal above) for each level of the stack
STACK = [
    ("contact", "metal1", "metal1"),
    ("via1", "metal1", "metal2"),
    ("via2", "metal2", "metal3"),
    ("via3", "metal3", "metal4"),
    ("via4", "metal4", "metal5"),
]


def _region(c: gf.Component, layer_name: str) -> kdb.Region:
    return kdb.Region(c.begin_shapes_rec(c.kcl.layer(*layer[layer_name])))


@pytest.mark.parametrize("metal_level", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("x_range", [(0, 1), (0, 0.5), (0, 3)])
def test_via_stack_levels(metal_level: int, x_range: tuple[float, float]) -> None:
    c = via_stack(x_range=x_range, y_range=(0, 1), metal_level=metal_level)

    for cut, metal_below, metal_above in STACK[:metal_level]:
        cuts = _region(c, cut)
        assert not cuts.is_empty(), f"no {cut} shapes for metal_level={metal_level}"
        if cut == "contact":
            # metal1 is the only metal touching the contacts
            assert (cuts - _region(c, "metal1")).is_empty()
            continue
        for metal in (metal_below, metal_above):
            assert (cuts - _region(c, metal)).is_empty(), (
                f"{cut} not enclosed by {metal} for metal_level={metal_level}"
            )

    # nothing is drawn above the requested level
    for cut, _, metal_above in STACK[metal_level:]:
        assert _region(c, cut).is_empty()
        assert _region(c, metal_above).is_empty()

    top_metal = STACK[metal_level - 1][2]
    assert c.ports["e1"].layer == c.kcl.layer(*layer["metal1"])
    assert c.ports["e2"].layer == c.kcl.layer(*layer[top_metal])


@pytest.mark.parametrize("metal_level", [0, 6])
def test_via_stack_invalid_level(metal_level: int) -> None:
    with pytest.raises(ValueError, match="metal_level"):
        via_stack(metal_level=metal_level)
