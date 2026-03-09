"""Write a GDS with all cells."""

import gdsfactory as gf

from gf180mcu import PDK, cells

if __name__ == "__main__":
    PDK.activate()

    c0 = cells.pad()
    c1 = cells.via_stack()
    c = gf.grid([c0, c1])
    c.show()
    s = c.to_3d()
    s.show()
