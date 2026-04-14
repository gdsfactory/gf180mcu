"""GF180MCU MOS capacitor parametric cells.

Geometry is derived from the open_pdks Magic VLSI generators:
  gf180mcu::nmoscap_3p3_draw / nmoscap_6p0_draw → gf180mcu::mos_draw

The MOS capacitor is structurally a MOSFET varactor:
  - Gate terminal: poly2 over the lc × wc gate area
  - Body terminal: nsd comp strips adjacent to the gate + outer lvpwell guard ring

All geometry is centered at origin and snapped to a 5 nm grid.

Magic ruleset used:
  contact_size     = 0.23  (painted) → 0.22 CIF cut
  diff_surround    = 0.065 (painted) → 0.07 CIF active surround
  poly_surround    = 0.065
  metal_surround   = 0.055 → 0.06 CIF
  gate_to_diffcont = 0.26
  gate_to_polycont = 0.28
  diff_spacing     = 0.33  (3p3) / 0.36 (6p0)
  diff_gate_space  = 0.11  (3p3) / 0.30 (6p0)
  sub_surround     = 0.12  (3p3) / 0.16 (6p0)
  metal_spacing    = 0.23
"""

from __future__ import annotations

from math import floor

import gdsfactory as gf

from gf180mcu.layers import layer

# ---------------------------------------------------------------------------
# Grid snapping — Magic CIF output grid is 5 nm
# ---------------------------------------------------------------------------

_GRID = 0.005  # 5 nm


def _snap(v: float) -> float:
    """Round *v* to the nearest 5 nm grid point."""
    return round(round(v / _GRID) * _GRID, 4)


# ---------------------------------------------------------------------------
# Physical GDS dimensions after CIF conversion
# ---------------------------------------------------------------------------

_CUT     = 0.22   # contact cut size (GDS layer 33)
_PITCH   = 0.47   # contact pitch (0.22 cut + 0.25 gap)
_DS      = 0.07   # active/poly CIF surround around cut
_MS      = 0.06   # metal1 CIF surround around cut


# ---------------------------------------------------------------------------
# Layer aliases
# ---------------------------------------------------------------------------

_L_COMP    = layer["comp"]
_L_POLY    = layer["poly2"]
_L_NPLUS   = layer["nplus"]
_L_PPLUS   = layer["pplus"]
_L_CONTACT = layer["contact"]
_L_METAL1  = layer["metal1"]
_L_NWELL   = layer["nwell"]
_L_LVPWELL = layer["lvpwell"]
_L_DUALGATE = layer["dualgate"]
_L_MOSCAP_MK = layer["mos_cap_mk"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _rect(c, x0, y0, x1, y1, lyr):
    """Add a snapped rectangle to component *c* on layer *lyr*."""
    x0, y0, x1, y1 = _snap(x0), _snap(y0), _snap(x1), _snap(y1)
    if abs(x1 - x0) < 1e-6 or abs(y1 - y0) < 1e-6:
        return
    c.add_polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], layer=lyr)


def _contacts(c, cx, cy, w_env, h_env):
    """Place 0.22×0.22 contact cuts within envelope (w_env, h_env) at (cx, cy)."""
    phys_w = max(w_env - 0.01, _CUT)
    phys_h = max(h_env - 0.01, _CUT)
    nx = max(1, floor((phys_w - _CUT) / _PITCH + 1 + 1e-6))
    ny = max(1, floor((phys_h - _CUT) / _PITCH + 1 + 1e-6))
    span_x = (nx - 1) * _PITCH
    span_y = (ny - 1) * _PITCH
    for ix in range(nx):
        for iy in range(ny):
            x = _snap(cx - span_x / 2.0 + ix * _PITCH)
            y = _snap(cy - span_y / 2.0 + iy * _PITCH)
            _rect(c, x - _CUT / 2, y - _CUT / 2,
                  x + _CUT / 2, y + _CUT / 2, _L_CONTACT)


# ---------------------------------------------------------------------------
# Guard ring (pwell substrate ring = lvpwell around the nwell device)
# Replicates gf180mcu::guard_ring with glc=1, grc=1, gtc=0, gbc=0
# ---------------------------------------------------------------------------

