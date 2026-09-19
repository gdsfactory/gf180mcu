"""Integration test for GF180MCU gflvs LVS config."""

from __future__ import annotations

import pytest

gflvs = pytest.importorskip("gflvs")

from gf180mcu.lvs import DEFAULT_LVS_CONFIG  # noqa: E402


def test_lvs_config_importable() -> None:
    assert DEFAULT_LVS_CONFIG is not None


def test_gds_table_nonempty() -> None:
    from gf180mcu.lvs.lvs import GDS_TABLE

    assert len(GDS_TABLE) > 0


def test_include_flags_control_device_templates() -> None:
    import gf180mcu.lvs.lvs as lvs_mod

    original = lvs_mod.INCLUDE_FET
    lvs_mod.INCLUDE_FET = False
    templates_without_fet = [
        *(lvs_mod.FET_TEMPLATES if lvs_mod.INCLUDE_FET else []),
        *(lvs_mod.RESISTOR_TEMPLATES if lvs_mod.INCLUDE_RESISTORS else []),
    ]
    lvs_mod.INCLUDE_FET = original
    assert len(templates_without_fet) == len(lvs_mod.RESISTOR_TEMPLATES)


def test_inverter_lvs_smoke() -> None:
    """Smoke: build inverter schematic + empty layout, run LVS, assert result returned."""
    import gdsfactory as gf
    from gflvs.gflvs_schema.circuit import TerminalReference
    from gflvs.schematic import (
        build_circuit,
        build_connection,
        build_external_module,
        build_module,
        build_module_reference,
        build_terminal,
    )

    from gf180mcu.lvs import run_lvs_gf180mcu

    nfet = build_external_module("nfet", terminals=[
        build_terminal("D"), build_terminal("G"), build_terminal("S"), build_terminal("B"),
    ])
    pfet = build_external_module("pfet", terminals=[
        build_terminal("D"), build_terminal("G"), build_terminal("S"), build_terminal("B"),
    ])
    top = build_module(
        name="inverter",
        module_references=[build_module_reference("mn", "nfet"), build_module_reference("mp", "pfet")],
        connections=[
            build_connection(
                "drain_net",
                source=TerminalReference(instance_name="mn", terminal_name="D"),
                target=TerminalReference(instance_name="mp", terminal_name="D"),
            ),
        ],
    )
    circuit = build_circuit("inverter", top_module="inverter", modules=[top], ext_modules=[nfet, pfet])
    layout = gf.Component("inverter")
    result = run_lvs_gf180mcu(layout, circuit)
    assert result is not None
