"""Tests for updating compressed geometry regression references."""

import gdsfactory as gf
from conftest import _config, difftest

from gf180mcu.layers import LAYER


def test_update_preserves_oasis_format(tmp_path, monkeypatch) -> None:
    """A forced reference update must write OASIS rather than renamed GDS bytes."""
    reference = gf.Component()
    reference.add_polygon([(0, 0), (2, 0), (2, 1), (0, 1)], layer=LAYER.metal1)
    path = tmp_path / "reference.oas"
    reference.write(path)
    component = gf.Component()
    component.add_polygon([(0, 0), (1, 0), (1, 1), (0, 1)], layer=LAYER.metal1)
    monkeypatch.setitem(_config, "update_gds_refs", True)
    monkeypatch.setitem(_config, "force_regen", True)
    difftest(component, test_name="reference", dirpath=tmp_path)
    assert path.read_bytes().startswith(b"%SEMI-OASIS")
