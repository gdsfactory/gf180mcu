#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REF_DIR="${REF_DIR:-$SCRIPT_DIR/../../tests/ref_gds}"
PARAMS_FILE="$SCRIPT_DIR/sweep_params.json"

if ! command -v magic &>/dev/null; then
    echo "Error: magic not found." >&2; exit 1
fi
if [ -z "${PDK_ROOT:-}" ]; then
    echo "Error: PDK_ROOT not set." >&2; exit 1
fi

echo "GF180MCU Magic reference GDS generator"
echo "PDK_ROOT: $PDK_ROOT"
echo "Output: $REF_DIR"

FILTER="${1:-}"

python3 - "$PARAMS_FILE" "$REF_DIR" "$FILTER" <<'PYEOF'
import json, sys, hashlib, pathlib, subprocess, os, tempfile

params_file, ref_dir, device_filter = sys.argv[1], sys.argv[2], sys.argv[3]
with open(params_file) as f:
    config = json.load(f)

param_maps = config.get("param_maps", {})
successes = failures = 0

for device_name, device_cfg in config["devices"].items():
    if device_filter and device_filter != device_name:
        continue
    out_dir = pathlib.Path(ref_dir) / device_name
    out_dir.mkdir(parents=True, exist_ok=True)
    pmap_ref = device_cfg.get("param_map_ref", "")
    pmap = param_maps.get(device_name, param_maps.get(pmap_ref, {}))

    for params in device_cfg["sweep"]:
        param_str = json.dumps(params, sort_keys=True)
        param_hash = hashlib.sha256(param_str.encode()).hexdigest()[:12]
        out_path = out_dir / f"{param_hash}.gds"

        tcl_overrides = []
        for py_name, value in sorted(params.items()):
            magic_name = pmap.get(py_name, py_name)
            tcl_val = ("1" if value else "0") if isinstance(value, bool) else str(value)
            tcl_overrides.append(f"{magic_name} {tcl_val}")
        override_str = " ".join(tcl_overrides)

        print(f"  [{device_name}] {params} -> {out_path.name}")

        tcl_script = f"""
set defaults [gf180mcu::{device_name}_defaults]
set overrides [dict create {override_str}]
set params [dict merge $defaults $overrides]
gf180mcu::{device_name}_draw $params
select top cell
expand
gds write {out_path}
puts "OK: {out_path}"
quit -noprompt
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tcl', delete=False) as f:
            f.write(tcl_script); tcl_path = f.name

        pdk_root = os.environ["PDK_ROOT"]
        magicrc = f"{pdk_root}/gf180mcuA/libs.tech/magic/gf180mcuA.magicrc"
        try:
            result = subprocess.run(
                ["magic", "-dnull", "-noconsole", "-rcfile", magicrc, tcl_path],
                capture_output=True, text=True, timeout=120,
                env={**os.environ, "PDK_ROOT": pdk_root}
            )
            if out_path.exists() and out_path.stat().st_size > 0:
                print(f"    OK ({out_path.stat().st_size} bytes)")
                successes += 1
            else:
                print(f"    FAILED", file=sys.stderr)
                if result.stderr: print(f"    {result.stderr[:300]}", file=sys.stderr)
                failures += 1
        except subprocess.TimeoutExpired:
            print(f"    TIMEOUT", file=sys.stderr); failures += 1
        finally:
            os.unlink(tcl_path)

print(f"\nDone: {successes} succeeded, {failures} failed")
PYEOF