def _guard_ring(c, gx, gy, metal_spacing=0.23):
    """Draw the lvpwell guard ring centered at origin.

    gx, gy : guard ring size measured between contact centres (painted coords).
    Draws: comp bars, contacts on left+right only, full metal1 ring, lvpwell,
           and the pplus guard ring implant (8 rects).
    """
    cs  = 0.23   # contact_size (painted)
    ds  = 0.065  # diff_surround (painted)
    ms  = 0.055  # metal_surround (painted)

    hw = gx / 2.0
    hh = gy / 2.0
    hcs = cs / 2.0

    difft  = cs + 2 * ds          # comp bar thickness = 0.36
    hdifft = difft / 2.0          # = 0.18

    hdiffw = (gx + difft) / 2.0   # half-width of top/bottom comp bars
    hdiffh = (gy + difft) / 2.0   # half-height of left/right comp bars

    # --- Comp bars ---
    _rect(c, -hdiffw, hh - hdifft, hdiffw, hh + hdifft, _L_COMP)   # top
    _rect(c, -hdiffw, -hh - hdifft, hdiffw, -hh + hdifft, _L_COMP) # bottom
    _rect(c, hw - hdifft, -hdiffh, hw + hdifft, hdiffh, _L_COMP)   # right
    _rect(c, -hw - hdifft, -hdiffh, -hw + hdifft, hdiffh, _L_COMP) # left

    # --- Metal1 ring (full ring, not just bars) ---
    hmetw = (gx + cs) / 2.0
    hmeth = (gy + cs) / 2.0
    _rect(c, -hmetw, hh - hcs, hmetw, hh + hcs, _L_METAL1)   # top
    _rect(c, -hmetw, -hh - hcs, hmetw, -hh + hcs, _L_METAL1) # bottom
    _rect(c, hw - hcs, -hmeth, hw + hcs, hmeth, _L_METAL1)    # right
    _rect(c, -hw - hcs, -hmeth, -hw + hcs, hmeth, _L_METAL1)  # left

    # --- Side contacts (left + right only; glc=grc=1, gtc=gbc=0) ---
    ch = gy - cs - 2 * (ms + metal_spacing)
    if ch < cs:
        ch = cs
    # Right contact
    _contacts(c, hw, 0, 0, ch)
    _rect(c, hw - hcs - ds, -ch / 2 - ds,
          hw + hcs + ds, ch / 2 + ds, _L_COMP)
    _rect(c, hw - hcs - ms, -ch / 2 - ms,
          hw + hcs + ms, ch / 2 + ms, _L_METAL1)
    # Left contact
    _contacts(c, -hw, 0, 0, ch)
    _rect(c, -hw - hcs - ds, -ch / 2 - ds,
          -hw + hcs + ds, ch / 2 + ds, _L_COMP)
    _rect(c, -hw - hcs - ms, -ch / 2 - ms,
          -hw + hcs + ms, ch / 2 + ms, _L_METAL1)

    # --- lvpwell (sub_type) ---
    sub_surr_physical = hcs + ds + 0.12  # contact_size/2 + diff_surround + sub_surround
    _rect(c, -hw - sub_surr_physical, -hh - sub_surr_physical,
          hw + sub_surr_physical, hh + sub_surr_physical, _L_LVPWELL)

    # --- pplus guard ring implant (8 rectangles matching Magic CIF output) ---
    enc_tb   = 0.02   # CIF bloat for top/bottom bars
    enc_side = 0.03   # CIF bloat for side bars
    # bar extents
    bx = hdiffw                      # outer x of top/bottom bars
    by_out = hh + hdifft             # outer y of top/bottom bars
    by_in  = hh - hdifft             # inner y of top/bottom bars
    sx_out = hw + hdifft             # outer x of side bars
    sx_in  = hw - hdifft             # inner x of side bars

    # side bar implant y = contact y extent + CIF bloat
    side_by = _snap(ch / 2.0 + ds + 0.03)

    # top bar
    _rect(c, -bx - enc_tb, by_in - enc_tb,
           bx + enc_tb, by_out + enc_tb, _L_PPLUS)
    # bottom bar
    _rect(c, -bx - enc_tb, -by_out - enc_tb,
           bx + enc_tb, -by_in + enc_tb, _L_PPLUS)
    # left side bar
    _rect(c, -sx_out - enc_side, -side_by,
          -sx_in + enc_side, side_by, _L_PPLUS)
    # right side bar
    _rect(c, sx_in - enc_side, -side_by,
          sx_out + enc_side, side_by, _L_PPLUS)
    # corner pieces (bridge between bars and side bars)
    _rect(c, -bx - enc_tb, side_by,
          -sx_in + enc_side, by_in - enc_tb, _L_PPLUS)  # top-left
    _rect(c, sx_in - enc_side, side_by,
           bx + enc_tb, by_in - enc_tb, _L_PPLUS)        # top-right
    _rect(c, -bx - enc_tb, -by_in + enc_tb,
          -sx_in + enc_side, -side_by, _L_PPLUS)          # bottom-left
    _rect(c, sx_in - enc_side, -by_in + enc_tb,
           bx + enc_tb, -side_by, _L_PPLUS)               # bottom-right


# ---------------------------------------------------------------------------
# Main MOS capacitor generator
# ---------------------------------------------------------------------------

