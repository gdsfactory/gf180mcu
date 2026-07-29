from __future__ import annotations

from functools import partial

import gdsfactory as gf
from gdsfactory.add_pins import add_electric_pins

from gf180mcu.layers import layer

_add_pins = partial(
    add_electric_pins,
    pin_layer_map={
        gf.kcl.layer(34, 0): layer.metal1_pin,
        gf.kcl.layer(36, 0): layer.metal2_pin,
        gf.kcl.layer(42, 0): layer.metal3_pin,
        gf.kcl.layer(46, 0): layer.metal4_pin,
        gf.kcl.layer(81, 0): layer.metal5_pin,
        gf.kcl.layer(53, 0): layer.metaltop_pin,
    },
)
