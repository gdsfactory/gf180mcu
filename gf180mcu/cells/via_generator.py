from math import ceil, floor
from typing import Any

import gdsfactory as gf
from gdsfactory.add_pins import add_electrical_pins
from gdsfactory.typings import Float2, LayerSpec, Size, Spacing

from gf180mcu.layers import layer


@gf.cell(tags=["via_generator"])
def via_generator(
    x_range: Float2 = (0, 1),
    y_range: Float2 = (0, 1),
    via_size: Float2 = (0.17, 0.17),
    via_layer: LayerSpec = (66, 44),
    via_enclosure: Float2 = (0.06, 0.06),
    via_spacing: Float2 = (0.17, 0.17),
) -> gf.Component:
    """Return only vias withen the range xrange and yrange while enclosing by via_enclosure
    and set number of rows and number of columns according to ranges and via size and spacing.

    Args:
        x_range: dx range.
        y_range: dy range.
        via_size: via size.
        via_layer: via layer.
        via_enclosure: via enclosure.
        via_spacing: via spacing.

    """
    c = gf.Component()

    width = x_range[1] - x_range[0]
    length = y_range[1] - y_range[0]
    nr = floor(length / (via_size[1] + via_spacing[1]))
    if (length - nr * via_size[1] - (nr - 1) * via_spacing[1]) / 2 < via_enclosure[1]:
        nr -= 1

    nr = max(nr, 1)
    nc = ceil(width / (via_size[0] + via_spacing[0]))

    if (
        round(width - nc * via_size[0] - (nc - 1) * via_spacing[0], 2)
    ) / 2 < via_enclosure[0]:
        nc -= 1

    nc = max(nc, 1)
    via_sp = (via_size[0] + via_spacing[0], via_size[1] + via_spacing[1])

    rect_via = gf.components.rectangle(size=via_size, layer=via_layer)

    via_arr = c.add_ref(
        rect_via, rows=nr, columns=nc, column_pitch=via_sp[0], row_pitch=via_sp[1]
    )

    via_arr.move((x_range[0], y_range[0]))

    via_arr.movex((width - nc * via_size[0] - (nc - 1) * via_spacing[0]) / 2)
    via_arr.movey((length - nr * via_size[1] - (nr - 1) * via_spacing[1]) / 2)

    # Add ports for top and bottom connections
    center_x = (x_range[0] + x_range[1]) / 2

    c.add_port(
        name="e1",
        center=(center_x, y_range[0]),
        width=width,
        orientation=270,
        layer=via_layer,
        port_type="electrical",
    )

    c.add_port(
        name="e2",
        center=(center_x, y_range[1]),
        width=width,
        orientation=90,
        layer=via_layer,
        port_type="electrical",
    )

    add_electrical_pins(c, port_pin_mapping={"e": ["e1", "e2"]})
    return c


# (via layer, metal layer above it) for each level of a via stack above metal1
_via_metal_levels = (
    (layer["via1"], layer["metal2"]),
    (layer["via2"], layer["metal3"]),
    (layer["via3"], layer["metal4"]),
    (layer["via4"], layer["metal5"]),
)


@gf.cell(tags=["via_generator"])
def via_stack(
    x_range: Float2 = (0, 1),
    y_range: Float2 = (0, 1),
    metal_level: int = 1,
    con_size: Size = (0.22, 0.22),
    con_enc: float = 0.07,
    m_enc: float = 0.06,
    con_spacing: Spacing = (0.28, 0.28),
    via_size: Size = (0.26, 0.26),
    via_spacing: Spacing = (0.26, 0.26),
    via_enc: Float2 = (0.06, 0.06),
    base_layer: LayerSpec = layer["metal1"],
    **kwargs: Any,
) -> gf.Component:
    """Returns a via stack within the range x_range and y_range, expecting the base_layer to be drawn.

    Args:
        x_range: dx range.
        y_range: dy range.
        metal_level: top metal of the stack (1 to 5).
        con_size: contact size.
        con_enc: contact enclosure.
        m_enc: metal enclosure of the contacts/vias below it.
        con_spacing: contact spacing.
        via_size: via size.
        via_spacing: via spacing.
        via_enc: enclosure of each via by the metal below it.
        base_layer: layer drawn around the bottom contacts, i.e. the first
            metal of the stack.

    return via stack till the metal level indicated where :
    metal_level 1 : till m1
    metal_level 2 : till m2
    metal_level 3 : till m3
    metal_level 4 : till m4
    metal_level 5 : till m5
    """
    if not 1 <= metal_level <= len(_via_metal_levels) + 1:
        raise ValueError(
            f"metal_level must be between 1 and {len(_via_metal_levels) + 1}, "
            f"got {metal_level}"
        )

    c = gf.Component()
    con_gen = via_generator(
        x_range=x_range,
        y_range=y_range,
        via_size=con_size,
        via_enclosure=(con_enc, con_enc),
        via_layer=layer["contact"],
        via_spacing=con_spacing,
    )
    con = c.add_ref(con_gen)
    m1_x = con.xsize + 2 * m_enc
    m1_y = con.ysize + 2 * m_enc
    m1 = c.add_ref(gf.components.rectangle(size=(m1_x, m1_y), layer=base_layer))
    m1.xmin = con.xmin - m_enc
    m1.ymin = con.ymin - m_enc

    top_metal = m1
    top_layer = base_layer
    top_width = m1_x

    for level, (via_layer, metal_layer) in enumerate(
        _via_metal_levels[: metal_level - 1], start=2
    ):
        via_gen = via_generator(
            x_range=(top_metal.xmin, top_metal.xmax),
            y_range=(top_metal.ymin, top_metal.ymax),
            via_size=via_size,
            via_enclosure=via_enc,
            via_layer=via_layer,
            via_spacing=via_spacing,
        )
        via = c.add_ref(via_gen)

        m_x = via.xsize + 2 * m_enc
        m_y = via.ysize + 2 * m_enc
        if level < metal_level:
            # intermediate metals must be large enough to enclose the next via
            m_x = max(m_x, via_size[0] + 2 * via_enc[0])
            m_y = max(m_y, via_size[1] + 2 * via_enc[1])

        m = c.add_ref(gf.components.rectangle(size=(m_x, m_y), layer=metal_layer))
        m.move((via.xmin - (m_x - via.xsize) / 2, via.ymin - (m_y - via.ysize) / 2))

        top_metal = m
        top_layer = metal_layer
        top_width = m_x

    center = ((x_range[0] + x_range[1]) / 2, (y_range[0] + y_range[1]) / 2)

    # Port at bottom layer
    c.add_port(
        name="e1",
        center=center,
        width=m1_x,
        orientation=0,
        layer=base_layer,
        port_type="electrical",
    )

    # Port at top metal layer
    c.add_port(
        name="e2",
        center=center,
        width=top_width,
        orientation=0,
        layer=top_layer,
        port_type="electrical",
    )

    add_electrical_pins(c, port_pin_mapping={"e": ["e1", "e2"]})
    return c
