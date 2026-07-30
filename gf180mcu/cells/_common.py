from __future__ import annotations

from gdsfactory.add_pins import add_electric_pins

from gf180mcu.layers import LAYER

_ELECTRICAL_DRAWING_LAYERS = (
    LAYER.metal1,  # (34, 0)
    LAYER.metal2,  # (36, 0)
    LAYER.metal3,  # (42, 0)
    LAYER.metal4,  # (46, 0)
    LAYER.metal5,  # (81, 0)
    LAYER.metaltop,  # (53, 0)
)


def _add_pins(component) -> None:
    """Register logical electrical pins; geometric pin drawing disabled pending reference GDS update."""
    add_electric_pins(
        component,
        pin_layer_map={
            component.kcl.layer(*s): None for s in _ELECTRICAL_DRAWING_LAYERS
        },
    )
