"""MOM (Metal-Over-Metal) interdigitated capacitor for GF180MCU.

Adapted from the IHP PDK ``cmom`` cell, simplified for the GF180MCU stack.
The capacitor consists of two interdigitated comb-shaped electrodes, stacked
on every metal layer between ``bottom_metal`` and ``top_metal`` and tied
together with vias at the comb backbones.
"""

from __future__ import annotations

from itertools import pairwise

import gdsfactory as gf

from gf180mcu.cells.via_generator import via_generator
from gf180mcu.layers import layer

# Available metal layers, ordered from bottom to top.
METAL_NAMES: tuple[str, ...] = (
    "metal1",
    "metal2",
    "metal3",
    "metal4",
    "metal5",
    "metaltop",
)

# Via layer that connects metal[i] to metal[i+1], parallel to METAL_NAMES.
VIA_BETWEEN: dict[tuple[str, str], str] = {
    ("metal1", "metal2"): "via1",
    ("metal2", "metal3"): "via2",
    ("metal3", "metal4"): "via3",
    ("metal4", "metal5"): "via4",
    ("metal5", "metaltop"): "via5",
}

# Minimum metal width per layer (um), from GF180MCU design rules.
MIN_WIDTH: dict[str, float] = {
    "metal1": 0.23,
    "metal2": 0.28,
    "metal3": 0.28,
    "metal4": 0.28,
    "metal5": 0.28,
    "metaltop": 0.44,
}

# Minimum metal spacing per layer (um).
MIN_SPACING: dict[str, float] = {
    "metal1": 0.23,
    "metal2": 0.28,
    "metal3": 0.28,
    "metal4": 0.28,
    "metal5": 0.28,
    "metaltop": 0.46,
}


@gf.cell
def cap_mom(
    n_fingers: int = 4,
    finger_length: float = 4.0,
    finger_spacing: float = 0.28,
    bottom_metal: str = "metal1",
    top_metal: str = "metal3",
) -> gf.Component:
    """Return a MOM interdigitated capacitor.

    Two comb electrodes are interdigitated on every metal layer from
    ``bottom_metal`` up to ``top_metal``. Plus / minus backbones on each
    metal level are stitched together with via arrays so the capacitor is a
    true 3D MOM stack.

    Args:
        n_fingers: number of fingers per electrode.
        finger_length: length of each finger (um).
        finger_spacing: edge-to-edge spacing between adjacent fingers (um).
            Smaller spacing gives larger capacitance.
        bottom_metal: lowest metal layer of the stack (e.g. ``"metal1"``).
        top_metal: highest metal layer of the stack (e.g. ``"metal3"``).

    Ports:
        plus: top backbone electrode.
        minus: bottom backbone electrode.
    """
    if bottom_metal not in METAL_NAMES:
        raise ValueError(f"bottom_metal {bottom_metal!r} not in {METAL_NAMES}")
    if top_metal not in METAL_NAMES:
        raise ValueError(f"top_metal {top_metal!r} not in {METAL_NAMES}")
    bottom_idx = METAL_NAMES.index(bottom_metal)
    top_idx = METAL_NAMES.index(top_metal)
    if top_idx < bottom_idx:
        raise ValueError("top_metal must be at or above bottom_metal")
    if n_fingers < 1:
        raise ValueError("n_fingers must be >= 1")

    stack_metals = METAL_NAMES[bottom_idx : top_idx + 1]

    # Use the worst-case (largest) min width / spacing across the stack so the
    # same drawn geometry is DRC-clean on every metal layer.
    finger_width = max(MIN_WIDTH[m] for m in stack_metals)
    min_spacing = max(MIN_SPACING[m] for m in stack_metals)
    if finger_spacing < min_spacing:
        raise ValueError(
            f"finger_spacing {finger_spacing} < min spacing {min_spacing} "
            f"for metals {stack_metals}"
        )

    # Layout pitch: a plus finger followed by a gap, a minus finger and another
    # gap repeats every ``finger_pitch * 2``.
    finger_pitch = finger_width + finger_spacing
    backbone_width = 3 * finger_width  # comply with min metal area
    total_width = (2 * n_fingers) * finger_pitch + finger_width

    c = gf.Component()
    plus_backbone_ref = None
    minus_backbone_ref = None

    for metal_name in stack_metals:
        metal_layer = layer[metal_name]
        finger = gf.components.rectangle(
            size=(finger_width, finger_length), layer=metal_layer
        )

        # Plus comb: fingers at columns 0, 2, 4, ... with backbone on top.
        plus_fingers = c.add_ref(
            finger,
            columns=n_fingers + 1,
            rows=1,
            column_pitch=2 * finger_pitch,
        )
        plus_fingers.ymin = finger_spacing

        # Minus comb: fingers at columns 1, 3, 5, ... with backbone on bottom.
        minus_fingers = c.add_ref(
            finger,
            columns=n_fingers,
            rows=1,
            column_pitch=2 * finger_pitch,
        )
        minus_fingers.xmin = finger_pitch
        minus_fingers.ymin = 0

        backbone = gf.components.rectangle(
            size=(total_width, backbone_width), layer=metal_layer
        )
        plus_backbone_ref = c.add_ref(backbone)
        plus_backbone_ref.ymin = finger_length + finger_spacing
        minus_backbone_ref = c.add_ref(backbone)
        minus_backbone_ref.ymax = 0

    # Stitch every adjacent metal pair together with vias on both backbones.
    for lower, upper in pairwise(stack_metals):
        via_layer = layer[VIA_BETWEEN[(lower, upper)]]
        for backbone_ref in (plus_backbone_ref, minus_backbone_ref):
            assert backbone_ref is not None
            c.add_ref(
                via_generator(
                    x_range=(backbone_ref.xmin, backbone_ref.xmax),
                    y_range=(backbone_ref.ymin, backbone_ref.ymax),
                    via_layer=via_layer,
                )
            )

    # Capacitor recognition marker covering full footprint.
    c.add_ref(gf.components.bbox(c, layer=layer["cap_mk"]))

    assert plus_backbone_ref is not None
    assert minus_backbone_ref is not None
    top_metal_layer = layer[top_metal]
    c.add_port(
        name="plus",
        center=(plus_backbone_ref.x, plus_backbone_ref.y),
        width=backbone_width,
        orientation=90,
        layer=top_metal_layer,
        port_type="electrical",
    )
    c.add_port(
        name="minus",
        center=(minus_backbone_ref.x, minus_backbone_ref.y),
        width=backbone_width,
        orientation=270,
        layer=top_metal_layer,
        port_type="electrical",
    )

    c.info["n_fingers"] = n_fingers
    c.info["finger_length"] = finger_length
    c.info["finger_spacing"] = finger_spacing
    c.info["finger_width"] = finger_width
    c.info["bottom_metal"] = bottom_metal
    c.info["top_metal"] = top_metal
    return c
