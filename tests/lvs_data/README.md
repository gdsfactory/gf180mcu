# LVS test data

Small foundry GDS files used by `tests/test_lvs_rules.py`:

- `ref_sc_INV_X1_7T5P0.gds`: 5 V standard-cell inverter.
- `rm1.gds`: metal1 resistor testcase.

Source: [google/globalfoundries-pdk-libs-gf180mcu_fd_pr](https://github.com/google/globalfoundries-pdk-libs-gf180mcu_fd_pr)
at `9f992d5`, `rules/klayout/lvs/testing`. License: Apache-2.0.

The repo gitignores `*.gds`, so these files were added with `git add -f`.
