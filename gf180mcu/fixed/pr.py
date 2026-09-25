"""GF180MCU primitive fixed-geometry cells (BJT and eFuse) from gf180mcu_fd_pr."""

from functools import partial
from pathlib import Path

import gdsfactory as gf

from gf180mcu.layers import LAYER
from gf180mcu.schematic import bjt_schematic, efuse_schematic

# ponytail: GDS sourced from local klayout/pymacros/cells/ (generated from fd_pr macros).
# fd_pr submodule (gf180mcu/src/gf180mcu_fd_pr) provides the KLayout Python macros
# to regenerate these files; top-level BJT GDS are not distributed in the upstream repo.
_GDS_DIR = Path(__file__).parent.parent.parent / "klayout" / "pymacros" / "cells"

_add_ports = gf.partial(
    gf.add_ports.add_ports_from_labels,
    port_layer=LAYER.metal1,
    layer_label=LAYER.metal1_label,
    port_type="electrical",
    port_width=0.2,
    get_name_from_label=True,
    guess_port_orientation=True,
)

_import_gds = partial(gf.import_gds, post_process=(_add_ports,))


# BJT NPN variants
@gf.cell(schematic_function=partial(bjt_schematic, model="vnpn_0p54x2"))
def npn_00p54x02p00() -> gf.Component:
    """NPN BJT 0.54um x 2.00um emitter."""
    return _import_gds(_GDS_DIR / "bjt" / "npn_00p54x02p00.gds")


@gf.cell(schematic_function=partial(bjt_schematic, model="vnpn_0p54x4"))
def npn_00p54x04p00() -> gf.Component:
    """NPN BJT 0.54um x 4.00um emitter."""
    return _import_gds(_GDS_DIR / "bjt" / "npn_00p54x04p00.gds")


@gf.cell(schematic_function=partial(bjt_schematic, model="vnpn_0p54x8"))
def npn_00p54x08p00() -> gf.Component:
    """NPN BJT 0.54um x 8.00um emitter."""
    return _import_gds(_GDS_DIR / "bjt" / "npn_00p54x08p00.gds")


@gf.cell(schematic_function=partial(bjt_schematic, model="vnpn_0p54x16"))
def npn_00p54x16p00() -> gf.Component:
    """NPN BJT 0.54um x 16.00um emitter."""
    return _import_gds(_GDS_DIR / "bjt" / "npn_00p54x16p00.gds")


@gf.cell(schematic_function=partial(bjt_schematic, model="vnpn_5x5"))
def npn_05p00x05p00() -> gf.Component:
    """NPN BJT 5.00um x 5.00um emitter."""
    return _import_gds(_GDS_DIR / "bjt" / "npn_05p00x05p00.gds")


@gf.cell(schematic_function=partial(bjt_schematic, model="vnpn_10x10"))
def npn_10p00x10p00() -> gf.Component:
    """NPN BJT 10.00um x 10.00um emitter."""
    return _import_gds(_GDS_DIR / "bjt" / "npn_10p00x10p00.gds")


# BJT PNP variants
@gf.cell(schematic_function=partial(bjt_schematic, model="vpnp_0p42x5"))
def pnp_05p00x00p42() -> gf.Component:
    """PNP BJT 5.00um x 0.42um emitter."""
    return _import_gds(_GDS_DIR / "bjt" / "pnp_05p00x00p42.gds")


@gf.cell(schematic_function=partial(bjt_schematic, model="vpnp_5x5"))
def pnp_05p00x05p00() -> gf.Component:
    """PNP BJT 5.00um x 5.00um emitter."""
    return _import_gds(_GDS_DIR / "bjt" / "pnp_05p00x05p00.gds")


@gf.cell(schematic_function=partial(bjt_schematic, model="vpnp_0p42x10"))
def pnp_10p00x00p42() -> gf.Component:
    """PNP BJT 10.00um x 0.42um emitter."""
    return _import_gds(_GDS_DIR / "bjt" / "pnp_10p00x00p42.gds")


@gf.cell(schematic_function=partial(bjt_schematic, model="vpnp_10x10"))
def pnp_10p00x10p00() -> gf.Component:
    """PNP BJT 10.00um x 10.00um emitter."""
    return _import_gds(_GDS_DIR / "bjt" / "pnp_10p00x10p00.gds")


# eFuse
@gf.cell(schematic_function=efuse_schematic)
def efuse() -> gf.Component:
    """Electronic fuse."""
    return _import_gds(_GDS_DIR / "efuse" / "efuse.gds")
