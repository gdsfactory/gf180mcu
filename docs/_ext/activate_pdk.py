"""Sphinx extension: activate gf180mcu PDK for docs build.

Autodoc renders cell docstrings that instantiate partials requiring an
active PDK. The package itself no longer activates on import, so we
activate here for the docs build only.
"""

import gf180mcu


def setup(app):
    gf180mcu.PDK.activate()
    return {"version": "0.1", "parallel_read_safe": True}
