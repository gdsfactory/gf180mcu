"""GF180MCU IO ring fixed-geometry cells from gf180mcu_fd_io."""

from functools import partial
from pathlib import Path
from typing import Literal

import gdsfactory as gf

from gf180mcu.layers import LAYER

MetalStack = Literal["3lm", "4lm", "5lm"]

_IO_LIB = Path(__file__).parent.parent / "src" / "gf180mcu_fd_io" / "cells"

_metal_layers = [
    (LAYER.metal1, LAYER.metal1_label),
    (LAYER.metal2, LAYER.metal2_label),
    (LAYER.metal3, LAYER.metal3_label),
    (LAYER.metal4, LAYER.metal4_label),
    (LAYER.metal5, LAYER.metal5_label),
    (LAYER.metaltop, LAYER.metaltop_label),
]

_add_ports = tuple(
    gf.partial(
        gf.add_ports.add_ports_from_labels,
        port_layer=metal,
        layer_label=label,
        port_type="electrical",
        port_width=0.2,
        get_name_from_label=True,
        guess_port_orientation=True,
    )
    for metal, label in _metal_layers
)

_import_gds = partial(gf.import_gds, post_process=_add_ports)


# --- Digital I/O ---
@gf.cell
def bi_t(metal_stack: MetalStack = "3lm") -> gf.Component:
    """Bidirectional digital IO w/ programmable pull up or pull down."""
    match metal_stack:
        case "3lm":
            return _import_gds(_IO_LIB / "bi_t" / "gf180mcu_fd_io__bi_t_3lm.gds")
        case "4lm":
            return _import_gds(_IO_LIB / "bi_t" / "gf180mcu_fd_io__bi_t_4lm.gds")
        case "5lm":
            return _import_gds(_IO_LIB / "bi_t" / "gf180mcu_fd_io__bi_t_5lm.gds")


@gf.cell
def bi_24t(metal_stack: MetalStack = "3lm") -> gf.Component:
    """Bidirectional digital IO 24mA drive w/ programmable pull up or pull down."""
    match metal_stack:
        case "3lm":
            return _import_gds(_IO_LIB / "bi_24t" / "gf180mcu_fd_io__bi_24t_3lm.gds")
        case "4lm":
            return _import_gds(_IO_LIB / "bi_24t" / "gf180mcu_fd_io__bi_24t_4lm.gds")
        case "5lm":
            return _import_gds(_IO_LIB / "bi_24t" / "gf180mcu_fd_io__bi_24t_5lm.gds")


@gf.cell
def in_c(metal_stack: MetalStack = "3lm") -> gf.Component:
    """Input only digital IO w/ programmable pull up or pull down (CMOS)."""
    match metal_stack:
        case "3lm":
            return _import_gds(_IO_LIB / "in_c" / "gf180mcu_fd_io__in_c_3lm.gds")
        case "4lm":
            return _import_gds(_IO_LIB / "in_c" / "gf180mcu_fd_io__in_c_4lm.gds")
        case "5lm":
            return _import_gds(_IO_LIB / "in_c" / "gf180mcu_fd_io__in_c_5lm.gds")


@gf.cell
def in_s(metal_stack: MetalStack = "3lm") -> gf.Component:
    """Input only digital IO w/ programmable pull up or pull down (Schmitt trigger)."""
    match metal_stack:
        case "3lm":
            return _import_gds(_IO_LIB / "in_s" / "gf180mcu_fd_io__in_s_3lm.gds")
        case "4lm":
            return _import_gds(_IO_LIB / "in_s" / "gf180mcu_fd_io__in_s_4lm.gds")
        case "5lm":
            return _import_gds(_IO_LIB / "in_s" / "gf180mcu_fd_io__in_s_5lm.gds")


# --- Analog I/O primary ESD protection ---
@gf.cell
def asig_5p0(metal_stack: MetalStack = "3lm") -> gf.Component:
    """Analog IO protection diodes (5V)."""
    match metal_stack:
        case "3lm":
            return _import_gds(
                _IO_LIB / "asig_5p0" / "gf180mcu_fd_io__asig_5p0_3lm.gds"
            )
        case "4lm":
            return _import_gds(
                _IO_LIB / "asig_5p0" / "gf180mcu_fd_io__asig_5p0_4lm.gds"
            )
        case "5lm":
            return _import_gds(
                _IO_LIB / "asig_5p0" / "gf180mcu_fd_io__asig_5p0_5lm.gds"
            )


# --- Filler I/O ---
@gf.cell
def fill1(metal_stack: MetalStack = "3lm") -> gf.Component:
    """1 micrometer width filler IO cell."""
    match metal_stack:
        case "3lm":
            return _import_gds(_IO_LIB / "fill1" / "gf180mcu_fd_io__fill1_3lm.gds")
        case "4lm":
            return _import_gds(_IO_LIB / "fill1" / "gf180mcu_fd_io__fill1_4lm.gds")
        case "5lm":
            return _import_gds(_IO_LIB / "fill1" / "gf180mcu_fd_io__fill1_5lm.gds")


