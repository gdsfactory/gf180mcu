"""Diode pcells matching Magic VLSI geometry exactly.

Implements gf180mcu::diode_nd2ps and diode_pd2nw from Magic generators.

All geometry derived from XOR regression against Magic VLSI reference GDS files.

Key geometry rules (from reference analysis):
  nd2ps 03v3: guard_inner = wa/2+0.300, guard_outer = wa/2+0.680 (strip=0.380)
  nd2ps 06v0: guard_inner = wa/2+0.400, guard_outer = wa/2+0.760 (strip=0.360)
  pd2nw 03v3 inner: same as nd2ps 03v3
  pd2nw 06v0 inner: guard_inner = wa/2+0.360, guard_outer = wa/2+0.720 (strip=0.360)
  pd2nw 03v3 outer: inner_outer+0.450 to inner_outer+0.810
  pd2nw 06v0 outer: inner_outer+0.520 to inner_outer+0.880

Contact rules:
  nc_x = floor((wa+0.15)/0.50), pitch_x = 0.47 if nc_x==2 else 0.50
  Guard ring side: nc_guard(nc, volt), pitch = 0.47 always
  Contact inset from guard comp outer: 0.190 (03v3), 0.180 (06v0 or outer guard)
"""

from math import floor

import gdsfactory as gf

from gf180mcu.layers import layer


# ---------------------------------------------------------------------------
# Helper: exact rectangle placement (bypasses gdsfactory snap_to_grid2x)
# ---------------------------------------------------------------------------

def _add_rect(c: gf.Component, x0: float, y0: float, x1: float, y1: float, lyr: str) -> None:
    """Add an exact rectangle polygon directly, avoiding snap-to-grid rounding."""
    c.add_polygon([(x0, y0), (x0, y1), (x1, y1), (x1, y0)], layer=layer[lyr])


# ---------------------------------------------------------------------------
# Helper: contact position generation
# ---------------------------------------------------------------------------

def _positions(nc: int, pitch: float) -> list:
    """nc contact centre positions centred on zero."""
    if nc == 1:
        return [0.0]
    start = -(nc - 1) / 2.0 * pitch
    return [round(start + i * pitch, 4) for i in range(nc)]


def _nc_inner(w: float) -> int:
    """Number of inner device contacts in dimension w."""
    return int((w + 0.15) / 0.50)


def _nc_guard(nc: int, volt: str) -> int:
    """Number of guard ring side contacts given inner contact count."""
    if volt == "3.3V":
        return nc + (1 if nc >= 4 and nc % 2 == 0 else 0)
    else:  # 6.0V
        return nc + 1


def _inner_pitch(nc: int) -> float:
    """Pitch for nc inner contacts."""
    return 0.47 if nc == 2 else 0.50


def _nc_outer_guard_side(og_inner_y: float) -> int:
    """nc for outer guard ring side contacts (left/right columns).

    Contact centres must satisfy: center_y ≤ og_inner_y - 0.340.
    (Empirically derived from reference GDS: 0.340 = contact_half + 0.230 rule.)
    """
    max_y = og_inner_y - 0.340
    odd_nc = 0
    for n in range(500):
        if n * 0.47 <= max_y + 1e-9:
            odd_nc = 2 * n + 1
        else:
            break
    even_nc = 0
    for n in range(1, 500):
        if (n - 0.5) * 0.47 <= max_y + 1e-9:
            even_nc = 2 * n
        else:
            break
    return max(odd_nc, even_nc)


def _place_contacts(c: gf.Component, xs: list, ys: list) -> None:
    """Place 0.22x0.22 contacts at all (x,y) combinations."""
    size = 0.22
    con_rect = gf.components.rectangle(size=(size, size), layer=layer["contact"])
    for x in xs:
        for y in ys:
            c.add_ref(con_rect).move((x - size / 2, y - size / 2))


