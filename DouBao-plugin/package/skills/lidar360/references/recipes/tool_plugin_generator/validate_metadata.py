#!/usr/bin/env python3
"""
LiDAR360 Tool Plugin metadata.json Validation Script

Validates metadata.json against the json_schema_spec.md specification.

Usage:
    python validate_metadata.py <path-to-metadata.json>

Exit codes:
    0 - Validation passed
    1 - Validation failed (error messages printed)
"""

import json
import re
import sys
from typing import Any, Dict, List, Tuple


class MetadataValidator:
    """metadata.json validator"""

    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """Run full validation, return (passed, error_list, warning_list)"""
        self.errors = []
        self.warnings = []

        self._check_top_level_structure()
        if self.errors:
            return False, self.errors, self.warnings

        self._validate_interface()
        self._validate_input_schema()
        self._validate_output_schema()

        return len(self.errors) == 0, self.errors, self.warnings

    def _add_error(self, path: str, message: str):
        self.errors.append(f"[ERROR] {path}: {message}")

    def _add_warning(self, path: str, message: str):
        self.warnings.append(f"[WARN]  {path}: {message}")

    # ========== Top-level structure ==========

    def _check_top_level_structure(self):
        for key in ["interface", "input_schema", "output_schema"]:
            if key not in self.data:
                self._add_error("root", f"Missing required field: {key}")
            elif not isinstance(self.data[key], dict):
                self._add_error("root", f"{key} must be an object")

    # ========== Interface validation ==========

    def _validate_interface(self):
        iface = self.data.get("interface", {})
        path = "interface"

        required_fields = ["name", "title", "description", "version"]
        for field in required_fields:
            if field not in iface:
                self._add_error(path, f"Missing required field: {field}")
            elif not isinstance(iface[field], str) or not iface[field].strip():
                self._add_error(path, f"{field} must be a non-empty string")

        # name: lowercase snake_case
        name = iface.get("name", "")
        if name and not re.match(r'^[a-z][a-z0-9_]*$', name):
            self._add_error(path, f"name must be lowercase snake_case (starts with a letter, only lowercase letters, digits, underscores): {name}")

        # version: must be v1 or v1.0.0
        version = iface.get("version", "")
        if version and not re.fullmatch(r'v?\d+(?:\.\d+){0,2}', version):
            self._add_error(path, f"version must be '1.0.0' or 'v1.0.0': {version}")

        # category: lowercase snake_case
        category = iface.get("category", "")
        if category and (not isinstance(category, str) or not re.match(r'^[a-z][a-z0-9_]*$', category)):
            self._add_error(path, f"category must be lowercase snake_case: {category}")

        # keywords: optional, but must be an array
        if "keywords" in iface and not isinstance(iface["keywords"], list):
            self._add_error(path, "keywords must be an array")

    # ========== Input Schema validation ==========

    def _validate_input_schema(self):
        schema = self.data.get("input_schema", {})
        path = "input_schema"

        if schema.get("type") != "object":
            self._add_error(path, "type must be 'object'")

        # properties
        if "properties" not in schema:
            self._add_error(path, "Missing properties field")
        elif not isinstance(schema["properties"], dict):
            self._add_error(path, "properties must be an object")
        else:
            self._validate_properties(schema["properties"], f"{path}.properties", is_output=False)

        # required
        if "required" not in schema:
            self._add_error(path, "Missing required field")
        elif not isinstance(schema["required"], list):
            self._add_error(path, "required must be an array")

        # input_data: optional
        if "input_data" in schema:
            self._validate_data_field(schema["input_data"], f"{path}.input_data", "input")

        # output_data: optional (output path within input schema)
        if "output_data" in schema:
            self._validate_data_field(schema["output_data"], f"{path}.output_data", "output")

    # ========== Output Schema validation ==========

    def _validate_output_schema(self):
        schema = self.data.get("output_schema", {})
        path = "output_schema"

        if schema.get("type") != "object":
            self._add_error(path, "type must be 'object'")

        # properties
        if "properties" not in schema:
            self._add_error(path, "Missing properties field")
        elif not isinstance(schema["properties"], dict):
            self._add_error(path, "properties must be an object")
        else:
            self._validate_properties(schema["properties"], f"{path}.properties", is_output=True)

        # required
        if "required" not in schema:
            self._add_error(path, "Missing required field")
        elif not isinstance(schema["required"], list):
            self._add_error(path, "required must be an array")

        # input_data: not allowed
        if "input_data" in schema:
            self._add_error(path, "input_data is not allowed in output_schema")

        # output_data: optional
        if "output_data" in schema:
            self._validate_data_field(schema["output_data"], f"{path}.output_data", "output")

    # ========== Properties validation ==========

    def _validate_properties(self, properties: Dict[str, Any], path: str, is_output: bool = False):
        valid_types = {"integer", "number", "string", "boolean"}

        # Get the required list for the current schema
        # path format: "input_schema.properties" or "output_schema.properties"
        schema_key = path.split(".")[0]  # "input_schema" or "output_schema"
        required_list = self.data.get(schema_key, {}).get("required", [])

        for field_name, field_def in properties.items():
            field_path = f"{path}.{field_name}"

            # Field name convention: only letters, digits, underscores; must start with a letter
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', field_name):
                self._add_error(field_path, f"Invalid field name (only letters, digits, underscores allowed; must start with a letter): {field_name}")

            if not isinstance(field_def, dict):
                self._add_error(field_path, "Field definition must be an object")
                continue

            # type check
            field_type = field_def.get("type")
            if field_type and field_type not in valid_types:
                self._add_error(field_path, f"type must be one of {valid_types}: {field_type}")

            # title check
            if "title" not in field_def:
                self._add_error(field_path, "Missing title field")

            # description check
            if "description" not in field_def:
                self._add_warning(field_path, "Missing description field")

            # Non-required parameters should have a default value (only checked for input_schema)
            if not is_output and field_name not in required_list and "default" not in field_def:
                self._add_warning(field_path, "Non-required parameter should provide a default value")

    # ========== Data field validation ==========

    def _validate_data_field(self, data: Any, path: str, direction: str):
        """Validate input_data or output_data field"""
        valid_file_types = {"file", "multifile", "dir"}

        if isinstance(data, dict):
            # Single data field
            self._validate_single_data_item(data, path, direction)
        elif isinstance(data, list):
            # Multiple data fields
            if len(data) == 0:
                self._add_error(path, "Array must not be empty")
            for i, item in enumerate(data):
                self._validate_single_data_item(item, f"{path}[{i}]", direction)
        else:
            self._add_error(path, "Must be an object or array")

    def _validate_single_data_item(self, item: Dict[str, Any], path: str, direction: str):
        """Validate a single data field item"""
        if not isinstance(item, dict):
            self._add_error(path, "Must be an object")
            return

        valid_file_types = {"file", "multifile", "dir"}

        # type check
        item_type = item.get("type")
        if not item_type:
            self._add_error(path, "Missing type field")
        elif item_type not in valid_file_types:
            self._add_error(path, f"type must be one of {valid_file_types}: {item_type}")

        # name check
        if "name" not in item:
            self._add_error(path, "Missing name field")
        else:
            name = item["name"]
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name):
                self._add_error(path, f"Invalid name (only letters, digits, underscores allowed; must start with a letter): {name}")

        # title check (required)
        if "title" not in item:
            self._add_error(path, "Missing title field")

        # description check
        if "description" not in item:
            self._add_warning(path, "Missing description field")

        # file/multifile types must have suffix_name
        if item_type in ("file", "multifile"):
            if "suffix_name" not in item:
                self._add_error(path, "file/multifile type must have a suffix_name field")
            else:
                suffixes = item["suffix_name"]
                if not isinstance(suffixes, list) or len(suffixes) == 0:
                    self._add_error(path, "suffix_name must be a non-empty array")
                else:
                    for suffix in suffixes:
                        if not isinstance(suffix, str):
                            self._add_error(path, f"suffix_name element must be a string: {suffix}")
                        elif suffix != suffix.lower():
                            self._add_error(path, f"suffix_name must be lowercase: {suffix}")


def validate_file(filepath: str) -> Tuple[bool, List[str], List[str]]:
    """Validate a metadata.json file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"[ERROR] JSON parse error: {e}"], []
    except FileNotFoundError:
        return False, [f"[ERROR] File not found: {filepath}"], []
    except Exception as e:
        return False, [f"[ERROR] Failed to read file: {e}"], []

    validator = MetadataValidator(data)
    return validator.validate()


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_metadata.py <path-to-metadata.json>")
        print("Example: python validate_metadata.py ./my_plugin/metadata.json")
        sys.exit(1)

    filepath = sys.argv[1]
    passed, errors, warnings = validate_file(filepath)

    # Print warnings
    for w in warnings:
        print(w)

    # Print errors
    for e in errors:
        print(e)

    # Print result
    if passed:
        print(f"\n[PASS] Validation passed: {filepath}")
        if warnings:
            print(f"  ({len(warnings)} warning(s))")
        sys.exit(0)
    else:
        print(f"\n[FAIL] Validation failed: {filepath}")
        print(f"  Errors: {len(errors)}, Warnings: {len(warnings)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
