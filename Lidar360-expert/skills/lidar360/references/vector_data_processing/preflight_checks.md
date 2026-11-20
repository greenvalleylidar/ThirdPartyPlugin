# Vector Data Processing Preflight Check List

## Mandatory Checks

The following checks apply to all vector processing tools and must be completed before any operation:

| Check Item | Requirement | Check Command |
|-------|------|---------|
| File exists | Input files are accessible | `list_loaded_layers`, target URL in `layers[].url` -> PASS |
| File format | shp/gpkg (input), gpkg (output) | - |
| Coordinate system | All data coordinate systems are consistent -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS | `get_data_information` x N |
| Write permission | Output directory is writable -> manual confirmation | - |

---

## Tool Execution

### clip_vector_by_polygon (Vector Clipping)
- [ ] Input vector exists -> `list_loaded_layers`, target URL in `layers[].url` -> PASS
- [ ] Clipping polygon vector exists -> `list_loaded_layers`, target URL in `layers[].url` -> PASS
- [ ] Layer corresponding to clip_layer_name exists
- [ ] Both datasets have overlapping spatial extents -> `get_data_information` x N, compare `bounds`, intersection area > 0 -> PASS

### merge_vectors (Merge Vectors)
- [ ] At least 2 input files
- [ ] All input types are consistent (point/line/polygon)
- [ ] Attribute field structures are compatible

### remove_duplicate_vertices (Remove Duplicate Vertices)
- [ ] Input geometry type is line or polygon
- [ ] Geometry data is complete and error-free

### vector_smooth_lines (Line Smoothing)
- [ ] Input contains line or polygon features
- [ ] Line segments are long enough for smoothing

### set_z_from_raster (Terrain Conforming)
- [ ] Raster file exists -> `list_loaded_layers` or `get_data_information`, `code == 0` -> PASS
- [ ] Vector and raster coordinate systems match -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS
- [ ] Vector and raster extents overlap -> `get_data_information` x N, compare `bounds`, intersection area > 0 -> PASS
- [ ] band_number is within the valid range

### split_by_attribute (Split by Attribute)
- [ ] split_field exists
- [ ] Field values are suitable as filenames

### extract_multi_values_to_points (Extract Multiple Values to Points)
- [ ] Input is point features
- [ ] All raster files exist -> `list_loaded_layers` or `get_data_information`, `code == 0` -> PASS
- [ ] Points and raster extents overlap -> `get_data_information` x N, compare `bounds`, intersection area > 0 -> PASS

---

## Other

### Common Issues

| Issue | Cause | Solution |
|-----|------|---------|
| Output is empty | No extent overlap | Check coordinate system and extents |
| Attributes lost | Incompatible fields | Unify field structures |
| Abnormal Z values | Coordinate system mismatch | Unify coordinate systems |
| Split failed | Field name error | Check field name case sensitivity |

---

**Recommendation**: Use `platform-get_layer_details` to verify spatial extents before execution.
