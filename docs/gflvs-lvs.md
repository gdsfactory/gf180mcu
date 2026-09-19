# LVS with gflvs — GF180MCU

## Installation

```bash
uv pip install gflvs
```

## Usage

```python
from gf180mcu.lvs import DEFAULT_LVS_CONFIG, run_lvs_gf180mcu

result = run_lvs_gf180mcu(lib_or_component, circuit)
```

## Configuration flags

Set these module-level booleans in `gf180mcu/lvs/lvs.py` (or override at runtime) to include or exclude device families:

| Flag | Default | Devices |
|---|---|---|
| `INCLUDE_FET` | `True` | nfet, pfet, nfet_06v0_nvt |
| `INCLUDE_RESISTORS` | `True` | res_rm1/rm2/rm3, res_ppolyf_u/s, res_npolyf_u/s, res_nplus_u, res_pplus_u, res_nwell |
| `INCLUDE_CAPACITORS` | `True` | cap_mim, cap_mos |
| `INCLUDE_DIODES` | `True` | diode_nd2ps, diode_pd2nw, diode_nw2ps, diode_pw2dw, diode_dw2ps, sc_diode |
| `INCLUDE_GUARDRING` | `True` | pcmpgr_gen |
| `INCLUDE_VIA_CELLS` | `True` | via_generator, via_stack |

## Running LVS tests

```bash
make test-lvs
```
