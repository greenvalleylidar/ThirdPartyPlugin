---
name: lidar360-vector-data-processing
description: LiDAR360 vector data processing module, updated from references/vector_data_processing/tools.md, covering Vector Clipping, Vector Processing, Vector Analysis, Vector Management.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

# Vector Data Processing Module (vector_data_processing)

> This skill index is synchronized from the Markdown documents under `references/vector_data_processing/`; the tool list is defined by `tools.md`.

---

## Detailed Documentation Index

| Document | Content | View |
|---------|---------|------|
| **Tool Registry** | Tool grouping, functions, input formats and key parameters | `read_file('references/vector_data_processing/tools.md')` |
| **Preflight Check Procedures** | Data, parameters, and dependency conditions to verify before executing tools | `read_file('references/vector_data_processing/preflight_checks.md')` |
| **Typical Examples** | Invocation examples and parameter combinations for common tasks | `read_file('references/vector_data_processing/examples.md')` |

---

## Tool Group Quick Reference

### Vector Clipping
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `clip_vector_by_polygon` | Clip vector by polygon | Vector+polygon | polygon_file, keep_inside |

### Vector Processing
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `remove_duplicate_vertices` | Remove duplicate vertices | Vector | tolerance |
| `vector_smooth_lines` | Line smoothing | Vector | smoothing_algorithm, tolerance |
| `split_by_attribute` | Split by attribute | Vector | attribute_name |

### Vector Analysis
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `extract_multi_values_to_points` | Extract multi-values to points | Vector+raster | raster_files |
| `set_z_from_raster` | Terrain conformance (assign Z from raster) | Vector+raster | band_number, scale, offset, no_data |

### Vector Management
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `merge_vectors` | Merge vectors | Multiple vectors | merge_method |

---

## Preflight Check Index

- General check items
- Per-tool specific checks
- clip_vector_by_polygon (vector clipping)
- merge_vectors (merge vectors)
- remove_duplicate_vertices (remove duplicate vertices)
- vector_smooth_lines (line smoothing)
- set_z_from_raster (terrain conformance)
- split_by_attribute (split by attribute)
- extract_multi_values_to_points (extract multi-values to points)
- Common issues

---

## Example Index

- Clipping example
- Scenario: Extract data by administrative region
- Merging example
- Scenario: Merge multi-phase survey data
- Editing example
- Scenario: Contour optimization processing
- Terrain conformance example
- Scenario: 2D road to 3D conversion
- Scenario: Elevation datum conversion
- Splitting and extraction example
- Scenario: Split data by land use type
- Scenario: Multi-factor sampling analysis
- Best practices
- Workflow suggestions
- Parameter optimization suggestions

---

## Common Parameters Index

| Configuration File | Content | View |
|-------------------|---------|------|
| **File Formats** | Point cloud, raster, vector, model format references | `read_file('references/profiles/file_formats.md')` |
| **Point Cloud Class Codes** | ASPRS/LiDAR360 common class codes | `read_file('references/profiles/class_codes.md')` |
| **Interpolation Methods** | DEM/DSM/raster generation common interpolation methods | `read_file('references/profiles/interpolation.md')` |
| **Scale** | Terrain, contour, and mapping scale references | `read_file('references/profiles/scale.md')` |

---

## Pre-Execution Checklist

> Before invoking a tool, confirm each check below. If any check fails, **do not execute the tool** — prompt the user to resolve the issue first.

### General Checks

| # | Check Item | Verification Method | Pass |
|---|-----------|-------------------|------|
| 1 | Input file path exists and is accessible | `get_data_information` -> `code == 0` | [ ] |
| 2 | Input data format matches tool requirements | Schema `suffix_name` comparison | [ ] |
| 3 | Output path is writable | Manual confirmation | [ ] |

### Results

- [ ] All passed -> Execute tool
- [ ] Some checks failed -> **Do not execute**, prompt user on which checks failed and provide resolution suggestions

---

## Invocation Conventions

- Quick invocation: `vector_data_processing-toolID`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "vector_data_processing-toolID"`
- Before execution, you **must** check the corresponding tool's check items in this module's `preflight_checks.md`. If checks fail, **do not execute** and prompt the user. For multi-step tasks, refer to `examples.md` first.
