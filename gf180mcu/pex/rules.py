"""Default gfpex parasitic-extraction rules for GF180MCU (gf180mcuD).

Usage::

    from gf180mcu.pex.rules import DEFAULT_PEX_RULES_CONFIG

Every value is carried over unchanged from gf-pex ``gfpexconfg/gf180mcuD.py`` (from KPEX);
``gf180mcuD.py:<line>`` in a tag refers to that file. A tag on a block comment applies to every number in the
block; a number with its own trailing tag overrides it.

Provenance tags:
    FOUNDRY <source>   value stated by a GF180MCU PDK document (gf180mcu-pdk.readthedocs.io)
    DERIVED <formula>  computed from other values (C = 8.854·k/t aF/µm², stacked thicknesses, ...)
    ASSUMED <source>   taken from KPEX / Magic's gf180mcuD tech data, no foundry page cited for it
    PALACE-FIT         fitted with gf-pex benchmarks/palace_benchmark.py (pending: TODO(palace))

Units (gfpex techfile): µm; sheet resistance mΩ/sq; contact/via resistance mΩ/cut; area, overlap and substrate
capacitance aF/µm²; perimeter and side-overlap aF/µm; sidewall in Magic form, `capacitance` aF/µm at a
1 µm reference spacing, C = capacitance·L/(s + offset) (a parallel plate gives 8.854·k·t with offset 0).
"""

#
# This creates a technology definition example for gf180mcu:
# https://gf180mcu-pdk.readthedocs.io/en/latest/analog/layout/inter_specs/inter_specs_3_43.html
# https://gf180mcu-pdk.readthedocs.io/en/latest/physical_verification/design_manual/drm_04_1.html
# https://gf180mcu-pdk.readthedocs.io/en/latest/analog/layout/inter_specs/inter_specs_2.html
#

from __future__ import annotations

from gfpex.gfpex import (
    CapacitanceInfo,
    ComputedLayerInfo,
    ComputedLayerKind,
    ConformalDielectricLayer,
    Contact,
    ContactResistance,
    DiffusionLayer,
    FieldOxideLayer,
    GDSPair,
    LayerInfo,
    LayerPurpose,
    LayerResistance,
    MetalLayer,
    NWellLayer,
    OverlapCapacitance,
    ProcessParasiticsInfo,
    ProcessStackInfo,
    ResistanceInfo,
    SideOverlapCapacitance,
    SidewallCapacitance,
    SimpleDielectricLayer,
    StackLayerInfo,
    StackLayerType,
    SubstrateCapacitance,
    SubstrateLayer,
    Techfile,
    ViaResistance,
)

__all__ = ["DEFAULT_PEX_RULES_CONFIG"]

DNWELL = LayerPurpose.PURPOSE_DNWELL
NWELL = LayerPurpose.PURPOSE_NWELL
DIFF = LayerPurpose.PURPOSE_DIFF
N_P_TAP = LayerPurpose.PURPOSE_NTAP_OR_PTAP
NTAP = LayerPurpose.PURPOSE_NTAP
PTAP = LayerPurpose.PURPOSE_PTAP
PIMP = LayerPurpose.PURPOSE_P_IMPLANT
NIMP = LayerPurpose.PURPOSE_N_IMPLANT
CONT = LayerPurpose.PURPOSE_CONTACT
METAL = LayerPurpose.PURPOSE_METAL
VIA = LayerPurpose.PURPOSE_VIA
MIM = LayerPurpose.PURPOSE_MIM_CAP

KREG = ComputedLayerKind.KIND_REGULAR
KCAP = ComputedLayerKind.KIND_DEVICE_CAPACITOR
KPIN = ComputedLayerKind.KIND_PIN
KLBL = ComputedLayerKind.KIND_LABEL

# TODO: Replace the current tech.layers, tech.lvs_computed_layers and tech.process_layer_stack with existing API on gdsfactory


