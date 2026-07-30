from __future__ import annotations

from gdsfactory.add_pins import add_electric_pins

from gf180mcu.layers import layer

_METAL_PIN_LAYERS: list[tuple[tuple[int, int], tuple[int, int]]] = [
    ((34, 0), layer.metal1_pin),
    ((36, 0), layer.metal2_pin),
    ((42, 0), layer.metal3_pin),
    ((46, 0), layer.metal4_pin),
    ((81, 0), layer.metal5_pin),
    ((53, 0), layer.metaltop_pin),
]


def _add_pins(component) -> None:
    """Add geometric pin markers and register logical pins for electrical ports."""
    kcl = component.kcl
    pin_layer_map = {
        kcl.layer(ln, dt): pin_spec
        for (ln, dt), pin_spec in _METAL_PIN_LAYERS
    }
    add_electric_pins(component, pin_layer_map=pin_layer_map)
