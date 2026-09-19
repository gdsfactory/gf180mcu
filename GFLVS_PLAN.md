# GFLVS LVS Config Plan — GF180MCU

## PDK Info
- Package: `gf180mcu`
- Classification: electronic (CMOS 180nm)
- Layers file: `gf180mcu/layers.py` (class `LAYER`)
- Dev branch: `dev/gflvs-config`
- Existing config: `gf180mcu/gf/lvs/lvs.py` (partially implemented)

## Namespace Note
Config lives at `gf180mcu/gf/lvs/lvs.py` — NOT inside a directory named `gflvs/`.
This avoids shadowing the installed `gflvs` library. The existing path follows this rule.

## Task: Retrofit Flag Switches into Existing Config

The config at `gf180mcu/gf/lvs/lvs.py` already defines GDS_TABLE, LAYER_CONNECTIVITY,
DEVICE_TEMPLATES, DEFAULT_LVS_CONFIG, and `run_lvs_gf180mcu()`. This plan adds:

### Files to Modify
- `gf180mcu/gf/lvs/lvs.py` — add INCLUDE_* flag switches (see below)

### Files to Create
- `tests/gflvs/test_lvs_gf180mcu.py` — inverter integration test
- `docs/gflvs-lvs.md` — usage documentation
- `.github/workflows/test_lvs.yml` — CI (workflow_dispatch only)
- `Makefile`: add `test-lvs` recipe

## Flag Switches (add near top of lvs.py, before DEVICE_TEMPLATES)

```python
# ── Device family switches ────────────────────────────────────────────────────
# Set to True/False to include/exclude device template families from LVS extraction.
INCLUDE_FET          = True   # nfet, pfet, nfet_06v0_nvt
INCLUDE_RESISTORS    = True   # res_rm1/rm2/rm3, res_ppolyf_u/s, res_npolyf_u/s, res_nplus_u, res_pplus_u, res_nwell
INCLUDE_CAPACITORS   = True   # cap_mim, cap_mos
INCLUDE_DIODES       = True   # diode_nd2ps, diode_pd2nw, diode_nw2ps, diode_pw2dw, diode_dw2ps, sc_diode
INCLUDE_GUARDRING    = True   # pcmpgr
INCLUDE_VIA_CELLS    = True   # via_generator, via_stack
```

Assemble DEVICE_TEMPLATES conditionally by grouping existing templates into lists:
```python
FET_TEMPLATES: list[DeviceTemplate] = [NFET_TEMPLATE, PFET_TEMPLATE, NFET_06V0_NVT_TEMPLATE]
RESISTOR_TEMPLATES: list[DeviceTemplate] = [RES_RM1_TEMPLATE, RES_RM2_TEMPLATE, ...]
CAPACITOR_TEMPLATES: list[DeviceTemplate] = [CAP_MIM_TEMPLATE, CAP_MOS_TEMPLATE]
DIODE_TEMPLATES: list[DeviceTemplate] = [DIODE_ND2PS_TEMPLATE, ...]
VIA_TEMPLATES: list[DeviceTemplate] = [VIA_GENERATOR_TEMPLATE, VIA_STACK_TEMPLATE]

DEVICE_TEMPLATES: list[DeviceTemplate] = [
    *(FET_TEMPLATES if INCLUDE_FET else []),
    *(RESISTOR_TEMPLATES if INCLUDE_RESISTORS else []),
    *(CAPACITOR_TEMPLATES if INCLUDE_CAPACITORS else []),
    *(DIODE_TEMPLATES if INCLUDE_DIODES else []),
    *([PCMPGR_TEMPLATE] if INCLUDE_GUARDRING else []),
    *(VIA_TEMPLATES if INCLUDE_VIA_CELLS else []),
]
```

## Test Circuit (3x3 Ring Modulator Transceiver — Electrical Variant)
File: `tests/gflvs/test_lvs_gf180mcu.py`

Build an inverter circuit (nfet + pfet) mirroring the pattern in
`tests/gf180mcu/inverter/build_layout.py` and `build_schematic.py`:
```python
pytest.importorskip("gflvs")
# pfet (M1, w_gate=0.44µm, l_gate=0.28µm, nf=1)
# nfet (M2, w_gate=0.22µm, l_gate=0.28µm, nf=1)
# Metal1 net connecting M1 drain to M2 drain (net "out")
# run_lvs_gf180mcu(lib, circuit) — smoke assertion (no raise)
```

## CI Workflow
File: `.github/workflows/test_lvs.yml`
```yaml
name: Test LVS (gflvs)
on:
  workflow_dispatch:
jobs:
  test-lvs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync --all-extras
      - run: uv pip install gflvs
      - run: make test-lvs
```

## Makefile Recipe
```makefile
test-lvs:
	uv run pytest tests/gflvs/ -v
```

## Verification
- [ ] `python -c "from gf180mcu.gf.lvs import DEFAULT_LVS_CONFIG, INCLUDE_FET"` succeeds
- [ ] Setting `INCLUDE_FET = False` removes FET templates from `DEVICE_TEMPLATES`
- [ ] Test skips cleanly when gflvs not installed (`pytest.importorskip`)
- [ ] `ruff check gf180mcu/gf/lvs/` passes
