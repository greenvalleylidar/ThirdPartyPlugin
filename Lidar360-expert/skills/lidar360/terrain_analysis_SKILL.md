---
name: lidar360-terrain-analysis
description: LiDAR360 terrain analysis module, updated from references/terrain/tools.md, covering Terrain Surface Generation, Contour Generation, Terrain Derivatives, Hydrological Analysis, Multi-temporal Analysis, Quality Control, Other Terrain Tools.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

# Terrain Analysis Module (terrain_analysis)

> This skill index is synchronized from the Markdown documents under `references/terrain/`; the tool list follows `tools.md`.

---

## Detailed Documentation Index

| Document | Content | View |
|---------|---------|------|
| **Tool Registry** | Tool groups, functions, input formats, and key parameters | `read_file('references/terrain/tools.md')` |
| **Preflight Check Workflows** | Data, parameter, and dependency conditions to verify before executing tools | `read_file('references/terrain/preflight_checks.md')` |
| **Typical Examples** | Invocation examples and parameter combinations for common tasks | `read_file('references/terrain/examples.md')` |
| **Detailed Workflows** | Complete business workflows with multi-tool collaboration | `read_file('references/terrain/workflows.md')` |

---

## Tool Group Quick Reference

### Terrain Surface Generation
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `generate_general_dem_from_pointcloud` | Generate DEM from point cloud | lidata | x_size, y_size, interpolator |
| `generate_general_dsm_from_pointcloud` | Generate DSM from point cloud | lidata | from_class, x_size, y_size, return_number |
| `generate_tiled_dem_from_pointcloud` | Generate tiled DEM from point cloud | lidata | x_size, y_size, interpolator, scale |
| `generate_tiled_dsm_from_pointcloud` | Generate tiled DSM from point cloud | lidata | from_class, x_size, y_size, interpolator, return_number, scale |
| `generate_chm` | Generate Canopy Height Model | DEM,DSM | - |
| `generate_dom_by_pixel_mode` | Generate DOM based on pixel mode | Image project | resolution_mode, auto_gsd, manual_gsd |
| `point_cloud_to_tin` | Generate TIN | lidata | from_class, tile_type |
| `tin_generate_dem` | Generate DEM from TIN | TIN | x_size, y_size, precision |

### Contour Generation
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `raster_to_contours` | Generate contours from raster | tif/img | interval(contour interval), base(benchmark elevation) |
| `generate_contour_from_pointcloud` | Generate contours from point cloud | lidata | from_class(2), scale, line_width |
| `generate_contour_from_tin` | Generate contours from TIN | TIN | from_class, scale, line_width |
| `generate_elevation_annotation` | Generate elevation annotation points | lidata | - |
| `merge_tiled_contours` | Merge tiled contours | shp | - |
| `merge_breaklines` | Merge breaklines | shp | - |

### Terrain Derivatives
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `slope_analysis` | Slope analysis | DEM(tif/img) | z_scale |
| `aspect_analysis` | Aspect analysis | DEM | z_scale |
| `roughness_analysis` | Roughness analysis | DEM | - |
| `generate_hill_shade` | Hillshade | DEM | azimuth, altitude, z_scales |
| `sky_view_factor` | Sky view factor | DEM | - |
| `viewshed_analysis` | Viewshed analysis | DEM+observation point | - |
| `annual_insolation` | Annual insolation | DEM | - |
| `solar_radiation` | Incident solar radiation | DEM | - |

### Hydrological Analysis
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `fill_sinks` | Fill sinks | DEM | minimum_slope, resampling_method, threshold |
| `flow_direction` | Flow direction | DEM | - |
| `flow_accumulation` | Flow accumulation | flow direction raster | flow_direction_method, convergence |
| `channel_network` | Channel network | DEM/flow accumulation raster | initiation_type, initiation_threshold |
| `drainage_analysis` | Drainage analysis | DEM | - |
| `flooding_analysis` | Flooding analysis | DEM | - |
| `generate_relative_elevation_model` | Generate relative elevation model | DEM + river centerline vector | - |

### Multi-temporal Analysis
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `pointcloud_change_detection` | Change detection | 2 periods lidata | cell_size, from_class, min_z_tolerance, max_z_tolerance |
| `pointcloud_deviation_analysis` | Deviation analysis | 2 periods lidata | cell_size, min_distance, max_distance |
| `pointcloud_construction_progress_analysis` | Construction progress analysis | 2 periods lidata | - |

### Quality Control
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `point_line_contradiction` | Contour contradiction check | Contours+annotation | - |
| `dem_edge_match` | DEM edge matching | Multi-period DEM | sample_type |

