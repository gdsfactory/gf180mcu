"""Annotation contracts through the registered, decorated cell factories."""

import inspect
import re
from pathlib import Path

import gdsfactory as gf
import pytest

import gf180mcu
from gf180mcu import cells, fixed
from gf180mcu.schematic import MODEL_DIR, RESISTORS


def schematic(name, **settings):
    # gf.cell's public function wraps the registered kfactory factory.
    return gf.kcl.factories[name].get_schematic(**settings)


def model(name, **settings):
    return schematic(name, **settings).info["models"][0]


@pytest.mark.parametrize(
    "name",
    [
        "nfet",
        "pfet",
        "nfet_06v0_nvt",
        "res",
        "diode_nd2ps",
        "diode_pd2nw",
        "diode_nw2ps",
        "diode_pw2dw",
        "diode_dw2ps",
        "sc_diode",
        "cap_mim",
        "cap_mos",
        "npn_00p54x02p00",
        "npn_00p54x04p00",
        "npn_00p54x08p00",
        "npn_00p54x16p00",
        "npn_05p00x05p00",
        "npn_10p00x10p00",
        "pnp_05p00x00p42",
        "pnp_05p00x05p00",
        "pnp_10p00x00p42",
        "pnp_10p00x10p00",
        "efuse",
    ],
)
def test_factory_metadata(name, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    func = gf180mcu.PDK.cells[name]
    settings = {k: p.default for k, p in inspect.signature(func).parameters.items()}
    s = schematic(name, **settings)
    assert isinstance(s.info["symbol"], str)
    (m,) = s.info["models"]
    assert m["language"] == "spice"
    assert m["implementation"] == "NgSpice"
    assert m["spice_type"] == ("D" if "diode" in name else "SUBCKT")
    assert [p["name"] for p in s.info["ports"]] == m["port_order"]
    assert set(s.ports) == set(m["port_order"])
    assert all(p["type"] == "electric" and p["side"] for p in s.info["ports"])
    path = Path(m["library"])
    assert path.is_absolute() and path.is_file()
    wrapper = path.read_text()
    vendor = (MODEL_DIR / "sm141064.ngspice").read_text()
    assert m["sections"] == ["typical", "ff", "ss"] + (
        ["fs", "sf"] if name in ("nfet", "pfet", "nfet_06v0_nvt") else []
    )
    for corner in m["sections"]:
        block = re.search(rf"(?ms)^\.lib {corner}\n(.*?)^\.endl {corner}$", wrapper)[1]
        assert ".include 'settings.inc'" in block
        section = re.search(r"\.lib 'sm141064.ngspice' (\w+)", block)[1]
        assert re.search(rf"(?im)^\s*\.lib {section}\s*$", vendor)
    assert re.search(rf"(?im)^\s*\.(?:subckt|model)\s+{re.escape(m['name'])}\s", vendor)


@pytest.mark.parametrize("name,prefix", [("nfet", "nmos"), ("pfet", "pmos")])
@pytest.mark.parametrize("volt,suffix", [("3.3V", "3p3"), ("6.0V", "6p0")])
def test_fets(name, prefix, volt, suffix):
    settings = dict(w_gate=2.5, l_gate=0.6, nf=4, volt=volt, label=True, grw=0)
    m = model(name, **settings)
    assert m["name"] == f"{prefix}_{suffix}"
    assert m["port_order"] == ["D", "G", "S", "B"]
    assert evaluate(m, settings) == pytest.approx(dict(w=10e-6, l=0.6e-6, nf=4))
    assert model("nfet_06v0_nvt", nf=3)["name"] == "nmos_6p0_nat"


def evaluate(m, settings):
    return {k: eval(v, {"__builtins__": {}}, settings) for k, v in m["params"].items()}


@pytest.mark.parametrize("variant", RESISTORS)
def test_resistors(variant):
    m = model("res", res_type=variant, l_res=12, w_res=2, r0_label="plus")
    assert m["name"] == variant
    assert m["port_order"] == ["r0", "r1"] + (
        [] if variant.startswith("rm") else ["bulk"]
    )
    assert evaluate(m, dict(l_res=12, w_res=2)) == pytest.approx(
        dict(r_length=12e-6, r_width=2e-6, s=1, par=1)
    )


@pytest.mark.parametrize(
    "name,volt,expected,extension",
    [
        ("diode_nd2ps", "3.3V", "np_3p3", 0),
        ("diode_nd2ps", "6.0V", "np_6p0", 0),
        ("diode_pd2nw", "3.3V", "pn_3p3", 0),
        ("diode_pd2nw", "6.0V", "pn_6p0", 0),
        ("diode_nw2ps", "3.3V", "nwp_3p3", 0.32),
        ("diode_nw2ps", "5/6V", "nwp_6p0", 0.32),
        ("diode_pw2dw", "3.3V", "dnwpw", 0.32),
        ("diode_pw2dw", "5/6V", "dnwpw", 0.32),
        ("diode_dw2ps", "3.3V", "dnwps", 1.24),
        ("diode_dw2ps", "5/6V", "dnwps", 1.32),
    ],
)
def test_diodes(name, volt, expected, extension):
    m = model(name, volt=volt, wa=2, la=3)
    assert m["name"] == expected
    assert m["port_order"] == ["anode", "cathode"]
    assert evaluate(m, dict(wa=2, la=3)) == pytest.approx(
        dict(
            area=(2 + extension) * (3 + extension) * 1e-12,
            pj=2 * (5 + 2 * extension) * 1e-6,
        ),
        abs=1e-24,
    )


def test_schottky_fingers():
    m = model("sc_diode", wa=2, la=3, m=4, cw=0.5)
    assert m["name"] == "sc_diode"
    assert evaluate(m, dict(wa=2, la=3, m=4)) == pytest.approx(
        dict(area=24e-12, pj=40e-6), rel=1e-12, abs=1e-24
    )


@pytest.mark.parametrize("kind", ["nmos", "pmos", "nmos_b", "pmos_b"])
@pytest.mark.parametrize("volt,suffix", [("3.3V", "3p3"), ("6.0V", "6p0")])
def test_capacitors(kind, volt, suffix):
    m = model("cap_mos", type=f"cap_{kind}", volt=volt, lc=4, wc=7, deepnwell=True)
    assert m["name"] == f"{kind[:4]}cap_{suffix}" + (
        "_b" if kind.endswith("_b") else ""
    )
    assert m["port_order"] == ["gate", "source_drain"]
    assert evaluate(m, dict(lc=4, wc=7)) == pytest.approx(
        dict(c_length=4e-6, c_width=7e-6)
    )
    mim = model("cap_mim", mim_option="B", metal_level="M6", lc=4, wc=7)
    assert mim["name"] == "mim_2p0fF"
    assert mim["port_order"] == ["top", "bottom"]
    assert evaluate(mim, dict(lc=4, wc=7)) == pytest.approx(
        dict(c_length=4e-6, c_width=7e-6)
    )


@pytest.mark.parametrize(
    "name,expected",
    [
        ("npn_00p54x02p00", "vnpn_0p54x2"),
        ("npn_00p54x04p00", "vnpn_0p54x4"),
        ("npn_00p54x08p00", "vnpn_0p54x8"),
        ("npn_00p54x16p00", "vnpn_0p54x16"),
        ("npn_05p00x05p00", "vnpn_5x5"),
        ("npn_10p00x10p00", "vnpn_10x10"),
        ("pnp_05p00x00p42", "vpnp_0p42x5"),
        ("pnp_10p00x00p42", "vpnp_0p42x10"),
        ("pnp_05p00x05p00", "vpnp_5x5"),
        ("pnp_10p00x10p00", "vpnp_10x10"),
    ],
)
def test_bjts(name, expected):
    m = model(name)
    assert m["name"] == expected
    pins = ["C", "B", "E"] + (["S"] if name.startswith("npn") else [])
    assert m["port_order"] == pins
    vendor = (MODEL_DIR / "sm141064.ngspice").read_text()
    assert re.search(
        rf"(?im)^\.subckt {expected}\s+{' +'.join(p.lower() for p in pins)}\s+par=",
        vendor,
    )
    assert not m["params"]


def test_efuse():
    assert callable(fixed.efuse)
    m = model("efuse")
    assert m["name"] == "efuse"
    assert m["port_order"] == ["in", "out"]
    assert m["params"] == {"pblow": "0"}


@pytest.mark.parametrize(
    "name,settings",
    [
        ("nfet", {"volt": "5.0V"}),
        ("pfet", {"volt": "10.0V"}),
        ("nfet", {"dss": True}),
        ("pfet", {"asym": True}),
        ("res", {"res_type": "unknown"}),
        ("cap_mos", {"type": "unknown"}),
        ("cap_mos", {"volt": "5.0V"}),
        ("diode_nd2ps", {"volt": "5.0V"}),
    ],
)
def test_unsupported(name, settings):
    with pytest.raises(ValueError, match="No verified GF180"):
        schematic(name, **settings)


def test_physical_terminals():
    d = cells.diode_nd2ps(wa=2, la=3)
    assert d.ports["cathode"].center == pytest.approx((0, 0))
    assert d.ports["anode"].center != pytest.approx((0, 0))
    c = cells.cap_mos(lc=4, wc=7)
    assert c.ports["source_drain"].center == pytest.approx((2.26, 0))
    assert c.ports["source_drain"].width == pytest.approx(7)
    assert c.ports["source_drain"].orientation == 0


def test_settings_are_defined_once():
    text = (MODEL_DIR / "settings.inc").read_text()
    assignments = re.findall(r"(\w+)=(\d+)", text)
    assert dict(assignments) == dict(
        sw_stat_global="0",
        sw_stat_mismatch="0",
        mc_skew="3",
        res_mc_skew="3",
        cap_mc_skew="3",
        fnoicor="0",
    )
    assert len(assignments) == 6
    for wrapper in MODEL_DIR.glob("*.lib"):
        assert "design.ngspice" not in wrapper.read_text()
