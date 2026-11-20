---
name: lidar360-projection
description: LiDAR360 Coordinate Reference System module, providing define projection and reproject functions. Define projection assigns a coordinate system to data without changing coordinate values; reproject transforms data from one coordinate system to another.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

`define_projection` updates projection metadata in place, and `define_transformation` / `fit_geoid_transformation` permanently write transformation configuration; both require L3 — first suggest a backup and obtain explicit confirmation.

# Coordinate Reference System Module (projection)

> This skill index is synchronized from the Markdown documents under `references/projection/`; the tool list follows `tools.md`.

---

## Documentation Index

| Document | Content | View |
|-----|------|------|
| **Tool Registry** | Tool grouping, functions, input formats, and key parameters | `read_file('references/projection/tools.md')` |
| **Preflight Checks** | Data, parameters, and dependency conditions to verify before executing tools | `read_file('references/projection/preflight_checks.md')` |
| **Typical Examples** | Invocation examples and parameter combinations for common tasks | `read_file('references/projection/examples.md')` |

---

## Tool Group Quick Reference

### Coordinate Reference System Definition and Transformation
| Tool ID | Function | Input Format | Key Parameters |
|-------|------|---------|---------|
| `define_projection` | Define a coordinate reference system for data (without changing coordinate values) | lidata/tif/shp/gpkg/libim/litree/obj, etc. | coordinate_name, h_authority_code, v_authority_code, is_use_seven_param, seven_param, wkt |
| `reproject` | Transform data from the source coordinate system to the target coordinate system | lidata/tif/shp/gpkg/libim/litree/obj, etc. | coordinate_name, h_authority_code, v_authority_code, is_use_seven_param, seven_param, wkt, output_data |

### Coordinate Query and Transformation
| Tool ID | Function | Input Format | Key Parameters |
|-------|------|---------|---------|
| `query_crs` | Query official, custom, or preset coordinate reference systems | - | authority_code, crs_type, keyword, source, limit, offset |
| `transform_coordinates` | Transform one or more coordinate points between coordinate systems | - | source_crs, target_crs, points, is_use_seven_param, seven_param |

### Coordinate Transformation Management
| Tool ID | Function | Input Format | Key Parameters |
|-------|------|---------|---------|
| `get_coordinate_transformations` | Get all stored coordinate transformation parameters | - | - |
| `define_transformation` | Define a new coordinate transformation and save permanently | - | name, type |
| `fit_geoid_transformation` | Fit geoid model from TXT/CSV file and save as coordinate transformation | txt/csv | input_data, method |
| `transformation_file_coordinates` | Apply a named coordinate transformation to a file | lidata/shp/gpkg/dxf/treedb/libim/obj | input_data, output_data, transformation_name |

---

## Preflight Check Index

- Check flow table
- Input data checks
- Coordinate system parameter checks
- Output path checks

---

## Example Index

- Example 1: Define WGS84 coordinate system for point cloud data
- Example 2: Reproject point cloud from WGS84 to CGCS2000
- Example 3: Precise coordinate transformation using seven parameters
- Example 4: Define and transform coordinate systems for raster data
- Example 5: Define and transform coordinate systems for vector data

---

## Common Parameter Index

| Config File | Content | View |
|---------|------|------|
| **File Formats** | Point cloud, raster, vector, model format reference | `read_file('references/profiles/file_formats.md')` |

---

## Pre-Execution Checklist

> Before calling a tool, confirm each of the following checks. If any check fails, **do not execute the tool**; prompt the user to resolve the issue first.

### General Checks

| # | Check Item | Verification Method | Pass |
|---|--------|---------|------|
| 1 | Input file path exists and is accessible | `get_data_information` -> `code == 0` | [ ] |
| 2 | Input data format matches tool requirements | Compare schema `suffix_name` | [ ] |
| 3 | Coordinate system parameters are correct (EPSG code or WKT) | Manual confirmation | [ ] |
| 4 | Output path is writable (reproject only) | Manual confirmation | [ ] |

### Result

- [ ] All passed -> Execute tool
- [ ] Any failed -> **Do not execute**; prompt the user with which checks failed and suggested resolutions

---

## Invocation Convention

- Quick invocation: `projection-<tool_id>`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "projection-<tool_id>"`
- Before execution, you **must** review the corresponding tool's check items in this module's `preflight_checks.md`. If any check fails, **do not execute** and prompt the user. For multi-step tasks, refer to `examples.md` first.
