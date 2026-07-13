from __future__ import annotations

import gdsfactory as gf
from gdsfactory.add_pins import add_pin_rectangle_inside

from gf180mcu.layers import layer

_LAYER_MAP = {
    layer.metal1:   layer.metal1_pin,
    layer.metal2:   layer.metal2_pin,
    layer.metal3:   layer.metal3_pin,
    layer.metal4:   layer.metal4_pin,
    layer.metal5:   layer.metal5_pin,
    layer.metaltop: layer.metaltop_pin,
}


def _add_pins(c: gf.Component) -> None:
    """Draw pin rectangles and register logical pins for all electrical ports."""
    by_name: dict[str, list] = {}
    for port in c.ports:
        if port.port_type == "electrical":
            by_name.setdefault(port.name, []).append(port)
    for name, ports in by_name.items():
        pin_layer = _LAYER_MAP.get(ports[0].layer)
        if pin_layer:
            for port in ports:
                add_pin_rectangle_inside(c, port, layer=pin_layer, layer_label=None)
        c.create_pin(ports=ports, name=name)
