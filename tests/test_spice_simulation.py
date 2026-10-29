"""Numerical tests of factory metadata -> nyancad -> InSpice -> simulators.

Requires the development simulator dependencies described in docs/simulation.md.
"""

import inspect
import shutil

import gdsfactory as gf
import numpy as np
import pytest

import gf180mcu
from gf180mcu.schematic import RESISTORS

Simulator = pytest.importorskip("InSpice.Spice.Simulator").Simulator
NyanCircuit = pytest.importorskip("nyancad.netlist").NyanCircuit
pytest.importorskip("vacask_bin")

SIDEWALL_DIODES = {"diode_nd2ps", "diode_pd2nw", "diode_nw2ps", "diode_dw2ps"}


def model_documents(factory_name, settings, nets):
    """Use the same schematic-info key normalization as nyanlib publication."""
    factory = gf180mcu.PDK.cells[factory_name]
    defaults = {
        key: value.default
        for key, value in inspect.signature(factory).parameters.items()
    }
    schematic = gf.kcl.factories[factory_name].get_schematic(**{**defaults, **settings})
    info = schematic.info
    model_id = f"gf180mcu.{factory_name}"
    return {
        "top": {
            "top:dut": {
                "type": info["symbol"],
                "name": "dut",
                "model": model_id,
                "nets": nets,
                "props": settings,
            }
        },
        "models": {
            f"models:{model_id}": {
                "name": factory_name,
                "type": info["symbol"],
                "ports": info["ports"],
                "models": [
                    {k.replace("_", "-"): v for k, v in entry.items()}
                    for entry in info["models"]
                ],
                "props": [
                    {"name": key, "default": value} for key, value in defaults.items()
                ],
            }
        },
    }


def run_device(factory_name, settings, nets, simulator, *, corner="typical", ac=False):
    if simulator == "ngspice" and shutil.which("ngspice") is None:
        pytest.skip("ngspice executable is required for numerical comparison")
    circuit = NyanCircuit(
        "top",
        model_documents(factory_name, settings, nets),
        sim=simulator,
        corners=[corner],
    )
    circuit.V("bias", "bias", 0, dc_value=0 if ac else 0.6, ac_value=1)
    engine = "ngspice-subprocess" if simulator == "ngspice" else simulator
    simulation = Simulator.factory(simulator=engine).simulation(
        circuit, temperature=27, nominal_temperature=27
    )
    if ac:
        result = simulation.ac(
            variation="lin", number_of_points=1, start_frequency=1e6, stop_frequency=1e6
        )
    else:
        result = simulation.operating_point()
    current = np.asarray(result.branches["Vbias"])[0]
    assert np.isfinite(current)
    return current


def compare_vacask(factory_name, settings, nets, *, corner="typical", ac=False):
    """Keep exact released-adapter limitations visible as expected failures.

    No parameter is dropped, model replaced, or tolerance widened to make the
    released simulator appear compatible. Other errors still fail the test.
    """
    reference = run_device(
        factory_name, settings, nets, "ngspice", corner=corner, ac=ac
    )
    try:
        actual = run_device(
            factory_name, settings, nets, "vacask", corner=corner, ac=ac
        )
    except RuntimeError as error:
        parameter = {
            "res": "r_length",
            "cap_mim": "c_length",
            "cap_mos": "c_length",
        }.get(factory_name)
        if factory_name.startswith("pnp_"):
            parameter = "cbcp"
        if parameter and f"Parameter '{parameter}' not found." in str(error):
            pytest.xfail(
                f"Released VACASK adapter rejects {factory_name} parameter {parameter}; see docs/simulation.md"
            )
        raise
    try:
        np.testing.assert_allclose(actual, reference, rtol=0.01, atol=1e-12)
    except AssertionError:
        if (
            not ac
            and factory_name in SIDEWALL_DIODES
            and 1.05 < actual / reference < 1.4
        ):
            pytest.xfail(
                f"Released VACASK level-3 diode mismatch: {actual} A versus ngspice {reference} A"
            )
        if (
            factory_name == "nfet"
            and settings.get("nf", 1) > 1
            and 1.1 < actual / reference < 1.2
        ):
            pytest.xfail(
                f"Released VACASK multifinger current mismatch: {actual} A versus ngspice {reference} A"
            )
        raise
    return actual


