"""GF180MCU digital standard cells imported from GDS.

Two libraries:
  - gf180mcu_fd_sc_mcu7t5v0: 7-track 5V standard cells (249 cells)
  - gf180mcu_fd_sc_mcu9t5v0: 9-track 5V standard cells (249 cells)
"""

from functools import partial
from pathlib import Path

import gdsfactory as gf

from gf180mcu.layers import LAYER

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

_SRC = Path(__file__).parent.parent / "src"


# ── 7-track 5V standard cells ──


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__addf_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/addf/gf180mcu_fd_sc_mcu7t5v0__addf_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__addf_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/addf/gf180mcu_fd_sc_mcu7t5v0__addf_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__addf_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/addf/gf180mcu_fd_sc_mcu7t5v0__addf_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__addh_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/addh/gf180mcu_fd_sc_mcu7t5v0__addh_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__addh_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/addh/gf180mcu_fd_sc_mcu7t5v0__addh_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__addh_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/addh/gf180mcu_fd_sc_mcu7t5v0__addh_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__and2_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/and2/gf180mcu_fd_sc_mcu7t5v0__and2_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__and2_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/and2/gf180mcu_fd_sc_mcu7t5v0__and2_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__and2_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/and2/gf180mcu_fd_sc_mcu7t5v0__and2_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__and3_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/and3/gf180mcu_fd_sc_mcu7t5v0__and3_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__and3_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/and3/gf180mcu_fd_sc_mcu7t5v0__and3_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__and3_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/and3/gf180mcu_fd_sc_mcu7t5v0__and3_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__and4_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/and4/gf180mcu_fd_sc_mcu7t5v0__and4_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__and4_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/and4/gf180mcu_fd_sc_mcu7t5v0__and4_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__and4_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/and4/gf180mcu_fd_sc_mcu7t5v0__and4_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__antenna() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/antenna/gf180mcu_fd_sc_mcu7t5v0__antenna.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__aoi21_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/aoi21/gf180mcu_fd_sc_mcu7t5v0__aoi21_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__aoi21_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/aoi21/gf180mcu_fd_sc_mcu7t5v0__aoi21_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__aoi21_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/aoi21/gf180mcu_fd_sc_mcu7t5v0__aoi21_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__aoi211_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/aoi211/gf180mcu_fd_sc_mcu7t5v0__aoi211_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__aoi211_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/aoi211/gf180mcu_fd_sc_mcu7t5v0__aoi211_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__aoi211_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/aoi211/gf180mcu_fd_sc_mcu7t5v0__aoi211_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__aoi22_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/aoi22/gf180mcu_fd_sc_mcu7t5v0__aoi22_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__aoi22_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/aoi22/gf180mcu_fd_sc_mcu7t5v0__aoi22_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__aoi22_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/aoi22/gf180mcu_fd_sc_mcu7t5v0__aoi22_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__aoi221_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/aoi221/gf180mcu_fd_sc_mcu7t5v0__aoi221_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__aoi221_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/aoi221/gf180mcu_fd_sc_mcu7t5v0__aoi221_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__aoi221_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/aoi221/gf180mcu_fd_sc_mcu7t5v0__aoi221_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__aoi222_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/aoi222/gf180mcu_fd_sc_mcu7t5v0__aoi222_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__aoi222_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/aoi222/gf180mcu_fd_sc_mcu7t5v0__aoi222_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__aoi222_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/aoi222/gf180mcu_fd_sc_mcu7t5v0__aoi222_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__buf_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/buf/gf180mcu_fd_sc_mcu7t5v0__buf_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__buf_12() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/buf/gf180mcu_fd_sc_mcu7t5v0__buf_12.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__buf_16() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/buf/gf180mcu_fd_sc_mcu7t5v0__buf_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__buf_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/buf/gf180mcu_fd_sc_mcu7t5v0__buf_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__buf_20() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/buf/gf180mcu_fd_sc_mcu7t5v0__buf_20.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__buf_3() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/buf/gf180mcu_fd_sc_mcu7t5v0__buf_3.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__buf_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/buf/gf180mcu_fd_sc_mcu7t5v0__buf_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__buf_8() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/buf/gf180mcu_fd_sc_mcu7t5v0__buf_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__bufz_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/bufz/gf180mcu_fd_sc_mcu7t5v0__bufz_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__bufz_12() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/bufz/gf180mcu_fd_sc_mcu7t5v0__bufz_12.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__bufz_16() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/bufz/gf180mcu_fd_sc_mcu7t5v0__bufz_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__bufz_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/bufz/gf180mcu_fd_sc_mcu7t5v0__bufz_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__bufz_3() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/bufz/gf180mcu_fd_sc_mcu7t5v0__bufz_3.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__bufz_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/bufz/gf180mcu_fd_sc_mcu7t5v0__bufz_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__bufz_8() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/bufz/gf180mcu_fd_sc_mcu7t5v0__bufz_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkbuf_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu7t5v0__clkbuf_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkbuf_12() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu7t5v0__clkbuf_12.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkbuf_16() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu7t5v0__clkbuf_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkbuf_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu7t5v0__clkbuf_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkbuf_20() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu7t5v0__clkbuf_20.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkbuf_3() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu7t5v0__clkbuf_3.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkbuf_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu7t5v0__clkbuf_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkbuf_8() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu7t5v0__clkbuf_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkinv/gf180mcu_fd_sc_mcu7t5v0__clkinv_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_12() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkinv/gf180mcu_fd_sc_mcu7t5v0__clkinv_12.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_16() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkinv/gf180mcu_fd_sc_mcu7t5v0__clkinv_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkinv/gf180mcu_fd_sc_mcu7t5v0__clkinv_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_20() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkinv/gf180mcu_fd_sc_mcu7t5v0__clkinv_20.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_3() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkinv/gf180mcu_fd_sc_mcu7t5v0__clkinv_3.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkinv/gf180mcu_fd_sc_mcu7t5v0__clkinv_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_8() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/clkinv/gf180mcu_fd_sc_mcu7t5v0__clkinv_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffnq/gf180mcu_fd_sc_mcu7t5v0__dffnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffnq/gf180mcu_fd_sc_mcu7t5v0__dffnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffnq/gf180mcu_fd_sc_mcu7t5v0__dffnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffnrnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffnrnq/gf180mcu_fd_sc_mcu7t5v0__dffnrnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffnrnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffnrnq/gf180mcu_fd_sc_mcu7t5v0__dffnrnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffnrnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffnrnq/gf180mcu_fd_sc_mcu7t5v0__dffnrnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffnrsnq/gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffnrsnq/gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffnrsnq/gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffnsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffnsnq/gf180mcu_fd_sc_mcu7t5v0__dffnsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffnsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffnsnq/gf180mcu_fd_sc_mcu7t5v0__dffnsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffnsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffnsnq/gf180mcu_fd_sc_mcu7t5v0__dffnsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffq_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dffq/gf180mcu_fd_sc_mcu7t5v0__dffq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffq_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dffq/gf180mcu_fd_sc_mcu7t5v0__dffq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffq_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dffq/gf180mcu_fd_sc_mcu7t5v0__dffq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffq_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dffq/gf180mcu_fd_sc_mcu7t5v0__sdffq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffq_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dffq/gf180mcu_fd_sc_mcu7t5v0__sdffq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffq_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dffq/gf180mcu_fd_sc_mcu7t5v0__sdffq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffrnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffrnq/gf180mcu_fd_sc_mcu7t5v0__dffrnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffrnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffrnq/gf180mcu_fd_sc_mcu7t5v0__dffrnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffrnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffrnq/gf180mcu_fd_sc_mcu7t5v0__dffrnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffrnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffrnq/gf180mcu_fd_sc_mcu7t5v0__sdffrnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffrnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffrnq/gf180mcu_fd_sc_mcu7t5v0__sdffrnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffrnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffrnq/gf180mcu_fd_sc_mcu7t5v0__sdffrnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffrsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffrsnq/gf180mcu_fd_sc_mcu7t5v0__dffrsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffrsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffrsnq/gf180mcu_fd_sc_mcu7t5v0__dffrsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffrsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffrsnq/gf180mcu_fd_sc_mcu7t5v0__dffrsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffrsnq/gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffrsnq/gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffrsnq/gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffsnq/gf180mcu_fd_sc_mcu7t5v0__dffsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffsnq/gf180mcu_fd_sc_mcu7t5v0__dffsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dffsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffsnq/gf180mcu_fd_sc_mcu7t5v0__dffsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffsnq/gf180mcu_fd_sc_mcu7t5v0__sdffsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffsnq/gf180mcu_fd_sc_mcu7t5v0__sdffsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/dffsnq/gf180mcu_fd_sc_mcu7t5v0__sdffsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dlya_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dlya/gf180mcu_fd_sc_mcu7t5v0__dlya_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dlya_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dlya/gf180mcu_fd_sc_mcu7t5v0__dlya_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dlya_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dlya/gf180mcu_fd_sc_mcu7t5v0__dlya_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dlyb_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dlyb/gf180mcu_fd_sc_mcu7t5v0__dlyb_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dlyb_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dlyb/gf180mcu_fd_sc_mcu7t5v0__dlyb_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dlyb_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dlyb/gf180mcu_fd_sc_mcu7t5v0__dlyb_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dlyc_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dlyc/gf180mcu_fd_sc_mcu7t5v0__dlyc_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dlyc_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dlyc/gf180mcu_fd_sc_mcu7t5v0__dlyc_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dlyc_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dlyc/gf180mcu_fd_sc_mcu7t5v0__dlyc_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dlyd_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dlyd/gf180mcu_fd_sc_mcu7t5v0__dlyd_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dlyd_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dlyd/gf180mcu_fd_sc_mcu7t5v0__dlyd_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__dlyd_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/dlyd/gf180mcu_fd_sc_mcu7t5v0__dlyd_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__endcap() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/endcap/gf180mcu_fd_sc_mcu7t5v0__endcap.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__fill_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/fill/gf180mcu_fd_sc_mcu7t5v0__fill_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__fill_16() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/fill/gf180mcu_fd_sc_mcu7t5v0__fill_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__fill_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/fill/gf180mcu_fd_sc_mcu7t5v0__fill_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__fill_32() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/fill/gf180mcu_fd_sc_mcu7t5v0__fill_32.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__fill_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/fill/gf180mcu_fd_sc_mcu7t5v0__fill_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__fill_64() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/fill/gf180mcu_fd_sc_mcu7t5v0__fill_64.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__fill_8() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/fill/gf180mcu_fd_sc_mcu7t5v0__fill_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__fillcap_16() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/fillcap/gf180mcu_fd_sc_mcu7t5v0__fillcap_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__fillcap_32() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/fillcap/gf180mcu_fd_sc_mcu7t5v0__fillcap_32.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__fillcap_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/fillcap/gf180mcu_fd_sc_mcu7t5v0__fillcap_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__fillcap_64() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/fillcap/gf180mcu_fd_sc_mcu7t5v0__fillcap_64.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__fillcap_8() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/fillcap/gf180mcu_fd_sc_mcu7t5v0__fillcap_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__filltie() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/filltie/gf180mcu_fd_sc_mcu7t5v0__filltie.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__hold() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/hold/gf180mcu_fd_sc_mcu7t5v0__hold.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__icgtn_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/icgtn/gf180mcu_fd_sc_mcu7t5v0__icgtn_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__icgtn_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/icgtn/gf180mcu_fd_sc_mcu7t5v0__icgtn_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__icgtn_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/icgtn/gf180mcu_fd_sc_mcu7t5v0__icgtn_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__icgtp_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/icgtp/gf180mcu_fd_sc_mcu7t5v0__icgtp_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__icgtp_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/icgtp/gf180mcu_fd_sc_mcu7t5v0__icgtp_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__icgtp_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/icgtp/gf180mcu_fd_sc_mcu7t5v0__icgtp_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__clkinv_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_12() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__clkinv_12.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_16() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__clkinv_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__clkinv_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_20() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__clkinv_20.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_3() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__clkinv_3.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__clkinv_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__clkinv_8() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__clkinv_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__inv_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__inv_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__inv_12() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__inv_12.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__inv_16() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__inv_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__inv_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__inv_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__inv_20() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__inv_20.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__inv_3() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__inv_3.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__inv_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__inv_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__inv_8() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/inv/gf180mcu_fd_sc_mcu7t5v0__inv_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__invz_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/invz/gf180mcu_fd_sc_mcu7t5v0__invz_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__invz_12() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/invz/gf180mcu_fd_sc_mcu7t5v0__invz_12.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__invz_16() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/invz/gf180mcu_fd_sc_mcu7t5v0__invz_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__invz_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/invz/gf180mcu_fd_sc_mcu7t5v0__invz_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__invz_3() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/invz/gf180mcu_fd_sc_mcu7t5v0__invz_3.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__invz_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/invz/gf180mcu_fd_sc_mcu7t5v0__invz_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__invz_8() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/invz/gf180mcu_fd_sc_mcu7t5v0__invz_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__latq_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/latq/gf180mcu_fd_sc_mcu7t5v0__latq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__latq_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/latq/gf180mcu_fd_sc_mcu7t5v0__latq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__latq_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/latq/gf180mcu_fd_sc_mcu7t5v0__latq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__latrnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/latrnq/gf180mcu_fd_sc_mcu7t5v0__latrnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__latrnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/latrnq/gf180mcu_fd_sc_mcu7t5v0__latrnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__latrnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/latrnq/gf180mcu_fd_sc_mcu7t5v0__latrnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__latrsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/latrsnq/gf180mcu_fd_sc_mcu7t5v0__latrsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__latrsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/latrsnq/gf180mcu_fd_sc_mcu7t5v0__latrsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__latrsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/latrsnq/gf180mcu_fd_sc_mcu7t5v0__latrsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__latsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/latsnq/gf180mcu_fd_sc_mcu7t5v0__latsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__latsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/latsnq/gf180mcu_fd_sc_mcu7t5v0__latsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__latsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/latsnq/gf180mcu_fd_sc_mcu7t5v0__latsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__mux2_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/mux2/gf180mcu_fd_sc_mcu7t5v0__mux2_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__mux2_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/mux2/gf180mcu_fd_sc_mcu7t5v0__mux2_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__mux2_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/mux2/gf180mcu_fd_sc_mcu7t5v0__mux2_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__mux4_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/mux4/gf180mcu_fd_sc_mcu7t5v0__mux4_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__mux4_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/mux4/gf180mcu_fd_sc_mcu7t5v0__mux4_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__mux4_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/mux4/gf180mcu_fd_sc_mcu7t5v0__mux4_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nand2_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/nand2/gf180mcu_fd_sc_mcu7t5v0__nand2_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nand2_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/nand2/gf180mcu_fd_sc_mcu7t5v0__nand2_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nand2_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/nand2/gf180mcu_fd_sc_mcu7t5v0__nand2_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nand3_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/nand3/gf180mcu_fd_sc_mcu7t5v0__nand3_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nand3_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/nand3/gf180mcu_fd_sc_mcu7t5v0__nand3_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nand3_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/nand3/gf180mcu_fd_sc_mcu7t5v0__nand3_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nand4_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/nand4/gf180mcu_fd_sc_mcu7t5v0__nand4_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nand4_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/nand4/gf180mcu_fd_sc_mcu7t5v0__nand4_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nand4_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/nand4/gf180mcu_fd_sc_mcu7t5v0__nand4_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nor2_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/nor2/gf180mcu_fd_sc_mcu7t5v0__nor2_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nor2_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/nor2/gf180mcu_fd_sc_mcu7t5v0__nor2_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nor2_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/nor2/gf180mcu_fd_sc_mcu7t5v0__nor2_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nor3_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/nor3/gf180mcu_fd_sc_mcu7t5v0__nor3_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nor3_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/nor3/gf180mcu_fd_sc_mcu7t5v0__nor3_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nor3_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/nor3/gf180mcu_fd_sc_mcu7t5v0__nor3_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nor4_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/nor4/gf180mcu_fd_sc_mcu7t5v0__nor4_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nor4_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/nor4/gf180mcu_fd_sc_mcu7t5v0__nor4_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__nor4_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/nor4/gf180mcu_fd_sc_mcu7t5v0__nor4_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai21_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai21/gf180mcu_fd_sc_mcu7t5v0__oai21_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai21_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai21/gf180mcu_fd_sc_mcu7t5v0__oai21_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai21_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai21/gf180mcu_fd_sc_mcu7t5v0__oai21_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai211_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai211/gf180mcu_fd_sc_mcu7t5v0__oai211_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai211_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai211/gf180mcu_fd_sc_mcu7t5v0__oai211_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai211_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai211/gf180mcu_fd_sc_mcu7t5v0__oai211_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai22_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai22/gf180mcu_fd_sc_mcu7t5v0__oai22_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai22_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai22/gf180mcu_fd_sc_mcu7t5v0__oai22_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai22_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai22/gf180mcu_fd_sc_mcu7t5v0__oai22_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai221_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai221/gf180mcu_fd_sc_mcu7t5v0__oai221_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai221_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai221/gf180mcu_fd_sc_mcu7t5v0__oai221_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai221_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai221/gf180mcu_fd_sc_mcu7t5v0__oai221_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai222_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai222/gf180mcu_fd_sc_mcu7t5v0__oai222_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai222_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai222/gf180mcu_fd_sc_mcu7t5v0__oai222_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai222_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai222/gf180mcu_fd_sc_mcu7t5v0__oai222_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai31_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai31/gf180mcu_fd_sc_mcu7t5v0__oai31_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai31_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai31/gf180mcu_fd_sc_mcu7t5v0__oai31_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai31_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai31/gf180mcu_fd_sc_mcu7t5v0__oai31_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai32_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai32/gf180mcu_fd_sc_mcu7t5v0__oai32_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai32_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai32/gf180mcu_fd_sc_mcu7t5v0__oai32_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai32_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai32/gf180mcu_fd_sc_mcu7t5v0__oai32_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai33_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai33/gf180mcu_fd_sc_mcu7t5v0__oai33_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai33_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai33/gf180mcu_fd_sc_mcu7t5v0__oai33_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__oai33_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/oai33/gf180mcu_fd_sc_mcu7t5v0__oai33_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__or2_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/or2/gf180mcu_fd_sc_mcu7t5v0__or2_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__or2_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/or2/gf180mcu_fd_sc_mcu7t5v0__or2_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__or2_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/or2/gf180mcu_fd_sc_mcu7t5v0__or2_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__or3_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/or3/gf180mcu_fd_sc_mcu7t5v0__or3_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__or3_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/or3/gf180mcu_fd_sc_mcu7t5v0__or3_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__or3_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/or3/gf180mcu_fd_sc_mcu7t5v0__or3_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__or4_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/or4/gf180mcu_fd_sc_mcu7t5v0__or4_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__or4_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/or4/gf180mcu_fd_sc_mcu7t5v0__or4_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__or4_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/or4/gf180mcu_fd_sc_mcu7t5v0__or4_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/sdffq/gf180mcu_fd_sc_mcu7t5v0__sdffq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/sdffq/gf180mcu_fd_sc_mcu7t5v0__sdffq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/sdffq/gf180mcu_fd_sc_mcu7t5v0__sdffq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffrnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/sdffrnq/gf180mcu_fd_sc_mcu7t5v0__sdffrnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffrnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/sdffrnq/gf180mcu_fd_sc_mcu7t5v0__sdffrnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffrnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/sdffrnq/gf180mcu_fd_sc_mcu7t5v0__sdffrnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/sdffrsnq/gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/sdffrsnq/gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/sdffrsnq/gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/sdffsnq/gf180mcu_fd_sc_mcu7t5v0__sdffsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/sdffsnq/gf180mcu_fd_sc_mcu7t5v0__sdffsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__sdffsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/sdffsnq/gf180mcu_fd_sc_mcu7t5v0__sdffsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__tieh() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/tieh/gf180mcu_fd_sc_mcu7t5v0__tieh.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__tiel() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/tiel/gf180mcu_fd_sc_mcu7t5v0__tiel.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__xnor2_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/xnor2/gf180mcu_fd_sc_mcu7t5v0__xnor2_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__xnor2_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/xnor2/gf180mcu_fd_sc_mcu7t5v0__xnor2_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__xnor2_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/xnor2/gf180mcu_fd_sc_mcu7t5v0__xnor2_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__xnor3_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/xnor3/gf180mcu_fd_sc_mcu7t5v0__xnor3_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__xnor3_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/xnor3/gf180mcu_fd_sc_mcu7t5v0__xnor3_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__xnor3_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu7t5v0/cells/xnor3/gf180mcu_fd_sc_mcu7t5v0__xnor3_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__xor2_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/xor2/gf180mcu_fd_sc_mcu7t5v0__xor2_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__xor2_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/xor2/gf180mcu_fd_sc_mcu7t5v0__xor2_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__xor2_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/xor2/gf180mcu_fd_sc_mcu7t5v0__xor2_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__xor3_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/xor3/gf180mcu_fd_sc_mcu7t5v0__xor3_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__xor3_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/xor3/gf180mcu_fd_sc_mcu7t5v0__xor3_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu7t5v0__xor3_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu7t5v0/cells/xor3/gf180mcu_fd_sc_mcu7t5v0__xor3_4.gds"
    )


