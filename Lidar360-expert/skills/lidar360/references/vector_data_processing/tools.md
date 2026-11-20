# Vector Data Processing Tools Registration
---

## Vector Clipping
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| clip_vector_by_polygon | Clip vector features using polygon features from another vector file. Extract portions of input vector that fall within the clipping polygons | Input data | clip_layer_name |

---

## Vector Processing
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| remove_duplicate_vertices | Removing duplicate vertices from features does not cause geometric degradation | SHP/GPKG | tolerance, use_z |
| vector_smooth_lines | Smooth the polylines and polygons in the vector file | SHP/DXF/GPKG/KML/LIGPKG | method |
| split_by_attribute | A feature class or table will be created for every unique combination of attributes from the Split Fields parameter value | SHP/GPKG | layer_name, split_fields |

---

## Vector Analysis
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| extract_multi_values_to_points | Extracts cell values at locations specified in a point feature class from one or more rasters and records the values to the attribute table of the point feature class | Input data | bilinear_interpolation |
| set_z_from_raster | Sets the Z value of each vertex in the feature geometry to a value sampled from a certain band within the grid layer.You can choose to scale the grid values by a preset amount, and the offsets can be added algebraically | Input data | band_number, offset |

---

## Vector Management
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| merge_vectors | Combines multiple input datasets into a single, new output dataset. This tool can combine point, line, or polygon feature classes | SHP/GPKG | feature_type |

---

## Common Parameter Explanation

### Smoothing Algorithms
| Algorithm | Description | Best For |
|---|------|---------|
| Chaikin | Corner cutting | Simple smoothing |
| Douglas_Peucker | Line simplification | Feature preservation |
| Bezier | Bezier curves | Smooth curves |
| Moving_Average | Moving average | General smoothing |

### Merge Methods
| Method | Description |
|---|------|
| Union | Union of all geometries |
| Intersection | Intersection of geometries |
| Difference | Difference between geometries |
| Dissolve | Dissolve boundaries |

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "vector_data_processing-toolID"
