# PEX with gfpex — GF180MCU

`gf180mcu/pex/rules.py` holds the default gfpex techfile for GF180MCU (gf180mcuD): layers and GDS pairs, the
KPEX computed layers, the process stack (z, thickness, dielectric k, contacts) and the parasitic tables (sheet,
contact and via resistance; substrate, overlap, sidewall and side-overlap capacitance). The values are carried
over unchanged from gf-pex `gfpexconfg/gf180mcuD.py`, which comes from KPEX.

## Installation

gfpex is optional and private; it is not a dependency of this package.

```bash
uv pip install networkx "kfnetlist @ git+https://github.com/gdsfactory/kfnetlist" \
    "gfpex @ git+https://github.com/doplaydo/gf-pex@dev/diogo-main"
```

## Usage

```python
from gf180mcu.pex.rules import DEFAULT_PEX_RULES_CONFIG  # a gfpex.gfpex.Techfile
```

## Provenance tags

Every block of numbers carries a tag:

| Tag | Meaning |
|---|---|
| `FOUNDRY <source>` | stated by a GF180MCU PDK document |
| `DERIVED <formula>` | computed from other values |
| `ASSUMED <source>` | taken from KPEX / Magic gf180mcuD tech data, no foundry page cited |
| `PALACE-FIT` | fitted with gf-pex `benchmarks/palace_benchmark.py` |

Palace-fit values are pending (`TODO(palace)`): the perimeter, sidewall and side-overlap coefficients are the
KPEX/Magic values until the Palace fit lands.

## Running the tests

```bash
make test-pex
```

The tests skip when gfpex is not installed. In CI, run the manual **Test PEX rules with gfpex** workflow; it needs
the `GFPEX_TOKEN` secret.
