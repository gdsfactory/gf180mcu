from gdsfactory.get_factories import get_cells
from gdsfactory.pdk import Pdk

from gf180mcu import cells, layers
from gf180mcu.config import PATH
from gf180mcu.layers import (
    LAYER,
    LAYER_STACK,
    LAYER_VIEWS,
    LayerMap,
    get_layer_stack,
    layer,
)
from gf180mcu.tech import cross_sections, routing_strategies

__all__ = [
    "LAYER",
    "LAYER_STACK",
    "LAYER_VIEWS",
    "PATH",
    "LayerMap",
    "get_layer_stack",
    "layer",
    "layers",
]
__version__ = "0.4.0"

_cells = get_cells(cells)


PDK = Pdk(
    name="gf180mcu",
    cells=_cells,
    layers=LAYER,
    layer_views=LAYER_VIEWS,
    layer_stack=LAYER_STACK,
    cross_sections=cross_sections,
    routing_strategies=routing_strategies,
)
PDK.activate()