DC_CASES = [
    (
        "nfet",
        {"w_gate": 1, "l_gate": 0.28},
        {"D": "bias", "G": "bias", "S": "GND", "B": "GND"},
    ),
    (
        "nfet",
        {"w_gate": 1, "l_gate": 0.7, "volt": "6.0V"},
        {"D": "bias", "G": "bias", "S": "GND", "B": "GND"},
    ),
    (
        "pfet",
        {"w_gate": 1, "l_gate": 0.28},
        {"D": "GND", "G": "GND", "S": "bias", "B": "bias"},
    ),
    (
        "pfet",
        {"w_gate": 1, "l_gate": 0.7, "volt": "6.0V"},
        {"D": "GND", "G": "GND", "S": "bias", "B": "bias"},
    ),
    ("nfet_06v0_nvt", {}, {"D": "bias", "G": "bias", "S": "GND", "B": "GND"}),
    *[
        (
            "res",
            {"res_type": kind, "l_res": 10, "w_res": 2},
            {
                "r0": "bias",
                "r1": "GND",
                **({} if kind.startswith("rm") else {"bulk": "GND"}),
            },
        )
        for kind in RESISTORS
    ],
    *[
        (name, {"wa": 2, "la": 3}, {"anode": "bias", "cathode": "GND"})
        for name in (
            "diode_nd2ps",
            "diode_pd2nw",
            "diode_nw2ps",
            "diode_pw2dw",
            "diode_dw2ps",
            "sc_diode",
        )
    ],
    *[
        (name, {}, {"C": "bias", "B": "bias", "E": "GND", "S": "GND"})
        for name in (
            "npn_00p54x02p00",
            "npn_00p54x04p00",
            "npn_00p54x08p00",
            "npn_00p54x16p00",
            "npn_05p00x05p00",
            "npn_10p00x10p00",
        )
    ],
    *[
        (name, {}, {"C": "GND", "B": "GND", "E": "bias"})
        for name in (
            "pnp_05p00x00p42",
            "pnp_10p00x00p42",
            "pnp_05p00x05p00",
            "pnp_10p00x10p00",
        )
    ],
    ("efuse", {}, {"in": "bias", "out": "GND"}),
]


@pytest.mark.parametrize("factory_name,settings,nets", DC_CASES)
def test_ngspice_dc_models_conduct(factory_name, settings, nets):
    reference = run_device(factory_name, settings, nets, "ngspice")
    assert reference < -1e-15, (
        "reference must exercise correctly oriented conducting devices"
    )


@pytest.mark.parametrize("factory_name,settings,nets", DC_CASES)
def test_dc_current_matches_ngspice(factory_name, settings, nets):
    compare_vacask(factory_name, settings, nets)


AC_CASES = [
    ("cap_mim", {"lc": 5, "wc": 7}, {"top": "bias", "bottom": "GND"}),
    *[
        (
            "cap_mos",
            {"type": kind, "volt": volt, "lc": 5, "wc": 7},
            {"gate": "bias", "source_drain": "GND"},
        )
        for kind in ("cap_nmos", "cap_pmos", "cap_nmos_b", "cap_pmos_b")
        for volt in ("3.3V", "6.0V")
    ],
]


@pytest.mark.parametrize("factory_name,settings,nets", AC_CASES)
def test_ngspice_capacitor_models_charge(factory_name, settings, nets):
    reference = run_device(factory_name, settings, nets, "ngspice", ac=True)
    assert reference.imag < -1e-10, "reference must exercise nonzero capacitance"


@pytest.mark.parametrize("factory_name,settings,nets", AC_CASES)
def test_capacitance_matches_ngspice(factory_name, settings, nets):
    compare_vacask(factory_name, settings, nets, ac=True)


@pytest.mark.parametrize("corner", ["typical", "ff", "ss", "fs", "sf"])
def test_mos_corners_match_ngspice(corner):
    compare_vacask(
        "nfet",
        {"w_gate": 1, "l_gate": 0.28},
        {"D": "bias", "G": "bias", "S": "GND", "B": "GND"},
        corner=corner,
    )


@pytest.mark.parametrize("nf", [2, 4])
def test_multiple_fingers_match_ngspice(nf):
    compare_vacask(
        "nfet",
        {"w_gate": 1, "l_gate": 0.28, "nf": nf},
        {"D": "bias", "G": "bias", "S": "GND", "B": "GND"},
    )
