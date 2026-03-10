"""Write a GDS with all cells."""

import gdsfactory as gf

from gf180mcu import PDK, cells

if __name__ == "__main__":
    PDK.activate()

    c1 = cells.straight(cross_section="strip", length=5)
    c2 = cells.straight(cross_section="metal1", length=5)
    c3 = cells.straight(cross_section="metal2", length=5)

    c = gf.grid([c1, c2, c3])
    c.show()
    s = c.to_3d()
    s.show()
