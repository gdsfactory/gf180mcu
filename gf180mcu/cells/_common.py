from __future__ import annotations

from functools import partial

from gdsfactory.add_pins import add_electric_pins

from gf180mcu.layers import layer

_add_pins = partial(
    add_electric_pins,
    pin_layer_map={
        layer.metal1: layer.metal1_pin,
        layer.metal2: layer.metal2_pin,
        layer.metal3: layer.metal3_pin,
        layer.metal4: layer.metal4_pin,
        layer.metal5: layer.metal5_pin,
        layer.metaltop: layer.metaltop_pin,
    },
)
