from __future__ import annotations

from gdsfactory.add_pins import add_electric_pins

_METAL_PIN_LAYERS = [
    ((34, 0), None),
    ((36, 0), None),
    ((42, 0), None),
    ((46, 0), None),
    ((81, 0), None),
    ((53, 0), None),
]


def _add_pins(component) -> None:
    """Register logical electrical pins; geometric pin drawing is disabled pending reference GDS update."""
    kcl = component.kcl
    pin_layer_map = {
        kcl.layer(ln, dt): pin_spec for (ln, dt), pin_spec in _METAL_PIN_LAYERS
    }
    add_electric_pins(component, pin_layer_map=pin_layer_map)
