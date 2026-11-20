---
name: lidar360-data-preprocessing
description: LiDAR360 data preprocessing module, updated from references/data_preprocessing/tools.md, covering Data Registration and Adjustment, Data Splitting and Cutting, Quality Analysis and Reconstruction, Data Inspection.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

# Data Preprocessing Module (data_preprocessing)

> This skill index is synchronized from the Markdown documents under `references/data_preprocessing/`; the tool list is defined by `tools.md`.

---

## Detailed Documentation Index

| Document | Content | View |
|---------|---------|------|
| **Tool Registry** | Tool grouping, functions, input formats and key parameters | `read_file('references/data_preprocessing/tools.md')` |
| **Preflight Check Procedures** | Data, parameters, and dependency conditions to verify before executing tools | `read_file('references/data_preprocessing/preflight_checks.md')` |
| **Detailed Workflows** | Data quality inspection, registration, trajectory adjustment, trajectory clipping, overlap cutting, and DJI reconstruction workflows | `read_file('references/data_preprocessing/workflows.md')` |

---

## Tool Group Quick Reference

### Data Registration and Adjustment
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `auto_registration` | Automatic registration | Reference+align point clouds | input_data, output_data, icp_optimize |
| `auto_image_registration` | Automatic image registration | Reference+align raster files | input_data, output_data, method, resampling_method |
| `trajectory_adjustment` | Flight strip adjustment | Point cloud+trajectory | input_data, flight_data, adjust_x/y/z, adjust_roll/pitch/heading |

### Data Splitting and Cutting
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `auto_split_trajectory` | Automatic trajectory splitting | POS/TRAJ | max_heading_change, min_duration, min_length |
| `cut_overlap` | Remove redundancy | Point clouds+POS files | type, method_type, edge, density, from_class, to_class |
| `cut_point_cloud_by_trajectory` | Clip point cloud by trajectory line | Point cloud+POS files | enable_buffer, buffer |

### Quality Analysis and Reconstruction
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `density_quality_analysis` | Density quality check | LiData | grid_size, upper_values, report_title, render_colors |
| `strip_overlap_analysis` | Strip overlap analysis | Point cloud files and trajectory files | overlap_threshold, input_data, output_data |
| `trajectory_quality_analysis` | Flight line quality check | TRAJ/POS/OUT | input_data, output_data |
| `dji_cloud_reconstruction` | DJI L1/L2/L3 reconstruction | DJI raw LiDAR directory | user_token, input_data, output_data |

### Data Inspection
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `elevation_difference_inspection` | Elevation difference quality check | >=2 LiData files | grid_size, elevation_difference_threshold |

---

## Workflow Index

- Workflow 1: Point cloud registration quality inspection
- Workflow 2: Strip adjustment and layering quality inspection
- Workflow 3: Automatic trajectory splitting and trajectory-based clipping
- Workflow 4: Overlap area processing, strip overlap analysis, and density quality inspection
- Trajectory quality inspection: Trajectory altitude, speed, and attitude quality analysis
- Workflow 5: DJI L1/L2/L3 post-reconstruction preprocessing (including optional trajectory quality analysis and strip adjustment)

---

## Preflight Check Index

- Check procedure table
- Quality check tools
- Adjustment tools
- UAV processing
- Pre-execution check template
- Common error handling
- Key configuration instructions

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

- Quick invocation: `data_preprocessing-toolID`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "data_preprocessing-toolID"`
- Before execution, you **must** check the corresponding tool's check items in this module's `preflight_checks.md`. If checks fail, **do not execute** and prompt the user. For multi-step tasks, refer to `workflows.md` first.
