# Analog schematic models

GF180 analog factories carry legacy `DSchematic` annotations, following the
IHP pattern. This covers MOSFETs, resistors, all six diode generators, MIM and
MOS capacitors, all fixed BJTs, and efuse. Metadata contains an explicit symbol,
electric ports, ordered model terminals, and parameter expressions evaluated
against the layout factory settings. Extra layout keyword arguments are accepted.

With the GF180 PDK active, access the registered decorated factory:

```python
import gdsfactory as gf
import gf180mcu

schematic = gf.kcl.factories["nfet"].get_schematic(w_gate=2, l_gate=0.6, nf=4)
model = schematic.info["models"][0]
```

## Simulator and corners

Only `language="spice"`, `implementation="NgSpice"` is advertised. VACASK consumes
these ngspice sources through its SPICE translation path. This integration needs
the include-options API in **InSpice PR #36**, the nyancad dialect/model-reference
plumbing, and the additional InSpice diode-perimeter (`pj`) and pulse/AC fixes
developed with these annotations. Install revisions containing those changes;
an arbitrary released version number is not evidence that it includes the feature.
Numerical simulator integration is tested separately from annotation contracts.

The bundled Xyce passive translations have broken equations/losses and are not
advertised as verified implementations.

Package-local absolute library paths are resolved from `gf180mcu/schematic.py`,
so model lookup does not depend on the process working directory. The libraries
in `gf180mcu/models/ngspice` provide `typical`, `ff`, and `ss`; `fets.lib` also
provides `fs` and `sf`. Each family wrapper loads the matching vendor section
from `sm141064.ngspice`. Efuse uses `resistors.lib`.

Shared `settings.inc` disables global statistics and mismatch, sets `mc_skew`,
`res_mc_skew`, and `cap_mc_skew` to 3, and sets `fnoicor=0`. Wrappers deliberately
do not include `design.ngspice` and redefine its parameters: VACASK rejects
duplicate `.param` declarations. VACASK's include deduplication handles the
shared settings file when several families are loaded together. Choose one
corner per family per simulation.

## Model and terminal contracts

All layout dimensions below are in micrometres; model lengths are in metres,
junction areas in square metres, and perimeters in metres.

| Family | Model | Ordered terminals | Parameters |
| --- | --- | --- | --- |
| NFET/PFET 3.3V, 6.0V | `nmos_3p3`, `pmos_3p3`, `nmos_6p0`, `pmos_6p0` | D, G, S, B | `w=w_gate*nf*1e-6`, `l=l_gate*1e-6`, `nf=nf` |
| Native NFET | `nmos_6p0_nat` | D, G, S, B | Same MOS dimensions |
| Metal resistors | `rm1`, `rm2`, `rm3` | r0, r1 | `r_length=l_res*1e-6`, `r_width=w_res*1e-6`, `s=1`, `par=1` |
| Other resistors | `nplus_u`, `pplus_u`, `npolyf_u`, `ppolyf_u`, `npolyf_s`, `ppolyf_s`, `nwell`, `ppolyf_u_1k`, `ppolyf_u_1k_6p0` | r0, r1, bulk | Same resistor dimensions |
| N+/Psub | `np_3p3`, `np_6p0` | anode, cathode | Diffusion junction area/perimeter |
| P+/Nwell | `pn_3p3`, `pn_6p0` | anode, cathode | Diffusion junction area/perimeter |
| Nwell/Psub | `nwp_3p3`, `nwp_6p0` | anode, cathode | Well junction area/perimeter |
| Pwell/DNW | `dnwpw` | anode, cathode | Well junction area/perimeter |
| DNW/Psub | `dnwps` | anode, cathode | Solid DNW junction area/perimeter |
| Schottky | `sc_diode` | anode, cathode | Sum over `m` fingers |
| MIM | `mim_2p0fF` | top, bottom | `c_length=lc*1e-6`, `c_width=wc*1e-6` |
| MOS capacitor | `nmoscap_3p3`, `pmoscap_3p3`, `nmoscap_6p0`, `pmoscap_6p0`, and each `_b` variant | gate, source_drain | Same capacitor dimensions |
| NPN | `vnpn_0p54x2`, `vnpn_0p54x4`, `vnpn_0p54x8`, `vnpn_0p54x16`, `vnpn_5x5`, `vnpn_10x10` | C, B, E, S | Fixed geometry, vendor defaults |
| PNP | `vpnp_0p42x5`, `vpnp_0p42x10`, `vpnp_5x5`, `vpnp_10x10` | C, B, E | Fixed geometry, vendor defaults |
| Efuse | `efuse` | in, out | `pblow=0` |

All models are `SUBCKT` instances except diodes, which are primitive `D`
instances. MOS `w_gate` is width **per finger**, while BSIM4 `w` is total width.
No extra MOS multiplicity property is invented. Nonmetal resistor bulk is an
explicit schematic terminal and must be connected by the circuit, never silently
grounded. NPN's fourth terminal is substrate, following the bundled subcircuit.
The fixed PNP factories named `pnp_05p00x00p42` and `pnp_10p00x00p42` map to
`vpnp_0p42x5` and `vpnp_0p42x10`, respectively.

