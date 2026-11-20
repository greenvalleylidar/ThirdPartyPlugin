---
name: lidar360-raster-data-processing
description: LiDAR360 raster data processing module, updated from references/raster_data_processing/tools.md, covering Clipping Tools, Mosaic Tools, Band Processing, Extraction Tools, Algebraic Operations, Data Management.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

# Raster Data Processing Module (raster_data_processing)

> This skill index is synchronized from the Markdown documents under `references/raster_data_processing/`; the tool list is defined by `tools.md`.

---

## Detailed Documentation Index

| Document | Content | View |
|---------|---------|------|
| **Tool Registry** | Tool grouping, functions, input formats and key parameters | `read_file('references/raster_data_processing/tools.md')` |
| **Preflight Check Procedures** | Data, parameters, and dependency conditions to verify before executing tools | `read_file('references/raster_data_processing/preflight_checks.md')` |
| **Typical Examples** | Invocation examples and parameter combinations for common tasks | `read_file('references/raster_data_processing/examples.md')` |

---

## Tool Group Quick Reference

### Clipping Tools
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `clip_raster_by_polygon` | Clip raster by polygon | tif/img + shp | input_data, layer_name, attribute_name, buffer, output_format, use_attribute_name |
| `clip_raster_by_draw_polygon` | Clip by drawn polygon | tif/img | input_data, polygons |
| `clip_raster_by_circle` | Clip by circle | tif/img | input_data, center_x, center_y, radius |
| `clip_raster_by_rectangle` | Clip by rectangle | tif/img | input_data, x_min, x_max, y_min, y_max |

### Mosaic Tools
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `raster_mosaic` | Image mosaicking | Multiple tif/img | input_data[], mosaic_method |

### Band Processing
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `composite_raster_bands` | Raster band compositing | Multiple single-band tif | input_data[] |
| `create_color_composite` | Create color composite | Multi-band tif | red_band, green_band, blue_band |

### Extraction Tools
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `extract_by_attributes` | Extract by attributes | tif/img | input_data, expression |
| `extract_raster_by_mask` | Extract by mask | tif/img + mask | input_data, extraction_region |

### Algebraic Operations
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `raster_calculator` | Raster calculator | tif/img | expression |

### Data Management
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `define_raster_nodata_value` | Define NoData value | tif/img | input_data, nodata_value |
| `raster_subdivision` | Image subdivision | tif/img | input_data, tile_size |

---

## Preflight Check Index

- Check procedure table
- Clipping tools
- Mosaic tools
- Band processing
- Extraction tools
- Algebraic operations
- Data management
- Pre-execution check template
- Common error troubleshooting

---

## Example Index

- Example 1: Raster clipping and extraction workflow
- Example 2: Raster mosaicking workflow
- Example 3: Band compositing and index calculation
- Example 4: Raster subdivision processing
- Common raster calculator expressions

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

- Quick invocation: `raster_data_processing-toolID`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "raster_data_processing-toolID"`
- Before execution, you **must** check the corresponding tool's check items in this module's `preflight_checks.md`. If checks fail, **do not execute** and prompt the user. For multi-step tasks, refer to `examples.md` first.
