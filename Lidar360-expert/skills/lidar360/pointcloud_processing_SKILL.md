---
name: lidar360-pointcloud-processing
description: LiDAR360 point cloud processing module, updated from references/pointcloud_processing/tools.md, covering Clipping/Splitting, Tiling/Division, Denoising/Smoothing, Extraction/Filtering, Normalization, Merging/Sampling, Attribute Enhancement, Boundary/Other.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

# Point Cloud Processing Module (pointcloud_processing)

> This skill index is synchronized from the Markdown documents under `references/pointcloud_processing/`; the tool list is defined by `tools.md`.

---

## Detailed Documentation Index

| Document | Content | View |
|---------|---------|------|
| **Tool Registry** | Tool grouping, functions, input formats and key parameters | `read_file('references/pointcloud_processing/tools.md')` |
| **Preflight Check Procedures** | Data, parameters, and dependency conditions to verify before executing tools | `read_file('references/pointcloud_processing/preflight_checks.md')` |
| **Typical Examples** | Invocation examples and parameter combinations for common tasks | `read_file('references/pointcloud_processing/examples.md')` |

---

## Tool Group Quick Reference

### Clipping/Splitting
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `clip_by_polygon` | Clip by polygon | lidata+shp/gpkg/kml | generate_file_type(0/1), attribute_name |
| `clip_by_rectangle` | Clip by rectangle | lidata | coordinate_array(x_min/max, y_min/max) |
| `clip_by_circle` | Clip by circle | lidata | coordinate_array(x, y, radius) |
| `clip_by_draw_polygon` | Clip by drawn polygon | lidata | polygon_list |
| `tile_by_line` | Split by line | lidata | start_point_x/y, end_point_x/y |

### Tiling/Division
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `tile_by_polygon` | Tile by polygon | lidata+shp/gpkg/dxf | buffer, is_use_attribute_name |
| `tile_by_range` | Tile by range | lidata | width, length, buffer, merge |
| `tile_by_point_number` | Tile by point count | lidata | point_number(default 50000) |
| `pointcloud_subdivision` | Point cloud subdivision | lidata | scale(0-10), subdivision_type(rectangle/longitude/latitude) |

### Denoising/Smoothing
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `pointcloud_outlier_removal` | Point cloud denoising | lidata | neighbor_points, multiples_of_std_deviation |
| `pointcloud_noise_filter` | Point cloud noise filtering | lidata | - |
| `pointcloud_smooth` | Point cloud smoothing | lidata | select_class, max_fix_distance, search_radius, smoothing_type |

### Extraction/Filtering
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `extract_pointcloud_by_class` | Extract point cloud by class | lidata | from_class(interactive selection) |
| `extract_pointcloud_by_elevation` | Extract point cloud by elevation | lidata | min_elevation, max_elevation, from_class |
| `extract_pointcloud_by_intensity` | Extract point cloud by intensity | lidata | min_intensity, max_intensity, from_class |
| `extract_pointcloud_by_return` | Extract point cloud by return number | lidata | return_num(1-4), from_class |
| `extract_pointcloud_by_gps_time` | Extract point cloud by GPS time | lidata | min_times, max_times, from_class |
| `extract_pointcloud_by_additional_attributes` | Extract point cloud by additional attributes | lidata | att_field_name |
| `split_pointcloud_by_attribute_label` | Split by attribute label | lidata | att_field_name, range_min, range_max, out_file_type |

### Normalization
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `normalize_by_ground_points` | Normalize point cloud by ground points | lidata | Requires classified ground points |
| `normalize_by_dem` | Normalize point cloud by DEM | lidata+tif | input_data, output_data |
| `denormalize` | Denormalize point cloud | lidata | input_data, output_data |

### Merging/Sampling
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `pointcloud_merge` | Point cloud merge | lidata array | ignore_different_att, treeID_reorder_deduplicate |
| `pointcloud_subsampling` | Point cloud resampling | lidata | sampling_type(0/1/2), sampling_rate, octree |

### Attribute Enhancement
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `pointcloud_vegetation_index` | Vegetation index | lidata | index_type(0=NDVI, 1=visible light difference) |
| `pointcloud_pcv` | PCV | lidata | No parameters, generates PCV additional attributes |
| `extract_color_from_ortho_image` | Orthophoto image texture mapping | lidata+tif | overwrite_color |
| `extract_color_from_image_project` | Image project texture mapping | lidata+liaep | overwrite_color |
| `brightness_contrast` | Brightness and contrast | lidata | brightness(-100~100), contrast(-100~50) |
| `extract_spectral_values_from_image` | Extract spectral values from image | lidata+image | attr_names, select_bands, near_infarred_band, default_nir |

### Boundary/Other
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `pointcloud_extract_boundary` | Boundary extraction | lidata | - |
| `transform_gps_time` | GPS time conversion | lidata | - |
| `segment_by_attribute` | Segment by attribute | lidata | search_radius, dimension, from_class |

---

## Preflight Check Index

- Check procedure table
- Clipping/Splitting
- Tiling/Cutting
- Denoising/Smoothing
- Extraction/Filtering
- Normalization
- Merging/Sampling
- Attribute Enhancement
- Boundary/Other
- Pre-execution check template
- Output path check

---

## Example Index

- Example 1: Standard point cloud preprocessing workflow
- Example 2: Normalization processing workflow
- Example 3: Point cloud clipping and tiling workflow
- Example 4: Extract specific objects by class
- Example 5: Point cloud coloring workflow
- Example 6: Point cloud resampling and merging workflow
- Example 7: Vegetation index calculation workflow
- Example 8: Boundary extraction workflow (basic, hexagonal, and concave hull methods)
- Example 9: Point cloud smoothing workflow (basic smoothing, elevation smoothing, multi-overlap smoothing)
- Example 10: Spatial clustering segmentation workflow (basic 2D clustering, 3D clustering with statistics, filtering by additional attributes)
- Example 11: Tile by point count workflow (basic point count tiling, small count dense tiling)
- Example 12: Point cloud subdivision workflow
- Recommended parameter values quick reference

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

- Quick invocation: `pointcloud_processing-toolID`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "pointcloud_processing-toolID"`
- Before execution, you **must** check the corresponding tool's check items in this module's `preflight_checks.md`. If checks fail, **do not execute** and prompt the user. For multi-step tasks, refer to `examples.md` or `workflows.md` first.