def _build_layers(tech: Techfile) -> None:
    # FOUNDRY drm_04_1 GDS pairs (gf180mcuD.py:82-227), checked against gf180mcu.layers.LAYER in the tests
    # https://gf180mcu-pdk.readthedocs.io/en/latest/physical_verification/design_manual/drm_04_1.html
    tech.layers.append(
        LayerInfo(
            purpose=DNWELL,
            name="DNWELL",
            drw_gds_pair=GDSPair(layer=12, datatype=0),
            description="Deep N-well",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=NWELL,
            name="Nwell",
            drw_gds_pair=GDSPair(layer=21, datatype=0),
            description="N-well region",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=DIFF,
            name="COMP",
            drw_gds_pair=GDSPair(layer=22, datatype=0),
            label_gds_pair=GDSPair(layer=22, datatype=10),
            description="Diffusion for device and interconnect",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=PIMP,
            name="Pplus",
            drw_gds_pair=GDSPair(layer=31, datatype=0),
            description="P+ source/drain implant",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=NIMP,
            name="Nplus",
            drw_gds_pair=GDSPair(layer=32, datatype=0),
            description="N+ source/drain implant",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=METAL,
            name="Poly2",
            drw_gds_pair=GDSPair(layer=30, datatype=0),
            label_gds_pair=GDSPair(layer=30, datatype=10),
            description="Polysilicon gate & interconnect",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=CONT,
            name="Contact",
            drw_gds_pair=GDSPair(layer=33, datatype=0),
            description="Contact to local interconnect",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=METAL,
            name="Metal1",
            drw_gds_pair=GDSPair(layer=34, datatype=0),
            label_gds_pair=GDSPair(layer=34, datatype=10),
            description="Metal 1 interconnect",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=VIA,
            name="Via1",
            drw_gds_pair=GDSPair(layer=35, datatype=0),
            description="Contact from Metal1 to Metal2",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=METAL,
            name="Metal2",
            drw_gds_pair=GDSPair(layer=36, datatype=0),
            label_gds_pair=GDSPair(layer=36, datatype=10),
            description="Metal 2 interconnect",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=VIA,
            name="Via2",
            drw_gds_pair=GDSPair(layer=38, datatype=0),
            description="Contact from Metal2 to Metal3",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=METAL,
            name="Metal3",
            drw_gds_pair=GDSPair(layer=42, datatype=0),
            label_gds_pair=GDSPair(layer=42, datatype=10),
            description="Metal 3 interconnect",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=VIA,
            name="Via3",
            drw_gds_pair=GDSPair(layer=40, datatype=0),
            description="Contact from Metal3 to Metal4",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=METAL,
            name="Metal4",
            drw_gds_pair=GDSPair(layer=46, datatype=0),
            label_gds_pair=GDSPair(layer=46, datatype=10),
            description="Metal 4 interconnect",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=VIA,
            name="Via4",
            drw_gds_pair=GDSPair(layer=41, datatype=0),
            description="Contact from Metal4 to Metal5",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=MIM,
            name="FuseTop",
            drw_gds_pair=GDSPair(layer=75, datatype=0),
            description="MiM capacitor plate over Metal5",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=METAL,
            name="Metal5",
            drw_gds_pair=GDSPair(layer=81, datatype=0),
            label_gds_pair=GDSPair(layer=81, datatype=10),
            description="Metal 5 interconnect",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=VIA,
            name="Via5",
            drw_gds_pair=GDSPair(layer=82, datatype=0),
            description="Contact from Metal5 to MetalTop",
        )
    )
    tech.layers.append(
        LayerInfo(
            purpose=METAL,
            name="MetalTop",
            drw_gds_pair=GDSPair(layer=53, datatype=0),
            label_gds_pair=GDSPair(layer=53, datatype=10),
            description="Top metal interconnect",
        )
    )


