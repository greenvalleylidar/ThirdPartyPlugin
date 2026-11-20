# Preflight Check Flow

## Mandatory Checks

The following checks apply to all model data processing tools and must be completed before any operation:

1. Confirm file format is correct
2. Check file count >=2 (merge tools) -> check input array length >= 2
3. Check coordinate system consistency -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS
4. Validate parameter ranges (`smooth_meshes.smooth_iterations` is 1-50)
5. Execute the tool
6. Check whether the output model file exists; if so, call get_data_information to obtain file information and verify that model type, spatial extent, or object count meets expectations

---

## Tool Execution

### Model Merging

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `merge_libim_files` | >=2 LiBIM files + same coordinate system -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS | "Insufficient LiBIM file count" / "Coordinate system mismatch" |
| `merge_3dtiles` | >=2 tileset.json + overlapping extents -> `get_data_information` x N, compare `bounds`, intersection area > 0 -> PASS | "Insufficient tileset count" / "No extent overlap" |

### Model Optimization

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `smooth_meshes` | Triangulated mesh model (litin/obj) + `smooth_iterations` is 1-50 | "Model file does not exist" / "Iteration count out of range" |

---

## Other

### Common Error Handling

| Error | Cause | Solution |
|-----|------|---------| 
| "Insufficient file count" | Fewer than 2 input files | Ensure at least 2 inputs |
| "Coordinate system mismatch" | Merged data uses different coordinate systems | Perform coordinate transformation first |
| "Iteration count exceeded" | smooth_iterations not in 1-50 | Set to an integer between 1-50 |
| "Format not supported" | Not .litin/.obj/.libim format | Convert to a supported format |
