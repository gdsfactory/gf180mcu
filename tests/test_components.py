import pathlib

import gdsfactory as gf
import kfactory as kf
import numpy as np
import pytest
from gdsfactory.component import Component
from gdsfactory.difftest import difftest
from pytest_regressions.data_regression import DataRegressionFixture

from gf180mcu import PDK

skip_test = {"res_dev"}
cells = PDK.cells
cell_names = set(cells.keys()) - set(skip_test)
dirpath = pathlib.Path(__file__).absolute().parent / "gds_ref"


@pytest.fixture(params=cell_names, scope="function")
def component(request) -> Component:
    return cells[request.param]()


def test_pdk_gds(component: Component) -> None:
    """Avoid regressions in GDS geometry shapes and layers."""
    difftest(component, dirpath=dirpath)


def test_pdk_settings(
    component: Component, data_regression: DataRegressionFixture
) -> None:
    """Avoid regressions when exporting settings."""
    data_regression.check(component.to_dict())


@pytest.mark.parametrize("component_name", cell_names)
def test_optical_port_positions(component_name: str) -> None:
    """Ensure that optical ports are positioned correctly."""
    component = cells[component_name]()
    if isinstance(component, gf.ComponentAllAngle):
        new_component = gf.Component()
        kf.VInstance(component).insert_into_flat(new_component, levels=0)
        new_component.add_ports(component.ports)
        component = new_component
    for port in component.ports:
        if port.port_type == "optical":
            port_layer = port.layer
            port_width = port.width
            port_position = port.center
            port_angle = port.orientation
            # get the edges of the optical layer corresponding to the port
            cs_region = kf.kdb.Region(component.begin_shapes_rec(port_layer))
            optical_edges = cs_region.edges()

            # get a small marker around the port position
            tolerance = 0.001
            poly = kf.kdb.DBox(-tolerance, -tolerance, tolerance, tolerance)
            dbu_in_um = port.kcl.to_um(1)
            port_marker = (
                kf.kdb.DPolygon(poly).transformed(port.dcplx_trans).to_itype(dbu_in_um)
            )
            port_marker_region = kf.kdb.Region(port_marker)

            # get the physical port edge that interacts with the marker
            # assert that there is exactly one edge interacting with the marker
            # and that it has the correct length
            interacting_edges = optical_edges.interacting(port_marker_region)
            if interacting_edges.is_empty():
                raise AssertionError(
                    f"No optical edge found for port {port.name} at position {port_position} with width {port_width} and angle {port_angle}."
                )
            port_edge = next(iter(interacting_edges.each()))
            edge_length = port_edge.length() * 0.001
            if not np.isclose(edge_length, port_width, atol=1e-3):
                raise AssertionError(
                    f"Port {port.name} has width {port_width}, but the optical edge length is {edge_length}."
                )
