import gdsfactory as gf
from gdsfactory.typings import Float2

from gf180mcu.cells.via_generator import via_generator, via_stack
from gf180mcu.layers import layer


@gf.cell
def diode_nd2ps(
    la: float = 0.1,
    wa: float = 0.1,
    cw: float = 0.1,
    volt: str = "3.3V",
    deepnwell: bool = False,
    pcmpgr: bool = False,
    label: bool = False,
    p_label: str = "",
    n_label: str = "",
) -> gf.Component:
    """Draw N+/LVPWELL diode (Outside DNWELL) by specifying parameters.

    Args::
        la: Float of diff length (anode).
        wa: Float of diff width (anode).
        cw: Float of cathode width.
        volt: String of operating voltage of the diode [3.3V, 5V/6V].
        deepnwell: Boolean of using Deep NWELL device.
        pcmpgr : Boolean of using P+ Guard Ring for Deep NWELL devices only.
        label: Boolean of adding labels.
    """
    c = gf.Component("diode_nd2ps_dev")

    comp_spacing: float = 0.48
    np_enc_comp: float = 0.16
    pp_enc_comp: float = 0.16

    con_size = 0.22
    con_sp = 0.28
    con_comp_enc = 0.07

    dg_enc_cmp = 0.24
    dn_enc_lvpwell = 2.5
    lvpwell_enc_ncmp = 0.6
    lvpwell_enc_pcmp = 0.16
    pcmpgr_enc_dn = 2.5

    # n generation
    ncmp = c.add_ref(gf.components.rectangle(size=(wa, la), layer=layer["comp"]))
    nplus = c.add_ref(
        gf.components.rectangle(
            size=(
                ncmp.xsize + (2 * np_enc_comp),
                ncmp.ysize + (2 * np_enc_comp),
            ),
            layer=layer["nplus"],
        )
    )
    nplus.xmin = ncmp.xmin - np_enc_comp
    nplus.ymin = ncmp.ymin - np_enc_comp
    diode_mk = c.add_ref(
        gf.components.rectangle(size=(ncmp.xsize, ncmp.ysize), layer=layer["diode_mk"])
    )
    diode_mk.xmin = ncmp.xmin
    diode_mk.ymin = ncmp.ymin

    ncmp_con = c.add_ref(
        via_stack(
            x_range=(ncmp.xmin, ncmp.xmax),
            y_range=(ncmp.ymin, ncmp.ymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
    )  # ncomp_con

    # p generation
    pcmp = c.add_ref(gf.components.rectangle(size=(cw, la), layer=layer["comp"]))
    pcmp.xmax = ncmp.xmin - comp_spacing
    pplus = c.add_ref(
        gf.components.rectangle(
            size=(
                pcmp.xsize + (2 * pp_enc_comp),
                pcmp.ysize + (2 * pp_enc_comp),
            ),
            layer=layer["pplus"],
        )
    )
    pplus.xmin = pcmp.xmin - pp_enc_comp
    pplus.ymin = pcmp.ymin - pp_enc_comp

    pcmp_con = c.add_ref(
        via_stack(
            x_range=(pcmp.xmin, pcmp.xmax),
            y_range=(pcmp.ymin, pcmp.ymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
    )  # pcomp_con

    # labels generation
    if label == 1:
        # n_label generation
        c.add_label(
            n_label,
            position=(
                ncmp_con.xmin + (ncmp_con.xsize / 2),
                ncmp_con.ymin + (ncmp_con.ysize / 2),
            ),
            layer=layer["metal1_label"],
        )

        # p_label generation
        c.add_label(
            p_label,
            position=(
                pcmp_con.xmin + (pcmp_con.xsize / 2),
                pcmp_con.ymin + (pcmp_con.ysize / 2),
            ),
            layer=layer["metal1_label"],
        )

    if volt == "5/6V":
        dg = c.add_ref(
            gf.components.rectangle(
                size=(
                    ncmp.xmax - pcmp.xmin + (2 * dg_enc_cmp),
                    ncmp.ysize + (2 * dg_enc_cmp),
                ),
                layer=layer["dualgate"],
            )
        )
        dg.xmin = pcmp.xmin - dg_enc_cmp
        dg.ymin = pcmp.ymin - dg_enc_cmp

    if deepnwell == 1:
        lvpwell = c.add_ref(
            gf.components.rectangle(
                size=(
                    ncmp.xmax - pcmp.xmin + (lvpwell_enc_ncmp + lvpwell_enc_pcmp),
                    ncmp.ysize + (2 * lvpwell_enc_ncmp),
                ),
                layer=layer["lvpwell"],
            )
        )

        lvpwell.xmin = pcmp.xmin - lvpwell_enc_pcmp
        lvpwell.ymin = ncmp.ymin - lvpwell_enc_ncmp

        dn_rect = c.add_ref(
            gf.components.rectangle(
                size=(
                    lvpwell.xsize + (2 * dn_enc_lvpwell),
                    lvpwell.ysize + (2 * dn_enc_lvpwell),
                ),
                layer=layer["dnwell"],
            )
        )

        dn_rect.xmin = lvpwell.xmin - dn_enc_lvpwell
        dn_rect.ymin = lvpwell.ymin - dn_enc_lvpwell

        if pcmpgr == 1:
            c_temp_gr = gf.Component("temp_store guard ring")
            rect_pcmpgr_in = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (dn_rect.xmax - dn_rect.xmin) + 2 * pcmpgr_enc_dn,
                        (dn_rect.ymax - dn_rect.ymin) + 2 * pcmpgr_enc_dn,
                    ),
                    layer=layer["comp"],
                )
            )
            rect_pcmpgr_in.move(
                (dn_rect.xmin - pcmpgr_enc_dn, dn_rect.ymin - pcmpgr_enc_dn)
            )
            rect_pcmpgr_out = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (rect_pcmpgr_in.xmax - rect_pcmpgr_in.xmin) + 2 * cw,
                        (rect_pcmpgr_in.ymax - rect_pcmpgr_in.ymin) + 2 * cw,
                    ),
                    layer=layer["comp"],
                )
            )
            rect_pcmpgr_out.move((rect_pcmpgr_in.xmin - cw, rect_pcmpgr_in.ymin - cw))
            c.add_ref(
                gf.boolean(
                    A=rect_pcmpgr_out,
                    B=rect_pcmpgr_in,
                    operation="A-B",
                    layer=layer["comp"],
                )
            )  # guardring Bulk draw

            psdm_in = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (rect_pcmpgr_in.xmax - rect_pcmpgr_in.xmin) - 2 * pp_enc_comp,
                        (rect_pcmpgr_in.ymax - rect_pcmpgr_in.ymin) - 2 * pp_enc_comp,
                    ),
                    layer=layer["pplus"],
                )
            )
            psdm_in.move(
                (
                    rect_pcmpgr_in.xmin + pp_enc_comp,
                    rect_pcmpgr_in.ymin + pp_enc_comp,
                )
            )
            psdm_out = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (rect_pcmpgr_out.xmax - rect_pcmpgr_out.xmin) + 2 * pp_enc_comp,
                        (rect_pcmpgr_out.ymax - rect_pcmpgr_out.ymin) + 2 * pp_enc_comp,
                    ),
                    layer=layer["pplus"],
                )
            )
            psdm_out.move(
                (
                    rect_pcmpgr_out.xmin - pp_enc_comp,
                    rect_pcmpgr_out.ymin - pp_enc_comp,
                )
            )
            c.add_ref(
                gf.boolean(A=psdm_out, B=psdm_in, operation="A-B", layer=layer["pplus"])
            )  # psdm draw

            # generatingg contacts

            c.add_ref(
                via_generator(
                    x_range=(
                        rect_pcmpgr_in.xmin + con_size,
                        rect_pcmpgr_in.xmax - con_size,
                    ),
                    y_range=(rect_pcmpgr_out.ymin, rect_pcmpgr_in.ymin),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # bottom contact

            c.add_ref(
                via_generator(
                    x_range=(
                        rect_pcmpgr_in.xmin + con_size,
                        rect_pcmpgr_in.xmax - con_size,
                    ),
                    y_range=(rect_pcmpgr_in.ymax, rect_pcmpgr_out.ymax),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # upper contact

            c.add_ref(
                via_generator(
                    x_range=(rect_pcmpgr_out.xmin, rect_pcmpgr_in.xmin),
                    y_range=(
                        rect_pcmpgr_in.ymin + con_size,
                        rect_pcmpgr_in.ymax - con_size,
                    ),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # right contact

            c.add_ref(
                via_generator(
                    x_range=(rect_pcmpgr_in.xmax, rect_pcmpgr_out.xmax),
                    y_range=(
                        rect_pcmpgr_in.ymin + con_size,
                        rect_pcmpgr_in.ymax - con_size,
                    ),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # left contact

            comp_m1_in = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(rect_pcmpgr_in.xsize, rect_pcmpgr_in.ysize),
                    layer=layer["metal1"],
                )
            )

            comp_m1_out = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (comp_m1_in.xsize) + 2 * cw,
                        (comp_m1_in.ysize) + 2 * cw,
                    ),
                    layer=layer["metal1"],
                )
            )
            comp_m1_out.move((rect_pcmpgr_in.xmin - cw, rect_pcmpgr_in.ymin - cw))
            c.add_ref(
                gf.boolean(
                    A=rect_pcmpgr_out,
                    B=rect_pcmpgr_in,
                    operation="A-B",
                    layer=layer["metal1"],
                )
            )  # guardring metal1

    # Add ports for anode and cathode
    c.add_port(
        name="anode",
        center=(ncmp_con.dcenter[0], ncmp_con.dcenter[1]),
        width=wa,
        orientation=0,
        layer=layer["metal1"],
        port_type="electrical",
    )

    c.add_port(
        name="cathode",
        center=(pcmp_con.dcenter[0], pcmp_con.dcenter[1]),
        width=cw,
        orientation=180,
        layer=layer["metal1"],
        port_type="electrical",
    )

    # VLSIR Simulation Metadata
    c.info["vlsir"] = {
        "spice_type": "DIODE",
        "spice_lib": "dio",
        "port_order": ["anode", "cathode"],
        "port_map": {},
        "params": {"l": la, "w": wa},
    }

    if volt == "3.3V":
        c.info["vlsir"].update({"model": "np_3p3"})
    else:
        c.info["vlsir"].update({"model": "np_6p0"})

    return c


@gf.cell
def diode_pd2nw(
    la: float = 0.1,
    wa: float = 0.1,
    cw: float = 0.1,
    volt: str = "3.3V",
    deepnwell: bool = False,
    pcmpgr: bool = False,
    label: bool = False,
    p_label: str = "",
    n_label: str = "",
) -> gf.Component:
    """Usage:-
     used to draw 3.3V P+/Nwell diode (Outside DNWELL) by specifying parameters
    Arguments:-
     la         : Float of diffusion length (anode)
     wa         : Float of diffusion width (anode)
     volt       : String of operating voltage of the diode [3.3V, 5V/6V]
     deepnwell  : Boolean of using Deep NWELL device
     pcmpgr     : Boolean of using P+ Guard Ring for Deep NWELL devices only.
    """
    c = gf.Component("diode_pd2nw_dev")

    comp_spacing: float = 0.48
    np_enc_comp: float = 0.16
    pp_enc_comp: float = 0.16

    con_size = 0.22
    con_sp = 0.28
    con_comp_enc = 0.07

    dg_enc_cmp = 0.24
    dn_enc_nwell = 0.5
    nwell_ncmp_enc = 0.12
    nwell_pcmp_enc = 0.43
    pcmpgr_enc_dn = 2.5

    # p generation
    pcmp = c.add_ref(gf.components.rectangle(size=(wa, la), layer=layer["comp"]))
    pplus = c.add_ref(
        gf.components.rectangle(
            size=(
                pcmp.xsize + (2 * pp_enc_comp),
                pcmp.ysize + (2 * pp_enc_comp),
            ),
            layer=layer["pplus"],
        )
    )
    pplus.xmin = pcmp.xmin - pp_enc_comp
    pplus.ymin = pcmp.ymin - pp_enc_comp
    diode_mk = c.add_ref(
        gf.components.rectangle(size=(pcmp.xsize, pcmp.ysize), layer=layer["diode_mk"])
    )
    diode_mk.xmin = pcmp.xmin
    diode_mk.ymin = pcmp.ymin

    pcmp_con = c.add_ref(
        via_stack(
            x_range=(pcmp.xmin, pcmp.xmax),
            y_range=(pcmp.ymin, pcmp.ymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
    )  # pcomp_contact

    # n generation
    ncmp = c.add_ref(gf.components.rectangle(size=(cw, la), layer=layer["comp"]))
    ncmp.xmax = pcmp.xmin - comp_spacing
    nplus = c.add_ref(
        gf.components.rectangle(
            size=(
                ncmp.xsize + (2 * np_enc_comp),
                ncmp.ysize + (2 * np_enc_comp),
            ),
            layer=layer["nplus"],
        )
    )
    nplus.xmin = ncmp.xmin - np_enc_comp
    nplus.ymin = ncmp.ymin - np_enc_comp

    ncmp_con = c.add_ref(
        via_stack(
            x_range=(ncmp.xmin, ncmp.xmax),
            y_range=(ncmp.ymin, ncmp.ymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
    )  # ncomp contact

    # labels generation
    if label == 1:
        # n_label generation
        c.add_label(
            n_label,
            position=(
                ncmp_con.xmin + (ncmp_con.xsize / 2),
                ncmp_con.ymin + (ncmp_con.ysize / 2),
            ),
            layer=layer["metal1_label"],
        )

        # p_label generation
        c.add_label(
            p_label,
            position=(
                pcmp_con.xmin + (pcmp_con.xsize / 2),
                pcmp_con.ymin + (pcmp_con.ysize / 2),
            ),
            layer=layer["metal1_label"],
        )

    if volt == "5/6V":
        dg = c.add_ref(
            gf.components.rectangle(
                size=(
                    pcmp.xmax - ncmp.xmin + (2 * dg_enc_cmp),
                    ncmp.ysize + (2 * dg_enc_cmp),
                ),
                layer=layer["dualgate"],
            )
        )
        dg.xmin = ncmp.xmin - dg_enc_cmp
        dg.ymin = ncmp.ymin - dg_enc_cmp

    # nwell generation
    nwell = c.add_ref(
        gf.components.rectangle(
            size=(
                pcmp.xmax - ncmp.xmin + (nwell_ncmp_enc + nwell_pcmp_enc),
                pcmp.ysize + (2 * nwell_pcmp_enc),
            ),
            layer=layer["nwell"],
        )
    )

    nwell.xmin = ncmp.xmin - nwell_ncmp_enc
    nwell.ymin = pcmp.ymin - nwell_pcmp_enc

    if deepnwell == 1:
        dn_rect = c.add_ref(
            gf.components.rectangle(
                size=(
                    nwell.xsize + (2 * dn_enc_nwell),
                    nwell.ysize + (2 * dn_enc_nwell),
                ),
                layer=layer["dnwell"],
            )
        )

        dn_rect.xmin = nwell.xmin - dn_enc_nwell
        dn_rect.ymin = nwell.ymin - dn_enc_nwell

        if pcmpgr == 1:
            c_temp_gr = gf.Component("temp_store guard ring")
            rect_pcmpgr_in = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (dn_rect.xmax - dn_rect.xmin) + 2 * pcmpgr_enc_dn,
                        (dn_rect.ymax - dn_rect.ymin) + 2 * pcmpgr_enc_dn,
                    ),
                    layer=layer["comp"],
                )
            )
            rect_pcmpgr_in.move(
                (dn_rect.xmin - pcmpgr_enc_dn, dn_rect.ymin - pcmpgr_enc_dn)
            )
            rect_pcmpgr_out = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (rect_pcmpgr_in.xmax - rect_pcmpgr_in.xmin) + 2 * cw,
                        (rect_pcmpgr_in.ymax - rect_pcmpgr_in.ymin) + 2 * cw,
                    ),
                    layer=layer["comp"],
                )
            )
            rect_pcmpgr_out.move((rect_pcmpgr_in.xmin - cw, rect_pcmpgr_in.ymin - cw))
            c.add_ref(
                gf.boolean(
                    A=rect_pcmpgr_out,
                    B=rect_pcmpgr_in,
                    operation="A-B",
                    layer=layer["comp"],
                )
            )  # Bulk guardring

            psdm_in = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (rect_pcmpgr_in.xmax - rect_pcmpgr_in.xmin) - 2 * pp_enc_comp,
                        (rect_pcmpgr_in.ymax - rect_pcmpgr_in.ymin) - 2 * pp_enc_comp,
                    ),
                    layer=layer["pplus"],
                )
            )
            psdm_in.move(
                (
                    rect_pcmpgr_in.xmin + pp_enc_comp,
                    rect_pcmpgr_in.ymin + pp_enc_comp,
                )
            )
            psdm_out = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (rect_pcmpgr_out.xmax - rect_pcmpgr_out.xmin) + 2 * pp_enc_comp,
                        (rect_pcmpgr_out.ymax - rect_pcmpgr_out.ymin) + 2 * pp_enc_comp,
                    ),
                    layer=layer["pplus"],
                )
            )
            psdm_out.move(
                (
                    rect_pcmpgr_out.xmin - pp_enc_comp,
                    rect_pcmpgr_out.ymin - pp_enc_comp,
                )
            )
            c.add_ref(
                gf.boolean(A=psdm_out, B=psdm_in, operation="A-B", layer=layer["pplus"])
            )  # psdm guardring

            # generatingg contacts

            c.add_ref(
                via_generator(
                    x_range=(
                        rect_pcmpgr_in.xmin + con_size,
                        rect_pcmpgr_in.xmax - con_size,
                    ),
                    y_range=(rect_pcmpgr_out.ymin, rect_pcmpgr_in.ymin),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # bottom contact

            c.add_ref(
                via_generator(
                    x_range=(
                        rect_pcmpgr_in.xmin + con_size,
                        rect_pcmpgr_in.xmax - con_size,
                    ),
                    y_range=(rect_pcmpgr_in.ymax, rect_pcmpgr_out.ymax),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # upper contact

            c.add_ref(
                via_generator(
                    x_range=(rect_pcmpgr_out.xmin, rect_pcmpgr_in.xmin),
                    y_range=(
                        rect_pcmpgr_in.ymin + con_size,
                        rect_pcmpgr_in.ymax - con_size,
                    ),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # right contact

            c.add_ref(
                via_generator(
                    x_range=(rect_pcmpgr_in.xmax, rect_pcmpgr_out.xmax),
                    y_range=(
                        rect_pcmpgr_in.ymin + con_size,
                        rect_pcmpgr_in.ymax - con_size,
                    ),
                    via_enclosure=(con_comp_enc, con_comp_enc),
                    via_layer=layer["contact"],
                    via_size=(con_size, con_size),
                    via_spacing=(con_sp, con_sp),
                )
            )  # left contact

            comp_m1_in = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(rect_pcmpgr_in.xsize, rect_pcmpgr_in.ysize),
                    layer=layer["metal1"],
                )
            )

            comp_m1_out = c_temp_gr.add_ref(
                gf.components.rectangle(
                    size=(
                        (comp_m1_in.xsize) + 2 * cw,
                        (comp_m1_in.ysize) + 2 * cw,
                    ),
                    layer=layer["metal1"],
                )
            )
            comp_m1_out.move((rect_pcmpgr_in.xmin - cw, rect_pcmpgr_in.ymin - cw))
            c.add_ref(
                gf.boolean(
                    A=rect_pcmpgr_out,
                    B=rect_pcmpgr_in,
                    operation="A-B",
                    layer=layer["metal1"],
                )
            )  # guardring metal1

    # Add ports for anode and cathode
    c.add_port(
        name="anode",
        center=(pcmp_con.dcenter[0], pcmp_con.dcenter[1]),
        width=wa,
        orientation=0,
        layer=layer["metal1"],
        port_type="electrical",
    )

    c.add_port(
        name="cathode",
        center=(ncmp_con.dcenter[0], ncmp_con.dcenter[1]),
        width=cw,
        orientation=180,
        layer=layer["metal1"],
        port_type="electrical",
    )

    c.info["vlsir"] = {
        "spice_type": "DIODE",
        "spice_lib": "dio",
        "port_order": ["anode", "cathode"],
        "port_map": {},
        "params": {"l": la, "w": wa},
    }

    if volt == "3.3V":
        c.info["vlsir"].update({"model": "pn_3p3"})
    else:
        c.info["vlsir"].update({"model": "pn_6p0"})

    return c


@gf.cell
def diode_nw2ps(
    la: float = 0.1,
    wa: float = 0.1,
    cw: float = 0.1,
    volt: str = "3.3V",
    label: bool = False,
    p_label: str = "",
    n_label: str = "",
) -> gf.Component:
    """Used to draw 3.3V Nwell/Psub diode by specifying parameters.

    Args:
        la: anode length.
        wa: anode width.
        cw: cathode width.
        volt: operating voltage of the diode [3.3V, 5V/6V]

    """
    c = gf.Component()

    comp_spacing: float = 0.48
    np_enc_comp: float = 0.16
    pp_enc_comp: float = 0.16

    dg_enc_cmp = 0.24

    nwell_ncmp_enc = 0.16

    # n generation
    ncmp = c.add_ref(gf.components.rectangle(size=(wa, la), layer=layer["comp"]))
    nplus = c.add_ref(
        gf.components.rectangle(
            size=(
                ncmp.xsize + (2 * np_enc_comp),
                ncmp.ysize + (2 * np_enc_comp),
            ),
            layer=layer["nplus"],
        )
    )
    nplus.xmin = ncmp.xmin - np_enc_comp
    nplus.ymin = ncmp.ymin - np_enc_comp
    diode_mk = c.add_ref(
        gf.components.rectangle(size=(ncmp.xsize, ncmp.ysize), layer=layer["diode_mk"])
    )
    diode_mk.xmin = ncmp.xmin
    diode_mk.ymin = ncmp.ymin

    nwell = c.add_ref(
        gf.components.rectangle(
            size=(
                ncmp.xsize + (2 * nwell_ncmp_enc),
                ncmp.ysize + (2 * nwell_ncmp_enc),
            ),
            layer=layer["nwell"],
        )
    )
    nwell.xmin = ncmp.xmin - nwell_ncmp_enc
    nwell.ymin = ncmp.ymin - nwell_ncmp_enc

    n_con = c.add_ref(
        via_stack(
            x_range=(ncmp.xmin, ncmp.xmax),
            y_range=(ncmp.ymin, ncmp.ymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
    )  # ncomp contact

    # p generation
    pcmp = c.add_ref(gf.components.rectangle(size=(cw, la), layer=layer["comp"]))
    pcmp.xmax = ncmp.xmin - comp_spacing
    pplus = c.add_ref(
        gf.components.rectangle(
            size=(
                pcmp.xsize + (2 * pp_enc_comp),
                pcmp.ysize + (2 * pp_enc_comp),
            ),
            layer=layer["pplus"],
        )
    )
    pplus.xmin = pcmp.xmin - pp_enc_comp
    pplus.ymin = pcmp.ymin - pp_enc_comp

    p_con = c.add_ref(
        via_stack(
            x_range=(pcmp.xmin, pcmp.xmax),
            y_range=(pcmp.ymin, pcmp.ymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
    )  # pcmop contact

    # labels generation
    if label == 1:
        # n_label generation
        c.add_label(
            n_label,
            position=(
                n_con.xmin + (n_con.xsize / 2),
                n_con.ymin + (n_con.ysize / 2),
            ),
            layer=layer["metal1_label"],
        )

        # p_label generation
        c.add_label(
            p_label,
            position=(
                p_con.xmin + (p_con.xsize / 2),
                p_con.ymin + (p_con.ysize / 2),
            ),
            layer=layer["metal1_label"],
        )

    if volt == "5/6V":
        dg = c.add_ref(
            gf.components.rectangle(
                size=(
                    ncmp.xmax - pcmp.xmin + (2 * dg_enc_cmp),
                    ncmp.ysize + (2 * dg_enc_cmp),
                ),
                layer=layer["dualgate"],
            )
        )
        dg.xmin = pcmp.xmin - dg_enc_cmp
        dg.ymin = pcmp.ymin - dg_enc_cmp

    # Add ports for anode and cathode
    c.add_port(
        name="anode",
        center=(n_con.dcenter[0], n_con.dcenter[1]),
        width=wa,
        orientation=0,
        layer=layer["metal1"],
        port_type="electrical",
    )

    c.add_port(
        name="cathode",
        center=(p_con.dcenter[0], p_con.dcenter[1]),
        width=cw,
        orientation=180,
        layer=layer["metal1"],
        port_type="electrical",
    )

    c.info["vlsir"] = {
        "spice_type": "DIODE",
        "spice_lib": "dio",
        "port_order": ["anode", "cathode"],
        "port_map": {},
        "params": {"l": la, "w": wa},
    }

    if volt == "3.3V":
        c.info["vlsir"].update({"model": "nwp_3p3"})
    else:
        c.info["vlsir"].update({"model": "nwp_6p0"})

    return c


@gf.cell
def diode_pw2dw(
    la: float = 0.1,
    wa: float = 0.1,
    cw: float = 0.1,
    volt: str = "3.3V",
    pcmpgr: bool = False,
    label: bool = False,
    p_label: str = "",
    n_label: str = "",
) -> gf.Component:
    """Used to draw LVPWELL/DNWELL diode by specifying parameters.

    Args:
        la: anode length.
        wa: anode width.
        cw: cathode width.
        volt: operating voltage of the diode [3.3V, 5V/6V]
        pcmpgr: if True, pcmpgr will be added.
        label: if True, labels will be added.
        p_label: p contact label.
        n_label: n contact label.

    """
    c = gf.Component()

    comp_spacing: float = 0.48
    np_enc_comp: float = 0.16
    pp_enc_comp: float = 0.16

    dg_enc_dn = 0.5

    lvpwell_enc_pcmp = 0.16
    dn_enc_lvpwell = 2.5

    con_size = 0.22
    con_sp = 0.28
    con_comp_enc = 0.07

    pcmpgr_enc_dn = 2.5

    # p generation
    pcmp = c.add_ref(gf.components.rectangle(size=(wa, la), layer=layer["comp"]))
    pplus = c.add_ref(
        gf.components.rectangle(
            size=(
                pcmp.xsize + (2 * pp_enc_comp),
                pcmp.ysize + (2 * pp_enc_comp),
            ),
            layer=layer["pplus"],
        )
    )
    pplus.xmin = pcmp.xmin - pp_enc_comp
    pplus.ymin = pcmp.ymin - pp_enc_comp
    diode_mk = c.add_ref(
        gf.components.rectangle(size=(pcmp.xsize, pcmp.ysize), layer=layer["diode_mk"])
    )
    diode_mk.xmin = pcmp.xmin
    diode_mk.ymin = pcmp.ymin

    lvpwell = c.add_ref(
        gf.components.rectangle(
            size=(
                pcmp.xsize + (2 * lvpwell_enc_pcmp),
                pcmp.ysize + (2 * lvpwell_enc_pcmp),
            ),
            layer=layer["lvpwell"],
        )
    )
    lvpwell.xmin = pcmp.xmin - lvpwell_enc_pcmp
    lvpwell.ymin = pcmp.ymin - lvpwell_enc_pcmp

    p_con = c.add_ref(
        via_stack(
            x_range=(pcmp.xmin, pcmp.xmax),
            y_range=(pcmp.ymin, pcmp.ymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
    )  # pcomp_contact

    # n generation
    ncmp = c.add_ref(gf.components.rectangle(size=(cw, la), layer=layer["comp"]))
    ncmp.xmax = pcmp.xmin - comp_spacing
    nplus = c.add_ref(
        gf.components.rectangle(
            size=(
                ncmp.xsize + (2 * np_enc_comp),
                ncmp.ysize + (2 * np_enc_comp),
            ),
            layer=layer["nplus"],
        )
    )
    nplus.xmin = ncmp.xmin - np_enc_comp
    nplus.ymin = ncmp.ymin - np_enc_comp

    n_con = c.add_ref(
        via_stack(
            x_range=(ncmp.xmin, ncmp.xmax),
            y_range=(ncmp.ymin, ncmp.ymax),
            base_layer=layer["comp"],
            metal_level=1,
        )
    )  # ncomp contact

    # labels generation
    if label == 1:
        # n_label generation
        c.add_label(
            n_label,
            position=(
                n_con.xmin + (n_con.xsize / 2),
                n_con.ymin + (n_con.ysize / 2),
            ),
            layer=layer["metal1_label"],
        )

        # p_label generation
        c.add_label(
            p_label,
            position=(
                p_con.xmin + (p_con.xsize / 2),
                p_con.ymin + (p_con.ysize / 2),
            ),
            layer=layer["metal1_label"],
        )

    dn_rect = c.add_ref(
        gf.components.rectangle(
            size=(
                lvpwell.xsize + (2 * dn_enc_lvpwell),
                lvpwell.ysize + (2 * dn_enc_lvpwell),
            ),
            layer=layer["dnwell"],
        )
    )

    dn_rect.xmin = lvpwell.xmin - dn_enc_lvpwell
    dn_rect.ymin = lvpwell.ymin - dn_enc_lvpwell

    if pcmpgr == 1:
        c_temp_gr = gf.Component("temp_store guard ring")
        rect_pcmpgr_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (dn_rect.xmax - dn_rect.xmin) + 2 * pcmpgr_enc_dn,
                    (dn_rect.ymax - dn_rect.ymin) + 2 * pcmpgr_enc_dn,
                ),
                layer=layer["comp"],
            )
        )
        rect_pcmpgr_in.move(
            (dn_rect.xmin - pcmpgr_enc_dn, dn_rect.ymin - pcmpgr_enc_dn)
        )
        rect_pcmpgr_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_in.xmax - rect_pcmpgr_in.xmin) + 2 * cw,
                    (rect_pcmpgr_in.ymax - rect_pcmpgr_in.ymin) + 2 * cw,
                ),
                layer=layer["comp"],
            )
        )
        rect_pcmpgr_out.move((rect_pcmpgr_in.xmin - cw, rect_pcmpgr_in.ymin - cw))
        c.add_ref(
            gf.boolean(
                A=rect_pcmpgr_out,
                B=rect_pcmpgr_in,
                operation="A-B",
                layer=layer["comp"],
            )
        )  # guardring Bulk

        psdm_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_in.xmax - rect_pcmpgr_in.xmin) - 2 * pp_enc_comp,
                    (rect_pcmpgr_in.ymax - rect_pcmpgr_in.ymin) - 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        psdm_in.move(
            (
                rect_pcmpgr_in.xmin + pp_enc_comp,
                rect_pcmpgr_in.ymin + pp_enc_comp,
            )
        )
        psdm_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_out.xmax - rect_pcmpgr_out.xmin) + 2 * pp_enc_comp,
                    (rect_pcmpgr_out.ymax - rect_pcmpgr_out.ymin) + 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        psdm_out.move(
            (
                rect_pcmpgr_out.xmin - pp_enc_comp,
                rect_pcmpgr_out.ymin - pp_enc_comp,
            )
        )
        c.add_ref(
            gf.boolean(A=psdm_out, B=psdm_in, operation="A-B", layer=layer["pplus"])
        )  # guardring psdm

        # generatingg contacts

        c.add_ref(
            via_generator(
                x_range=(
                    rect_pcmpgr_in.xmin + con_size,
                    rect_pcmpgr_in.xmax - con_size,
                ),
                y_range=(rect_pcmpgr_out.ymin, rect_pcmpgr_in.ymin),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # bottom contact

        c.add_ref(
            via_generator(
                x_range=(
                    rect_pcmpgr_in.xmin + con_size,
                    rect_pcmpgr_in.xmax - con_size,
                ),
                y_range=(rect_pcmpgr_in.ymax, rect_pcmpgr_out.ymax),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # upper contact

        c.add_ref(
            via_generator(
                x_range=(rect_pcmpgr_out.xmin, rect_pcmpgr_in.xmin),
                y_range=(
                    rect_pcmpgr_in.ymin + con_size,
                    rect_pcmpgr_in.ymax - con_size,
                ),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # right contact

        c.add_ref(
            via_generator(
                x_range=(rect_pcmpgr_in.xmax, rect_pcmpgr_out.xmax),
                y_range=(
                    rect_pcmpgr_in.ymin + con_size,
                    rect_pcmpgr_in.ymax - con_size,
                ),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # left contact

        comp_m1_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(rect_pcmpgr_in.xsize, rect_pcmpgr_in.ysize),
                layer=layer["metal1"],
            )
        )

        comp_m1_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (comp_m1_in.xsize) + 2 * cw,
                    (comp_m1_in.ysize) + 2 * cw,
                ),
                layer=layer["metal1"],
            )
        )
        comp_m1_out.move((rect_pcmpgr_in.xmin - cw, rect_pcmpgr_in.ymin - cw))
        c.add_ref(
            gf.boolean(
                A=rect_pcmpgr_out,
                B=rect_pcmpgr_in,
                operation="A-B",
                layer=layer["metal1"],
            )
        )  # guardring metal1

    if volt == "5/6V":
        dg = c.add_ref(
            gf.components.rectangle(
                size=(
                    dn_rect.xsize + (2 * dg_enc_dn),
                    dn_rect.ysize + (2 * dg_enc_dn),
                ),
                layer=layer["dualgate"],
            )
        )
        dg.xmin = dn_rect.xmin - dg_enc_dn
        dg.ymin = dn_rect.ymin - dg_enc_dn

    # Add ports for anode and cathode
    c.add_port(
        name="anode",
        center=(p_con.dcenter[0], p_con.dcenter[1]),
        width=wa,
        orientation=0,
        layer=layer["metal1"],
        port_type="electrical",
    )

    c.add_port(
        name="cathode",
        center=(n_con.dcenter[0], n_con.dcenter[1]),
        width=cw,
        orientation=180,
        layer=layer["metal1"],
        port_type="electrical",
    )

    c.info["vlsir"] = {
        "model": "dnwpw",
        "spice_type": "DIODE",
        "spice_lib": "dio",
        "port_order": ["anode", "cathode"],
        "port_map": {},
        "params": {"l": la, "w": wa},
    }

    return c


@gf.cell
def diode_dw2ps(
    la: float = 0.1,
    wa: float = 0.1,
    cw: float = 0.1,
    volt: str = "3.3V",
    pcmpgr: bool = False,
    label: bool = False,
    p_label: str = "",
    n_label: str = "",
) -> gf.Component:
    """Used to draw LVPWELL/DNWELL diode by specifying parameters.

    Args:
        la: anode length.
        wa: anode width.
        cw: cathode width.
        volt: operating voltage of the diode [3.3V, 5V/6V].
        pcmpgr: True if pwell guardring is required.
        label: True if labels are required.
        p_label: label for pwell.
        n_label: label for nwell.

    """
    c = gf.Component()

    if volt == "5/6V":
        dn_enc_ncmp = 0.66
    else:
        dn_enc_ncmp = 0.62

    comp_spacing = 0.32
    np_enc_comp: float = 0.16
    pp_enc_comp: float = 0.16

    con_size = 0.22
    con_sp = 0.28
    con_comp_enc = 0.07

    dg_enc_dn = 0.5

    pcmpgr_enc_dn = 2.5

    if (wa < ((2 * cw) + comp_spacing)) or (la < ((2 * cw) + comp_spacing)):
        ncmp = c.add_ref(gf.components.rectangle(size=(wa, la), layer=layer["comp"]))

        n_con = c.add_ref(
            via_stack(
                x_range=(ncmp.xmin, ncmp.xmax),
                y_range=(ncmp.ymin, ncmp.ymax),
                base_layer=layer["comp"],
                metal_level=1,
            )
        )  # ncomp_contact

        nplus = c.add_ref(
            gf.components.rectangle(
                size=(
                    ncmp.xsize + (2 * np_enc_comp),
                    ncmp.ysize + (2 * np_enc_comp),
                ),
                layer=layer["nplus"],
            )
        )
        nplus.xmin = ncmp.xmin - np_enc_comp
        nplus.ymin = ncmp.ymin - np_enc_comp
    else:
        c_temp = gf.Component("temp_store guard ring")
        ncmp_in = c_temp.add_ref(
            gf.components.rectangle(
                size=(wa - (2 * cw), la - (2 * cw)),
                layer=layer["comp"],
            )
        )
        ncmp_out = c_temp.add_ref(
            gf.components.rectangle(
                size=(wa, la),
                layer=layer["comp"],
            )
        )
        ncmp_out.move((ncmp_in.xmin - cw, ncmp_in.ymin - cw))
        ncmp = c.add_ref(
            gf.boolean(
                A=ncmp_out,
                B=ncmp_in,
                operation="A-B",
                layer=layer["comp"],
            )
        )

        pplus_in = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    (ncmp_in.xmax - ncmp_in.xmin) - 2 * pp_enc_comp,
                    (ncmp_in.ymax - ncmp_in.ymin) - 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        pplus_in.move(
            (
                ncmp_in.xmin + pp_enc_comp,
                ncmp_in.ymin + pp_enc_comp,
            )
        )
        pplus_out = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    (ncmp_out.xmax - ncmp_out.xmin) + 2 * pp_enc_comp,
                    (ncmp_out.ymax - ncmp_out.ymin) + 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        pplus_out.move(
            (
                ncmp_out.xmin - pp_enc_comp,
                ncmp_out.ymin - pp_enc_comp,
            )
        )
        c.add_ref(
            gf.boolean(A=pplus_out, B=pplus_in, operation="A-B", layer=layer["nplus"])
        )  # nplus

        # generatingg contacts

        c.add_ref(
            via_generator(
                x_range=(
                    ncmp_in.xmin + con_size,
                    ncmp_in.xmax - con_size,
                ),
                y_range=(ncmp_out.ymin, ncmp_in.ymin),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # bottom contact

        c.add_ref(
            via_generator(
                x_range=(
                    ncmp_in.xmin + con_size,
                    ncmp_in.xmax - con_size,
                ),
                y_range=(ncmp_in.ymax, ncmp_out.ymax),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # upper contact

        n_con = c.add_ref(
            via_generator(
                x_range=(ncmp_out.xmin, ncmp_in.xmin),
                y_range=(
                    ncmp_in.ymin + con_size,
                    ncmp_in.ymax - con_size,
                ),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # left contact

        c.add_ref(
            via_generator(
                x_range=(ncmp_in.xmax, ncmp_out.xmax),
                y_range=(
                    ncmp_in.ymin + con_size,
                    ncmp_in.ymax - con_size,
                ),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # right contact

        comp_m1_in = c_temp.add_ref(
            gf.components.rectangle(
                size=(ncmp_in.xsize, ncmp_in.ysize),
                layer=layer["metal1"],
            )
        )

        comp_m1_out = c_temp.add_ref(
            gf.components.rectangle(
                size=(
                    (comp_m1_in.xsize) + 2 * cw,
                    (comp_m1_in.xsize) + 2 * cw,
                ),
                layer=layer["metal1"],
            )
        )
        comp_m1_out.move((ncmp_in.xmin - cw, ncmp_in.ymin - cw))
        c.add_ref(
            gf.boolean(
                A=ncmp_out,
                B=ncmp_in,
                operation="A-B",
                layer=layer["metal1"],
            )
        )  # guardring metal1

    # labels generation
    if label == 1:
        # n_label generation
        c.add_label(
            n_label,
            position=(
                n_con.xmin + (n_con.xsize / 2),
                n_con.ymin + (n_con.ysize / 2),
            ),
            layer=layer["metal1_label"],
        )

    # generate dnwell

    dn_rect = c.add_ref(
        gf.components.rectangle(
            size=(
                ncmp.xsize + (2 * dn_enc_ncmp),
                ncmp.ysize + (2 * dn_enc_ncmp),
            ),
            layer=layer["dnwell"],
        )
    )
    dn_rect.xmin = ncmp.xmin - dn_enc_ncmp
    dn_rect.ymin = ncmp.ymin - dn_enc_ncmp

    diode_mk = c.add_ref(
        gf.components.rectangle(
            size=(dn_rect.xsize, dn_rect.ysize), layer=layer["diode_mk"]
        )
    )
    diode_mk.xmin = dn_rect.xmin
    diode_mk.ymin = dn_rect.ymin

    if pcmpgr == 1:
        c_temp_gr = gf.Component("temp_store guard ring")
        rect_pcmpgr_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (dn_rect.xmax - dn_rect.xmin) + 2 * pcmpgr_enc_dn,
                    (dn_rect.ymax - dn_rect.ymin) + 2 * pcmpgr_enc_dn,
                ),
                layer=layer["comp"],
            )
        )
        rect_pcmpgr_in.move(
            (dn_rect.xmin - pcmpgr_enc_dn, dn_rect.ymin - pcmpgr_enc_dn)
        )
        rect_pcmpgr_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_in.xmax - rect_pcmpgr_in.xmin) + 2 * cw,
                    (rect_pcmpgr_in.ymax - rect_pcmpgr_in.ymin) + 2 * cw,
                ),
                layer=layer["comp"],
            )
        )
        rect_pcmpgr_out.move((rect_pcmpgr_in.xmin - cw, rect_pcmpgr_in.ymin - cw))
        c.add_ref(
            gf.boolean(
                A=rect_pcmpgr_out,
                B=rect_pcmpgr_in,
                operation="A-B",
                layer=layer["comp"],
            )
        )  # guardring Bulk

        psdm_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_in.xmax - rect_pcmpgr_in.xmin) - 2 * pp_enc_comp,
                    (rect_pcmpgr_in.ymax - rect_pcmpgr_in.ymin) - 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        psdm_in.move(
            (
                rect_pcmpgr_in.xmin + pp_enc_comp,
                rect_pcmpgr_in.ymin + pp_enc_comp,
            )
        )
        psdm_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_out.xmax - rect_pcmpgr_out.xmin) + 2 * pp_enc_comp,
                    (rect_pcmpgr_out.ymax - rect_pcmpgr_out.ymin) + 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        psdm_out.move(
            (
                rect_pcmpgr_out.xmin - pp_enc_comp,
                rect_pcmpgr_out.ymin - pp_enc_comp,
            )
        )
        c.add_ref(
            gf.boolean(A=psdm_out, B=psdm_in, operation="A-B", layer=layer["pplus"])
        )  # psdm

        # generatingg contacts

        c.add_ref(
            via_generator(
                x_range=(
                    rect_pcmpgr_in.xmin + con_size,
                    rect_pcmpgr_in.xmax - con_size,
                ),
                y_range=(rect_pcmpgr_out.ymin, rect_pcmpgr_in.ymin),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # bottom contact

        c.add_ref(
            via_generator(
                x_range=(
                    rect_pcmpgr_in.xmin + con_size,
                    rect_pcmpgr_in.xmax - con_size,
                ),
                y_range=(rect_pcmpgr_in.ymax, rect_pcmpgr_out.ymax),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # upper contact

        p_con = c.add_ref(
            via_generator(
                x_range=(rect_pcmpgr_out.xmin, rect_pcmpgr_in.xmin),
                y_range=(
                    rect_pcmpgr_in.ymin + con_size,
                    rect_pcmpgr_in.ymax - con_size,
                ),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # left contact

        c.add_ref(
            via_generator(
                x_range=(rect_pcmpgr_in.xmax, rect_pcmpgr_out.xmax),
                y_range=(
                    rect_pcmpgr_in.ymin + con_size,
                    rect_pcmpgr_in.ymax - con_size,
                ),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # right contact

        # labels generation
        if label == 1:
            # n_label generation
            c.add_label(
                p_label,
                position=(
                    p_con.xmin + (p_con.xsize / 2),
                    p_con.ymin + (p_con.ysize / 2),
                ),
                layer=layer["metal1_label"],
            )

        comp_m1_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(rect_pcmpgr_in.xsize, rect_pcmpgr_in.ysize),
                layer=layer["metal1"],
            )
        )

        comp_m1_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_in.xmax - rect_pcmpgr_in.xmin) + 2 * cw,
                    (rect_pcmpgr_in.ymax - rect_pcmpgr_in.ymin) + 2 * cw,
                ),
                layer=layer["metal1"],
            )
        )
        comp_m1_out.move((rect_pcmpgr_in.xmin - cw, rect_pcmpgr_in.ymin - cw))
        c.add_ref(
            gf.boolean(
                A=rect_pcmpgr_out,
                B=rect_pcmpgr_in,
                operation="A-B",
                layer=layer["metal1"],
            )
        )  # guardring metal1

    # generate dualgate

    if volt == "5/6V":
        dg = c.add_ref(
            gf.components.rectangle(
                size=(
                    dn_rect.xsize + (2 * dg_enc_dn),
                    dn_rect.ysize + (2 * dg_enc_dn),
                ),
                layer=layer["dualgate"],
            )
        )
        dg.xmin = dn_rect.xmin - dg_enc_dn
        dg.ymin = dn_rect.ymin - dg_enc_dn

    # Add ports for anode and cathode
    c.add_port(
        name="anode",
        center=(n_con.dcenter[0], n_con.dcenter[1]),
        width=wa,
        orientation=0,
        layer=layer["metal1"],
        port_type="electrical",
    )

    if pcmpgr == 1:
        # For pcmpgr case, cathode is on the guardring
        c.add_port(
            name="cathode",
            center=(p_con.dcenter[0], p_con.dcenter[1]),
            width=cw,
            orientation=180,
            layer=layer["metal1"],
            port_type="electrical",
        )

    c.info["vlsir"] = {
        "model": "dnwps",
        "spice_type": "DIODE",
        "spice_lib": "dio",
        "port_order": ["anode", "cathode"],
        "port_map": {},
        "params": {"l": la, "w": wa},
    }

    return c


@gf.cell
def sc_diode(
    la: float = 0.1,
    wa: float = 0.1,
    cw: float = 0.1,
    m: int = 1,
    pcmpgr: bool = False,
    label: bool = False,
    p_label: str = "",
    n_label: str = "",
) -> gf.Component:
    """Used to draw N+/LVPWELL diode (Outside DNWELL) by specifying parameters.

    Args:
     la         : Float of diff length (anode)
     wa         : Float of diff width (anode)
     m          : Integer of number of fingers
     pcmpgr     : Boolean of using P+ Guard Ring for Deep NWELL devices only

    """
    c = gf.Component("sc_diode_dev")

    sc_enc_comp = 0.16
    sc_comp_spacing = 0.28
    dn_enc_sc_an = 1.4
    np_enc_comp = 0.03
    m1_w = 0.23
    pcmpgr_enc_dn = 2.5
    pp_enc_comp: float = 0.16

    con_size = 0.22
    con_sp = 0.28
    con_comp_enc = 0.07

    # cathode draw
    @gf.cell
    def sc_cathode_strap(size: Float2 = (0.1, 0.1)) -> gf.Component:
        """Returns sc_diode cathode array element.

        Args :
            size : size of cathode array element
        """
        c = gf.Component()

        ncmp = c.add_ref(gf.components.rectangle(size=size, layer=layer["comp"]))

        nplus = c.add_ref(
            gf.components.rectangle(
                size=(
                    ncmp.xsize + (2 * np_enc_comp),
                    ncmp.ysize + (2 * np_enc_comp),
                ),
                layer=layer["nplus"],
            )
        )
        nplus.xmin = ncmp.xmin - np_enc_comp
        nplus.ymin = ncmp.ymin - np_enc_comp

        c.add_ref(
            via_stack(
                x_range=(ncmp.xmin, ncmp.xmax),
                y_range=(ncmp.ymin, ncmp.ymax),
                base_layer=layer["comp"],
                metal_level=1,
            )
        )  # ncomp contact

        return c

    @gf.cell
    def sc_anode_strap(size: Float2 = (0.1, 0.1)) -> gf.Component:
        """Returns sc_diode anode array element.

        Args :
            size : size of anode array element
        """
        c = gf.Component()
        cmp = c.add_ref(gf.components.rectangle(size=size, layer=layer["comp"]))
        c.add_ref(
            via_stack(
                x_range=(cmp.xmin, cmp.xmax),
                y_range=(cmp.ymin, cmp.ymax),
                base_layer=layer["comp"],
                metal_level=1,
            )
        )  # comp contact
        return c

    sc_an = sc_anode_strap(size=(wa, la))
    sc_cath = sc_cathode_strap(size=(cw, la))

    sc_cathode = c.add_ref(
        component=sc_cath,
        rows=1,
        columns=(m + 1),
        column_pitch=cw + wa + (2 * sc_comp_spacing),
    )

    cath_m1_xmin = sc_cathode.xmin
    cath_m1_ymin = sc_cathode.ymin
    cath_m1_xmax = sc_cathode.xmax

    cath_m1_v = c.add_ref(
        component=gf.components.rectangle(
            size=(
                cath_m1_xmax - cath_m1_xmin,
                cath_m1_ymin - sc_cathode.ymin + m1_w,
            ),
            layer=layer["metal1"],
        ),
        rows=1,
        columns=(m + 1),
        column_pitch=(cw + wa + (2 * sc_comp_spacing)),
    )

    cath_m1_v.xmin = cath_m1_xmin
    cath_m1_v.ymax = cath_m1_ymin
    cath_m1_h = c.add_ref(
        gf.components.rectangle(size=(cath_m1_v.xsize, m1_w), layer=layer["metal1"])
    )
    cath_m1_h.xmin = cath_m1_v.xmin
    cath_m1_h.ymax = cath_m1_v.ymin

    # cathode label generation
    if label == 1:
        c.add_label(
            n_label,
            position=(
                cath_m1_h.xmin + (cath_m1_h.xsize / 2),
                cath_m1_h.ymin + (cath_m1_h.ysize / 2),
            ),
            layer=layer["metal1_label"],
        )

    sc_anode = c.add_ref(
        component=sc_an,
        rows=1,
        columns=m,
        column_pitch=(wa + cw + (2 * sc_comp_spacing)),
    )
    sc_anode.xmin = sc_cathode.xmin + (cw + sc_comp_spacing)
    an_m1_xmin = sc_anode.xmin
    an_m1_ymin = sc_anode.ymin
    an_m1_xmax = sc_anode.xmax
    an_m1_ymax = sc_anode.ymax

    if m > 1:
        an_m1_v = c.add_ref(
            component=gf.components.rectangle(
                size=(
                    an_m1_xmax - an_m1_xmin,
                    cath_m1_ymin - sc_an.ymin + m1_w,
                ),
                layer=layer["metal1"],
            ),
            rows=1,
            columns=m,
            spacing=((cw + wa + (2 * sc_comp_spacing)), 0),
        )

        an_m1_v.xmin = an_m1_xmin
        an_m1_v.ymin = an_m1_ymax

        an_m1_h = c.add_ref(
            gf.components.rectangle(size=(an_m1_v.xsize, m1_w), layer=layer["metal1"])
        )
        an_m1_h.xmin = an_m1_v.xmin
        an_m1_h.ymin = an_m1_v.ymax

        # anode label generation
        if label == 1:
            c.add_label(
                p_label,
                position=(
                    an_m1_h.xmin + (an_m1_h.xsize / 2),
                    an_m1_h.ymin + (an_m1_h.ysize / 2),
                ),
                layer=layer["metal1_label"],
            )

    else:
        # anode label generation
        if label == 1:
            c.add_label(
                p_label,
                position=(
                    an_m1_xmin + ((an_m1_xmax - an_m1_xmin) / 2),
                    an_m1_ymin + ((an_m1_ymax - an_m1_ymin) / 2),
                ),
                layer=layer["metal1_label"],
            )

    # diode_mk
    diode_mk = c.add_ref(
        gf.components.rectangle(
            size=(
                sc_cathode.xsize + (2 * sc_enc_comp),
                sc_cathode.ysize + (2 * sc_enc_comp),
            ),
            layer=layer["schottky_diode"],
        )
    )
    diode_mk.xmin = sc_cathode.xmin - sc_enc_comp
    diode_mk.ymin = sc_cathode.ymin - sc_enc_comp

    # dnwell
    dn_rect = c.add_ref(
        gf.components.rectangle(
            size=(
                sc_anode.xsize + (2 * dn_enc_sc_an),
                sc_anode.ysize + (2 * dn_enc_sc_an),
            ),
            layer=layer["dnwell"],
        )
    )
    dn_rect.xmin = sc_anode.xmin - dn_enc_sc_an
    dn_rect.ymin = sc_anode.ymin - dn_enc_sc_an

    if pcmpgr == 1:
        c_temp_gr = gf.Component("temp_store guard ring")
        rect_pcmpgr_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (dn_rect.xmax - dn_rect.xmin) + 2 * pcmpgr_enc_dn,
                    (dn_rect.ymax - dn_rect.ymin) + 2 * pcmpgr_enc_dn,
                ),
                layer=layer["comp"],
            )
        )
        rect_pcmpgr_in.move(
            (dn_rect.xmin - pcmpgr_enc_dn, dn_rect.ymin - pcmpgr_enc_dn)
        )
        rect_pcmpgr_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_in.xmax - rect_pcmpgr_in.xmin) + 2 * cw,
                    (rect_pcmpgr_in.ymax - rect_pcmpgr_in.ymin) + 2 * cw,
                ),
                layer=layer["comp"],
            )
        )
        rect_pcmpgr_out.move((rect_pcmpgr_in.xmin - cw, rect_pcmpgr_in.ymin - cw))
        c.add_ref(
            gf.boolean(
                A=rect_pcmpgr_out,
                B=rect_pcmpgr_in,
                operation="A-B",
                layer=layer["comp"],
            )
        )  # guardring Bulk

        psdm_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_in.xmax - rect_pcmpgr_in.xmin) - 2 * pp_enc_comp,
                    (rect_pcmpgr_in.ymax - rect_pcmpgr_in.ymin) - 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        psdm_in.move(
            (
                rect_pcmpgr_in.xmin + pp_enc_comp,
                rect_pcmpgr_in.ymin + pp_enc_comp,
            )
        )
        psdm_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (rect_pcmpgr_out.xmax - rect_pcmpgr_out.xmin) + 2 * pp_enc_comp,
                    (rect_pcmpgr_out.ymax - rect_pcmpgr_out.ymin) + 2 * pp_enc_comp,
                ),
                layer=layer["pplus"],
            )
        )
        psdm_out.move(
            (
                rect_pcmpgr_out.xmin - pp_enc_comp,
                rect_pcmpgr_out.ymin - pp_enc_comp,
            )
        )
        c.add_ref(
            gf.boolean(A=psdm_out, B=psdm_in, operation="A-B", layer=layer["pplus"])
        )  # psdm

        # generatingg contacts
        c.add_ref(
            via_generator(
                x_range=(
                    rect_pcmpgr_in.xmin + con_size,
                    rect_pcmpgr_in.xmax - con_size,
                ),
                y_range=(rect_pcmpgr_out.ymin, rect_pcmpgr_in.ymin),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # bottom contact

        c.add_ref(
            via_generator(
                x_range=(
                    rect_pcmpgr_in.xmin + con_size,
                    rect_pcmpgr_in.xmax - con_size,
                ),
                y_range=(rect_pcmpgr_in.ymax, rect_pcmpgr_out.ymax),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # upper contact

        c.add_ref(
            via_generator(
                x_range=(rect_pcmpgr_out.xmin, rect_pcmpgr_in.xmin),
                y_range=(
                    rect_pcmpgr_in.ymin + con_size,
                    rect_pcmpgr_in.ymax - con_size,
                ),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # right contact

        c.add_ref(
            via_generator(
                x_range=(rect_pcmpgr_in.xmax, rect_pcmpgr_out.xmax),
                y_range=(
                    rect_pcmpgr_in.ymin + con_size,
                    rect_pcmpgr_in.ymax - con_size,
                ),
                via_enclosure=(con_comp_enc, con_comp_enc),
                via_layer=layer["contact"],
                via_size=(con_size, con_size),
                via_spacing=(con_sp, con_sp),
            )
        )  # left contact

        comp_m1_in = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(rect_pcmpgr_in.xsize, rect_pcmpgr_in.ysize),
                layer=layer["metal1"],
            )
        )

        comp_m1_out = c_temp_gr.add_ref(
            gf.components.rectangle(
                size=(
                    (comp_m1_in.xsize) + 2 * cw,
                    (comp_m1_in.ysize) + 2 * cw,
                ),
                layer=layer["metal1"],
            )
        )
        comp_m1_out.move((rect_pcmpgr_in.xmin - cw, rect_pcmpgr_in.ymin - cw))
        c.add_ref(
            gf.boolean(
                A=rect_pcmpgr_out,
                B=rect_pcmpgr_in,
                operation="A-B",
                layer=layer["metal1"],
            )
        )  # guardring metal1

    # Add ports for anode and cathode
    c.add_port(
        name="anode",
        center=(cath_m1_h.dcenter[0], cath_m1_h.dcenter[1]),
        width=cath_m1_h.xsize,
        orientation=270,
        layer=layer["metal1"],
        port_type="electrical",
    )

    if m > 1:
        c.add_port(
            name="cathode",
            center=(an_m1_h.dcenter[0], an_m1_h.dcenter[1]),
            width=an_m1_h.xsize,
            orientation=90,
            layer=layer["metal1"],
            port_type="electrical",
        )
    else:
        # For single finger, use anode center
        c.add_port(
            name="cathode",
            center=(
                an_m1_xmin + ((an_m1_xmax - an_m1_xmin) / 2),
                an_m1_ymin + ((an_m1_ymax - an_m1_ymin) / 2),
            ),
            width=wa,
            orientation=90,
            layer=layer["metal1"],
            port_type="electrical",
        )

    c.info["vlsir"] = {
        "model": "sc_diode",
        "spice_type": "DIODE",
        "spice_lib": "dio",
        "port_order": ["anode", "cathode"],
        "port_map": {},
        "params": {"l": la, "w": wa, "m": m},
    }

    # creating layout and cell in klayout
    return c


if __name__ == "__main__":
    c = sc_diode()
    # c = diode_pd2nw()
    c.show()
