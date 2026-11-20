---
name: lidar360-imagery-processing
description: LiDAR360 imagery processing module, updated from references/imagery_processing/tools.md, covering Image Alignment and Registration, Image Processing, Image Group Management, Export and Texture.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

# Imagery Processing Module (imagery_processing)

> This skill index is synchronized from the Markdown documents under `references/imagery_processing/`; the tool list follows `tools.md`.

---

## Detailed Documentation Index

| Document | Content | View |
|---------|---------|------|
| **Tool Registry** | Tool groups, functions, input formats, and key parameters | `read_file('references/imagery_processing/tools.md')` |
| **Preflight Check Workflows** | Data, parameter, and dependency conditions to verify before executing tools | `read_file('references/imagery_processing/preflight_checks.md')` |
| **Typical Examples** | Invocation examples and parameter combinations for common tasks | `read_file('references/imagery_processing/examples.md')` |
| **Detailed Workflows** | Complete business workflows with multi-tool collaboration | `read_file('references/imagery_processing/workflows.md')` |

---

## Tool Group Quick Reference

### Image Alignment and Registration
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `new_image_project` | Create new image project | Images | - |
| `image_alignment` | Image alignment | LIAEP | - |
| `align_to_point_cloud` | Align to point cloud | Images+point cloud | input_data, output_data |
| `update_alignment` | Update alignment | Image project | input_data |

### Image Processing
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `image_defogging` | Image defogging | Images | block, radius |
| `image_project_generate_dsm` | Generate DSM from image project | Image project | input_data, output_data |
| `orthomosaic` | Generate DOM based on orthorectification | Multiple images | input_data, output_data |
| `semantic_feature_extraction` | Semantic feature extraction | TIF/TIFF/IMG | input_data, output_data |

> **Note**: `semantic_feature_extraction` depends on the SAM3 model. Before invocation, confirm the model exists; if missing, first call `platform-lidar360_software_information` to get the download link and download it. See `preflight_checks.md` for details.

### Image Group Management
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `image_divide_group` | Image grouping | Image group | input_data |
| `image_merge_group` | Image merge groups | Multiple groups | input_data |

### Export and Texture
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `export_image_project` | Export image project | Image project | input_data, output_data |
| `export_quality_report` | Export quality report | Image project | input_data, output_data |
| `texture_mapping_for_3d_mesh` | 3D mesh texture mapping | Images+3D mesh | precision |

---

## Preflight Check Index

- Check workflow table
- Image matching/aerial triangulation
- Orthophoto mosaicing
- Image enhancement
- Image management
- Texture mapping
- Quality assessment
- Data export
- SAM3 model check (specific to semantic_feature_extraction)
- Pre-execution check template
- Key dependencies

---

## Example Index

- Example 1: Standard orthophoto production workflow
- Example 2: Image and point cloud fusion workflow
- Example 3: 3D model texture mapping workflow
- Example 4: Large-area image block processing workflow
- Example 5: Image semantic feature extraction workflow
- Recommended parameter values quick reference

---

## Workflow Index

- Workflow overview
- Image processing workflows
- Workflow 1: Standard DOM generation workflow (point cloud to DSM)
- Workflow 2: Spectral angle classification workflow
- Workflow 3: Spectral classification mapping to point cloud workflow
- Workflow 4: 3D model texture mapping workflow
- Workflow 5: Image project and point cloud alignment workflow
- Workflow 6: Image project DOM generation workflow (image project to DSM)
- Parameter configuration quick reference
- DOM generation parameter recommendations
- Spectral angle classification parameter recommendations
- Point cloud mask classification mapping
- Common issues and solutions
- Issue 1: Image alignment failure
- Issue 2: DOM geometric distortion
- Issue 3: Low spectral angle classification accuracy
- Issue 4: Unsatisfactory mask mapping results
- Issue 5: Missing texture mapping
- Workflow selection recommendations
- Related documents

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

- Quick invocation: `imagery_processing-toolID`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "imagery_processing-toolID"`
- Before execution, you **must** check the corresponding tool's check items in this module's `preflight_checks.md`. If checks fail, **do not execute** and prompt the user; for multi-step tasks, refer to `examples.md` or `workflows.md` first.
