"""Write cell docs as Markdown with kwasm viewers."""

import base64
import inspect
import pathlib
import traceback

import kwasm.embed
import matplotlib
import matplotlib.pyplot as plt
from gdsfactory.serialization import clean_value_json

matplotlib.use("Agg")

from gf180mcu import PDK, logic
from gf180mcu.config import PATH

PDK.activate()
cells = PDK.cells

docs_dir = pathlib.Path(__file__).parent.absolute()
filepath = docs_dir / "cells.md"
logic_7t_path = docs_dir / "logic_7t.md"
logic_9t_path = docs_dir / "logic_9t.md"
kwasm_dir = docs_dir / "kwasm"
gds_dir = kwasm_dir / "gds"

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


def _setup_kwasm_viewer() -> None:
    gds_dir.mkdir(parents=True, exist_ok=True)
    viewer_path = kwasm_dir / "viewer.html"
    if viewer_path.exists():
        return
    template = kwasm.embed._read_artifacts()
    template = template.replace("KWASM_GDS_B64", "")
    lyp_path = PATH.lyp
    if lyp_path.exists():
        lyp_b64 = base64.b64encode(lyp_path.read_bytes()).decode("ascii")
        template = template.replace("KWASM_LYP_B64", lyp_b64)
    else:
        template = template.replace("KWASM_LYP_B64", "")
    template = template.replace("KWASM_LYRDB_B64", "")
    template = template.replace("KWASM_NETLIST_B64", "")
    viewer_path.write_text(template)


def _write_gds(name: str, cell_func) -> bool:
    try:
        sig = inspect.signature(cell_func)
        defaults = {}
        for p in sig.parameters:
            v = sig.parameters[p].default
            if isinstance(v, int | float | str | tuple):
                defaults[p] = v
        c = cell_func(**defaults)
        c.write(str(gds_dir / f"{name}.gds"))
        c.plot()
        plt.savefig(str(gds_dir / f"{name}.png"), dpi=150, bbox_inches="tight")
        plt.close("all")
    except Exception:
        traceback.print_exc()
        plt.close("all")
        return False
    else:
        return True


def _module_for(name: str) -> str:
    if "fd_sc_mcu7t5v0" in name or "fd_sc_mcu9t5v0" in name:
        return "gf180mcu.logic"
    if name in ("efuse",) or name.startswith("npn_") or name.startswith("pnp_"):
        return "gf180mcu.fixed"
    return "gf180mcu.cells"


pcell_names = []
fixed_names = []
logic_7t_names = []
logic_9t_names = []

for name in sorted(cells.keys()):
    if name in skip or name.startswith("_"):
        continue
    if "fd_sc_mcu" in name:
        continue
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


_setup_kwasm_viewer()

with open(filepath, "w+") as f:
    f.write("# Cells\n\n")
    f.write("## Parametric Cells (PCells)\n\n")

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
        f.write(f"### {name}\n\n")
        f.write(f"::: {mod}.{name}\n\n")
        if name not in skip_plot:
            has_gds = _write_gds(name, cells[name])
            if has_gds:
                f.write('=== "Static"\n\n')
                f.write(f"    ![{name}](kwasm/gds/{name}.png)\n\n")
                f.write('=== "Dynamic"\n\n')
                f.write(
                    f'    <iframe src="kwasm/viewer.html?url=gds/{name}.gds"'
                    f' loading="lazy" width="100%" height="400"'
                    f' style="border:none"></iframe>\n\n'
                )
            f.write("```python\n")
            f.write("import gf180mcu\n\n")
            f.write("gf180mcu.PDK.activate()\n")
            f.write(f'c = gf180mcu._cells["{name}"]({kwargs})\n')
            f.write("c.draw_ports()\n")
            f.write("c.plot()\n")
            f.write("```\n\n")

    f.write("## Fixed Cells (BJT, eFuse)\n\n")

    for name in fixed_names:
        print(name)
        mod = _module_for(name)
        f.write(f"### {name}\n\n")
        f.write(f"::: {mod}.{name}\n\n")

print(f"Wrote {filepath}")


def _write_logic_page(path: pathlib.Path, title: str, names: list[str]) -> None:
    with open(path, "w+") as f:
        f.write(f"# {title}\n\n")
        for name in names:
            print(name)
            func = getattr(logic, name)
            f.write(f"## {name}\n\n")
            f.write(f"::: gf180mcu.logic.{name}\n\n")
            has_gds = _write_gds(name, func)
            if has_gds:
                f.write('=== "Static"\n\n')
                f.write(f"    ![{name}](kwasm/gds/{name}.png)\n\n")
                f.write('=== "Dynamic"\n\n')
                f.write(
                    f'    <iframe src="kwasm/viewer.html?url=gds/{name}.gds"'
                    f' loading="lazy" width="100%" height="400"'
                    f' style="border:none"></iframe>\n\n'
                )
            f.write("```python\n")
            f.write("from gf180mcu import PDK, logic\n\n")
            f.write("PDK.activate()\n")
            f.write(f"c = logic.{name}()\n")
            f.write("c.plot()\n")
            f.write("```\n\n")
    print(f"Wrote {path}")


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
