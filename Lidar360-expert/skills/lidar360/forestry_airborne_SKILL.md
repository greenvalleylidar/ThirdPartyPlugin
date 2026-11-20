---
name: lidar360-forestry-airborne
description: LiDAR360 airborne forestry module, updated from references/forestry_airborne/tools.md, covering Tree Segmentation, Forest Metrics, Tree Attribute Statistics, CHM Processing, Regression and Prediction, Data Management and Other.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

`clear_tree_id`, `its_mosaicing`, and `als_clear_treeid_by_file` are L3 in-place modifications; you must first suggest a backup, describe the impact, and obtain explicit confirmation.

# Airborne Forestry Module (forestry_airborne)

> This skill index is synchronized from the Markdown documents under `references/forestry_airborne/`; the tool list follows `tools.md`.

---

## Individual Tree Segmentation Decision Tree (Must Ask Before Starting)

> **Before executing any individual tree segmentation task, you must first ask the user about the data source, then select the corresponding workflow based on the response.**

| User-Specified Data Source | Recommended Workflow | Key Tool |
|---------------------------|---------------------|---------|
| Handheld/vehicle/static scan (TLS) | [Terrestrial] Trunk-based individual tree segmentation -> switch to `forestry_terrestrial_SKILL.md` | tls_trunk_based_tree_segmentation |
| Airborne (ALS), trunk class relatively distinct | [Airborne] Trunk-based segmentation | trunk_based_tree_segmentation |
| Airborne (ALS), trunk class not distinct | CHM seed points -> Seed point-based segmentation | generate_seed_points_from_chm + pointcloud_segmentation_from_seed_points |
| Unknown/unsure data source | [Terrestrial] Universal individual tree segmentation -> switch to `forestry_terrestrial_SKILL.md` | universal_tree_segmentation |

**Interaction Flow**: Ask data source -> Select workflow based on response -> Preflight check -> Invoke tool

---

## Detailed Documentation Index

| Document | Content | View |
|---------|---------|------|
| **Tool Registry** | Tool groups, functions, input formats, and key parameters | `read_file('references/forestry_airborne/tools.md')` |
| **Preflight Check Workflows** | Data, parameter, and dependency conditions to verify before executing tools | `read_file('references/forestry_airborne/preflight_checks.md')` |
| **Typical Examples** | Invocation examples and parameter combinations for common tasks | `read_file('references/forestry_airborne/examples.md')` |
| **Detailed Workflows** | Complete business workflows with multi-tool collaboration | `read_file('references/forestry_airborne/workflows.md')` |
| **Tree Species Model Index** | 70 tree species models supported by individual tree modeling and their 0-69 indices | `read_file('references/profiles/model_library_tree_species_chinese_english_comparison_table.md')` |

---

## Individual Tree Modeling Workflow

> Use `forestry_airborne-generate_tree_model` to generate tree models. When the user requests to generate LiTree, individual tree model, tree model, or tree species model mapping, refer to this workflow and "Generate tree model (generate_tree_model)" in `references/forestry_airborne/examples.md`.

**Workflow**:
```
Read treedb -> Extract unique tree species -> Replace empty species with Default -> Read/provide tree species model index table -> User specifies tree_model for each -> Generate tree_modes_list -> Call generate_tree_model
```

**tree_kind Rules**:
- `tree_kind` comes from the unique tree species strings read from the input `treedb`.
- When the tree species string is empty, `Default` must be used instead.
- For example, when tree species values are `Species1`, `Species2`, empty, empty, empty, the `tree_kind` should be `Species1`, `Species2`, `Default`.

**tree_model Rules**:
- `tree_model` is the LiDAR360 tree species model library index, currently ranging from `0~69`.
- Index meanings follow `references/profiles/model_library_tree_species_chinese_english_comparison_table.md`.
- The user must specify `tree_model` for each `tree_kind` individually; do not auto-guess.
- If `treedb` cannot be read or the user does not want to set parameters, a simplified configuration can be used: `tree_modes_list: [{"tree_kind":"Default","tree_model":0}]`.

---

## Tool Group Quick Reference

### Tree Segmentation
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `individual_tree_segmentation` | Individual tree segmentation from point cloud | lidata | from_class, grid_size, buffer_size, height_above_ground |
| `individual_tree_crown_segmentation` | Individual tree crown segmentation | lidata | overlap_ratio, confidence_threshold, input_data, output_data |
| `trunk_based_tree_segmentation` | Tree-based segmentation | lidata | from_class, trunk_class, foliage_class, use_gpu_first, height_above_ground, min_tree_height, optimize_color, input_data, output_data |
| `generate_seed_points_from_chm` | Generate seed points from CHM | CHM | maximum_tree_height, minimum_tree_height, buffer_size, is_smooth, sigma, radius_pix, input_data, output_data |
| `pointcloud_segmentation_from_seed_points` | Point cloud segmentation from seed points | lidata+seed_points | from_class, height_above_ground, min_tree_height, optimize_color, input_data, output_data |