# ── 9-track 5V standard cells ──


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__addf_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/addf/gf180mcu_fd_sc_mcu9t5v0__addf_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__addf_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/addf/gf180mcu_fd_sc_mcu9t5v0__addf_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__addf_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/addf/gf180mcu_fd_sc_mcu9t5v0__addf_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__addh_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/addh/gf180mcu_fd_sc_mcu9t5v0__addh_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__addh_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/addh/gf180mcu_fd_sc_mcu9t5v0__addh_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__addh_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/addh/gf180mcu_fd_sc_mcu9t5v0__addh_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__and2_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/and2/gf180mcu_fd_sc_mcu9t5v0__and2_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__and2_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/and2/gf180mcu_fd_sc_mcu9t5v0__and2_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__and2_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/and2/gf180mcu_fd_sc_mcu9t5v0__and2_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__and3_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/and3/gf180mcu_fd_sc_mcu9t5v0__and3_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__and3_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/and3/gf180mcu_fd_sc_mcu9t5v0__and3_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__and3_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/and3/gf180mcu_fd_sc_mcu9t5v0__and3_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__and4_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/and4/gf180mcu_fd_sc_mcu9t5v0__and4_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__and4_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/and4/gf180mcu_fd_sc_mcu9t5v0__and4_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__and4_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/and4/gf180mcu_fd_sc_mcu9t5v0__and4_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__antenna() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/antenna/gf180mcu_fd_sc_mcu9t5v0__antenna.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__aoi21_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/aoi21/gf180mcu_fd_sc_mcu9t5v0__aoi21_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__aoi21_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/aoi21/gf180mcu_fd_sc_mcu9t5v0__aoi21_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__aoi21_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/aoi21/gf180mcu_fd_sc_mcu9t5v0__aoi21_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__aoi211_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/aoi211/gf180mcu_fd_sc_mcu9t5v0__aoi211_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__aoi211_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/aoi211/gf180mcu_fd_sc_mcu9t5v0__aoi211_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__aoi211_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/aoi211/gf180mcu_fd_sc_mcu9t5v0__aoi211_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__aoi22_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/aoi22/gf180mcu_fd_sc_mcu9t5v0__aoi22_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__aoi22_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/aoi22/gf180mcu_fd_sc_mcu9t5v0__aoi22_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__aoi22_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/aoi22/gf180mcu_fd_sc_mcu9t5v0__aoi22_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__aoi221_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/aoi221/gf180mcu_fd_sc_mcu9t5v0__aoi221_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__aoi221_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/aoi221/gf180mcu_fd_sc_mcu9t5v0__aoi221_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__aoi221_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/aoi221/gf180mcu_fd_sc_mcu9t5v0__aoi221_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__aoi222_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/aoi222/gf180mcu_fd_sc_mcu9t5v0__aoi222_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__aoi222_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/aoi222/gf180mcu_fd_sc_mcu9t5v0__aoi222_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__aoi222_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/aoi222/gf180mcu_fd_sc_mcu9t5v0__aoi222_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__buf_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/buf/gf180mcu_fd_sc_mcu9t5v0__buf_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__buf_12() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/buf/gf180mcu_fd_sc_mcu9t5v0__buf_12.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__buf_16() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/buf/gf180mcu_fd_sc_mcu9t5v0__buf_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__buf_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/buf/gf180mcu_fd_sc_mcu9t5v0__buf_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__buf_20() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/buf/gf180mcu_fd_sc_mcu9t5v0__buf_20.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__buf_3() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/buf/gf180mcu_fd_sc_mcu9t5v0__buf_3.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__buf_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/buf/gf180mcu_fd_sc_mcu9t5v0__buf_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__buf_8() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/buf/gf180mcu_fd_sc_mcu9t5v0__buf_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__bufz_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/bufz/gf180mcu_fd_sc_mcu9t5v0__bufz_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__bufz_12() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/bufz/gf180mcu_fd_sc_mcu9t5v0__bufz_12.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__bufz_16() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/bufz/gf180mcu_fd_sc_mcu9t5v0__bufz_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__bufz_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/bufz/gf180mcu_fd_sc_mcu9t5v0__bufz_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__bufz_3() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/bufz/gf180mcu_fd_sc_mcu9t5v0__bufz_3.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__bufz_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/bufz/gf180mcu_fd_sc_mcu9t5v0__bufz_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__bufz_8() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/bufz/gf180mcu_fd_sc_mcu9t5v0__bufz_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkbuf_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu9t5v0__clkbuf_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkbuf_12() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu9t5v0__clkbuf_12.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkbuf_16() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu9t5v0__clkbuf_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkbuf_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu9t5v0__clkbuf_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkbuf_20() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu9t5v0__clkbuf_20.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkbuf_3() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu9t5v0__clkbuf_3.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkbuf_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu9t5v0__clkbuf_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkbuf_8() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkbuf/gf180mcu_fd_sc_mcu9t5v0__clkbuf_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkinv/gf180mcu_fd_sc_mcu9t5v0__clkinv_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_12() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkinv/gf180mcu_fd_sc_mcu9t5v0__clkinv_12.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_16() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkinv/gf180mcu_fd_sc_mcu9t5v0__clkinv_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkinv/gf180mcu_fd_sc_mcu9t5v0__clkinv_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_20() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkinv/gf180mcu_fd_sc_mcu9t5v0__clkinv_20.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_3() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkinv/gf180mcu_fd_sc_mcu9t5v0__clkinv_3.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkinv/gf180mcu_fd_sc_mcu9t5v0__clkinv_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_8() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/clkinv/gf180mcu_fd_sc_mcu9t5v0__clkinv_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffnq/gf180mcu_fd_sc_mcu9t5v0__dffnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffnq/gf180mcu_fd_sc_mcu9t5v0__dffnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffnq/gf180mcu_fd_sc_mcu9t5v0__dffnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffnrnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffnrnq/gf180mcu_fd_sc_mcu9t5v0__dffnrnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffnrnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffnrnq/gf180mcu_fd_sc_mcu9t5v0__dffnrnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffnrnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffnrnq/gf180mcu_fd_sc_mcu9t5v0__dffnrnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffnrsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffnrsnq/gf180mcu_fd_sc_mcu9t5v0__dffnrsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffnrsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffnrsnq/gf180mcu_fd_sc_mcu9t5v0__dffnrsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffnrsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffnrsnq/gf180mcu_fd_sc_mcu9t5v0__dffnrsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffnsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffnsnq/gf180mcu_fd_sc_mcu9t5v0__dffnsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffnsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffnsnq/gf180mcu_fd_sc_mcu9t5v0__dffnsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffnsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffnsnq/gf180mcu_fd_sc_mcu9t5v0__dffnsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffq_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dffq/gf180mcu_fd_sc_mcu9t5v0__dffq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffq_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dffq/gf180mcu_fd_sc_mcu9t5v0__dffq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffq_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dffq/gf180mcu_fd_sc_mcu9t5v0__dffq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffq_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dffq/gf180mcu_fd_sc_mcu9t5v0__sdffq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffq_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dffq/gf180mcu_fd_sc_mcu9t5v0__sdffq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffq_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dffq/gf180mcu_fd_sc_mcu9t5v0__sdffq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffrnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffrnq/gf180mcu_fd_sc_mcu9t5v0__dffrnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffrnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffrnq/gf180mcu_fd_sc_mcu9t5v0__dffrnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffrnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffrnq/gf180mcu_fd_sc_mcu9t5v0__dffrnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffrnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffrnq/gf180mcu_fd_sc_mcu9t5v0__sdffrnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffrnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffrnq/gf180mcu_fd_sc_mcu9t5v0__sdffrnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffrnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffrnq/gf180mcu_fd_sc_mcu9t5v0__sdffrnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffrsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffrsnq/gf180mcu_fd_sc_mcu9t5v0__dffrsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffrsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffrsnq/gf180mcu_fd_sc_mcu9t5v0__dffrsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffrsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffrsnq/gf180mcu_fd_sc_mcu9t5v0__dffrsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffrsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffrsnq/gf180mcu_fd_sc_mcu9t5v0__sdffrsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffrsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffrsnq/gf180mcu_fd_sc_mcu9t5v0__sdffrsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffrsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffrsnq/gf180mcu_fd_sc_mcu9t5v0__sdffrsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffsnq/gf180mcu_fd_sc_mcu9t5v0__dffsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffsnq/gf180mcu_fd_sc_mcu9t5v0__dffsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dffsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffsnq/gf180mcu_fd_sc_mcu9t5v0__dffsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffsnq/gf180mcu_fd_sc_mcu9t5v0__sdffsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffsnq/gf180mcu_fd_sc_mcu9t5v0__sdffsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/dffsnq/gf180mcu_fd_sc_mcu9t5v0__sdffsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dlya_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dlya/gf180mcu_fd_sc_mcu9t5v0__dlya_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dlya_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dlya/gf180mcu_fd_sc_mcu9t5v0__dlya_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dlya_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dlya/gf180mcu_fd_sc_mcu9t5v0__dlya_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dlyb_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dlyb/gf180mcu_fd_sc_mcu9t5v0__dlyb_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dlyb_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dlyb/gf180mcu_fd_sc_mcu9t5v0__dlyb_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dlyb_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dlyb/gf180mcu_fd_sc_mcu9t5v0__dlyb_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dlyc_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dlyc/gf180mcu_fd_sc_mcu9t5v0__dlyc_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dlyc_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dlyc/gf180mcu_fd_sc_mcu9t5v0__dlyc_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dlyc_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dlyc/gf180mcu_fd_sc_mcu9t5v0__dlyc_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dlyd_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dlyd/gf180mcu_fd_sc_mcu9t5v0__dlyd_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dlyd_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dlyd/gf180mcu_fd_sc_mcu9t5v0__dlyd_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__dlyd_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/dlyd/gf180mcu_fd_sc_mcu9t5v0__dlyd_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__endcap() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/endcap/gf180mcu_fd_sc_mcu9t5v0__endcap.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__fill_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/fill/gf180mcu_fd_sc_mcu9t5v0__fill_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__fill_16() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/fill/gf180mcu_fd_sc_mcu9t5v0__fill_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__fill_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/fill/gf180mcu_fd_sc_mcu9t5v0__fill_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__fill_32() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/fill/gf180mcu_fd_sc_mcu9t5v0__fill_32.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__fill_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/fill/gf180mcu_fd_sc_mcu9t5v0__fill_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__fill_64() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/fill/gf180mcu_fd_sc_mcu9t5v0__fill_64.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__fill_8() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/fill/gf180mcu_fd_sc_mcu9t5v0__fill_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__fillcap_16() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/fillcap/gf180mcu_fd_sc_mcu9t5v0__fillcap_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__fillcap_32() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/fillcap/gf180mcu_fd_sc_mcu9t5v0__fillcap_32.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__fillcap_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/fillcap/gf180mcu_fd_sc_mcu9t5v0__fillcap_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__fillcap_64() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/fillcap/gf180mcu_fd_sc_mcu9t5v0__fillcap_64.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__fillcap_8() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/fillcap/gf180mcu_fd_sc_mcu9t5v0__fillcap_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__filltie() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/filltie/gf180mcu_fd_sc_mcu9t5v0__filltie.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__hold() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/hold/gf180mcu_fd_sc_mcu9t5v0__hold.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__icgtn_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/icgtn/gf180mcu_fd_sc_mcu9t5v0__icgtn_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__icgtn_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/icgtn/gf180mcu_fd_sc_mcu9t5v0__icgtn_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__icgtn_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/icgtn/gf180mcu_fd_sc_mcu9t5v0__icgtn_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__icgtp_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/icgtp/gf180mcu_fd_sc_mcu9t5v0__icgtp_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__icgtp_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/icgtp/gf180mcu_fd_sc_mcu9t5v0__icgtp_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__icgtp_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/icgtp/gf180mcu_fd_sc_mcu9t5v0__icgtp_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__clkinv_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_12() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__clkinv_12.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_16() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__clkinv_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__clkinv_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_20() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__clkinv_20.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_3() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__clkinv_3.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__clkinv_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__clkinv_8() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__clkinv_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__inv_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__inv_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__inv_12() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__inv_12.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__inv_16() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__inv_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__inv_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__inv_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__inv_20() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__inv_20.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__inv_3() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__inv_3.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__inv_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__inv_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__inv_8() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/inv/gf180mcu_fd_sc_mcu9t5v0__inv_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__invz_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/invz/gf180mcu_fd_sc_mcu9t5v0__invz_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__invz_12() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/invz/gf180mcu_fd_sc_mcu9t5v0__invz_12.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__invz_16() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/invz/gf180mcu_fd_sc_mcu9t5v0__invz_16.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__invz_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/invz/gf180mcu_fd_sc_mcu9t5v0__invz_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__invz_3() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/invz/gf180mcu_fd_sc_mcu9t5v0__invz_3.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__invz_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/invz/gf180mcu_fd_sc_mcu9t5v0__invz_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__invz_8() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/invz/gf180mcu_fd_sc_mcu9t5v0__invz_8.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__latq_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/latq/gf180mcu_fd_sc_mcu9t5v0__latq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__latq_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/latq/gf180mcu_fd_sc_mcu9t5v0__latq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__latq_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/latq/gf180mcu_fd_sc_mcu9t5v0__latq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__latrnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/latrnq/gf180mcu_fd_sc_mcu9t5v0__latrnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__latrnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/latrnq/gf180mcu_fd_sc_mcu9t5v0__latrnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__latrnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/latrnq/gf180mcu_fd_sc_mcu9t5v0__latrnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__latrsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/latrsnq/gf180mcu_fd_sc_mcu9t5v0__latrsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__latrsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/latrsnq/gf180mcu_fd_sc_mcu9t5v0__latrsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__latrsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/latrsnq/gf180mcu_fd_sc_mcu9t5v0__latrsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__latsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/latsnq/gf180mcu_fd_sc_mcu9t5v0__latsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__latsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/latsnq/gf180mcu_fd_sc_mcu9t5v0__latsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__latsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/latsnq/gf180mcu_fd_sc_mcu9t5v0__latsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__mux2_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/mux2/gf180mcu_fd_sc_mcu9t5v0__mux2_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__mux2_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/mux2/gf180mcu_fd_sc_mcu9t5v0__mux2_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__mux2_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/mux2/gf180mcu_fd_sc_mcu9t5v0__mux2_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__mux4_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/mux4/gf180mcu_fd_sc_mcu9t5v0__mux4_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__mux4_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/mux4/gf180mcu_fd_sc_mcu9t5v0__mux4_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__mux4_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/mux4/gf180mcu_fd_sc_mcu9t5v0__mux4_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nand2_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/nand2/gf180mcu_fd_sc_mcu9t5v0__nand2_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nand2_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/nand2/gf180mcu_fd_sc_mcu9t5v0__nand2_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nand2_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/nand2/gf180mcu_fd_sc_mcu9t5v0__nand2_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nand3_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/nand3/gf180mcu_fd_sc_mcu9t5v0__nand3_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nand3_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/nand3/gf180mcu_fd_sc_mcu9t5v0__nand3_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nand3_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/nand3/gf180mcu_fd_sc_mcu9t5v0__nand3_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nand4_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/nand4/gf180mcu_fd_sc_mcu9t5v0__nand4_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nand4_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/nand4/gf180mcu_fd_sc_mcu9t5v0__nand4_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nand4_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/nand4/gf180mcu_fd_sc_mcu9t5v0__nand4_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nor2_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/nor2/gf180mcu_fd_sc_mcu9t5v0__nor2_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nor2_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/nor2/gf180mcu_fd_sc_mcu9t5v0__nor2_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nor2_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/nor2/gf180mcu_fd_sc_mcu9t5v0__nor2_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nor3_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/nor3/gf180mcu_fd_sc_mcu9t5v0__nor3_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nor3_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/nor3/gf180mcu_fd_sc_mcu9t5v0__nor3_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nor3_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/nor3/gf180mcu_fd_sc_mcu9t5v0__nor3_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nor4_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/nor4/gf180mcu_fd_sc_mcu9t5v0__nor4_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nor4_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/nor4/gf180mcu_fd_sc_mcu9t5v0__nor4_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__nor4_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/nor4/gf180mcu_fd_sc_mcu9t5v0__nor4_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai21_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai21/gf180mcu_fd_sc_mcu9t5v0__oai21_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai21_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai21/gf180mcu_fd_sc_mcu9t5v0__oai21_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai21_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai21/gf180mcu_fd_sc_mcu9t5v0__oai21_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai211_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai211/gf180mcu_fd_sc_mcu9t5v0__oai211_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai211_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai211/gf180mcu_fd_sc_mcu9t5v0__oai211_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai211_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai211/gf180mcu_fd_sc_mcu9t5v0__oai211_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai22_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai22/gf180mcu_fd_sc_mcu9t5v0__oai22_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai22_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai22/gf180mcu_fd_sc_mcu9t5v0__oai22_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai22_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai22/gf180mcu_fd_sc_mcu9t5v0__oai22_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai221_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai221/gf180mcu_fd_sc_mcu9t5v0__oai221_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai221_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai221/gf180mcu_fd_sc_mcu9t5v0__oai221_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai221_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai221/gf180mcu_fd_sc_mcu9t5v0__oai221_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai222_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai222/gf180mcu_fd_sc_mcu9t5v0__oai222_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai222_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai222/gf180mcu_fd_sc_mcu9t5v0__oai222_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai222_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai222/gf180mcu_fd_sc_mcu9t5v0__oai222_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai31_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai31/gf180mcu_fd_sc_mcu9t5v0__oai31_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai31_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai31/gf180mcu_fd_sc_mcu9t5v0__oai31_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai31_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai31/gf180mcu_fd_sc_mcu9t5v0__oai31_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai32_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai32/gf180mcu_fd_sc_mcu9t5v0__oai32_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai32_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai32/gf180mcu_fd_sc_mcu9t5v0__oai32_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai32_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai32/gf180mcu_fd_sc_mcu9t5v0__oai32_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai33_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai33/gf180mcu_fd_sc_mcu9t5v0__oai33_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai33_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai33/gf180mcu_fd_sc_mcu9t5v0__oai33_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__oai33_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/oai33/gf180mcu_fd_sc_mcu9t5v0__oai33_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__or2_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/or2/gf180mcu_fd_sc_mcu9t5v0__or2_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__or2_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/or2/gf180mcu_fd_sc_mcu9t5v0__or2_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__or2_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/or2/gf180mcu_fd_sc_mcu9t5v0__or2_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__or3_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/or3/gf180mcu_fd_sc_mcu9t5v0__or3_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__or3_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/or3/gf180mcu_fd_sc_mcu9t5v0__or3_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__or3_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/or3/gf180mcu_fd_sc_mcu9t5v0__or3_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__or4_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/or4/gf180mcu_fd_sc_mcu9t5v0__or4_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__or4_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/or4/gf180mcu_fd_sc_mcu9t5v0__or4_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__or4_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/or4/gf180mcu_fd_sc_mcu9t5v0__or4_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/sdffq/gf180mcu_fd_sc_mcu9t5v0__sdffq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/sdffq/gf180mcu_fd_sc_mcu9t5v0__sdffq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/sdffq/gf180mcu_fd_sc_mcu9t5v0__sdffq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffrnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/sdffrnq/gf180mcu_fd_sc_mcu9t5v0__sdffrnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffrnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/sdffrnq/gf180mcu_fd_sc_mcu9t5v0__sdffrnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffrnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/sdffrnq/gf180mcu_fd_sc_mcu9t5v0__sdffrnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffrsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/sdffrsnq/gf180mcu_fd_sc_mcu9t5v0__sdffrsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffrsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/sdffrsnq/gf180mcu_fd_sc_mcu9t5v0__sdffrsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffrsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/sdffrsnq/gf180mcu_fd_sc_mcu9t5v0__sdffrsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffsnq_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/sdffsnq/gf180mcu_fd_sc_mcu9t5v0__sdffsnq_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffsnq_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/sdffsnq/gf180mcu_fd_sc_mcu9t5v0__sdffsnq_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__sdffsnq_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/sdffsnq/gf180mcu_fd_sc_mcu9t5v0__sdffsnq_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__tieh() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/tieh/gf180mcu_fd_sc_mcu9t5v0__tieh.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__tiel() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/tiel/gf180mcu_fd_sc_mcu9t5v0__tiel.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__xnor2_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/xnor2/gf180mcu_fd_sc_mcu9t5v0__xnor2_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__xnor2_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/xnor2/gf180mcu_fd_sc_mcu9t5v0__xnor2_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__xnor2_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/xnor2/gf180mcu_fd_sc_mcu9t5v0__xnor2_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__xnor3_1() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/xnor3/gf180mcu_fd_sc_mcu9t5v0__xnor3_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__xnor3_2() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/xnor3/gf180mcu_fd_sc_mcu9t5v0__xnor3_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__xnor3_4() -> gf.Component:
    return _import_gds(
        _SRC
        / "gf180mcu_fd_sc_mcu9t5v0/cells/xnor3/gf180mcu_fd_sc_mcu9t5v0__xnor3_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__xor2_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/xor2/gf180mcu_fd_sc_mcu9t5v0__xor2_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__xor2_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/xor2/gf180mcu_fd_sc_mcu9t5v0__xor2_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__xor2_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/xor2/gf180mcu_fd_sc_mcu9t5v0__xor2_4.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__xor3_1() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/xor3/gf180mcu_fd_sc_mcu9t5v0__xor3_1.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__xor3_2() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/xor3/gf180mcu_fd_sc_mcu9t5v0__xor3_2.gds"
    )


@gf.cell
def gf180mcu_fd_sc_mcu9t5v0__xor3_4() -> gf.Component:
    return _import_gds(
        _SRC / "gf180mcu_fd_sc_mcu9t5v0/cells/xor3/gf180mcu_fd_sc_mcu9t5v0__xor3_4.gds"
    )
