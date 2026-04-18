from gdsfactory.get_factories import get_cells
from gdsfactory.pdk import Pdk

from gf180mcu import cells, fixed, layers, logic
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
    "cells",
    "fixed",
    "get_layer_stack",
    "layer",
    "layers",
    "logic",
]
__version__ = "0.5.0"

# Logic cells are DRC-clean pre-built std cells imported from GDS; they don't
# need to be test-built as PDK partials, so exclude them from PDK.cells.
# Access via `from gf180mcu import logic` instead.
_cells = get_cells([cells, fixed])


PDK = Pdk(
    name="gf180mcu",
    cells=_cells,
    layers=LAYER,
    layer_views=LAYER_VIEWS,
    layer_stack=LAYER_STACK,
    cross_sections=cross_sections,
    routing_strategies=routing_strategies,
)