def _build_lvs_computed_layers(tech: Techfile) -> None:
    # ASSUMED KPEX computed-layer GDS pairs, internal to the extractor, not drawn layers (gf180mcuD.py:230-543)
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=DNWELL,
                name="dnwell",
                description="Deep NWell",
                drw_gds_pair=GDSPair(layer=12, datatype=0),
            ),
            original_layer_name="DNWELL",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=NWELL,
                name="Nwell",
                description="NWell",
                drw_gds_pair=GDSPair(layer=21, datatype=0),
            ),
            original_layer_name="Nwell",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=NIMP,
                name="nsd",
                description="borrow from nsdm",
                drw_gds_pair=GDSPair(layer=32, datatype=44),
            ),
            original_layer_name="Nplus",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=PIMP,
                name="psd",
                description="borrow from psdm",
                drw_gds_pair=GDSPair(layer=31, datatype=20),
            ),
            original_layer_name="Pplus",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=NTAP,
                name="ntap_conn",
                description="Separate ntap, original tap is 65,44, we need seperate ntap/ptap",  # codespell:ignore
                drw_gds_pair=GDSPair(layer=65, datatype=144),
            ),
            original_layer_name="tap",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=PTAP,
                name="ptap_conn",
                description="Separate ptap, original tap is 65,44, we need seperate ntap/ptap",  # codespell:ignore
                drw_gds_pair=GDSPair(layer=65, datatype=244),
            ),
            original_layer_name="tap",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=METAL,
                name="poly_con",
                description="Computed layer for poly",
                drw_gds_pair=GDSPair(layer=30, datatype=0),
            ),
            original_layer_name="Poly2",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=METAL,
                name="metal1_con",
                description="Computed layer for met1",
                drw_gds_pair=GDSPair(layer=34, datatype=0),
            ),
            original_layer_name="Metal1",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=METAL,
                name="metal2_con",
                description="Computed layer for met2",
                drw_gds_pair=GDSPair(layer=36, datatype=0),
            ),
            original_layer_name="Metal2",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=METAL,
                name="metal3_con",
                description="Computed layer for met3 (no cap)",
                drw_gds_pair=GDSPair(layer=42, datatype=0),
            ),
            original_layer_name="Metal3",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=METAL,
                name="metal4_con",
                description="Computed layer for met4 (no cap)",
                drw_gds_pair=GDSPair(layer=46, datatype=0),
            ),
            original_layer_name="Metal4",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=METAL,
                name="metal5_con",
                description="Computed layer for met5",
                drw_gds_pair=GDSPair(layer=81, datatype=0),
            ),
            original_layer_name="Metal5",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=METAL,
                name="metaltop_con",
                description="Computed layer for metaltop",
                drw_gds_pair=GDSPair(layer=53, datatype=0),
            ),
            original_layer_name="MetalTop",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=CONT,
                name="m1_nsd_con",
                description="Computed layer for contact from nsdm to Metal1",
                drw_gds_pair=GDSPair(layer=66, datatype=4401),
            ),
            original_layer_name="Contact",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=CONT,
                name="m1_psd_con",
                description="Computed layer for contact from psdm to Metal1",
                drw_gds_pair=GDSPair(layer=66, datatype=4402),
            ),
            original_layer_name="Contact",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=CONT,
                name="m1_poly_con",
                description="Computed layer for contact from poly to Metal1",
                drw_gds_pair=GDSPair(layer=66, datatype=4403),
            ),
            original_layer_name="Contact",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=VIA,
                name="via3_n_cap",
                description="Computed layer for via3 (no MIM cap)",
                drw_gds_pair=GDSPair(layer=40, datatype=144),
            ),
            original_layer_name="Via3",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=VIA,
                name="via4_n_cap",
                description="Computed layer for via4 (no MIM cap)",
                drw_gds_pair=GDSPair(layer=41, datatype=144),
            ),
            original_layer_name="Via4",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KREG,
            layer_info=LayerInfo(
                purpose=VIA,
                name="via5_con",
                description="Computed layer for via5",
                drw_gds_pair=GDSPair(layer=82, datatype=0),
            ),
            original_layer_name="Via5",
        )
    )

    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KLBL,
            layer_info=LayerInfo(
                purpose=METAL,
                name="comp_label",
                description="LABEL drawn at diffusion layer",
                drw_gds_pair=GDSPair(layer=30, datatype=10),
            ),
            original_layer_name="COMP_label",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KLBL,
            layer_info=LayerInfo(
                purpose=METAL,
                name="Poly2_Label",
                description="LABEL drawn at poly2 layer",
                drw_gds_pair=GDSPair(layer=30, datatype=10),
            ),
            original_layer_name="Poly2_label",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KLBL,
            layer_info=LayerInfo(
                purpose=METAL,
                name="metal1_Label",
                description="LABEL drawn at Metal1 layer",
                drw_gds_pair=GDSPair(layer=34, datatype=10),
            ),
            original_layer_name="Metal1_label",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KLBL,
            layer_info=LayerInfo(
                purpose=METAL,
                name="metal2_Label",
                description="LABEL drawn at Metal2 layer",
                drw_gds_pair=GDSPair(layer=36, datatype=10),
            ),
            original_layer_name="Metal2_label",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KLBL,
            layer_info=LayerInfo(
                purpose=METAL,
                name="metal3_Label",
                description="LABEL drawn at Metal3 layer",
                drw_gds_pair=GDSPair(layer=42, datatype=10),
            ),
            original_layer_name="Metal3_label",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KLBL,
            layer_info=LayerInfo(
                purpose=METAL,
                name="metal4_Label",
                description="LABEL drawn at Metal4 layer",
                drw_gds_pair=GDSPair(layer=46, datatype=10),
            ),
            original_layer_name="Metal4_label",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KLBL,
            layer_info=LayerInfo(
                purpose=METAL,
                name="metal5_Label",
                description="LABEL drawn at Metal5 layer",
                drw_gds_pair=GDSPair(layer=81, datatype=10),
            ),
            original_layer_name="Metal5_label",
        )
    )
    tech.lvs_computed_layers.append(
        ComputedLayerInfo(
            kind=KLBL,
            layer_info=LayerInfo(
                purpose=METAL,
                name="metaltop_Label",
                description="LABEL drawn at MetalTop layer",
                drw_gds_pair=GDSPair(layer=53, datatype=10),
            ),
            original_layer_name="MetalTop_label",
        )
    )


