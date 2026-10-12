"""This script generates a reticle with all the cells in the library."""

import gdsfactory as gf
from gdsfactory.get_factories import get_cells

from gf180mcu import LAYER, PDK, fixed, logic
from gf180mcu import cells as pcells

skip = {
    "all_cells",
}


@gf.cell
def all_cells(draw_ports: bool = False) -> gf.Component:
    """Returns a sample reticle with all cells."""
    c = gf.Component()
    cells = []
    library_cells = get_cells([pcells, fixed, logic])

    for cell_name, cell in PDK.cells.items():
        if cell_name in skip or cell_name not in library_cells:
            continue
        try:
            cell_instance = cell()
            if draw_ports:
                cell_instance.draw_ports()
            cells.append(cell_instance)
        except Exception as e:
            print(f"Error instantiating cell {cell_name}: {e}")

    cell_matrix = c << gf.pack(cells)[0]
    floorplan = c << gf.c.rectangle(
        size=(cell_matrix.xsize + 20, cell_matrix.ysize + 20),
        layer=LAYER.border,
    )
    floorplan.center = cell_matrix.center
    return c


if __name__ == "__main__":
    PDK.activate()
    c = all_cells(draw_ports=True)
    gdspath = c.write_gds()
    gf.show(gdspath)
