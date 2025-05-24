# Migration from gf180

The `gf180` package has been deprecated in favor of `gf180mcu`. This guide will help you migrate your code from `gf180` to `gf180mcu`.

## Why the change?

The name change from `gf180` to `gf180mcu` was made to better align with GlobalFoundries' naming conventions for their 180nm MCU process technology. The functionality remains identical, but the package name better reflects the specific process being targeted.

## Migration steps

### 1. Update your dependencies

Replace `gf180` with `gf180mcu` in your project dependencies:

```bash
# If using pip
pip install gf180mcu  # Instead of gf180

# If using uv
uv pip install gf180mcu  # Instead of gf180

# If using poetry
poetry add gf180mcu  # Instead of gf180
```

In your requirements.txt or pyproject.toml, replace `gf180` with `gf180mcu`.

### 2. Update your imports

Simply replace all imports of `gf180` with `gf180mcu`:

```python
# Old code
import gf180
from gf180 import some_component

# New code
import gf180mcu
from gf180mcu import some_component
```

### 3. Update function calls and references

Replace all references to `gf180` with `gf180mcu`:

```python
# Old code
component = gf180.diode_dw2ps()
gf180.PDK.activate()

# New code
component = gf180mcu.diode_dw2ps()
gf180mcu.PDK.activate()
```

## Compatibility period

The `gf180` package will continue to work as a thin wrapper around `gf180mcu` for a transition period, but it will show deprecation warnings. The package will eventually be removed, so we recommend migrating to `gf180mcu` as soon as possible.

## Getting help

If you encounter any issues during migration, please [open an issue on GitHub](https://github.com/gdsfactory/gf180mcu/issues).
