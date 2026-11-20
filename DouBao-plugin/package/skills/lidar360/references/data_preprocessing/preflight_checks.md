# Preflight Check Flow

## Mandatory Checks

The following checks apply to all data preprocessing tools and must be completed before any operation:

1. Confirm point cloud data format is correct (lidata)
2. Confirm raster data format is correct (tif/tiff/img/dat, image registration)
3. Check coordinate system consistency (multi-temporal data) -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS
4. Check whether extents overlap (elevation difference analysis, registration) -> `get_data_information` x N, compare `bounds`, intersection area > 0 -> PASS
5. Validate trajectory file format and count (strip overlap and trajectory quality analysis) -> check file extensions (.traj/.pos/.out) + file count matches
6. Validate DJI user_token validity (UAV processing) -> call `dji_cloud_reconstruction`, not a "missing DJI cloud service token" error -> PASS
7. Execute the tool
8. Check whether the output HTML report path exists -> manual confirmation; if it exists, open or read the report summary, verify that the report title, statistics, and anomaly flags meet expectations

---

## Tool Execution

### Quality Check Tools

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `density_quality_analysis` | >=1 point cloud (lidata format) | "Please load point cloud data first" |
| `strip_overlap_analysis` | >=2 point clouds (lidata format) + >=1 trajectory file (traj/pos/out) + overlap_threshold in (0,100] range | "Insufficient point cloud count" / "Missing trajectory file" / "Invalid overlap threshold" |
| `trajectory_quality_analysis` | >=1 trajectory file (traj/pos/out) + output HTML path is writable | "Missing trajectory file" / "Output path is not writable" |
| `elevation_difference_inspection` | >=2 point clouds (lidata format) + same coordinate system -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS + overlapping extents -> `get_data_information` x N, compare `bounds`, intersection area > 0 -> PASS | "Insufficient point cloud count" / "Coordinate system mismatch" / "No extent overlap" |

### Registration Tools

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `auto_registration` | >=2 point clouds (lidata format) + expected overlap extent | "Insufficient point cloud count" / "Missing reference point cloud" / "Missing point cloud to register" |
| `auto_image_registration` | >=2 raster files (tif/tiff/img/dat format) + reference raster and raster to register | "Insufficient raster count" / "Missing reference raster" / "Missing raster to register" |

### Adjustment Tools

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `trajectory_adjustment` | Trajectory file + point cloud + coordinate system known | "Missing trajectory file" / "Missing point cloud data" / "Coordinate system not defined" |

### UAV Processing

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `dji_cloud_reconstruction` | DJI user_token + raw data directory | "Missing DJI cloud service token" / "Invalid raw data directory" |

---

## Other

### Common Error Handling

| Error | Cause | Solution |
|-----|------|---------| 
| "Point cloud format not supported" | Not .lidata format | Convert to lidata format |
| "Raster format not supported" | Not tif/tiff/img/dat format | Convert to a supported raster format |
| "Coordinate system mismatch" | Multi-temporal data uses different coordinate systems | Perform coordinate transformation first |
| "DJI authentication failed" | Invalid user_token | Check cloud service token configuration |
| "Trajectory file missing" | No trajectory file provided | Import trajectory data |

### Key Configuration Notes

DJI L1/L2/L3 reconstruction requires a valid DJI cloud service token:
- `user_token`: Cloud service token for the DJI drone application

How to obtain: Get it from the DJI developer platform or the corresponding cloud service