def _build_process_stack(tech: Techfile) -> None:
    # https://gf180mcu-pdk.readthedocs.io/en/latest/_images/2_cross_section_43.png
    # FOUNDRY z and thickness from the cross-section above; ASSUMED KPEX dielectric k and contact geometry
    # (gf180mcuD.py:546-823)
    tech.process_stack = ProcessStackInfo()
    psi = tech.process_stack

    # SUBSTRATE
    psi.layers.append(
        StackLayerInfo(
            name="subs",
            layer_type=StackLayerType.LAYER_TYPE_SUBSTRATE,
            substrate_layer=SubstrateLayer(height=0.0, thickness=0.33, reference="fox"),
        )
    )

    # NWELL / DIFF
    psi.layers.append(
        StackLayerInfo(
            name="Nwell",
            layer_type=StackLayerType.LAYER_TYPE_NWELL,
            nwell_layer=NWellLayer(z=0.0, reference="fox"),
        )
    )
    psi.layers.append(
        StackLayerInfo(
            name="Nplus",
            layer_type=StackLayerType.LAYER_TYPE_DIFFUSION,
            diffusion_layer=DiffusionLayer(
                z=0.312,
                reference="fox",
                contact_above=Contact(
                    name="M1-Nplus",
                    layer_below="Nplus",
                    metal_above="Metal1",
                    thickness=0.9361,
                    width=0.22,
                    spacing=0.17,
                    border=0.0,
                ),
            ),
        )
    )
    psi.layers.append(
        StackLayerInfo(
            name="Pplus",
            layer_type=StackLayerType.LAYER_TYPE_DIFFUSION,
            diffusion_layer=DiffusionLayer(
                z=0.312,
                reference="fox",
                contact_above=Contact(
                    name="M1-Pplus",
                    layer_below="Pplus",
                    metal_above="Metal1",
                    thickness=0.9361,
                    width=0.22,
                    spacing=0.17,
                    border=0.0,
                ),
            ),
        )
    )

    # FOX
    psi.layers.append(
        StackLayerInfo(
            name="fox",
            layer_type=StackLayerType.LAYER_TYPE_FIELD_OXIDE,
            field_oxide_layer=FieldOxideLayer(dielectric_k=4.0),
        )
    )

    # POLY2
    psi.layers.append(
        StackLayerInfo(
            name="Poly2",
            layer_type=StackLayerType.LAYER_TYPE_METAL,
            metal_layer=MetalLayer(
                z=0.32,
                thickness=0.2,
                contact_above=Contact(
                    name="M1-Poly",
                    layer_below="Poly2",
                    metal_above="Metal1",
                    thickness=0.4299,
                    width=0.22,
                    spacing=0.17,
                    border=0.0,
                ),
            ),
        )
    )
    psi.layers.append(
        StackLayerInfo(
            name="nit",
            layer_type=StackLayerType.LAYER_TYPE_CONFORMAL_DIELECTRIC,
            conformal_dielectric_layer=ConformalDielectricLayer(
                dielectric_k=7.0,
                thickness_over_metal=0.05,
                thickness_where_no_metal=0.05,
                thickness_sidewall=0.05,
                reference="Poly2",
            ),
        )
    )
    psi.layers.append(
        StackLayerInfo(
            name="ild",
            layer_type=StackLayerType.LAYER_TYPE_SIMPLE_DIELECTRIC,
            simple_dielectric_layer=SimpleDielectricLayer(
                dielectric_k=4.0, reference="nit"
            ),
        )
    )

    # METAL1
    psi.layers.append(
        StackLayerInfo(
            name="Metal1",
            layer_type=StackLayerType.LAYER_TYPE_METAL,
            metal_layer=MetalLayer(
                z=1.23,
                thickness=0.55,
                contact_above=Contact(
                    name="Via1_con",
                    layer_below="Metal1",
                    metal_above="Metal2",
                    thickness=1.3761 - (0.9361 + 0.1),  # DERIVED as in gf180mcuD.py:667
                    width=0.26,
                    spacing=0.19,
                    border=0.0,
                ),
            ),
        )
    )
    psi.layers.append(
        StackLayerInfo(
            name="imd1",
            layer_type=StackLayerType.LAYER_TYPE_SIMPLE_DIELECTRIC,
            simple_dielectric_layer=SimpleDielectricLayer(
                dielectric_k=4.0, reference="ild"
            ),
        )
    )

    # METAL2
    psi.layers.append(
        StackLayerInfo(
            name="Metal2",
            layer_type=StackLayerType.LAYER_TYPE_METAL,
            metal_layer=MetalLayer(
                z=2.38,
                thickness=0.55,
                contact_above=Contact(
                    name="Via2_con",
                    layer_below="Metal2",
                    metal_above="Metal3",
                    thickness=0.27,
                    width=0.26,
                    spacing=0.17,
                    border=0.055,
                ),
            ),
        )
    )
    psi.layers.append(
        StackLayerInfo(
            name="imd2",
            layer_type=StackLayerType.LAYER_TYPE_SIMPLE_DIELECTRIC,
            simple_dielectric_layer=SimpleDielectricLayer(
                dielectric_k=4.0, reference="imd1"
            ),
        )
    )

    # METAL3
    psi.layers.append(
        StackLayerInfo(
            name="Metal3",
            layer_type=StackLayerType.LAYER_TYPE_METAL,
            metal_layer=MetalLayer(
                z=3.53,
                thickness=0.55,
                contact_above=Contact(
                    name="Via3_con",
                    layer_below="Metal3",
                    metal_above="Metal4",
                    thickness=0.42,
                    width=0.26,
                    spacing=0.20,
                    border=0.04,
                ),
            ),
        )
    )
    psi.layers.append(
        StackLayerInfo(
            name="imd3",
            layer_type=StackLayerType.LAYER_TYPE_SIMPLE_DIELECTRIC,
            simple_dielectric_layer=SimpleDielectricLayer(
                dielectric_k=4.0, reference="imd2"
            ),
        )
    )

    # METAL4
    psi.layers.append(
        StackLayerInfo(
            name="Metal4",
            layer_type=StackLayerType.LAYER_TYPE_METAL,
            metal_layer=MetalLayer(
                z=4.68,
                thickness=0.55,
                contact_above=Contact(
                    name="Via4_ncap",
                    layer_below="Metal4",
                    metal_above="Metal5",
                    thickness=0.505,
                    width=0.26,
                    spacing=0.80,
                    border=0.19,
                ),
            ),
        )
    )
    psi.layers.append(
        StackLayerInfo(
            name="imd4",
            layer_type=StackLayerType.LAYER_TYPE_SIMPLE_DIELECTRIC,
            simple_dielectric_layer=SimpleDielectricLayer(
                dielectric_k=4.0, reference="imd3"
            ),
        )
    )

    # METAL5
    psi.layers.append(
        StackLayerInfo(
            name="Metal5",
            layer_type=StackLayerType.LAYER_TYPE_METAL,
            metal_layer=MetalLayer(
                z=6.13,
                thickness=0.55,
                contact_above=Contact(
                    name="via5_con",
                    layer_below="Metal5",
                    metal_above="MetalTop",
                    thickness=0.505,
                    width=0.26,
                    spacing=0.36,
                    border=0.06,
                ),
            ),
        )
    )
    psi.layers.append(
        StackLayerInfo(
            name="imd5",
            layer_type=StackLayerType.LAYER_TYPE_SIMPLE_DIELECTRIC,
            simple_dielectric_layer=SimpleDielectricLayer(
                dielectric_k=4.0, reference="imd4"
            ),
        )
    )

    # METALTOP
    psi.layers.append(
        StackLayerInfo(
            name="MetalTop",
            layer_type=StackLayerType.LAYER_TYPE_METAL,
            # DERIVED z = Metal5 z + Metal5 thickness + via5 thickness (gf180mcuD.py:800)
            metal_layer=MetalLayer(z=6.13 + 0.55 + 0.505, thickness=1.1925),
        )
    )
    psi.layers.append(
        StackLayerInfo(
            name="pass",
            layer_type=StackLayerType.LAYER_TYPE_SIMPLE_DIELECTRIC,
            simple_dielectric_layer=SimpleDielectricLayer(
                dielectric_k=4.0, reference="imd5"
            ),
        )
    )
    psi.layers.append(
        StackLayerInfo(
            name="sin",
            layer_type=StackLayerType.LAYER_TYPE_SIMPLE_DIELECTRIC,
            simple_dielectric_layer=SimpleDielectricLayer(
                dielectric_k=8.5225, reference="pass"
            ),
        )
    )
    psi.layers.append(
        StackLayerInfo(
            name="air",
            layer_type=StackLayerType.LAYER_TYPE_SIMPLE_DIELECTRIC,
            simple_dielectric_layer=SimpleDielectricLayer(
                dielectric_k=8.5225, reference="sin"
            ),
        )
    )


