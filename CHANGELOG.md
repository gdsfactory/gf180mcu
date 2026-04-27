# CHANGELOG

<!-- towncrier release notes start -->

## [1.0.0](https://github.com/gdsfactory/gf180mcu/releases/tag/v1.0.0) - 2026-04-27

First stable release. Marks API parity with the upstream Magic Tcl pcell
generators and a stable public surface for downstream tools.

### Breaking

- Refactor electrical pcells for Magic parity ([#91](https://github.com/gdsfactory/gf180mcu/pull/91))
  - Ports the Magic Tcl primitive generators (FETs, BJTs, diodes, capacitors, resistors, guard rings) to Python with XOR-validated parity against reference GDS.
  - Restructures cell modules under `gf180mcu/cells/`, adds `gf180mcu/logic` and `gf180mcu/fixed` collections.
  - Ports missing KLayout diode variants `nw2ps`, `pw2dw`, `dw2ps`, `sc_diode`.
- VLSIR-based netlisting support ([#51](https://github.com/gdsfactory/gf180mcu/pull/51)).
- Layer-stack overlap fixes + interdig cell rework ([#81](https://github.com/gdsfactory/gf180mcu/pull/81)).

### New

- `@cell` type tags on all components ([#94](https://github.com/gdsfactory/gf180mcu/pull/94)).
- DRC workflow + numeric DRC badge ([#78](https://github.com/gdsfactory/gf180mcu/pull/78), [#79](https://github.com/gdsfactory/gf180mcu/pull/79)).
- Metric badge workflows + README dashboard ([#92](https://github.com/gdsfactory/gf180mcu/pull/92)).
- Auto-label PDK workflow ([#103](https://github.com/gdsfactory/gf180mcu/pull/103)).
- Issue auto-label CI ([#59](https://github.com/gdsfactory/gf180mcu/pull/59)).
- Add missing pins ([#37](https://github.com/gdsfactory/gf180mcu/pull/37)).

### Fixes

- Activate PDK via sphinx extension instead of package import ([#99](https://github.com/gdsfactory/gf180mcu/pull/99)).
- Hide private repo links from public docs ([#77](https://github.com/gdsfactory/gf180mcu/pull/77)).
- LICENSE clarifications ([#97](https://github.com/gdsfactory/gf180mcu/pull/97)).

### Maintenance

- Sync drift-enforced workflow templates from upstream (`pages.yml`, `dependabot.yml`, `release-drafter.yml`, `test_code.yml`, `issue.yml`, `claude-pr-review.yml`) ([#96](https://github.com/gdsfactory/gf180mcu/pull/96), [#98](https://github.com/gdsfactory/gf180mcu/pull/98)).
- Centralize CI workflows ([#75](https://github.com/gdsfactory/gf180mcu/pull/75)).
- Switch dependabot to `uv` ecosystem with cooldown ([#80](https://github.com/gdsfactory/gf180mcu/pull/80), [#86](https://github.com/gdsfactory/gf180mcu/pull/86)).
- Dependabot interval to monthly + ignore doplaydo actions ([#70](https://github.com/gdsfactory/gf180mcu/pull/70), [#73](https://github.com/gdsfactory/gf180mcu/pull/73)).
- Bump `gdsfactory` to `<9.40.2` ([#89](https://github.com/gdsfactory/gf180mcu/pull/89), [#65](https://github.com/gdsfactory/gf180mcu/pull/65)).
- Python 3.13/3.14 support bump ([#58](https://github.com/gdsfactory/gf180mcu/pull/58)).
- Bump `actions/checkout` 5 → 6 ([#49](https://github.com/gdsfactory/gf180mcu/pull/49)).
- Add code owners ([#55](https://github.com/gdsfactory/gf180mcu/pull/55)).
- Install / pre-commit / release instructions in README ([#67](https://github.com/gdsfactory/gf180mcu/pull/67)).

## 0.4.0

- create cells folder [#14](https://github.com/gdsfactory/gf180/pull/14)
- add ports [#12](https://github.com/gdsfactory/gf180/pull/12)

## 0.3.1

- Update to gdsfactory 9.12.1

## 0.3.0

- Update package

## 0.1.1 (2025-05-24)

- Package renamed from gf180 to gf180mcu to better align with GlobalFoundries naming
- Added migration guide for users transitioning from gf180
- The original gf180 package is now deprecated and serves as a wrapper for gf180mcu
