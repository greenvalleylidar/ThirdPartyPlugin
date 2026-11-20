---
name: lidar360-model-data-processing
description: LiDAR360 model data processing module, updated from references/model_data_processing/tools.md, covering Model Merging, Model Processing.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

# Model Data Processing Module (model_data_processing)

> This skill index is synchronized from the Markdown documents under `references/model_data_processing/`; the tool list follows `tools.md`.

---

## Detailed Documentation Index

| Document | Content | View |
|---------|---------|------|
| **Tool Registry** | Tool groups, functions, input formats, and key parameters | `read_file('references/model_data_processing/tools.md')` |
| **Preflight Check Workflows** | Data, parameter, and dependency conditions to verify before executing tools | `read_file('references/model_data_processing/preflight_checks.md')` |

---

## Tool Group Quick Reference

### Model Merging
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `merge_libim_files` | Merge multiple LiBIM files into one LiBIM file | LiBIM | - |
| `merge_3dtiles` | Merge multiple 3D Tiles root tilesets into one | TILESET.JSON | - |

### Model Processing
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `smooth_meshes` | Perform mesh smoothing on input TIN model and save result as new model | LiTin/OBJ | smooth_iterations |

---

## Preflight Check Index

- Check workflow table
- Model merging
- Model optimization
- Pre-execution check template
- Common error handling

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

- Quick invocation: `model_data_processing-toolID`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "model_data_processing-toolID"`
- Before execution, you **must** check the corresponding tool's check items in this module's `preflight_checks.md`. If checks fail, **do not execute** and prompt the user.