@gf.cell
def fill5(metal_stack: MetalStack = "3lm") -> gf.Component:
    """5 micrometers width filler IO cell."""
    match metal_stack:
        case "3lm":
            return _import_gds(_IO_LIB / "fill5" / "gf180mcu_fd_io__fill5_3lm.gds")
        case "4lm":
            return _import_gds(_IO_LIB / "fill5" / "gf180mcu_fd_io__fill5_4lm.gds")
        case "5lm":
            return _import_gds(_IO_LIB / "fill5" / "gf180mcu_fd_io__fill5_5lm.gds")


@gf.cell
def fill10(metal_stack: MetalStack = "3lm") -> gf.Component:
    """10 micrometers width filler IO cell."""
    match metal_stack:
        case "3lm":
            return _import_gds(_IO_LIB / "fill10" / "gf180mcu_fd_io__fill10_3lm.gds")
        case "4lm":
            return _import_gds(_IO_LIB / "fill10" / "gf180mcu_fd_io__fill10_4lm.gds")
        case "5lm":
            return _import_gds(_IO_LIB / "fill10" / "gf180mcu_fd_io__fill10_5lm.gds")


@gf.cell
def fillnc(metal_stack: MetalStack = "3lm") -> gf.Component:
    """No-connect filler IO cell."""
    match metal_stack:
        case "3lm":
            return _import_gds(_IO_LIB / "fillnc" / "gf180mcu_fd_io__fillnc_3lm.gds")
        case "4lm":
            return _import_gds(_IO_LIB / "fillnc" / "gf180mcu_fd_io__fillnc_4lm.gds")
        case "5lm":
            return _import_gds(_IO_LIB / "fillnc" / "gf180mcu_fd_io__fillnc_5lm.gds")


@gf.cell
def brk2(metal_stack: MetalStack = "3lm") -> gf.Component:
    """2 micrometers no-connection break IO cell."""
    match metal_stack:
        case "3lm":
            return _import_gds(_IO_LIB / "brk2" / "gf180mcu_fd_io__brk2_3lm.gds")
        case "4lm":
            return _import_gds(_IO_LIB / "brk2" / "gf180mcu_fd_io__brk2_4lm.gds")
        case "5lm":
            return _import_gds(_IO_LIB / "brk2" / "gf180mcu_fd_io__brk2_5lm.gds")


@gf.cell
def brk5(metal_stack: MetalStack = "3lm") -> gf.Component:
    """5 micrometers no-connection break IO cell."""
    match metal_stack:
        case "3lm":
            return _import_gds(_IO_LIB / "brk5" / "gf180mcu_fd_io__brk5_3lm.gds")
        case "4lm":
            return _import_gds(_IO_LIB / "brk5" / "gf180mcu_fd_io__brk5_4lm.gds")
        case "5lm":
            return _import_gds(_IO_LIB / "brk5" / "gf180mcu_fd_io__brk5_5lm.gds")


@gf.cell
def cor(metal_stack: MetalStack = "3lm") -> gf.Component:
    """Corner filler IO cell."""
    match metal_stack:
        case "3lm":
            return _import_gds(_IO_LIB / "cor" / "gf180mcu_fd_io__cor_3lm.gds")
        case "4lm":
            return _import_gds(_IO_LIB / "cor" / "gf180mcu_fd_io__cor_4lm.gds")
        case "5lm":
            return _import_gds(_IO_LIB / "cor" / "gf180mcu_fd_io__cor_5lm.gds")


# --- Power I/O ---
@gf.cell
def dvdd(metal_stack: MetalStack = "3lm") -> gf.Component:
    """DVDD power supply IO cell."""
    match metal_stack:
        case "3lm":
            return _import_gds(_IO_LIB / "dvdd" / "gf180mcu_fd_io__dvdd_3lm.gds")
        case "4lm":
            return _import_gds(_IO_LIB / "dvdd" / "gf180mcu_fd_io__dvdd_4lm.gds")
        case "5lm":
            return _import_gds(_IO_LIB / "dvdd" / "gf180mcu_fd_io__dvdd_5lm.gds")


@gf.cell
def dvss(metal_stack: MetalStack = "3lm") -> gf.Component:
    """DVSS power supply IO cell."""
    match metal_stack:
        case "3lm":
            return _import_gds(_IO_LIB / "dvss" / "gf180mcu_fd_io__dvss_3lm.gds")
        case "4lm":
            return _import_gds(_IO_LIB / "dvss" / "gf180mcu_fd_io__dvss_4lm.gds")
        case "5lm":
            return _import_gds(_IO_LIB / "dvss" / "gf180mcu_fd_io__dvss_5lm.gds")