### Other Terrain Tools
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `terrain_features` | Terrain features | DEM | is_select_slope, is_select_aspect, is_select_hill_shade, is_select_roughness |
| `create_dem_dsm_for_dom` | DEM/DSM generation for DOM workflow | Image project and point cloud | input_data, output_data |

---

## Preflight Check Index

- Check workflow table
- Surface generation
- Contours
- Terrain derivatives (all require DEM)
- Hydrological analysis (all require valid DEM)
- Multi-temporal analysis
- Quality control
- Pre-execution check template

---

## Example Index

- Example 1: Point cloud to DEM generation workflow
- Example 2: Point cloud to DSM generation workflow
- Example 3: Point cloud to contour generation workflow
- Example 4: Point cloud to TIN generation workflow
- Example 5: Canopy height model generation workflow
- Example 6: Digital orthophoto map (DOM) generation workflow
- Example 7: Terrain derivative analysis workflow
- Example 8: Viewshed analysis workflow
- Example 9: Hydrological analysis workflow
- Recommended parameter values quick reference

---

## Common Parameters Index

| Configuration File | Content | View |
|-------------------|---------|------|
| **File Formats** | Point cloud, raster, vector, model format references | `read_file('references/profiles/file_formats.md')` |
| **Point Cloud Class Codes** | ASPRS/LiDAR360 common class codes | `read_file('references/profiles/class_codes.md')` |
| **Interpolation Methods** | Common interpolation methods for DEM/DSM/raster generation | `read_file('references/profiles/interpolation.md')` |
| **Scale** | Terrain, contour, and mapping scale references | `read_file('references/profiles/scale.md')` |

---

## Parameter Confirmation Gate: Scenario Prompt and Recommended Values

> Applies to all tools that require the user to determine DEM/DSM grid resolution:
> `generate_general_dem_from_pointcloud`, `generate_tiled_dem_from_pointcloud`,
> `generate_general_dsm_from_pointcloud`, `generate_tiled_dsm_from_pointcloud`.

Before invoking these tools:

1. If the user has **not specified an application scenario** in the current request and has not given a resolution directly, **you must** ask for the scenario first and **display the table below verbatim**.

| Scenario | DEM Resolution | Contour Scale | Contour Interval |
|---|---|---|---|
| Building design | 0.3 m | 1:500 | 0.5 m |
| Urban planning | 0.5-1 m | 1:1000 | 1 m |
| Engineering surveying | 1 m | 1:2000 | 2 m |
| Forestry inventory | 2-3 m | 1:10000 | 5 m |
| Provincial planning | 5-10 m | 1:50000 | 20 m |

2. Map the scenario resolution to both `x_size` and `y_size`; if the user gives an explicit value or chooses "other", use that value.
3. Confirm `interpolator` (0 = IDW, 1 = Kriging, 2 = TIN) in the same round - the table does not cover interpolation, so the user must choose.
4. Do **not** substitute schema defaults (0.3 m, interpolator = 0) for the scenario confirmation unless the user explicitly accepts the defaults.
5. If the mean point spacing of the loaded point cloud is clearly larger than the chosen resolution (e.g. ~0.9 m ground point spacing with 0.3 m resolution), warn about possible interpolation artifacts and continue only after user confirmation.
6. Once the scenario and interpolation method are confirmed, reuse them for subsequent similar calls in the same session and **do not ask again**; use the latest instruction when the user changes the scenario.
7. Report the scenario, `x_size`/`y_size`, and `interpolator` actually used in the result summary.

---

## Pre-Execution Checklist

> Before invoking a tool, confirm each of the following checks. If any check fails, **do not execute the tool** - prompt the user to resolve first.

### General Checks

| # | Check Item | Verification Method | Pass |
|---|-----------|-------------------|------|
| 1 | Input file path exists and is accessible | `get_data_information` -> `code == 0` | [ ] |
| 2 | Input data format matches tool requirements | schema `suffix_name` comparison | [ ] |
| 3 | Output path is writable | Manual confirmation | [ ] |
| 4 | DEM/DSM resolution confirmed by scenario (user gave a resolution or answered the scenario prompt) | User confirmation record | [ ] |

### Result

- [ ] All passed -> Execute tool
- [ ] Some items failed -> **Do not execute**, prompt user on which checks failed and resolution suggestions

---

## Invocation Convention

- Quick invocation: `terrain_analysis-toolID`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "terrain_analysis-toolID"`
- Before execution, you **must** check the corresponding tool's check items in this module's `preflight_checks.md`. If checks fail, **do not execute** and prompt the user; for multi-step tasks, refer to `examples.md` or `workflows.md` first.
