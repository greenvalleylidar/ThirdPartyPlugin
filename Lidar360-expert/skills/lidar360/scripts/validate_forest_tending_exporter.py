from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


PROHIBITED_IMPORTS = {"forest_tending_sdk.xlsx"}


def run_probe(python_exe: Path, install_root: Path) -> dict[str, Any]:
    code = r'''
import json
import os
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
site = root / "python310" / "Lib" / "site-packages"
for path in (site, root, root / "plugins"):
    if path.exists():
        text = str(path)
        if text not in sys.path:
            sys.path.insert(0, text)
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(text)

import forest_tending_sdk as sdk

excel_methods = []
try:
    import ExcelDocumentPy
    excel_methods = [name for name in dir(ExcelDocumentPy.ExcelDocument) if not name.startswith("_")]
except Exception:
    pass

print(json.dumps({
    "exports": list(getattr(sdk, "__all__", [])),
    "tree_fields": list(sdk.TreeFields.names()),
    "stand_fields": list(sdk.StandFields.names()),
    "exporter_methods": [name for name in dir(sdk.ForestTendingOperationRecordExporter) if not name.startswith("_")],
    "sheet_fields": list(getattr(sdk.SheetData, "__annotations__", {}).keys()),
    "excel_methods": excel_methods,
}))
'''
    process = subprocess.run(
        [str(python_exe), "-c", code, str(install_root)],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    lines = [line.strip() for line in process.stdout.splitlines() if line.strip()]
    for line in reversed(lines):
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    detail = process.stderr.strip() or process.stdout.strip() or "SDK probe produced no JSON"
    raise RuntimeError(detail)


def dotted_name(node: ast.AST) -> str | None:
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
        return ".".join(reversed(parts))
    return None


class ExporterValidator(ast.NodeVisitor):
    def __init__(self, api: dict[str, Any]) -> None:
        self.api = api
        self.errors: list[str] = []
        self.defined_methods: set[str] = set()
        self.sheet_data_vars: set[str] = set()
        self.excel_doc_vars: set[str] = set()
        self.add_sheet_results: set[str] = set()

    def error(self, node: ast.AST, message: str) -> None:
        self.errors.append(f"line {getattr(node, 'lineno', '?')}: {message}")

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.defined_methods.add(item.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module or ""
        if module in PROHIBITED_IMPORTS:
            self.error(node, f"unsupported import: {module}")
        if module == "forest_tending_sdk":
            exports = set(self.api.get("exports", []))
            for alias in node.names:
                if alias.name != "*" and alias.name not in exports:
                    self.error(node, f"forest_tending_sdk does not export {alias.name!r}")
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        targets = [target.id for target in node.targets if isinstance(target, ast.Name)]
        call_name = dotted_name(node.value.func) if isinstance(node.value, ast.Call) else None
        for target in targets:
            if call_name == "SheetData":
                self.sheet_data_vars.add(target)
            elif call_name in {"ExcelDocument", "ExcelDocumentPy.ExcelDocument"}:
                self.excel_doc_vars.add(target)
            elif call_name and call_name.endswith(".addSheet"):
                self.add_sheet_results.add(target)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if isinstance(node.value, ast.Name):
            if node.value.id == "TreeFields" and node.attr not in set(self.api.get("tree_fields", [])):
                self.error(node, f"unknown TreeFields member: {node.attr}")
            if node.value.id == "StandFields" and node.attr not in set(self.api.get("stand_fields", [])):
                self.error(node, f"unknown StandFields member: {node.attr}")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            owner = node.func.value.id
            method = node.func.attr
            if owner == "self":
                allowed = set(self.api.get("exporter_methods", [])) | self.defined_methods
                if method not in allowed:
                    self.error(node, f"unknown exporter method: self.{method}()")
            if owner in self.sheet_data_vars:
                self.error(node, f"SheetData has fields only; unsupported method call: {owner}.{method}()")
            if owner in self.add_sheet_results:
                self.error(node, "do not treat ExcelDocument.addSheet() result as a sheet object")
            if owner in self.excel_doc_vars and method not in set(self.api.get("excel_methods", [])):
                self.error(node, f"unknown ExcelDocument method: {method}()")
        self.generic_visit(node)


def import_script(python_exe: Path, install_root: Path, script: Path) -> None:
    code = r'''
import importlib.util
import os
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
script = Path(sys.argv[2]).resolve()
site = root / "python310" / "Lib" / "site-packages"
for path in (site, root, root / "plugins"):
    if path.exists():
        text = str(path)
        if text not in sys.path:
            sys.path.insert(0, text)
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(text)

spec = importlib.util.spec_from_file_location("custom_tending_exporter_validation", script)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot create module spec")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
'''
    process = subprocess.run(
        [str(python_exe), "-c", code, str(install_root), str(script)],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip() or "module import failed"
        raise RuntimeError(detail)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a LiDAR360 forest-tending operation-record exporter.")
    parser.add_argument("--install-root", type=Path, required=True)
    parser.add_argument("--script", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    install_root = args.install_root.expanduser().resolve()
    script = args.script.expanduser().resolve()
    python_exe = install_root / "python310" / "python.exe"
    if not python_exe.is_file():
        raise FileNotFoundError(f"LiDAR360 Python not found: {python_exe}")
    if not script.is_file():
        raise FileNotFoundError(f"Exporter script not found: {script}")

    source = script.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(script))
    api = run_probe(python_exe, install_root)
    validator = ExporterValidator(api)
    validator.visit(tree)
    if validator.errors:
        for error in validator.errors:
            print(error, file=sys.stderr)
        return 1

    compile_process = subprocess.run([str(python_exe), "-m", "py_compile", str(script)], check=False)
    if compile_process.returncode != 0:
        return compile_process.returncode
    import_script(python_exe, install_root, script)
    print("Exporter API validation passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
