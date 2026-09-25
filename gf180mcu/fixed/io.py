"""GF180MCU IO ring fixed-geometry cells from gf180mcu_fd_io."""

from functools import partial
from pathlib import Path

import gdsfactory as gf

from gf180mcu.layers import LAYER

_IO_LIB = Path(__file__).parent.parent / "src" / "gf180mcu_fd_io" / "cells"

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


# --- Digital I/O ---
@gf.cell
def bi_t() -> gf.Component:
    """Bidirectional digital IO w/ programmable pull up or pull down."""
    return _import_gds(_IO_LIB / "bi_t" / "gf180mcu_fd_io__bi_t_3lm.gds")


@gf.cell
def bi_24t() -> gf.Component:
    """Bidirectional digital IO 24mA drive w/ programmable pull up or pull down."""
    return _import_gds(_IO_LIB / "bi_24t" / "gf180mcu_fd_io__bi_24t_3lm.gds")


@gf.cell
def in_c() -> gf.Component:
    """Input only digital IO w/ programmable pull up or pull down (CMOS)."""
    return _import_gds(_IO_LIB / "in_c" / "gf180mcu_fd_io__in_c_3lm.gds")


@gf.cell
def in_s() -> gf.Component:
    """Input only digital IO w/ programmable pull up or pull down (Schmitt trigger)."""
    return _import_gds(_IO_LIB / "in_s" / "gf180mcu_fd_io__in_s_3lm.gds")


# --- Analog I/O primary ESD protection ---
@gf.cell
def asig_5p0() -> gf.Component:
    """Analog IO protection diodes (5V)."""
    return _import_gds(_IO_LIB / "asig_5p0" / "gf180mcu_fd_io__asig_5p0_3lm.gds")


# --- Filler I/O ---
@gf.cell
def fill1() -> gf.Component:
    """1 micrometer width filler IO cell."""
    return _import_gds(_IO_LIB / "fill1" / "gf180mcu_fd_io__fill1_3lm.gds")


@gf.cell
def fill5() -> gf.Component:
    """5 micrometers width filler IO cell."""
    return _import_gds(_IO_LIB / "fill5" / "gf180mcu_fd_io__fill5_3lm.gds")


@gf.cell
def fill10() -> gf.Component:
    """10 micrometers width filler IO cell."""
    return _import_gds(_IO_LIB / "fill10" / "gf180mcu_fd_io__fill10_3lm.gds")


@gf.cell
def fillnc() -> gf.Component:
    """No-connect filler IO cell."""
    return _import_gds(_IO_LIB / "fillnc" / "gf180mcu_fd_io__fillnc_3lm.gds")


@gf.cell
def brk2() -> gf.Component:
    """2 micrometers no-connection break IO cell."""
    return _import_gds(_IO_LIB / "brk2" / "gf180mcu_fd_io__brk2_3lm.gds")


@gf.cell
def brk5() -> gf.Component:
    """5 micrometers no-connection break IO cell."""
    return _import_gds(_IO_LIB / "brk5" / "gf180mcu_fd_io__brk5_3lm.gds")


@gf.cell
def cor() -> gf.Component:
    """Corner filler IO cell."""
    return _import_gds(_IO_LIB / "cor" / "gf180mcu_fd_io__cor_3lm.gds")


# --- Power I/O ---
@gf.cell
def dvdd() -> gf.Component:
    """DVDD power supply IO cell."""
    return _import_gds(_IO_LIB / "dvdd" / "gf180mcu_fd_io__dvdd_3lm.gds")


@gf.cell
def dvss() -> gf.Component:
    """DVSS power supply IO cell."""
    return _import_gds(_IO_LIB / "dvss" / "gf180mcu_fd_io__dvss_3lm.gds")
