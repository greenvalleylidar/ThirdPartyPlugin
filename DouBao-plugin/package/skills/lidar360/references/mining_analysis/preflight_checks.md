# Mining Analysis Preflight Check Flow

## Mandatory Checks

The following checks apply to all mining analysis tools and must be completed before any operation:

1. Confirm input point cloud is readable, coordinates, units, and elevation range are normal -> `get_data_information` check `code == 0` and `bounds` are reasonable
2. Decide whether to perform denoising, resampling, and smoothing based on point cloud quality -> manual confirmation
3. Check ground point classification results, confirm slope benches and slope faces have not been erroneously removed -> `preflight_check(check_item=0)` check `has_ground_points`
4. After generating TIN/OBJ, check the triangulated mesh: holes, spikes, excessively long triangle edges, over-smoothing -> `preflight_check(check_item=3)` check `is_tin && is_valid`; holes/spikes require manual confirmation
5. Set slope angle and minimum line length thresholds -> schema numeric range validation
6. Execute slope top and toe line extraction
7. Validate output DXF/SHP: line segment continuity, slope top/toe positions, coordinates are correct -> manual confirmation

---

## Tool Execution

### Extract Slope Top and Toe Lines from Point Cloud

| Check Item | Verification Method | Failure Message |
|--------|---------|---------|
| Input OBJ/LiTin triangulated mesh model exists and is readable | `get_data_information` check `code == 0` | "Please generate the triangulated mesh model first" |
| Mesh coordinates, units, and range are normal, no large-area holes or abnormal spikes | `preflight_check(check_item=3)` check `is_tin && is_valid`; holes/spikes require manual confirmation | "Insufficient mesh quality" |
| Slope angle range is valid: `min_slope_angle < max_slope_angle` | Schema numeric range validation | "Slope angle range is invalid" |
| `min_length > 0` | Schema numeric range validation | "Minimum line length threshold is invalid" |
| Output format is DXF or SHP | Schema `suffix_name` comparison | "Output format is invalid" |

### Extract Slope Lines from Existing Model

| Tool | Check Item | Verification Method | Failure Message |
|-----|--------|---------|---------|
| `extract_toes_and_crests` | OBJ/LiTin coordinates, units, and range are normal | `get_data_information` check `code == 0` and `bounds` are reasonable | "Model coordinates or units are abnormal" |
| `extract_toes_and_crests` | Mesh has no large-area holes or spikes | `preflight_check(check_item=3)` check `is_valid`; holes/spikes require manual confirmation | "Insufficient mesh quality" |
| `extract_toes_and_crests` | Model represents real slope benches | Manual confirmation (no read-only tool can verify model semantic quality) | "Model lacks valid slope structures" |

### Tunnel Analysis

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `extract_tunnel_centerline` | OBJ triangulated mesh model exists | "Please generate the triangulated mesh model first" |
| `compute_normal_vectors` | Point cloud exists and road/tunnel area is valid | "Please load point cloud data first" / "Area is invalid" |

### Surface Reconstruction

| Tool | Check Item | Verification Method | Failure Message |
|-----|--------|---------|---------|
| `surface_reconstruction` | Point cloud exists and necessary denoising is complete | `get_data_information` check `code == 0`; denoising quality requires manual confirmation | "Please load point cloud data first" / "Denoising recommended first" |
| `surface_reconstruction` | `select_class` matches the target feature class | `get_data_information` check `present_classes` contains target class | "Modeling class not set" |

---

## Other

### Common Error Handling

| Error | Cause | Solution |
|-----|------|---------| 
| "Insufficient mesh quality" | Low point cloud density, high noise, or TIN has holes | Improve point cloud quality, reduce `max_triangle_edge`, check model smoothing |
| "Output is empty" | Slope angle range too narrow or input model has no obvious slopes | Widen `min_slope_angle/max_slope_angle`, check OBJ/LiTin |
| "Too many slope line fragments" | Model noise is high or `min_length` is too small | Increase model smoothing passes, raise `min_length` |
| "Slope line offset" | Point cloud smoothing/resampling overdone or classification errors | Reduce preprocessing intensity, recheck ground point classification |
| "Output format is invalid" | `save_format` does not match output suffix | DXF uses `save_format=0`, SHP uses `save_format=1` |