def _build_parasitics(tech: Techfile) -> None:
    # https://gf180mcu-pdk.readthedocs.io/en/latest/analog/layout/inter_specs/inter_specs_2_1.html
    # https://gf180mcu-pdk.readthedocs.io/en/latest/analog/spice/elec_specs/elec_specs_5_1.html
    tech.process_parasitics = ProcessParasiticsInfo(
        side_halo=8.0,  # ASSUMED KPEX gf180mcuD.py:830
        resistance=ResistanceInfo(),
        capacitance=CapacitanceInfo(),
    )
    ex = tech.process_parasitics
    ri = ex.resistance
    ci = ex.capacitance

    # sheet resistance (mΩ/sq)
    # https://gf180mcu-pdk.readthedocs.io/en/latest/analog/spice/elec_specs/elec_specs_5_1.html
    # FOUNDRY elec_specs_5_1 (gf180mcuD.py:838-844)
    ri.layers.append(LayerResistance(layer_name="Poly2", resistance=7300))
    ri.layers.append(LayerResistance(layer_name="Metal1", resistance=90))
    ri.layers.append(LayerResistance(layer_name="Metal2", resistance=90))
    ri.layers.append(LayerResistance(layer_name="Metal3", resistance=90))
    ri.layers.append(LayerResistance(layer_name="Metal4", resistance=90))
    ri.layers.append(LayerResistance(layer_name="Metal5", resistance=90))
    ri.layers.append(LayerResistance(layer_name="MetalTop", resistance=40))

    # contact resistance (mΩ/CNT)
    # https://gf180mcu-pdk.readthedocs.io/en/latest/analog/spice/elec_specs/elec_specs_5_2.html
    # FOUNDRY elec_specs_5_2 (gf180mcuD.py:848-856)
    ri.contacts.append(
        ContactResistance(
            contact_name="M1-Nplus",
            device_layer_name="Nplus",
            layer_above="Metal1",
            resistance=6300,
        )
    )
    ri.contacts.append(
        ContactResistance(
            contact_name="M1-Pplus",
            device_layer_name="Pplus",
            layer_above="Metal1",
            resistance=5200,
        )
    )
    ri.contacts.append(
        ContactResistance(
            contact_name="M1-Poly",
            device_layer_name="Poly2",
            layer_above="Metal1",
            resistance=5900,
        )
    )

    # via resistance (mΩ/CNT)
    # ASSUMED KPEX gf180mcuD.py:859-864
    ri.vias.append(ViaResistance(via_name="M1-Poly", resistance=5900))
    ri.vias.append(ViaResistance(via_name="Via1", resistance=4500))
    ri.vias.append(ViaResistance(via_name="Via2", resistance=4500))
    ri.vias.append(ViaResistance(via_name="Via3", resistance=4500))
    ri.vias.append(ViaResistance(via_name="Via4", resistance=4500))
    ri.vias.append(ViaResistance(via_name="Via5", resistance=4500))

    # substrate capacitance, Magic's defaultareacap / defaultperimeter:
    # - area (aF/µm²): per µm² of the layer over the substrate, with no conductor in between (the plate term)
    # - perimeter (aF/µm): per µm of edge, the whole fringe of an isolated edge: no same-layer neighbour and no
    #   intervening conductor within side_halo (8 µm) of it. Magic keeps (2/π)·atan(0.02·area·s) of it when the
    #   nearest neighbour is at a spacing s
    # ASSUMED KPEX/Magic gf180mcuD.py:871-877; perimeter: TODO(palace)
    ci.substrates.append(
        SubstrateCapacitance(
            layer_name="Poly2", area_capacitance=110.67, perimeter_capacitance=50.72
        )
    )
    ci.substrates.append(
        SubstrateCapacitance(
            layer_name="Metal1", area_capacitance=29.304, perimeter_capacitance=39.431
        )
    )
    ci.substrates.append(
        SubstrateCapacitance(
            layer_name="Metal2", area_capacitance=15.016, perimeter_capacitance=33.298
        )
    )
    ci.substrates.append(
        SubstrateCapacitance(
            layer_name="Metal3", area_capacitance=10.094, perimeter_capacitance=30.021
        )
    )
    ci.substrates.append(
        SubstrateCapacitance(
            layer_name="Metal4", area_capacitance=7.602, perimeter_capacitance=28.153
        )
    )
    ci.substrates.append(
        SubstrateCapacitance(
            layer_name="Metal5", area_capacitance=5.798, perimeter_capacitance=30.386
        )
    )
    ci.substrates.append(
        SubstrateCapacitance(
            layer_name="MetalTop", area_capacitance=6.32, perimeter_capacitance=38.85
        )
    )

    diff_nonfet = "COMP"
    poly_nonres = "Poly2"
    all_active = "COMP"

    # overlap capacitance (aF/µm²), Magic's defaultoverlap: per µm² where the top layer covers the bottom one with no
    # conductor in between; no lateral reference distance (the vertical gap is in the value)
    # ASSUMED KPEX/Magic gf180mcuD.py:885-916
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Poly2", bottom_layer_name="Nwell", capacitance=110.67
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Poly2", bottom_layer_name="LVPWELL", capacitance=110.67
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal1", bottom_layer_name="LVPWELL", capacitance=29.304
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal1", bottom_layer_name="Nwell", capacitance=29.304
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal1", bottom_layer_name=diff_nonfet, capacitance=30.502
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal1", bottom_layer_name="Poly2", capacitance=51.434
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal2", bottom_layer_name="LVPWELL", capacitance=15.016
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal2", bottom_layer_name="Nwell", capacitance=15.016
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal2", bottom_layer_name=diff_nonfet, capacitance=17.305
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal2", bottom_layer_name=poly_nonres, capacitance=19.263
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal2", bottom_layer_name="Metal1", capacitance=59.027
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal3", bottom_layer_name="Nwell", capacitance=10.094
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal3", bottom_layer_name="LVPWELL", capacitance=10.094
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal3", bottom_layer_name=diff_nonfet, capacitance=11.079
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal3", bottom_layer_name=poly_nonres, capacitance=11.85
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal3", bottom_layer_name="Metal1", capacitance=20.238
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal3", bottom_layer_name="Metal2", capacitance=59.027
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal4", bottom_layer_name="Nwell", capacitance=7.602
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal4", bottom_layer_name="LVPWELL", capacitance=7.602
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal4", bottom_layer_name=all_active, capacitance=8.148
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal4", bottom_layer_name=poly_nonres, capacitance=8.557
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal4", bottom_layer_name="Metal1", capacitance=12.212
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal4", bottom_layer_name="Metal2", capacitance=20.238
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal4", bottom_layer_name="Metal3", capacitance=59.027
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal5", bottom_layer_name="Nwell", capacitance=5.798
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal5", bottom_layer_name="LVPWELL", capacitance=5.798
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal5", bottom_layer_name=all_active, capacitance=6.11
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal5", bottom_layer_name=poly_nonres, capacitance=6.337
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal5", bottom_layer_name="Metal1", capacitance=8.142
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal5", bottom_layer_name="Metal2", capacitance=11.067
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal5", bottom_layer_name="Metal3", capacitance=17.276
        )
    )
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="Metal5", bottom_layer_name="Metal4", capacitance=39.351
        )
    )
    # estimate: parallel plate eps0 * 4.0 / 0.4um, no foundry MetalTop/Metal5 value available
    # DERIVED 8.854·4.0/0.4 (gf180mcuD.py:918)
    ci.overlaps.append(
        OverlapCapacitance(
            top_layer_name="MetalTop", bottom_layer_name="Metal5", capacitance=88.5
        )
    )

    # sidewall capacitance, Magic's defaultsidewall: C = capacitance · L · 1 µm / (s + offset) for facing edges of
    # length L at a spacing s, searched within side_halo (8 µm). `capacitance` (aF/µm) is the coupling per µm of
    # edge at the reference spacing s + offset = 1 µm (s = 1 µm - offset); `offset` (µm) bends the 1/s law near
    # the minimum spacing
    # ASSUMED KPEX/Magic gf180mcuD.py:924-929; TODO(palace)
    ci.sidewalls.append(
        SidewallCapacitance(layer_name="Poly2", capacitance=11.098, offset=-0.082)
    )
    ci.sidewalls.append(
        SidewallCapacitance(layer_name="Metal1", capacitance=40.512, offset=-0.053)
    )
    ci.sidewalls.append(
        SidewallCapacitance(layer_name="Metal2", capacitance=46.736, offset=0.289)
    )
    ci.sidewalls.append(
        SidewallCapacitance(layer_name="Metal3", capacitance=70.675, offset=0.534)
    )
    ci.sidewalls.append(
        SidewallCapacitance(layer_name="Metal4", capacitance=77.388, offset=0.611)
    )
    ci.sidewalls.append(
        SidewallCapacitance(layer_name="Metal5", capacitance=114.86, offset=0.025)
    )

    # sidewall-overlap capacitance (aF/µm), Magic's defaultsideoverlap: per µm of an in-layer edge, the whole fringe
    # to the out layer when that layer spans the full side_halo (8 µm) beside the edge, unshielded. A strip of it
    # from d_near to d_far keeps (2/π)·(atan(k·d_far) - atan(k·d_near)), with k = 0.02 · the pair's overlap
    # capacitance (per µm)
    # ASSUMED KPEX/Magic gf180mcuD.py:935-981; TODO(palace)
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Poly2", out_layer_name="Nwell", capacitance=50.72
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Poly2", out_layer_name="LVPWELL", capacitance=50.72
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal1", out_layer_name="Nwell", capacitance=39.431
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal1", out_layer_name="LVPWELL", capacitance=39.431
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal1", out_layer_name=diff_nonfet, capacitance=43.406
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal1", out_layer_name=poly_nonres, capacitance=46.700
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Poly2", out_layer_name="Metal1", capacitance=17.946
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal2", out_layer_name="Nwell", capacitance=33.298
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal2", out_layer_name="LVPWELL", capacitance=33.298
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal2", out_layer_name=diff_nonfet, capacitance=35.189
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal2", out_layer_name=poly_nonres, capacitance=36.169
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Poly2", out_layer_name="Metal2", capacitance=8.706
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal2", out_layer_name="Metal1", capacitance=47.566
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal1", out_layer_name="Metal2", capacitance=32.048
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal3", out_layer_name="Nwell", capacitance=30.021
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal3", out_layer_name="LVPWELL", capacitance=30.021
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal3", out_layer_name=diff_nonfet, capacitance=31.40
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal3", out_layer_name=poly_nonres, capacitance=31.927
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Poly2", out_layer_name="Metal3", capacitance=5.895
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal3", out_layer_name="Metal1", capacitance=36.609
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal1", out_layer_name="Metal3", capacitance=18.135
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal3", out_layer_name="Metal2", capacitance=49.011
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal2", out_layer_name="Metal3", capacitance=36.626
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal4", out_layer_name="Nwell", capacitance=28.153
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal4", out_layer_name="LVPWELL", capacitance=40.99
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal4", out_layer_name=diff_nonfet, capacitance=29.065
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal4", out_layer_name=poly_nonres, capacitance=29.407
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Poly2", out_layer_name="Metal4", capacitance=8.557
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal4", out_layer_name="Metal1", capacitance=32.104
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal1", out_layer_name="Metal4", capacitance=13.159
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal4", out_layer_name="Metal2", capacitance=36.563
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal2", out_layer_name="Metal4", capacitance=22.405
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal4", out_layer_name="Metal3", capacitance=47.871
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal3", out_layer_name="Metal4", capacitance=39.964
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal5", out_layer_name="Nwell", capacitance=30.386
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal5", out_layer_name="LVPWELL", capacitance=30.386
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal5", out_layer_name=diff_nonfet, capacitance=31.165
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal5", out_layer_name=poly_nonres, capacitance=31.458
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Poly2", out_layer_name="Metal5", capacitance=3.365
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal5", out_layer_name="Metal1", capacitance=33.316
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal1", out_layer_name="Metal5", capacitance=9.825
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal5", out_layer_name="Metal2", capacitance=36.591
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal2", out_layer_name="Metal5", capacitance=15.764
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal5", out_layer_name="Metal3", capacitance=41.466
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal3", out_layer_name="Metal5", capacitance=22.988
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal5", out_layer_name="Metal4", capacitance=52.692
        )
    )
    ci.sideoverlaps.append(
        SideOverlapCapacitance(
            in_layer_name="Metal4", out_layer_name="Metal5", capacitance=34.954
        )
    )


def _build() -> Techfile:
    tech = Techfile(name="gf180mcuD")
    _build_layers(tech)
    _build_lvs_computed_layers(tech)
    _build_process_stack(tech)
    _build_parasitics(tech)
    return tech


DEFAULT_PEX_RULES_CONFIG = _build()
