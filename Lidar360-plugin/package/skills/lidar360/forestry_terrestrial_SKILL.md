---
name: lidar360-forestry-terrestrial
description: LiDAR360 terrestrial forestry module, updated from references/forestry_terrestrial/tools.md, covering Individual Tree Segmentation, Forest Metrics Calculation, Attribute Statistics and Estimation, Biomass and Modeling, Feature Extraction and Analysis, Data Processing.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

In-place write tools such as individual tree segmentation execute at L3: after a backup suggestion, an impact description, and explicit confirmation.

# Terrestrial Forestry Module (forestry_terrestrial)

> This skill index is synchronized from the Markdown documents under `references/forestry_terrestrial/`; the tool list follows `tools.md`.

---

## Individual Tree Segmentation Decision Tree (Must Ask Before Starting)

> **Before executing any individual tree segmentation task, you must first ask the user about the data source, then select the corresponding workflow based on the response.**

| User-Specified Data Source | Recommended Workflow | Key Tool |
|---------------------------|---------------------|---------|
| Handheld/vehicle/static scan (TLS) | [Terrestrial] Trunk-based individual tree segmentation | tls_trunk_based_tree_segmentation |
| Airborne (ALS), trunk class relatively distinct | [Airborne] Trunk-based segmentation -> switch to `forestry_airborne_SKILL.md` | trunk_based_tree_segmentation |
| Airborne (ALS), trunk class not distinct | CHM seed points -> Seed point-based segmentation -> switch to `forestry_airborne_SKILL.md` | generate_seed_points_from_chm + pointcloud_segmentation_from_seed_points |
| Unknown/unsure data source | [Terrestrial] Universal individual tree segmentation | universal_tree_segmentation |

**Interaction Flow**: Ask data source -> Select workflow based on response -> Preflight check -> Invoke tool

---

## Detailed Documentation Index

| Document | Content | View |
|---------|---------|------|
| **Tool Registry** | Tool groups, functions, input formats, and key parameters | `read_file('references/forestry_terrestrial/tools.md')` |
| **Preflight Check Workflows** | Data, parameter, and dependency conditions to verify before executing tools | `read_file('references/forestry_terrestrial/preflight_checks.md')` |
| **Typical Examples** | Invocation examples and parameter combinations for common tasks | `read_file('references/forestry_terrestrial/examples.md')` |
| **Detailed Workflows** | Complete business workflows with multi-tool collaboration | `read_file('references/forestry_terrestrial/workflows.md')` |

---

## Tool Group Quick Reference

### Individual Tree Segmentation
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `tls_point_cloud_segmentation` | Terrestrial point cloud individual tree segmentation | See tool registry | from_class, cluster_tolerance, minimum_cluster_size, height_above_ground, trunk_height, min_tree_height, optimize_color |
| `tls_point_cloud_segmentation_from_seed_points` | Seed point-based segmentation | See tool registry | Perform individual tree segmentation on point cloud based on seed point file |
| `tls_trunk_based_tree_segmentation` | Trunk-based segmentation | See tool registry | Extract tree trunks from point cloud, then perform individual tree segmentation based on trunks |
| `universal_tree_segmentation` | Universal individual tree segmentation | See tool registry | Universal individual tree segmentation supporting both terrestrial and airborne data, directly outputs segmentation results |

### Forest Metrics Calculation
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `tls_calculate_forest_metrics_by_grid` | Calculate forestry population metrics by grid | See tool registry | Divide point cloud by horizontal grid and calculate point cloud forestry population metrics for each cell; if polygon is provided, only divide grid within polygon |
| `tls_calculate_forest_metrics_by_polygon` | Calculate forestry population metrics by polygon | See tool registry | Divide point cloud into multiple cells and calculate point cloud forestry population metrics for each cell within the polygon |
| `tls_calculate_forest_metrics_by_stands` | Calculate forestry population metrics by stand | See tool registry | Treat input LiData as one stand and calculate overall forestry population metrics |

### Attribute Statistics and Estimation
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `tls_statistic_tree_attribute` | Individual tree attribute statistics | See tool registry | Recalculate and add individual tree point cloud attributes |

### Biomass and Modeling
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `tree_biomass_estimation` | Biomass estimation | See tool registry | Use biomass models to calculate tree biomass from individual tree attribute table |

### Feature Extraction and Analysis
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `tls_tree_trunk_extraction` | Rainforest trunk extraction | See tool registry | Extract tree trunks from normalized terrestrial point cloud data |
| `tls_spatial_structure_quantification` | Spatial structure quantification | See tool registry | Quantitatively describe and analyze canopy structure of forests or vegetation |
| `tls_tree_based_fuzzy_matching` | Tree-based fuzzy matching | See tool registry | Automatically match GPS-collected points with individual tree attribute file |

### Data Processing
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `tls_extract_tree_image_report` | Individual tree report | See tool registry | Generate individual tree image report with individual tree attributes |
| `forest_tending_planning` | Generate reports and operation design tables based on forest tending plan | LiData + TreeDB + JSON | - |

### Tree Species Identification
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `classify_using_trained_tree_species_model` | Classify tree species in segmented point cloud using custom-trained tree species identification model | LiData | input_data, model, confidence_threshold |
| `train_tree_species_identification_model` | Train custom deep learning model to identify tree species from individual tree point clouds | Input data | input_data, task_name, task_description |

---

## Preflight Check Index

- Check workflow overview
- Terrestrial forestry analysis check
- Individual tree segmentation tools
- Forest metrics calculation tools
- Biomass calculation tools
- Attribute statistics tools
- Feature extraction and analysis tools
- Report generation tools
- Quick reference table
- Terrestrial forestry tools

---

## Example Index

- Terrestrial forestry examples
- Individual tree segmentation examples
- Forest metrics calculation examples
- Biomass calculation examples
- Special analysis examples
- Parameter references
- Individual tree segmentation parameter recommendations
- Biomass calculation result types
- Biomass model types
- Common issues
- Q1: TLS segmentation results are unsatisfactory
- Q2: Biomass calculation results are empty
- Related documents

---

## Workflow Index

- Workflow overview
- Terrestrial forestry workflows
- Workflow 1: Standard terrestrial individual tree segmentation workflow
- Workflow 2: Terrestrial universal individual tree segmentation workflow
- Workflow 3: Terrestrial biomass estimation workflow
- Workflow 4: Terrestrial rainforest analysis workflow
- Workflow 5: Forest tending planning workflow
- Airborne + terrestrial fusion workflow
- Workflow 6: Airborne + terrestrial point cloud fusion
- Parameter configuration quick reference
- Scene type (scene_type)
- Interpolation method (interpolator)
- Key class codes (ASPRS standard)
- Individual tree segmentation parameter recommendations
- Forest metrics calculation parameters
- Biomass calculation result types
- Biomass model types
- Common issues and solutions
- Issue 1: TLS segmentation results are unsatisfactory
- Issue 2: Biomass calculation results are empty
- Issue 3: Poor segmentation results after fusion
- Issue 4: Coordinate system mismatch causes fusion failure
- Issue 5: Rainforest trunk extraction is incomplete
- Issue 6: Understory vegetation interferes with segmentation
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

- Quick invocation: `forestry_terrestrial-toolID`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "forestry_terrestrial-toolID"`
- Before execution, you **must** check the corresponding tool's check items in this module's `preflight_checks.md`. If checks fail, **do not execute** and prompt the user; for multi-step tasks, refer to `examples.md` or `workflows.md` first.