### Forest Metrics
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `calculate_forest_metrics_by_grid` | Calculate forest metrics by grid | lidata | is_select_elevation_metrics, is_select_intensity_metrics, is_select_canopy_cover, is_select_gap_fraction, is_select_leaf_area_index, from_class, x_grid_size, y_grid_size, height_break, extinction_coefficient, output_type, input_data, output_data |
| `calculate_forest_metrics_by_polygon` | Calculate forest metrics by polygon | lidata+polygon | is_select_elevation_metrics, is_select_intensity_metrics, is_select_canopy_cover, is_select_gap_fraction, is_select_leaf_area_index, from_class, height_break, extinction_coefficient, input_data, output_data |
| `calculate_forest_metrics_by_forest_stands` | Calculate forest metrics by forest stands | lidata+stands | is_select_elevation_metrics, is_select_intensity_metrics, is_select_canopy_cover, is_select_gap_fraction, is_select_leaf_area_index, from_class, height_break, extinction_coefficient, input_data, output_data |

### Tree Attribute Statistics
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `als_individual_tree_attribute_statistics` | ALS statistic tree attribute | lidata | attribute_types |
| `extract_tree_crown_boundaries` | Statistic tree crown contours | lidata | contour_interval |

### CHM Processing
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `chm_pits_filling` | CHM pits filling | CHM | filling_method |
| `chm_segmentation` | CHM segmentation | CHM | segmentation_parameters |

### Regression and Prediction
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `linear_regression` | Linear regression | Training data | target_variable, predictor_variables |
| `random_forest_regression` | Random forest regression | Training data | n_estimators, max_depth |
| `svm_regression` | SVM regression | Training data | kernel_type, C_value |
| `fann_regression` | FANN regression | Training data | network_structure |
| `regression_prediction` | Regression prediction | New data | model_path |

### Data Management and Other
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `generate_tree_model` | Generate tree model | TreeDB | tree_modes_list, input_data, output_data |
| `its_mosaicing` | ITS mosaicing | Multiple segments | input_data, recalculate_tree_id, tile_buffer |
| `forest_stands_delineating` | Forest stands delineating | lidata | method, cell_size, min_stand_area, min_height, max_height, input_data, output_data |
| `forest_structure_change_detection` | Forest structure change detection | 2 periods lidata | x_size, y_size, height_break, input_data, output_data |
| `auto_registration_forest` | Auto registration forest | Multiple datasets | input_data, output_data |
| `clear_tree_id` | Clear tree ID | lidata | filter_by_height, min_height, max_height, input_data |
| `als_clear_treeid_by_file` | ALS clear tree ID by file | lidata+file | input_data |
| `extract_by_tree_id` | Extract by tree ID | lidata | filter_by, extract_to, output_format, input_data, output_data |

---

## Preflight Check Index

- Check workflow overview
- Airborne forestry analysis check
- Individual tree segmentation tools
- CHM-related tools
- Forest metrics calculation tools
- Regression analysis tools
- Data processing tools
- Quick reference table
- Airborne forestry tools

---

## Example Index

- Airborne forestry examples
- Individual tree segmentation examples
- CHM processing examples
- Forest metrics calculation examples
- Regression analysis examples
- Data processing examples
- Individual tree modeling examples
- Parameter references
- Individual tree segmentation parameter recommendations
- Forest metrics calculation parameter recommendations
- Regression analysis parameter recommendations
- Common issues
- Q1: Too few trees after individual tree segmentation
- Related documents

---

## Workflow Index

- Workflow overview
- Airborne forestry workflows
- Workflow 1: Standard airborne individual tree segmentation workflow
- Workflow 2: CHM-assisted segmentation workflow
- Workflow 3: Image-based segmentation workflow
- Workflow 4: Complete forest resource inventory workflow
- Workflow 5: Regression analysis and model prediction workflow
- Workflow 6: Multi-temporal change detection workflow
- Parameter configuration quick reference
- Scene type (scene_type)
- Interpolation method (interpolator)
- Key class codes (ASPRS standard)
- Individual tree segmentation parameter recommendations
- Forest metrics calculation parameters
- Regression model selection
- Common issues and solutions
- Issue 1: Too few trees after individual tree segmentation
- Issue 2: Multi-temporal data cannot be registered
- Issue 3: CHM segmentation boundaries are inaccurate
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

### Tool-Specific Checks

> Check the corresponding tool's check items in this module's `preflight_checks.md` and confirm each one (see `tool_call_conventions.md` verification method reference table):

| # | Check Item | Verification Method | Pass |
|---|-----------|-------------------|------|
| 1 | (Obtained from preflight_checks.md) | (Obtained from preflight_checks.md) | [ ] |
| 2 | ... | ... | [ ] |

### Result

- [ ] All passed -> Execute tool
- [ ] Some items failed -> **Do not execute**, prompt user on which checks failed and resolution suggestions

---

## Invocation Convention

- Quick invocation: `forestry_airborne-toolID`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "forestry_airborne-toolID"`
- Before execution, you **must** check the corresponding tool's check items in this module's `preflight_checks.md`. If checks fail, **do not execute** and prompt the user; for multi-step tasks, refer to `examples.md` or `workflows.md` first.
