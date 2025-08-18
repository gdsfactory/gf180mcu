import sys

from gdsfactory.get_factories import get_cells
from gdsfactory.pdk import Pdk

from gf180mcu import config, diode, fet, layers
from gf180mcu.cap_mim import (
    cap_mim,
)
from gf180mcu.cap_mos import (
    cap_mos,
    cap_mos_inst,
)
from gf180mcu.config import PATH
from gf180mcu.diode import (
    diode_dw2ps,
    diode_nd2ps,
    diode_nw2ps,
    diode_pd2nw,
    diode_pw2dw,
    sc_diode,
)
from gf180mcu.fet import (
    add_gate_labels,
    add_inter_sd_labels,
    alter_interdig,
    bulk_gr_gen,
    get_patt_label,
    hv_gen,
    interdigit,
    labels_gen,
    nfet,
    nfet_06v0_nvt,
    nfet_deep_nwell,
    pfet,
    pfet_deep_nwell,
)
from gf180mcu.guardring import (
    pcmpgr_gen,
)
from gf180mcu.layers import (
    LAYER,
    LAYER_STACK,
    LAYER_VIEWS,
    LayerMap,
    get_layer_stack,
    layer,
)
from gf180mcu.res import (
    nplus_res,
    npolyf_res,
    plus_res_inst,
    polyf_res_inst,
    pplus_res,
    ppolyf_res,
    ppolyf_u_high_Rs_res,
    res,
    well_res,
)
from gf180mcu.tech import cross_sections, routing_strategies
from gf180mcu.via_generator import (
    via_generator,
    via_stack,
)
from gf180mcu.waveguides import bend, bend_s, straight, wire_corner, wire_corner45

__all__ = [
    "LAYER",
    "LAYER_STACK",
    "LAYER_VIEWS",
    "PATH",
    "LayerMap",
    "add_gate_labels",
    "add_inter_sd_labels",
    "alter_interdig",
    "bend",
    "bend_s",
    "bulk_gr_gen",
    "cap_mim",
    "cap_mos",
    "cap_mos",
    "cap_mos_inst",
    "config",
    "diode",
    "diode_dw2ps",
    "diode_nd2ps",
    "diode_nw2ps",
    "diode_pd2nw",
    "diode_pw2dw",
    "fet",
    "get_layer_stack",
    "get_patt_label",
    "hv_gen",
    "interdigit",
    "labels_gen",
    "layer",
    "layers",
    "nfet",
    "nfet_06v0_nvt",
    "nfet_deep_nwell",
    "nplus_res",
    "npolyf_res",
    "pcmpgr_gen",
    "pfet",
    "pfet_deep_nwell",
    "plus_res_inst",
    "polyf_res_inst",
    "pplus_res",
    "ppolyf_res",
    "ppolyf_u_high_Rs_res",
    "res",
    "sc_diode",
    "straight",
    "via_generator",
    "via_stack",
    "well_res",
    "wire_corner",
    "wire_corner45",
]
__version__ = "0.3.2"

cells = get_cells(sys.modules[__name__])


PDK = Pdk(
    name="gf180mcu",
    cells=cells,
    layers=LAYER,
    layer_views=LAYER_VIEWS,
    layer_stack=LAYER_STACK,
    cross_sections=cross_sections,
    routing_strategies=routing_strategies,
)
PDK.activate()
