# ---
# jupyter:
#   jupytext:
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Layout
#
# > **NOTE**: If you were previously using the `gf180` package, it has been renamed to `gf180mcu` and the original package is now deprecated.
#
# ## Layout driven flow
#
# You can import the PDK and layout any of the standard cells

# %%
from gf180mcu import PDK, cells

# %%
PDK.activate()
c = cells.diode_dw2ps()
c.plot()