@gf.cell
def cap_mos(
    type: str = "cap_nmos",
    lc: float = 0.1,
    wc: float = 0.1,
    volt: str = "3.3V",
    deepnwell: bool = False,
    pcmpgr: bool = False,
    label: bool = False,
    g_label: str = "",
    sd_label: str = "",
) -> gf.Component:
    """MOS capacitor (NMOS varactor) matching Magic VLSI reference geometry.

    The structure is centered at the origin.  The gate terminal is poly2 over
    the lc × wc active area; the body terminal is the surrounding comp ring.

    Args:
        type: "cap_nmos" (NMOS) or "cap_pmos" (PMOS).
        lc: Capacitor gate length (µm).
        wc: Capacitor gate width (µm).
        volt: Operating voltage — "3.3V" or "6.0V".
        deepnwell: Unused (reserved).
        pcmpgr: Unused (reserved).
        label: Add metal1 labels.
        g_label: Gate label text.
        sd_label: Source/drain label text.
    """
    c = gf.Component()

    is_nmos = "cap_nmos" in type
    is_6v   = volt in ("6.0V", "5/6V", "5.0V")

    hl = lc / 2.0   # gate half-length (x direction)
    hw = wc / 2.0   # gate half-width  (y direction)

    # ----- Voltage-specific Magic ruleset parameters -----
    if is_6v:
        diff_spacing   = 0.36
        diff_gate_space = 0.30
        sub_surround   = 0.16
        metal_spacing  = 0.23
    else:  # 3.3V
        diff_spacing   = 0.33
        diff_gate_space = 0.11
        sub_surround   = 0.12
        metal_spacing  = 0.23

    # Shared Magic ruleset constants
    cs  = 0.23     # contact_size (painted)
    ds  = 0.065    # diff_surround (painted)
    ps  = 0.065    # poly_surround
    ms  = 0.055    # metal_surround
    g2d = 0.26     # gate_to_diffcont (painted)
    g2p = 0.28     # gate_to_polycont (painted)

    hcs = cs / 2.0

    # =========================================================
    # 1. mos_cap_mk marker — exactly lc × wc
    # =========================================================
    _rect(c, -hl, -hw, hl, hw, _L_MOSCAP_MK)

    # =========================================================
    # 2. Poly2 gate
    #    x: ±hl  (exact gate length)
    #    y: ±(hw + gate_to_polycont + hcs + poly_surround)
    # =========================================================
    poly_ext = g2p + hcs + ps          # = 0.28 + 0.115 + 0.065 = 0.46
    _rect(c, -hl, -(hw + poly_ext), hl, hw + poly_ext, _L_POLY)

    # =========================================================
    # 3. Inner comp strips (S/D contacts adjacent to gate)
    #    Each strip: x from ±hl to ±(hl + g2d + hcs + ds), y: ±hw
    #    Contact centre at ±(hl + g2d)
    # =========================================================
    inner_comp_xmax = _snap(hl + g2d + hcs + ds)   # = hl + 0.44

    # Right strip
    _rect(c, hl, -hw, inner_comp_xmax, hw, _L_COMP)
    # Left strip
    _rect(c, -inner_comp_xmax, -hw, -hl, hw, _L_COMP)

    # Inner comp contacts (vertical, centered on each strip at x = ±(hl+g2d))
    cdw = wc - 2 * ds   # painted contact height = wc - 0.13
    _contacts(c,  (hl + g2d), 0, 0, cdw)
    _contacts(c, -(hl + g2d), 0, 0, cdw)
    # Active surround for inner contacts
    _rect(c,  (hl + g2d) - hcs - ds, -hw,  (hl + g2d) + hcs + ds, hw, _L_COMP)
    _rect(c, -(hl + g2d) - hcs - ds, -hw, -(hl + g2d) + hcs + ds, hw, _L_COMP)
    # Metal1 on inner comp contacts
    _rect(c,  (hl + g2d) - hcs - ms, -(hw - ms),
               (hl + g2d) + hcs + ms,  (hw - ms), _L_METAL1)
    _rect(c, -(hl + g2d) - hcs - ms, -(hw - ms),
              -(hl + g2d) + hcs + ms,  (hw - ms), _L_METAL1)

    # =========================================================
    # 4. Poly contacts (top + bottom of gate)
    #    Centre at y = ±(hw + g2p)
    # =========================================================
    cpl = lc - 2 * ps   # painted poly contact width

    # Top poly contact
    pc_y = hw + g2p
    _contacts(c, 0, pc_y, cpl, 0)
    _rect(c, -(hl + ps), pc_y - hcs - ps,
              (hl + ps), pc_y + hcs + ps, _L_POLY)
    _rect(c, -(hl + ms), pc_y - hcs - ms,
              (hl + ms), pc_y + hcs + ms, _L_METAL1)

    # Bottom poly contact
    _contacts(c, 0, -pc_y, cpl, 0)
    _rect(c, -(hl + ps), -pc_y - hcs - ps,
              (hl + ps), -pc_y + hcs + ps, _L_POLY)
    _rect(c, -(hl + ms), -pc_y - hcs - ms,
              (hl + ms), -pc_y + hcs + ms, _L_METAL1)

    if label and g_label:
        c.add_label(
            g_label,
            position=(0, pc_y),
            layer=layer["metal1_label"],
        )

    # =========================================================
    # 5. nplus (device implant over the gate + inner S/D area)
    #    CIF nplus bloat: +0.225 in x (= g2d+hcs+bloat), +0.23 in y
    # =========================================================
    nplus_x = _snap(hl + g2d + hcs + 0.225)    # = hl + 0.60
    nplus_y = _snap(hw + 0.23)
    _rect(c, -nplus_x, -nplus_y, nplus_x, nplus_y, _L_NPLUS)

    # =========================================================
    # 6. nwell (dev_sub_type) — surrounds entire mos_device bbox
    #    bbox x: ±(hl + g2d + hcs + ms + sub_surround)
    #    bbox y: ±(hw + g2p + hcs + ps + sub_surround)
    #    (CIF uses metal extent for the bbox used for nwell calculation)
    # =========================================================
    nwell_x = _snap(hl + g2d + hcs + ms + sub_surround)
    nwell_y = _snap(hw + g2p + hcs + ps + sub_surround)
    _rect(c, -nwell_x, -nwell_y, nwell_x, nwell_y, _L_NWELL)

    # =========================================================
    # 7. Guard ring (lvpwell = sub_type pwell)
    #    gx = fw + 2*(diff_spacing + ds) + cs
    #    gy = fh + 2*(max(dev_sub_dist, 0) + ds) + cs
    #    For 3p3: dev_sub_dist=0.12 with sub_surr=0.12 → check vs diff_gate_space=0.11
    #             (0.12+0.12=0.24 > 0.11) → use dev_sub_dist+ds for gy
    #             (0.12+0.12=0.24 < diff_spacing=0.33) → use diff_spacing+ds for gx
    #    For 6p0: dev_sub_dist=0 (not specified), sub_surr=0.16 → 0+0.16=0.16 < 0.36 → diff_spacing
    #             0+0.16=0.16 < 0.30 → diff_gate_space for gy
    # =========================================================
    dev_sub_dist = 0.12 if not is_6v else 0.0

    # fw: full device width (x direction, including metal at S/D contacts + nwell)
    fw = 2 * (hl + g2d + hcs + ms + sub_surround)
    # fh: full device height (y direction, including poly contacts + nwell)
    fh = 2 * (hw + g2p + hcs + ps + sub_surround)

    # Guard ring size (Magic's mos_draw formulae)
    _use_dsd_gy = (dev_sub_dist + sub_surround) > diff_gate_space
    _use_dsd_gx = (dev_sub_dist + sub_surround) > diff_spacing

    if _use_dsd_gx:
        gx = fw + 2 * (dev_sub_dist + ds) + cs
    else:
        gx = fw + 2 * (diff_spacing + ds) + cs

    if _use_dsd_gy:
        gy = fh + 2 * (dev_sub_dist + ds) + cs
    else:
        gy = fh + 2 * (diff_gate_space + ds) + cs

    _guard_ring(c, gx, gy, metal_spacing=metal_spacing)

    # =========================================================
    # 8. Dualgate (6.0V only) — enc from measured reference
    #    enc_x = 1.56, enc_y = 1.52 relative to gate centre
    # =========================================================
    if is_6v:
        dg_enc_x = 1.56
        dg_enc_y = 1.52
        _rect(c, -hl - dg_enc_x, -hw - dg_enc_y,
               hl + dg_enc_x,  hw + dg_enc_y, _L_DUALGATE)

    # =========================================================
    # 9. Ports
    # =========================================================
    c.add_port(
        name="gate",
        center=(0.0, float(_snap(hw + g2p))),
        width=float(lc),
        orientation=90,
        layer=_L_METAL1,
        port_type="electrical",
    )
    c.add_port(
        name="source_drain",
        center=(0.0, float(-_snap(hw + g2p))),
        width=float(lc),
        orientation=270,
        layer=_L_METAL1,
        port_type="electrical",
    )

    # =========================================================
    # 10. VLSIR metadata
    # =========================================================
    prefix  = "nmoscap" if is_nmos else "pmoscap"
    voltage = "3p3" if not is_6v else "6p0"
    suffix  = "_b" if "_b" in type else ""
    c.info["vlsir"] = {
        "spice_type": "SUBCKT",
        "spice_lib": "moscap",
        "port_order": ["1", "2"],
        "port_map": {"source_drain": "1", "gate": "2"},
        "params": {"c_length": lc, "c_width": wc},
        "model": f"{prefix}_{voltage}{suffix}",
    }

    return c