def _guard_ring_comp(
    c: gf.Component,
    guard_inner_x: float,
    guard_inner_y: float,
    guard_outer_x: float,
    guard_outer_y: float,
    lyr: str = "comp",
) -> None:
    """Draw guard ring comp as 4 strips (ring shape, no overlap with inner device comp)."""
    # Top strip: from y=guard_inner_y to y=guard_outer_y, x=-guard_outer to +guard_outer
    c.add_ref(
        gf.components.rectangle(
            size=(2 * guard_outer_x, guard_outer_y - guard_inner_y), layer=layer[lyr]
        )
    ).move((-guard_outer_x, guard_inner_y))
    # Bottom strip
    c.add_ref(
        gf.components.rectangle(
            size=(2 * guard_outer_x, guard_outer_y - guard_inner_y), layer=layer[lyr]
        )
    ).move((-guard_outer_x, -guard_outer_y))
    # Left strip: x=-guard_outer to x=-guard_inner, y=-guard_inner to y=+guard_inner
    c.add_ref(
        gf.components.rectangle(
            size=(guard_outer_x - guard_inner_x, 2 * guard_inner_y), layer=layer[lyr]
        )
    ).move((-guard_outer_x, -guard_inner_y))
    # Right strip
    c.add_ref(
        gf.components.rectangle(
            size=(guard_outer_x - guard_inner_x, 2 * guard_inner_y), layer=layer[lyr]
        )
    ).move((guard_inner_x, -guard_inner_y))


def _pplus_ring(
    c: gf.Component,
    guard_inner_x: float,
    guard_inner_y: float,
    guard_outer_x: float,
    guard_outer_y: float,
    outer_enc: float = 0.030,
    inner_enc: float = 0.030,
    cap_thickness: float = 0.010,
    lyr: str = "pplus",
) -> None:
    """Draw a pplus/nplus ring matching Magic VLSI decomposition (nd2ps style).

    Outer boundary: guard_outer + outer_enc, with thin caps protruding at
    centre of each edge (half-width = guard_inner - 0.125).
    Inner hole: guard_inner - inner_enc.
    Uses direct polygon placement to avoid snap_to_grid2x rounding.
    """
    pp_outer_x = round(guard_outer_x + outer_enc, 4)
    pp_outer_y = round(guard_outer_y + outer_enc, 4)
    main_outer_x = round(pp_outer_x - cap_thickness, 4)
    main_outer_y = round(pp_outer_y - cap_thickness, 4)
    pp_inner_x = round(guard_inner_x - inner_enc, 4)
    pp_inner_y = round(guard_inner_y - inner_enc, 4)
    cap_half_x = round(guard_inner_x - 0.125, 4)
    cap_half_y = round(guard_inner_y - 0.125, 4)

    # Main top band: x=[-main_outer_x, main_outer_x], y=[pp_inner_y, main_outer_y]
    _add_rect(c, -main_outer_x, pp_inner_y, main_outer_x, main_outer_y, lyr)
    # Main bottom band
    _add_rect(c, -main_outer_x, -main_outer_y, main_outer_x, -pp_inner_y, lyr)
    # Main left strip: x=[-main_outer_x, -pp_inner_x], y=[-pp_inner_y, pp_inner_y]
    _add_rect(c, -main_outer_x, -pp_inner_y, -pp_inner_x, pp_inner_y, lyr)
    # Main right strip
    _add_rect(c, pp_inner_x, -pp_inner_y, main_outer_x, pp_inner_y, lyr)
    # Thin top cap: x=[-cap_half_x, cap_half_x], y=[main_outer_y, pp_outer_y]
    _add_rect(c, -cap_half_x, main_outer_y, cap_half_x, pp_outer_y, lyr)
    # Thin bottom cap
    _add_rect(c, -cap_half_x, -pp_outer_y, cap_half_x, -main_outer_y, lyr)
    # Thin left cap: x=[-pp_outer_x, -main_outer_x], y=[-cap_half_y, cap_half_y]
    _add_rect(c, -pp_outer_x, -cap_half_y, -main_outer_x, cap_half_y, lyr)
    # Thin right cap
    _add_rect(c, main_outer_x, -cap_half_y, pp_outer_x, cap_half_y, lyr)


