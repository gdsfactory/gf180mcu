from __future__ import annotations

from collections import defaultdict

from gdsfactory import Component
from gdsfactory.add_pins import AddPinFunction, add_pin_rectangle_inside
from gdsfactory.typings import LayerSpec


def _add_pins(component, port_pin_mapping: dict[str, list[str]] | None = None) -> None:
    """Register logical electrical pins; geometric pin drawing disabled pending reference GDS update."""
    from gf180mcu import LAYER

    _add_electric_pins(
        component,
        port_pin_mapping=port_pin_mapping,
        # Avoid XOR diff regressions against refs in label layers.
        pin_label_layer_map={
            LAYER.comp: LAYER.comp_label,
            LAYER.poly2: LAYER.poly2_label,
            LAYER.metal1: LAYER.metal1_label,
            LAYER.metal2: LAYER.metal2_label,
            LAYER.metal3: LAYER.metal3_label,
            LAYER.metal4: LAYER.metal4_label,
            LAYER.metal5: LAYER.metal5_label,
            LAYER.metaltop: LAYER.metaltop_label,
        },
    )


# TODO: replace gdsfactory.add_pins:add_electric_pins in next gdsfactory release
def _add_electric_pins(
    component: Component,
    port_pin_mapping: dict[str, list[str]] | None = None,
    pin_layer_map: dict[LayerSpec, LayerSpec] | None = None,
    pin_label_layer_map: dict[LayerSpec, LayerSpec] | None = None,
    default_pin_layer: LayerSpec | None = None,
    default_label_layer: LayerSpec | None = None,
    pin_function: AddPinFunction = add_pin_rectangle_inside,  # type: ignore[assignment]
    pin_type: str = "DC",
) -> None:
    """Draw pin markers and register logical pins for all electrical ports.

    Groups ports by name, draws a pin rectangle for each port on the
    corresponding pin layer, and calls ``component.create_pin()`` to register
    a logical pin for each group.  Pin markers are only drawn when a pin
    layer or label layer is resolvable (via the layer maps or defaults).

    Args:
        component: Component to add pins to.
        port_pin_mapping: Explicit mapping from pin name to port names.
            When provided, each key becomes a logical pin whose ports are
            looked up by name from the component. When None, electrical
            ports are auto-grouped by their own name.
        pin_layer_map: Mapping from port layer to pin layer for PDK-specific
            layer routing. When None, ``default_pin_layer`` is used as
            fallback (which itself defaults to None, meaning no pin markers
            are drawn).
        pin_label_layer_map: Mapping from port layer to label layer for
            PDK-specific label routing. When None, ``default_label_layer``
            is used as fallback.
        default_pin_layer: Fallback pin layer used when ``pin_layer_map``
            is not provided.
        default_label_layer: Fallback label layer used when
            ``pin_label_layer_map`` is not provided.
        pin_function: Function to draw each pin marker.
        pin_type: Pin type string passed to create_pin().
    """
    if port_pin_mapping is not None:
        by_name: dict[str, list] = {
            pin_name: [component.ports[pn] for pn in port_names]
            for pin_name, port_names in port_pin_mapping.items()
        }
    else:
        by_name: dict[str, list] = defaultdict(list)
        [
            by_name[port.name].append(port)
            for port in component.ports
            if port.port_type == "electrical"
        ]

    for name, ports in by_name.items():
        for port in ports:
            pin_layer = (
                pin_layer_map.get(port.layer) if pin_layer_map else default_pin_layer
            )
            label_layer = (
                pin_label_layer_map.get(port.layer)
                if pin_label_layer_map
                else default_label_layer
            )
            if pin_layer or label_layer:
                pin_function(component, port, layer=pin_layer, layer_label=label_layer)
        component.create_pin(ports=ports, name=name, pin_type=pin_type)
