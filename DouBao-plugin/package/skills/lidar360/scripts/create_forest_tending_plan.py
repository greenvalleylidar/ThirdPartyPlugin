from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_PLAN_NAME = "crop-tree-selection.json"
DEFAULT_EXPORTER_NAME = "tending_operation_record_exporter.py"


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def write_json_new(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=4)
        stream.write("\n")


def normalized(path: Path) -> Path:
    return path.expanduser().resolve(strict=False)


def require_new_plan_path(install_root: Path, base_plan: Path, output_plan: Path) -> None:
    plan_directory = normalized(install_root) / "config" / "ForestAnalysis"
    base = normalized(base_plan)
    output = normalized(output_plan)
    expected_base = plan_directory / DEFAULT_PLAN_NAME
    if base != expected_base:
        raise ValueError(f"Base plan must be the installed read-only default: {expected_base}")
    if base == output:
        raise ValueError("Output plan must not overwrite the base plan.")
    if output.name.casefold() == DEFAULT_PLAN_NAME.casefold():
        raise ValueError(f"The built-in plan name is protected: {DEFAULT_PLAN_NAME}")
    if output.parent != plan_directory:
        raise ValueError(f"Output plan must be created in: {plan_directory}")
    if output.exists():
        raise FileExistsError(f"Output plan already exists: {output}")


def application_relative_path(install_root: Path, target: Path) -> str:
    root = normalized(install_root)
    resolved = normalized(target)
    try:
        relative = resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Path is outside the LiDAR360 installation: {resolved}") from exc
    return relative.as_posix()


def load_schema_file(path: Path) -> dict[str, Any]:
    schema = read_json(path)
    if isinstance(schema.get("schema"), dict):
        schema = schema["schema"]
    return schema


def run_schema(python_exe: Path, hook_script: Path) -> dict[str, Any]:
    process = subprocess.run(
        [str(python_exe), str(hook_script), "--lidar360-schema"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip() or "unknown schema error"
        raise RuntimeError(f"Failed to load hook schema: {detail}")
    try:
        value = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Hook schema output is not valid JSON.") from exc
    if not isinstance(value, dict):
        raise RuntimeError("Hook schema output must be a JSON object.")
    if isinstance(value.get("schema"), dict):
        value = value["schema"]
    return value


def schema_list(schema: dict[str, Any], *keys: str) -> list[dict[str, Any]]:
    for key in keys:
        value = schema.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def parameter_defaults(definitions: list[dict[str, Any]]) -> dict[str, Any]:
    defaults: dict[str, Any] = {}
    for definition in definitions:
        key = definition.get("key")
        if isinstance(key, str) and key and "default" in definition:
            defaults[key] = definition["default"]
    return defaults


def update_hook_config(
    plan: dict[str, Any],
    install_root: Path,
    hook_script: Path,
    schema: dict[str, Any] | None,
) -> None:
    config = plan.setdefault("PythonHookConfig", {})
    if not isinstance(config, dict):
        raise ValueError("PythonHookConfig must be an object.")
    config["enabled"] = True
    config["scriptPath"] = application_relative_path(install_root, hook_script)
    config["scriptPathType"] = "application"

    if schema is None:
        config["outputFields"] = []
        config["parameterDefinitions"] = []
        config["parameters"] = {}
        return

    fields = schema_list(schema, "fields", "outputFields")
    parameters = schema_list(schema, "parameters", "parameterDefinitions")
    config["outputFields"] = fields
    config["parameterDefinitions"] = parameters
    config["parameters"] = parameter_defaults(parameters)


def update_export_config(
    plan: dict[str, Any],
    install_root: Path,
    exporter_script: Path | None,
) -> None:
    config = plan.setdefault("RecordExportConfig", {})
    if not isinstance(config, dict):
        raise ValueError("RecordExportConfig must be an object.")
    if exporter_script is None:
        return
    if normalized(exporter_script).name.casefold() == DEFAULT_EXPORTER_NAME.casefold():
        raise ValueError("The built-in operation-record exporter is protected; use a custom exporter.")
    config["enabled"] = True
    config["exporterScriptPath"] = application_relative_path(install_root, exporter_script)
    config["exporterScriptPathType"] = "application"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new LiDAR360 forest-tending plan without overwriting built-in files."
    )
    parser.add_argument("--install-root", type=Path, required=True)
    parser.add_argument("--base-plan", type=Path, required=True)
    parser.add_argument("--output-plan", type=Path, required=True)
    parser.add_argument("--hook-script", type=Path, required=True)
    parser.add_argument("--schema-file", type=Path)
    parser.add_argument("--python-exe", type=Path)
    parser.add_argument("--exporter-script", type=Path)
    parser.add_argument("--report-title")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    install_root = normalized(args.install_root)
    base_plan = normalized(args.base_plan)
    output_plan = normalized(args.output_plan)
    hook_script = normalized(args.hook_script)

    if not (install_root / "LiDAR360.exe").is_file():
        raise FileNotFoundError(f"LiDAR360.exe not found under: {install_root}")
    if not base_plan.is_file():
        raise FileNotFoundError(f"Base plan not found: {base_plan}")
    if not hook_script.is_file():
        raise FileNotFoundError(f"Hook script not found: {hook_script}")
    require_new_plan_path(install_root, base_plan, output_plan)

    schema: dict[str, Any] | None = None
    if args.schema_file:
        schema = load_schema_file(normalized(args.schema_file))
    elif args.python_exe:
        python_exe = normalized(args.python_exe)
        if not python_exe.is_file():
            raise FileNotFoundError(f"Python executable not found: {python_exe}")
        schema = run_schema(python_exe, hook_script)

    plan = read_json(base_plan)
    update_hook_config(plan, install_root, hook_script, schema)
    update_export_config(
        plan,
        install_root,
        normalized(args.exporter_script) if args.exporter_script else None,
    )
    if args.report_title is not None:
        plan["Report Title"] = args.report_title

    write_json_new(output_plan, plan)
    print(str(output_plan))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