def _pplus_ring_outer(
    c: gf.Component,
    og_inner_x: float,
    og_inner_y: float,
    og_outer_x: float,
    og_outer_y: float,
    lyr: str = "pplus",
) -> None:
    """Draw pd2nw outer guard ring pplus matching Magic VLSI decomposition.

    Outer extent: og_outer_x+0.030 (x), og_outer_y+0.020 (y, asymmetric).
    Inner hole: og_inner - 0.160.
    Thin inner-transition strips at og_inner - 0.125 (connect sides to top/bottom).
    """
    opp_outer_x = round(og_outer_x + 0.030, 4)
    opp_outer_y = round(og_outer_y + 0.020, 4)
    main_outer_x = round(opp_outer_x - 0.010, 4)  # = og_outer + 0.020
    opp_inner_x = round(og_inner_x - 0.160, 4)
    opp_inner_y = round(og_inner_y - 0.160, 4)
    transition_y = round(og_inner_y - 0.125, 4)  # = opp_inner_y + 0.035

    # Main top: x=[-main_outer_x, main_outer_x], y=[transition_y, opp_outer_y]
    _add_rect(c, -main_outer_x, transition_y, main_outer_x, opp_outer_y, lyr)
    # Thin top transition: x=[-opp_outer_x, opp_outer_x], y=[opp_inner_y, transition_y]
    _add_rect(c, -opp_outer_x, opp_inner_y, opp_outer_x, transition_y, lyr)
    # Left side: x=[-opp_outer_x, -opp_inner_x], y=[-opp_inner_y, opp_inner_y]
    _add_rect(c, -opp_outer_x, -opp_inner_y, -opp_inner_x, opp_inner_y, lyr)
    # Right side
    _add_rect(c, opp_inner_x, -opp_inner_y, opp_outer_x, opp_inner_y, lyr)
    # Thin bottom transition
    _add_rect(c, -opp_outer_x, -transition_y, opp_outer_x, -opp_inner_y, lyr)
    # Main bottom
    _add_rect(c, -main_outer_x, -opp_outer_y, main_outer_x, -transition_y, lyr)


def _guard_contacts(
    c: gf.Component,
    guard_contact_x: float,
    guard_contact_y: float,
    nc_gx: int,
    nc_gy: int,
) -> None:
    """Place guard ring contacts on all four sides.

    Left/right cols at x=±guard_contact_x, y positions from nc_gy.
    Top/bottom rows at y=±guard_contact_y, x positions from nc_gx.
    """
    gy_pos = _positions(nc_gy, 0.47)
    gx_pos = _positions(nc_gx, 0.47)
    _place_contacts(c, [-guard_contact_x], gy_pos)
    _place_contacts(c, [guard_contact_x], gy_pos)
    _place_contacts(c, gx_pos, [guard_contact_y])
    _place_contacts(c, gx_pos, [-guard_contact_y])


def _guard_metal1(
    c: gf.Component,
    guard_inner_x: float,
    guard_inner_y: float,
    guard_comp_outer_x: float,
    guard_comp_outer_y: float,
    diff_surround: float = 0.065,
) -> None:
    """Draw guard ring metal1 as a ring (4 strips).

    Outer edge: guard_comp_outer - diff_surround.
    Inner edge: guard_inner + diff_surround.
    """
    m1_outer_x = round(guard_comp_outer_x - diff_surround, 4)
    m1_outer_y = round(guard_comp_outer_y - diff_surround, 4)
    m1_inner_x = round(guard_inner_x + diff_surround, 4)
    m1_inner_y = round(guard_inner_y + diff_surround, 4)
    # Top strip
    c.add_ref(
        gf.components.rectangle(
            size=(2 * m1_outer_x, m1_outer_y - m1_inner_y), layer=layer["metal1"]
        )
    ).move((-m1_outer_x, m1_inner_y))
    # Bottom strip
    c.add_ref(
        gf.components.rectangle(
            size=(2 * m1_outer_x, m1_outer_y - m1_inner_y), layer=layer["metal1"]
        )
    ).move((-m1_outer_x, -m1_outer_y))
    # Left strip
    c.add_ref(
        gf.components.rectangle(
            size=(m1_outer_x - m1_inner_x, 2 * m1_inner_y), layer=layer["metal1"]
        )
    ).move((-m1_outer_x, -m1_inner_y))
    # Right strip
    c.add_ref(
        gf.components.rectangle(
            size=(m1_outer_x - m1_inner_x, 2 * m1_inner_y), layer=layer["metal1"]
        )
    ).move((m1_inner_x, -m1_inner_y))


def _inner_metal1(c: gf.Component, wa: float, la: float) -> None:
    """Draw inner device metal1 rectangle.

    Long dimension gets half-0.010 extent; short dimension gets half-0.065.
    Square devices: wa (x) is treated as "long" → x gets -0.010.
    """
    if la > wa:
        m1_hx = round(wa / 2 - 0.065, 4)
        m1_hy = round(la / 2 - 0.010, 4)
    else:
        m1_hx = round(wa / 2 - 0.010, 4)
        m1_hy = round(la / 2 - 0.065, 4)
    c.add_ref(
        gf.components.rectangle(size=(2 * m1_hx, 2 * m1_hy), layer=layer["metal1"])
    ).move((-m1_hx, -m1_hy))


# ---------------------------------------------------------------------------
# diode_nd2ps
# ---------------------------------------------------------------------------