Diffusion diodes use `area=wa*la*1e-12`, `pj=2*(wa+la)*1e-6`.
Nwell/Psub and Pwell/DNW use a junction rectangle with **0.32 added to each
dimension**. DNW/Psub uses **1.24** added at 3.3V or **1.32** at 5/6V;
this is a solid rectangle, not an annulus, and `cw` is not its junction width.
Schottky uses `area=m*wa*la*1e-12`, `pj=2*m*(wa+la)*1e-6`, with no additional
multiplicity factor. Diffusion diodes accept documented `3.3V`/`6.0V` spellings;
well diodes also accept their documented `5/6V` spelling. Pwell/DNW and DNW/Psub
use the same named model at either voltage, without invented voltage suffixes.

## Layout limitations

These annotations describe requested electrical variants; they do **not** claim
layout-versus-schematic validation. All existing polygons are preserved.

* MOS 5V/10V, DSS, and asymmetric geometry variants lack verified model mappings;
  requesting their schematics raises a focused `ValueError`.
* Ignored diode `deepnwell`/`pcmpgr` options do not produce fabricated isolation
  models. Several diode layouts lack physical ports even though their schematics
  have explicit terminals. N+/Psub physical names are corrected: the centre N+
  contact is cathode and the P+ guard is anode.
* Nonmetal resistor physical endpoint placement/bulk access is not validated by
  these annotations; the schematic's bulk connection must be provided explicitly.
* MIM `mim_option="B"` and `metal_level` are currently ignored by geometry.
  They do not select a different electrical density; the model remains 2 fF/µm².
* MOS capacitor `type` selects `cap_nmos`, `cap_pmos`, or their `_b` electrical
  variants at `3.3V`/`6.0V`. Implant/well variants are not actually honored by
  the current layout, and 3.3V geometry lacks comp under the gate. Isolation
  options are also ignored. The source/drain physical port is corrected to the
  actual right-hand contact at `(lc/2 + 0.26, 0)`, facing right, rather than the
  second poly gate contact. These terminal fixes do not repair polygons.
* Fixed GDS loading retains its existing repository-relative asset location;
  schematic model lookup works independently of those GDS assets.

## Numerical verification and current VACASK limits

`tests/test_spice_simulation.py` runs real factory annotations through nyancad and
InSpice. It verifies 34 DC cases and nine AC capacitor cases against ngspice,
including every public analog family. Separate comparisons exercise the released
`vacask-bin==0.3.4.dev0`, five MOS corners, and multiple fingers. Conditions are
27 °C with statistical variation disabled.

The reference ngspice cases all conduct/charge with finite, correctly signed
results. VACASK matches the tested single-finger MOS cases, native NMOS, all six
NPN variants, efuse, Pwell/DNW diode, and Schottky diode within 1%. The five NMOS
corner comparisons also pass.

The following exact compatibility failures remain visible as expected failures
in the comparative tests. Other exceptions and numerical discrepancies fail
normally; no model equations or tolerances are changed to conceal them.

| Case | Released VACASK limitation |
| --- | --- |
| All resistor variants | Rejects overriding `r_length`: SPICE header defaults such as `r_length=l` become non-overridable dependent parameters in the adapter. |
| MIM and MOS capacitors | Same issue for `c_length`; a reduced probe also exposes unsupported voltage-dependent capacitance expressions after bypassing that first issue. |
| Four PNP variants | Rejects `cbcp` and related zero-valued model parameters that ngspice tolerates. |
| N+/Psub, P+/Nwell, Nwell/Psub, DNW/Psub diode tests | Level-3 diode DC currents differ from ngspice by approximately 11–31% in the tested bias/geometry, despite preserving area and perimeter. |
| Two- and four-finger NMOS tests | Approximately 12.5% current discrepancy versus ngspice in the tested geometry; the total-width/finger mapping itself is retained explicitly in both decks. |

The dashboard integration suite in GDSFactory++ separately resolves all 23
factories through `resolveFactories`, reads the actual nyanlib, and runs a CMOS
inverter through `spiceSimulate`. OP, a 0–3.3 V DC sweep, AC, and pulsed transient
pass, including high/low output checks. This establishes the complete metadata,
worker, and results path; it does not establish compatibility of the cases above.

The SPICE worker also re-evaluates metadata for each factory invocation before
netlisting. This is essential for `volt`, `res_type`, and MOS-capacitor `type`:
two instances of one factory can select different models and terminal counts.
An additional RPC test checks mixed 3.3 V/6 V MOS models against ngspice reference
currents, rather than relying on the default entry in `models.nyanlib`.

### Development checks

Use a project virtual environment with editable GF180, the updated InSpice and
nyancad checkouts, `vacask-bin==0.3.4.dev0`, pytest, and an `ngspice` executable.
Run from the GF180 project:

```bash
.venv/bin/python -m pytest tests/test_schematic.py tests/test_spice_simulation.py -q
```

The wheel includes the annotation module, six family wrappers, shared settings,
and original vendor library, so their paths also work from an installed PDK.
