"""Generate doc pages for all GF180MCU cells.

Writes:
  docs/cells.rst       — PCells + Fixed
  docs/logic_7t.rst    — 7-track 5V std cells (with plots)
  docs/logic_9t.rst    — 9-track 5V std cells (with plots)
"""

import inspect
import pathlib

from gdsfactory.serialization import clean_value_json

from gf180mcu import PDK, logic

docs_dir = pathlib.Path(__file__).parent.absolute()
filepath = docs_dir / "cells.rst"
logic_7t_path = docs_dir / "logic_7t.rst"
logic_9t_path = docs_dir / "logic_9t.rst"
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
    if "fd_sc_mcu" in name:
        continue  # std cells documented on dedicated logic_7t/9t pages
    if name in ("efuse",) or name.startswith("npn_") or name.startswith("pnp_"):
        fixed_names.append(name)
    else:
        pcell_names.append(name)

for name in sorted(n for n in dir(logic) if not n.startswith("_")):
    if not callable(getattr(logic, name)):
        continue
    if "fd_sc_mcu7t5v0" in name:
        logic_7t_names.append(name)
    elif "fd_sc_mcu9t5v0" in name:
        logic_9t_names.append(name)


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


def _write_logic_page(path: pathlib.Path, title: str, names: list[str]) -> None:
    with open(path, "w+") as f:
        underline = "=" * len(title)
        f.write(f"{title}\n{underline}\n\n")
        for name in names:
            print(name)
            f.write(
                f"""
{name}
{"^" * len(name)}

.. autofunction:: gf180mcu.logic.{name}

.. plot::

   from gf180mcu import PDK, logic
   PDK.activate()
   logic.{name}().plot()

"""
            )


_write_logic_page(
    logic_7t_path,
    "Logic Cells — 7-track 5V (gf180mcu_fd_sc_mcu7t5v0)",
    logic_7t_names,
)
_write_logic_page(
    logic_9t_path,
    "Logic Cells — 9-track 5V (gf180mcu_fd_sc_mcu9t5v0)",
    logic_9t_names,
)