@gf.cell
def diode_nd2ps(
    la: float = 0.45,
    wa: float = 0.45,
    volt: str = "3.3V",
    deepnwell: bool = False,
    pcmpgr: bool = False,
    label: bool = False,
    p_label: str = "",
    n_label: str = "",
) -> gf.Component:
    """Draw N+/LVPWELL diode matching Magic VLSI geometry.

    Args:
        la: diffusion length (anode).
        wa: diffusion width (anode).
        volt: operating voltage ("3.3V" or "6.0V").
        deepnwell: use Deep NWELL device (not implemented).
        pcmpgr: use P+ Guard Ring for DNWELL (not implemented).
        label: add labels (not implemented).
        p_label: p terminal label.
        n_label: n terminal label.
    """
    c = gf.Component()

    diff_surround = 0.065
    lvpwell_enc = 0.12

    # Voltage-dependent geometry constants (all from reference GDS analysis)
    if volt == "3.3V":
        dev_spacing = 0.300   # gap between inner comp and guard ring comp inner edge
        guard_inner_offset = 0.300   # guard_inner = wa/2 + this
        guard_outer_offset = 0.680   # guard_outer = wa/2 + this (strip = 0.380)
        contact_inset = 0.190        # guard contact center to guard comp outer edge
        nplus_enc = 0.16
        dg_enc = 0.24
    else:  # 6.0V
        dev_spacing = 0.400
        guard_inner_offset = 0.400
        guard_outer_offset = 0.760
        contact_inset = 0.180
        nplus_enc = 0.16
        dg_enc = 0.24

    hw = wa / 2
    hl = la / 2

    # Guard ring comp geometry
    guard_inner_x = round(hw + guard_inner_offset, 4)
    guard_inner_y = round(hl + guard_inner_offset, 4)
    guard_outer_x = round(hw + guard_outer_offset, 4)
    guard_outer_y = round(hl + guard_outer_offset, 4)

    # Guard ring contact centre positions
    guard_contact_x = round(guard_outer_x - contact_inset, 4)
    guard_contact_y = round(guard_outer_y - contact_inset, 4)

    # Contact counts
    nc_x = _nc_inner(wa)
    nc_y = _nc_inner(la)
    nc_gx = _nc_guard(nc_x, volt)
    nc_gy = _nc_guard(nc_y, volt)
    pitch_x = _inner_pitch(nc_x)
    pitch_y = _inner_pitch(nc_y)

    # --- Inner device ---
    # Comp
    c.add_ref(
        gf.components.rectangle(size=(wa, la), layer=layer["comp"])
    ).move((-hw, -hl))

    # Diode marker
    c.add_ref(
        gf.components.rectangle(size=(wa, la), layer=layer["diode_mk"])
    ).move((-hw, -hl))

    # N+ implant (solid rect enclosing inner comp)
    nplus_hw = round(hw + nplus_enc, 4)
    nplus_hl = round(hl + nplus_enc, 4)
    c.add_ref(
        gf.components.rectangle(
            size=(2 * nplus_hw, 2 * nplus_hl), layer=layer["nplus"]
        )
    ).move((-nplus_hw, -nplus_hl))

    # Inner contacts
    inner_xs = _positions(nc_x, pitch_x)
    inner_ys = _positions(nc_y, pitch_y)
    _place_contacts(c, inner_xs, inner_ys)

    # Inner metal1
    _inner_metal1(c, wa, la)

    # --- Guard ring (P+ comp ring) ---
    # Guard ring comp: 4 strips (ring shape)
    _guard_ring_comp(c, guard_inner_x, guard_inner_y, guard_outer_x, guard_outer_y)

    # P+ implant: ring with notched corners matching Magic VLSI decomposition
    _pplus_ring(c, guard_inner_x, guard_inner_y, guard_outer_x, guard_outer_y, lyr="pplus")

    # Guard ring metal1 (ring: 4 strips)
    _guard_metal1(c, guard_inner_x, guard_inner_y, guard_outer_x, guard_outer_y, diff_surround)

    # Guard ring contacts
    _guard_contacts(c, guard_contact_x, guard_contact_y, nc_gx, nc_gy)

    # LVPWELL
    lvp_hx = round(guard_outer_x + lvpwell_enc, 4)
    lvp_hy = round(guard_outer_y + lvpwell_enc, 4)
    c.add_ref(
        gf.components.rectangle(
            size=(2 * lvp_hx, 2 * lvp_hy), layer=layer["lvpwell"]
        )
    ).move((-lvp_hx, -lvp_hy))

    # Dualgate for 6.0V
    if volt == "6.0V":
        dg_hx = round(guard_outer_x + dg_enc, 4)
        dg_hy = round(guard_outer_y + dg_enc, 4)
        c.add_ref(
            gf.components.rectangle(
                size=(2 * dg_hx, 2 * dg_hy), layer=layer["dualgate"]
            )
        ).move((-dg_hx, -dg_hy))

    # Ports
    c.add_port(
        name="anode",
        center=(0, 0),
        width=wa,
        orientation=0,
        layer=layer["metal1"],
        port_type="electrical",
    )
    c.add_port(
        name="cathode",
        center=(0, guard_contact_y),
        width=2 * guard_outer_x,
        orientation=90,
        layer=layer["metal1"],
        port_type="electrical",
    )

    return c


