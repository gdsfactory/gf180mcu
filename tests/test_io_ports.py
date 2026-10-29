"""Regression tests for IO labels repeated across metal layers."""

import pytest

from gf180mcu import PDK, fixed


@pytest.mark.parametrize("metal_stack", ["3lm", "4lm", "5lm"])
@pytest.mark.parametrize(
    "cell_name", ["dvdd", "dvss", "asig_5p0", "bi_t", "bi_24t", "in_c", "in_s"]
)
def test_io_ports_are_unique(cell_name: str, metal_stack: str) -> None:
    """Retain every labeled connection with a unique electrical port name."""
    PDK.activate()
    component = getattr(fixed, cell_name)(metal_stack=metal_stack)
    names = [port.name for port in component.ports]
    assert names
    assert len(names) == len(set(names))
    assert all(port.port_type == "electrical" for port in component.ports)
    label_layers = [(34, 10), (36, 10), (42, 10), (46, 10), (81, 10), (53, 10)]
    assert len(names) == sum(
        len(component.get_labels(layer=layer)) for layer in label_layers
    )
