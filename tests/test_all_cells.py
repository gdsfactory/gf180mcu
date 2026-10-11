"""Regression coverage for the library sample reticle."""

import gdsfactory as gf

from gf180mcu import PDK
from gf180mcu.cells import dn_rect
from gf180mcu.samples.all_cells import all_cells


def test_all_cells_ignores_registered_generic_and_sample_cells(monkeypatch) -> None:
    """GDSFactory+ registration must not add generic cells or recurse."""
    monkeypatch.setattr(
        PDK,
        "cells",
        {"dn_rect": dn_rect, "rectangle": gf.c.rectangle, "all_cells": all_cells},
    )
    component = all_cells()
    packed = next(iter(component.insts)).cell
    assert [instance.cell.name for instance in packed.insts] == [dn_rect().name]
