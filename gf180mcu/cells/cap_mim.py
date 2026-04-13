import gdsfactory as gf

from gf180mcu.cells.via_generator import via_generator
from gf180mcu.layers import layer

# (top_metal, bottom_metal, via, top_label, bottom_label) per MIM option.
_MIM_LAYER_STACK: dict[tuple[str, str], tuple[str, str, str, str, str]] = {
    ("MIM-A", "M3"): ("metal3", "metal2", "via2", "metal3_label", "metal2_label"),
    ("MIM-B", "M4"): ("metal4", "metal3", "via3", "metal4_label", "metal3_label"),
    ("MIM-B", "M5"): ("metal5", "metal4", "via4", "metal5_label", "metal4_label"),
    ("MIM-B", "M6"): ("metaltop", "metal5", "via5", "metaltop_label", "metal5_label"),
}


@gf.cell
def cap_mim(
    mim_option: str = "MIM-A",
    metal_level: str = "M4",
    length: float = 2,
    width: float = 2,
    label: bool = False,
    top_label: str = "",
    bottom_label: str = "",
) -> gf.Component:
    """Return a MIM (Metal-Insulator-Metal) capacitor.

    Args:
        mim_option: ``"MIM-A"`` (between M2/M3) or ``"MIM-B"`` (between M3 and
            ``metal_level``).
        metal_level: top metal level for ``MIM-B``: ``"M4"``, ``"M5"`` or
            ``"M6"``. Ignored for ``MIM-A``.
        length: capacitor length (um).
        width: capacitor width (um).
        label: if True, add labels to the top and bottom electrodes.
        top_label: text for the top electrode label.
        bottom_label: text for the bottom electrode label.
    """
    key = ("MIM-A", "M3") if mim_option == "MIM-A" else (mim_option, metal_level)
    if key not in _MIM_LAYER_STACK:
        raise ValueError(
            f"Unsupported (mim_option, metal_level)={key}. "
            f"Valid combinations: {list(_MIM_LAYER_STACK)}"
        )
    top_metal, bottom_metal, via_name, top_label_name, bottom_label_name = (
        _MIM_LAYER_STACK[key]
    )
    top_metal_layer = layer[top_metal]
    bottom_metal_layer = layer[bottom_metal]
    via_layer = layer[via_name]
    top_label_layer = layer[top_label_name]
    bottom_label_layer = layer[bottom_label_name]

    via_size = (0.22, 0.22)
    via_spacing = (0.5, 0.5)
    via_enclosure = (0.4, 0.4)
    bottom_enclosure = 0.6
    marker_width = 0.1

    c = gf.Component()

    top_plate = c.add_ref(
        gf.components.rectangle(size=(width, length), layer=top_metal_layer)
    )

    fusetop = c.add_ref(
        gf.components.rectangle(
            size=(top_plate.xsize, top_plate.ysize), layer=layer["fusetop"]
        )
    )
    fusetop.xmin = top_plate.xmin
    fusetop.ymin = top_plate.ymin

    mim_marker = c.add_ref(
        gf.components.rectangle(
            size=(fusetop.xsize, marker_width), layer=layer["mim_l_mk"]
        )
    )
    mim_marker.xmin = fusetop.xmin
    mim_marker.ymin = fusetop.ymin

    bottom_plate = c.add_ref(
        gf.components.rectangle(
            size=(
                top_plate.xsize + 2 * bottom_enclosure,
                top_plate.ysize + 2 * bottom_enclosure,
            ),
            layer=bottom_metal_layer,
        )
    )
    bottom_plate.xmin = top_plate.xmin - bottom_enclosure
    bottom_plate.ymin = top_plate.ymin - bottom_enclosure

    cap_marker = c.add_ref(
        gf.components.rectangle(
            size=(bottom_plate.xsize, bottom_plate.ysize), layer=layer["cap_mk"]
        )
    )
    cap_marker.xmin = bottom_plate.xmin
    cap_marker.ymin = bottom_plate.ymin

    if label:
        c.add_label(
            top_label,
            position=(
                top_plate.xmin + top_plate.xsize / 2,
                bottom_plate.xmin + bottom_plate.ysize / 2,
            ),
            layer=top_label_layer,
        )
        c.add_label(
            bottom_label,
            position=(
                bottom_plate.xmin + bottom_plate.xsize / 2,
                bottom_plate.ymin + (top_plate.ymin - bottom_plate.ymin) / 2,
            ),
            layer=bottom_label_layer,
        )

    c.add_ref(
        via_generator(
            x_range=(top_plate.xmin, top_plate.xmax),
            y_range=(top_plate.ymin, top_plate.ymax),
            via_enclosure=via_enclosure,
            via_layer=via_layer,
            via_size=via_size,
            via_spacing=via_spacing,
        )
    )

    c.add_port(
        name="top",
        center=(top_plate.dcenter[0], top_plate.dcenter[1]),
        width=top_plate.xsize,
        orientation=90,
        layer=top_metal_layer,
        port_type="electrical",
    )
    c.add_port(
        name="bottom",
        center=(bottom_plate.dcenter[0], bottom_plate.dcenter[1]),
        width=bottom_plate.xsize,
        orientation=90,
        layer=bottom_metal_layer,
        port_type="electrical",
    )

    c.info["vlsir"] = {
        "spice_type": "SUBCKT",
        "spice_lib": "mim_cap",
        "port_order": ["1", "2"],
        "port_map": {"top": "1", "bottom": "2"},
        "params": {"c_length": length, "c_width": width},
    }
    if mim_option == "MIM-B":
        c.info["vlsir"].update({"model": "mim_1p0fF"})
    else:
        c.info["vlsir"].update({"model": "mim_2p0fF"})

    return c
