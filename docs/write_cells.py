"""Generate cells.rst documentation for all GF180MCU cells.

Groups cells into PCells, Fixed, and Logic sections.
"""

import inspect
import pathlib

from gdsfactory.serialization import clean_value_json

from gf180mcu import PDK

filepath = pathlib.Path(__file__).parent.absolute() / "cells.rst"
cells = PDK.cells

skip = {
    "LIBRARY",
    "circuit_names",
    "component_factory",
    "component_names",
    "container_names",
    "component_names_test_ports",
    "component_names_skip_test",
    "component_names_skip_test_ports",
    "dataclasses",
    "library",
    "waveguide_template",
}

skip_plot: tuple[str, ...] = ("add_fiber_array_siepic",)
skip_settings: tuple[str, ...] = ("flatten", "safe_cell_names")

# Categorize cells
pcell_names = []
fixed_names = []
logic_7t_names = []
logic_9t_names = []

for name in sorted(cells.keys()):
    if name in skip or name.startswith("_"):
        continue
    if "fd_sc_mcu7t5v0" in name:
        logic_7t_names.append(name)
    elif "fd_sc_mcu9t5v0" in name:
        logic_9t_names.append(name)
    elif name in ("efuse",) or name.startswith("npn_") or name.startswith("pnp_"):
        fixed_names.append(name)
    else:
        pcell_names.append(name)


def _module_for(name: str) -> str:
    if "fd_sc_mcu7t5v0" in name or "fd_sc_mcu9t5v0" in name:
        return "gf180mcu.logic"
    if name in ("efuse",) or name.startswith("npn_") or name.startswith("pnp_"):
        return "gf180mcu.fixed"
    return "gf180mcu.cells"


with open(filepath, "w+") as f:
    f.write(
        """
Cells
=============================

Parametric Cells (PCells)
-----------------------------
"""
    )

    for name in pcell_names:
        print(name)
        mod = _module_for(name)
        sig = inspect.signature(cells[name])
        kwargs = ", ".join(
            [
                f"{p}={clean_value_json(sig.parameters[p].default)!r}"
                for p in sig.parameters
                if isinstance(sig.parameters[p].default, int | float | str | tuple)
                and p not in skip_settings
            ]
        )
        f.write(
            f"""

{name}
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: {mod}.{name}

.. plot::
  :include-source:

  import gf180mcu

  c = gf180mcu._cells["{name}"]({kwargs})
  c = c.copy()
  c.draw_ports()
  c.plot()

"""
        )

    f.write(
        """

Fixed Cells (BJT, eFuse)
-----------------------------
"""
    )

    for name in fixed_names:
        print(name)
        mod = _module_for(name)
        f.write(
            f"""

{name}
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: {mod}.{name}

"""
        )

    f.write(
        """

Logic Cells — 7-track 5V (gf180mcu_fd_sc_mcu7t5v0)
-----------------------------------------------------
"""
    )

    for name in logic_7t_names:
        print(name)
        f.write(f"- ``{name}``\n")

    f.write(
        """

Logic Cells — 9-track 5V (gf180mcu_fd_sc_mcu9t5v0)
-----------------------------------------------------
"""
    )

    for name in logic_9t_names:
        print(name)
        f.write(f"- ``{name}``\n")
