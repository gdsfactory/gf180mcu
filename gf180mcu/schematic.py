"""Legacy DSchematic annotations for GF180's bundled ngspice models.

Dimensions in expressions refer to factory settings in micrometres. Extra
layout settings are deliberately accepted by every callback.
"""

from functools import partial
from pathlib import Path

from kfactory.schematic import DSchematic

MODEL_DIR = Path(__file__).resolve().parent / "models" / "ngspice"
CORNERS = ["typical", "ff", "ss"]
RESISTORS = (
    "rm1",
    "rm2",
    "rm3",
    "nplus_u",
    "pplus_u",
    "npolyf_u",
    "ppolyf_u",
    "npolyf_s",
    "ppolyf_s",
    "nwell",
    "ppolyf_u_1k",
    "ppolyf_u_1k_6p0",
)


def primitive(
    symbol: str,
    ports: list[tuple[str, str]],
    model: str,
    library: str,
    params: dict[str, str],
    *,
    spice_type: str = "SUBCKT",
    corners: list[str] | None = None,
) -> DSchematic:
    """Build symbol metadata and real schematic ports in model pin order."""
    s = DSchematic()
    s.info["symbol"] = symbol
    positions = {
        "left": (-1, 0, 180),
        "right": (1, 0, 0),
        "top": (0, 1, 90),
        "bottom": (0, -1, 270),
    }
    s.info["ports"] = [
        {"name": name, "side": side, "type": "electric"} for name, side in ports
    ]
    for name, side in ports:
        x, y, orientation = positions[side]
        s.create_port(
            name=name, cross_section="metal1", x=x, y=y, orientation=orientation
        )
    s.info["models"] = [
        {
            "language": "spice",
            "implementation": "NgSpice",
            "name": model,
            "spice_type": spice_type,
            "library": str(MODEL_DIR / f"{library}.lib"),
            "sections": list(corners or CORNERS),
            "port_order": [name for name, _ in ports],
            "params": params,
        }
    ]
    return s


def fet_schematic(
    polarity: str = "n",
    native: bool = False,
    volt: str = "3.3V",
    dss: bool = False,
    asym: bool = False,
    **kwargs: object,
) -> DSchematic:
    if dss or asym or (not native and volt not in ("3.3V", "6.0V")):
        raise ValueError(
            "No verified GF180 model mapping for 5V/10V, DSS or asymmetric MOS"
        )
    model = (
        "nmos_6p0_nat"
        if native
        else f"{polarity}mos_{'3p3' if volt == '3.3V' else '6p0'}"
    )
    return primitive(
        f"{polarity}mos",
        [("D", "top"), ("G", "left"), ("S", "bottom"), ("B", "right")],
        model,
        "fets",
        {"w": "w_gate * nf * 1e-6", "l": "l_gate * 1e-6", "nf": "nf"},
        corners=[*CORNERS, "fs", "sf"],
    )


nfet_schematic = partial(fet_schematic, polarity="n")
pfet_schematic = partial(fet_schematic, polarity="p")
native_schematic = partial(fet_schematic, native=True)


def res_schematic(res_type: str = "rm1", **kwargs: object) -> DSchematic:
    if res_type not in RESISTORS:
        raise ValueError(f"No verified GF180 resistor model: {res_type}")
    ports = [("r0", "top"), ("r1", "bottom")]
    if res_type not in ("rm1", "rm2", "rm3"):
        ports.append(("bulk", "right"))
    return primitive(
        "resistor",
        ports,
        res_type,
        "resistors",
        {"r_length": "l_res * 1e-6", "r_width": "w_res * 1e-6", "s": "1", "par": "1"},
    )


def diode_schematic(kind: str, volt: str = "3.3V", **kwargs: object) -> DSchematic:
    voltages = {"3.3V": "3p3", "6.0V": "6p0"}
    if kind in ("nw2ps", "pw2dw", "dw2ps"):
        voltages["5/6V"] = "6p0"
    if kind != "sc" and volt not in voltages:
        raise ValueError(f"No verified GF180 {kind} diode voltage: {volt}")
    names = {"nd2ps": "np", "pd2nw": "pn", "nw2ps": "nwp"}
    model = (
        f"{names[kind]}_{voltages[volt]}"
        if kind in names
        else {"pw2dw": "dnwpw", "dw2ps": "dnwps", "sc": "sc_diode"}[kind]
    )
    width, length = "wa", "la"
    if kind in ("nw2ps", "pw2dw", "dw2ps"):
        extension = (1.24 if volt == "3.3V" else 1.32) if kind == "dw2ps" else 0.32
        width, length = f"(wa + {extension})", f"(la + {extension})"
    multiplier = "m * " if kind == "sc" else ""
    return primitive(
        "diode",
        [("anode", "top"), ("cathode", "bottom")],
        model,
        "diodes",
        {
            "area": f"{multiplier}{width} * {length} * 1e-12",
            "pj": f"2 * {multiplier}({width} + {length}) * 1e-6",
        },
        spice_type="D",
    )


def mim_schematic(**kwargs: object) -> DSchematic:
    return primitive(
        "capacitor",
        [("top", "top"), ("bottom", "bottom")],
        "mim_2p0fF",
        "mimcaps",
        {"c_length": "lc * 1e-6", "c_width": "wc * 1e-6"},
    )


def moscap_schematic(
    type: str = "cap_nmos", volt: str = "3.3V", **kwargs: object
) -> DSchematic:
    if type not in ("cap_nmos", "cap_pmos", "cap_nmos_b", "cap_pmos_b") or volt not in (
        "3.3V",
        "6.0V",
    ):
        raise ValueError(f"No verified GF180 MOS capacitor model: {type}, {volt}")
    model = f"{type[4:8]}cap_{'3p3' if volt == '3.3V' else '6p0'}"
    if type.endswith("_b"):
        model += "_b"
    return primitive(
        "capacitor",
        [("gate", "top"), ("source_drain", "bottom")],
        model,
        "moscaps",
        {"c_length": "lc * 1e-6", "c_width": "wc * 1e-6"},
    )


def bjt_schematic(model: str, **kwargs: object) -> DSchematic:
    ports = [("C", "top"), ("B", "left"), ("E", "bottom")]
    if model.startswith("vnpn"):
        ports.append(("S", "right"))
    return primitive(
        "npn" if model.startswith("vnpn") else "pnp", ports, model, "bjts", {}
    )


def efuse_schematic(**kwargs: object) -> DSchematic:
    return primitive(
        "resistor",
        [("in", "top"), ("out", "bottom")],
        "efuse",
        "resistors",
        {"pblow": "0"},
    )
