---
name: lidar360-attribute-table
description: Attribute table calculation and operations. Used to perform field calculations on the attribute tables of vector data, tabular data, and building data.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

`save_after_calculation=true` persists back to the input attribute table and executes at L3: first suggest a backup, show the target file and field, and obtain explicit confirmation; if not confirmed, nothing is written to disk.

# attribute_table Attribute Table Module

## Module Overview

The attribute table module provides field calculation capabilities for the attribute tables of vector data (GPKG, DXF, SHP, KML), tabular data (CSV, TreeDB), and building data (LiBIM) loaded in LiDAR360.

## When to Invoke

- The user needs to calculate attribute table fields or create new fields
- The user mentions "attribute table calculation", "field calculator", "calculate field", or "update attribute field"
- The user needs to perform batch calculations on attributes of vector, tabular, or building data

## Invocation Conventions

Read `references/attribute_table/tools.md` to obtain the tool registry.
Before execution, read `references/attribute_table/preflight_checks.md` and perform the preflight checks according to the procedure.
When encountering errors, refer to the error-handling table in `references/attribute_table/preflight_checks.md`.
For usage examples, refer to `references/attribute_table/examples.md`.

When invoking, pass the documents under `references/attribute_table/` as context:
- `read_file('references/attribute_table/tools.md')`
- `read_file('references/attribute_table/preflight_checks.md')`
- `read_file('references/attribute_table/examples.md')`

## Tool List

### Field Calculation
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|--------------|----------------|
| `attribute_table_field_calculator` | Calculate attribute table fields using a field expression; the result is written to an existing field or a new field | gpkg/dxf/shp/kml/csv/treedb/libim | input_file, operation, target_field, expression |

## Usage Workflow

1. **Confirm input data**: Check that the input file path exists and the format is supported
2. **Select operation type**: `update_field` (update an existing field) or `create_field` (create a new field)
3. **Write the calculation expression**: Use field calculator syntax, e.g. `"height" * 2`
4. **Execute calculation**: Call `attribute_table_field_calculator`
5. **Save result**: To persist, set `save_after_calculation=true`

## Notes

- Field names must use field calculator syntax (e.g. `"field_name"`)
- When creating a new field, you can specify the field type (integer/double/text/datetime)
- Calculation scope can be selected by row/feature ID
- It is recommended to back up the data before calculation