# ---------------------------------------------------------------------------
# diode_pd2nw
# ---------------------------------------------------------------------------

@gf.cell
def diode_pd2nw(
    la: float = 0.45,
    wa: float = 0.45,
    volt: str = "3.3V",
    deepnwell: bool = False,
    pcmpgr: bool = False,
    label: bool = False,
    p_label: str = "",
    n_label: str = "",
) -> gf.Component:
    """Draw P+/Nwell diode matching Magic VLSI geometry.

    Args:
        la: diffusion length.
        wa: diffusion width.
        volt: operating voltage ("3.3V" or "6.0V").
        deepnwell: use Deep NWELL device (not implemented).
        pcmpgr: use P+ Guard Ring for DNWELL (not implemented).
        label: add labels (not implemented).
        p_label: p terminal label.
        n_label: n terminal label.
    """
    c = gf.Component()

    diff_surround = 0.065
    lvpwell_enc = 0.12

    if volt == "3.3V":
        # Inner guard ring
        ig_inner_offset = 0.300   # guard_inner = wa/2 + this
        ig_outer_offset = 0.680   # guard_outer = wa/2 + this
        ig_contact_inset = 0.190
        nw_enc = 0.12
        nplus_enc_out = 0.16     # nplus outer enc on ig_outer
        nplus_enc_in = 0.090     # nplus inner enc on ig_inner (inward)
        lvpwell_enc = 0.12
        # Outer guard ring (relative to inner guard outer)
        og_inner_gap = 0.450     # outer_guard_inner = inner_guard_outer + this
        og_strip = 0.360         # outer_guard_outer = outer_guard_inner + this
        # outer_guard_outer = inner_guard_outer + 0.450 + 0.360 = inner_guard_outer + 0.810
        og_contact_inset = 0.180
        dg_enc = 0.24
    else:  # 6.0V
        ig_inner_offset = 0.360
        ig_outer_offset = 0.720
        ig_contact_inset = 0.180
        nw_enc = 0.16
        nplus_enc_out = 0.16
        nplus_enc_in = 0.070     # nplus inner enc (inward) for 6.0V
        lvpwell_enc = 0.16
        og_inner_gap = 0.520
        og_strip = 0.360
        og_contact_inset = 0.180
        dg_enc = 0.24

    hw = wa / 2
    hl = la / 2

    # Inner guard ring geometry
    ig_inner_x = round(hw + ig_inner_offset, 4)
    ig_inner_y = round(hl + ig_inner_offset, 4)
    ig_outer_x = round(hw + ig_outer_offset, 4)
    ig_outer_y = round(hl + ig_outer_offset, 4)
    ig_contact_x = round(ig_outer_x - ig_contact_inset, 4)
    ig_contact_y = round(ig_outer_y - ig_contact_inset, 4)

    # Outer guard ring geometry
    og_inner_x = round(ig_outer_x + og_inner_gap, 4)
    og_inner_y = round(ig_outer_y + og_inner_gap, 4)
    og_outer_x = round(og_inner_x + og_strip, 4)
    og_outer_y = round(og_inner_y + og_strip, 4)
    og_contact_x = round(og_outer_x - og_contact_inset, 4)
    og_contact_y = round(og_outer_y - og_contact_inset, 4)

    # Contact counts
    nc_x = _nc_inner(wa)
    nc_y = _nc_inner(la)
    nc_gx = _nc_guard(nc_x, volt)
    nc_gy = _nc_guard(nc_y, volt)
    pitch_x = _inner_pitch(nc_x)
    pitch_y = _inner_pitch(nc_y)

    # Outer guard ring side nc: side contacts are in y direction, constrained by og_inner_y
    nc_outer_side_y = _nc_outer_guard_side(og_inner_y)

    # --- Inner device (P+ diffusion) ---
    c.add_ref(
        gf.components.rectangle(size=(wa, la), layer=layer["comp"])
    ).move((-hw, -hl))

    c.add_ref(
        gf.components.rectangle(size=(wa, la), layer=layer["diode_mk"])
    ).move((-hw, -hl))

    # P+ implant on inner device
    pplus_hw = round(hw + 0.16, 4)
    pplus_hl = round(hl + 0.16, 4)
    c.add_ref(
        gf.components.rectangle(
            size=(2 * pplus_hw, 2 * pplus_hl), layer=layer["pplus"]
        )
    ).move((-pplus_hw, -pplus_hl))

    # Inner contacts
    inner_xs = _positions(nc_x, pitch_x)
    inner_ys = _positions(nc_y, pitch_y)
    _place_contacts(c, inner_xs, inner_ys)

    # Inner metal1
    _inner_metal1(c, wa, la)

    # --- Inner guard ring (N+ comp ring = cathode) ---
    _guard_ring_comp(c, ig_inner_x, ig_inner_y, ig_outer_x, ig_outer_y)

    # N+ implant: ring (annular) matching inner guard ring comp
    np_outer_x = round(ig_outer_x + nplus_enc_out, 4)
    np_outer_y = round(ig_outer_y + nplus_enc_out, 4)
    np_inner_x = round(ig_inner_x - nplus_enc_in, 4)
    np_inner_y = round(ig_inner_y - nplus_enc_in, 4)
    _guard_ring_comp(c, np_inner_x, np_inner_y, np_outer_x, np_outer_y, lyr="nplus")

    # Inner guard ring metal1 (ring: 4 strips)
    _guard_metal1(c, ig_inner_x, ig_inner_y, ig_outer_x, ig_outer_y, diff_surround)

    # Inner guard ring contacts
    _guard_contacts(c, ig_contact_x, ig_contact_y, nc_gx, nc_gy)

    # Nwell
    nw_hx = round(ig_outer_x + nw_enc, 4)
    nw_hy = round(ig_outer_y + nw_enc, 4)
    c.add_ref(
        gf.components.rectangle(
            size=(2 * nw_hx, 2 * nw_hy), layer=layer["nwell"]
        )
    ).move((-nw_hx, -nw_hy))

    # --- Outer guard ring (P+ comp = LVPWELL ground) ---
    _guard_ring_comp(c, og_inner_x, og_inner_y, og_outer_x, og_outer_y)

    # Outer pplus: ring with asymmetric outer (x:+0.030, y:+0.020) matching Magic decomposition
    _pplus_ring_outer(c, og_inner_x, og_inner_y, og_outer_x, og_outer_y, lyr="pplus")

    # Outer guard ring metal1 (ring: 4 strips)
    _guard_metal1(c, og_inner_x, og_inner_y, og_outer_x, og_outer_y, diff_surround)

    # Outer guard ring contacts (left/right columns only, no top/bottom rows)
    og_gy_positions = _positions(nc_outer_side_y, 0.47)
    _place_contacts(c, [-og_contact_x], og_gy_positions)
    _place_contacts(c, [og_contact_x], og_gy_positions)

    # LVPWELL: ring (outer guard ring to nwell boundary)
    lvp_outer_x = round(og_outer_x + lvpwell_enc, 4)
    lvp_outer_y = round(og_outer_y + lvpwell_enc, 4)
    lvp_inner_x = round(nw_hx, 4)
    lvp_inner_y = round(nw_hy, 4)
    _guard_ring_comp(c, lvp_inner_x, lvp_inner_y, lvp_outer_x, lvp_outer_y, lyr="lvpwell")

    # Dualgate for 6.0V
    if volt == "6.0V":
        dg_hx = round(og_outer_x + dg_enc, 4)
        dg_hy = round(og_outer_y + dg_enc, 4)
        c.add_ref(
            gf.components.rectangle(
                size=(2 * dg_hx, 2 * dg_hy), layer=layer["dualgate"]
            )
        ).move((-dg_hx, -dg_hy))

    # Ports
    c.add_port(
        name="anode",
        center=(0, 0),
        width=wa,
        orientation=0,
        layer=layer["metal1"],
        port_type="electrical",
    )
    c.add_port(
        name="cathode",
        center=(0, ig_contact_y),
        width=2 * ig_outer_x,
        orientation=90,
        layer=layer["metal1"],
        port_type="electrical",
    )

    return c
