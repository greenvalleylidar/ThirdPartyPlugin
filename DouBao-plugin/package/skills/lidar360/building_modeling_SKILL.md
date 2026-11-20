---
name: lidar360-building-modeling
description: LiDAR360 building modeling module, updated from references/building_modeling/tools.md, covering Building Creation and Extraction, Building Analysis, Texture Mapping.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

`building_attributes_calculate` modifies the input LiBIM in place; it executes at L3 after a backup suggestion, an impact description, and explicit confirmation.

# Building Modeling Module (building_modeling)

> This skill index is synchronized from the Markdown documents under `references/building_modeling/`; the tool list follows `tools.md`.

---

## Detailed Documentation Index

| Document | Content | View |
|---------|---------|------|
| **Tool Registry** | Tool groups, functions, input formats, and key parameters | `read_file('references/building_modeling/tools.md')` |
| **Preflight Checks** | Data checks and parameter validation before tool invocation | `read_file('references/building_modeling/preflight_checks.md')` |
| **Typical Examples** | Invocation examples and parameter combinations for common tasks | `read_file('references/building_modeling/examples.md')` |
| **Workflows** | Multi-step processing workflows across tools | `read_file('references/building_modeling/workflows.md')` |

---

## Tool Group Quick Reference

### Building Creation and Extraction
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `auto_create_buildings` | Automatically batch-create LOD2 building models | Input data | roof_class, ground_class |
| `extract_building_footprint_from_image` | Use deep learning to extract building footprints from imagery (must be DOM or three-channel color imagery), output building footprint vector file (SHP) and optional mask file (TIF); the schema description and outputSchema suffix may be inconsistent at runtime — verify against the current outputSchema before execution | TIF/TIFF/JPG/PNG/JPEG/BMP | - |

### Building Analysis
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `building_attributes_calculate` | Automatically calculate building model attributes (height, eave height, base elevation, roof orientation, roof shape, etc.), will directly modify the input LiBIM file | Input data | - |

### Texture Mapping
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `ortho_texture_mapper_for_libim` | Use orthophoto imagery to perform texture mapping for LiBIM building models (DOM and LiBIM must use the same coordinate system) | Input data | - |
| `oblique_texture_mapper_for_libim` | Use oblique imagery to perform texture mapping for LiBIM building models | Input data | max_oblique_angle |

---

## Example Index

- Workflow 1: Complete 3D building modeling workflow
- Workflow 2: Extract building footprints from imagery workflow
- Workflow 3: Building model attribute analysis workflow
- Usage notes
- Tool selection recommendations

---

## Common Parameters Index

| Configuration File | Content | View |
|-------------------|---------|------|
| **File Formats** | Point cloud, raster, vector, model format references | `read_file('references/profiles/file_formats.md')` |
| **Point Cloud Class Codes** | ASPRS/LiDAR360 common class codes | `read_file('references/profiles/class_codes.md')` |
| **Interpolation Methods** | Common interpolation methods for DEM/DSM/raster generation | `read_file('references/profiles/interpolation.md')` |
| **Scale** | Terrain, contour, and mapping scale references | `read_file('references/profiles/scale.md')` |

---

## Pre-Execution Checklist

> Before invoking a tool, confirm each of the following checks. If any check fails, **do not execute the tool** — prompt the user to resolve first.

### General Checks

| # | Check Item | Verification Method | Pass |
|---|-----------|-------------------|------|
| 1 | Input file path exists and is accessible | `get_data_information` -> `code == 0` | [ ] |
| 2 | Input data format matches tool requirements | schema `suffix_name` comparison | [ ] |
| 3 | Output path is writable | Manual confirmation | [ ] |

### Result

- [ ] All passed -> Execute tool
- [ ] Some items failed -> **Do not execute**, prompt user on which checks failed and resolution suggestions

---

## Invocation Convention

- Quick invocation: `building_modeling-toolID`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "building_modeling-toolID"`
- Before execution, you **must** check the corresponding tool's check items in this module's `preflight_checks.md`. If checks fail, **do not execute** and prompt the user; for multi-step tasks, refer to `examples.md` or `workflows.md` first.
