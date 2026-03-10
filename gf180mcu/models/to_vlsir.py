"""
GDSF -> VLSIR Conversion Utilities (Minimal MVP)

Converts a single GDSFactory Component with vlsir metadata to VLSIR protobuf format.

Required vlsir info structure:
    c.info["vlsir"] = {
        "model": "nmos",           # Required: SPICE model name
        "spice_type": "MOS",       # Required: SpiceType (MOS, RESISTOR, etc.)
        "port_order": ["D", "G", "S", "B"],  # Required: Port names in SPICE order
        "params": {"w": 1e-6, "l": 100e-9},  # Optional: Device parameters
        "port_map": {"D": "d", "G": "g"},    # Optional: Component port -> VLSIR port mapping
    }

If port_map is provided, validation checks that component ports in the map exist.
If port_map is not provided, port_order names must match component port names exactly.

Usage:
    import gdsfactory as gf
    from to_vlsir import to_proto, to_spice

    @gf.cell
    def my_resistor():
        c = gf.Component()
        c.add_port(name="p", center=(0, 0), width=0.1, orientation=180, layer=(250, 0))
        c.add_port(name="n", center=(1, 0), width=0.1, orientation=0, layer=(250, 0))
        c.info["vlsir"] = {
            "model": "rpoly",
            "spice_type": "RESISTOR",
            "port_order": ["p", "n"],
            "params": {"r": 1000},
        }
        return c

    pkg = to_proto(my_resistor())
    spice_str = to_spice(my_resistor())
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import vlsir
import vlsir.circuit_pb2 as vckt

if TYPE_CHECKING:
    from gdsfactory.component import Component


# Required fields in vlsir metadata
REQUIRED_VLSIR_FIELDS = ("model", "spice_type", "port_order")

# Mapping from string names to proto enum values
_SPICE_TYPE_MAP: dict[str, int] = {
    "SUBCKT": vckt.SpiceType.SUBCKT,
    "RESISTOR": vckt.SpiceType.RESISTOR,
    "CAPACITOR": vckt.SpiceType.CAPACITOR,
    "INDUCTOR": vckt.SpiceType.INDUCTOR,
    "MOS": vckt.SpiceType.MOS,
    "DIODE": vckt.SpiceType.DIODE,
    "BIPOLAR": vckt.SpiceType.BIPOLAR,
    "VSOURCE": vckt.SpiceType.VSOURCE,
    "ISOURCE": vckt.SpiceType.ISOURCE,
    "VCVS": vckt.SpiceType.VCVS,
    "VCCS": vckt.SpiceType.VCCS,
    "CCCS": vckt.SpiceType.CCCS,
    "CCVS": vckt.SpiceType.CCVS,
    "TLINE": vckt.SpiceType.TLINE,
}


def validate_vlsir_metadata(component: Component) -> dict[str, Any]:
    """
    Validate that component has proper vlsir metadata.

    Args:
        component: GDSFactory Component to validate

    Returns:
        The vlsir metadata dict

    Raises:
        ValueError: If vlsir metadata is missing or incomplete
    """
    if "vlsir" not in component.info:
        raise ValueError(
            f"Component '{component.name}' missing required 'vlsir' metadata in .info dict. "
            f"Expected: component.info['vlsir'] = {{'model': ..., 'spice_type': ..., "
            f"'port_order': [...]}}"
        )

    vlsir_info = component.info["vlsir"]

    missing = [f for f in REQUIRED_VLSIR_FIELDS if f not in vlsir_info]
    if missing:
        raise ValueError(
            f"Component '{component.name}' vlsir metadata missing required fields: {missing}. "
            f"Required fields: {REQUIRED_VLSIR_FIELDS}"
        )

    # Validate spice_type is recognized
    spice_type = vlsir_info["spice_type"]
    if isinstance(spice_type, str) and spice_type.upper() not in _SPICE_TYPE_MAP:
        raise ValueError(
            f"Component '{component.name}' has unknown spice_type '{spice_type}'. "
            f"Valid types: {list(_SPICE_TYPE_MAP.keys())}"
        )

    # Validate port_order is a non-empty list
    port_order = vlsir_info["port_order"]
    if not isinstance(port_order, list) or len(port_order) == 0:
        raise ValueError(
            f"Component '{component.name}' port_order must be a non-empty list, "
            f"got: {port_order}"
        )

    # Validate ports - either via port_map or direct port_order matching
    component_ports = {p.name for p in component.ports}
    port_map = vlsir_info.get("port_map")

    if port_map is not None:
        # Validate port_map: component ports in the map must exist
        if not isinstance(port_map, dict):
            raise ValueError(
                f"Component '{component.name}' port_map must be a dict, "
                f"got: {type(port_map).__name__}"
            )
        missing_ports = set(port_map.keys()) - component_ports
        if missing_ports:
            raise ValueError(
                f"Component '{component.name}' port_map contains component ports not found: "
                f"{sorted(missing_ports)}. Available ports: {sorted(component_ports)}"
            )
    else:
        # No port_map: port_order names must match component port names exactly
        port_order_set = set(port_order)
        missing_ports = port_order_set - component_ports
        if missing_ports:
            raise ValueError(
                f"Component '{component.name}' port_order contains ports not found on component: "
                f"{sorted(missing_ports)}. Available ports: {sorted(component_ports)}. "
                f"Consider adding a 'port_map' to map component ports to VLSIR ports."
            )

    return vlsir_info


def _spice_type_to_proto(spice_type: str | int) -> int:
    """Convert string or int spice_type to proto enum value."""
    if isinstance(spice_type, int):
        return spice_type
    return _SPICE_TYPE_MAP.get(spice_type.upper(), vckt.SpiceType.SUBCKT)


def to_proto(component: Component, domain: str = "") -> vckt.Package:
    """
    Convert a single GDSFactory Component to a VLSIR Package.

    The component MUST have valid vlsir metadata in component.info["vlsir"].

    Args:
        component: Component with vlsir metadata
        domain: Package domain name (e.g., "myproject")

    Returns:
        VLSIR Package containing a top-level module with the device instance

    Raises:
        ValueError: If component lacks valid vlsir metadata
    """
    vlsir_info = validate_vlsir_metadata(component)

    # Create package
    pkg = vckt.Package(domain=domain)

    # Build qualified name for the device model
    model_name = vlsir_info["model"]
    qname = vlsir.utils.QualifiedName(
        name=model_name,
        domain=domain,
    )

    # Create ExternalModule for the device
    spice_type = _spice_type_to_proto(vlsir_info["spice_type"])
    ext_mod = vckt.ExternalModule(name=qname, spicetype=spice_type)

    # Add ports from port_order
    port_order = vlsir_info["port_order"]
    for port_name in port_order:
        ext_mod.signals.append(vckt.Signal(name=port_name, width=1))
        port = vckt.Port(signal=port_name)
        port.direction = vckt.Port.Direction.INOUT
        ext_mod.ports.append(port)

    pkg.ext_modules.append(ext_mod)

    # Create a top-level module that instantiates the device
    top_module = vckt.Module()
    top_module.name = component.name or "top"

    # Add signals to the top module (these become the external ports)
    for port_name in port_order:
        top_module.signals.append(vckt.Signal(name=port_name, width=1))
        port = vckt.Port(signal=port_name)
        port.direction = vckt.Port.Direction.INOUT
        top_module.ports.append(port)

    # Create an instance of the device
    inst = vckt.Instance(name="X1")
    inst.module.external.CopyFrom(qname)

    # Connect the instance ports to the top-level signals
    for port_name in port_order:
        conn = vckt.Connection(
            portname=port_name, target=vckt.ConnectionTarget(sig=port_name)
        )
        inst.connections.append(conn)

    # Add parameters from the vlsir metadata
    params = vlsir_info.get("params", {})
    if isinstance(params, dict):
        for key, val in params.items():
            if val is not None:
                # Convert parameter value to VLSIR ParamValue
                param = vlsir.Param(name=key)
                if isinstance(val, bool):
                    param.value.literal = str(val).lower()
                elif isinstance(val, int):
                    param.value.int64_value = val
                elif isinstance(val, float):
                    param.value.double_value = val
                elif isinstance(val, str):
                    param.value.literal = val
                else:
                    param.value.literal = str(val)
                inst.parameters.append(param)

    top_module.instances.append(inst)
    pkg.modules.append(top_module)

    return pkg


def to_spice(component: Component, domain: str = "", fmt: str = "spice") -> str:
    """
    Convert a single GDSFactory Component to SPICE netlist string.

    Requires vlsirtools: pip install vlsirtools

    Args:
        component: Component with vlsir metadata
        domain: Package domain name
        fmt: Netlist format - "spectre", "spice", "ngspice", "xyce", "hspice"

    Returns:
        SPICE netlist as a string

    Raises:
        ImportError: If vlsirtools is not installed
        ValueError: If component lacks valid vlsir metadata
    """
    try:
        from io import StringIO

        import vlsirtools.netlist
    except ImportError:
        raise ImportError(
            "vlsirtools required for SPICE export. Install with: pip install vlsirtools"
        ) from None

    pkg = to_proto(component, domain=domain)
    buffer = StringIO()
    vlsirtools.netlist(pkg, dest=buffer, fmt=fmt.lower())
    return buffer.getvalue()


if __name__ == "__main__":
    import gdsfactory as gf

    SCHEM_LAYER = (250, 0)

    @gf.cell
    def resistor(resistance: float = 1e3) -> gf.Component:
        c = gf.Component()
        c.add_port(
            name="p", center=(0, 0), width=0.1, orientation=180, layer=SCHEM_LAYER
        )
        c.add_port(name="n", center=(1, 0), width=0.1, orientation=0, layer=SCHEM_LAYER)
        c.info["vlsir"] = {
            "model": "rpoly",
            "spice_type": "RESISTOR",
            "port_order": ["p", "n"],
            "params": {"r": resistance},
        }
        return c

    # Test valid component
    r = resistor(resistance=10e3)
    pkg = to_proto(r, domain="example")
    print("Package:", pkg)
    print("\nSPICE netlist:")
    print(to_spice(r, fmt="spice"))

    # Test invalid component (missing vlsir metadata)
    @gf.cell
    def bad_component() -> gf.Component:
        c = gf.Component()
        return c

    try:
        to_proto(bad_component())
    except ValueError as e:
        print(f"\nExpected error for missing metadata: {e}")
