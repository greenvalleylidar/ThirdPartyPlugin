# Preflight Check Procedures

## Mandatory Checks

The following check items apply to all point cloud processing tools and must be completed before executing any operation:

1. Confirm the selected layer type is point cloud
2. Check if point cloud attributes meet requirements (RGB/NIR/GPSTime, etc.)
3. Check if prerequisites are met: ground points classified -> `preflight_check(check_item=0)`, `has_ground_points == true` -> PASS; DEM valid -> `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS
4. Check parameter validity (range/threshold/size, etc.)
5. Execute tool
6. Check if the output point cloud file exists; if so, call get_data_information to get file info, and verify point count, classification, attribute fields, or spatial extent match expectations

---

## Tool Execution

### Clipping/Splitting

| Tool | Check Items | Failure Message |
|-----|-------------|----------------|
| `clip_by_polygon` | Point cloud type + vector polygon | "Please select a point cloud first" / "Please load a vector polygon first" |
| `clip_by_rectangle` | Point cloud type + valid coordinate range | "Please select a point cloud first" / "Invalid coordinate range (x_min < x_max)" |
| `clip_by_circle` | Point cloud type + radius > 0 | "Please select a point cloud first" / "Radius must be greater than 0" |
| `clip_by_draw_polygon` | Point cloud type + polygon drawn | "Please select a point cloud first" / "Please draw a polygon first" |
| `tile_by_line` | Point cloud type + two points not coincident | "Please select a point cloud first" / "Start and end points cannot coincide" |

### Tiling/Cutting

| Tool | Check Items | Failure Message |
|-----|-------------|----------------|
| `tile_by_polygon` | Point cloud type + vector polygon | "Please select a point cloud first" / "Please load a vector polygon first" |
| `tile_by_range` | Point cloud type + width/length > 0 | "Please select a point cloud first" / "Invalid tile size" |
| `tile_by_point_number` | Point cloud type + point count > 0 | "Please select a point cloud first" / "Point count must be greater than 0" |
| `pointcloud_subdivision` | Point cloud type + valid scale | "Please select a point cloud first" / "Invalid scale" |

### Denoising/Smoothing

| Tool | Check Items | Failure Message |
|-----|-------------|----------------|
| `pointcloud_outlier_removal` | Point cloud type + neighbor_points >= 3 | "Please select a point cloud first" / "Insufficient neighborhood points" |
| `pointcloud_noise_filter` | Point cloud type | "Please select a point cloud first" |
| `pointcloud_smooth` | Point cloud type + search_radius > 0 | "Please select a point cloud first" / "Invalid search radius" |

### Extraction/Filtering

| Tool | Check Items | Failure Message |
|-----|-------------|----------------|
| `extract_pointcloud_by_class` | Point cloud type + class selection | "Please select a point cloud first" / "Please select extraction class" |
| `extract_pointcloud_by_elevation` | Point cloud type + valid elevation range | "Please select a point cloud first" / "Invalid elevation range" |
| `extract_pointcloud_by_intensity` | Point cloud type + valid intensity range | "Please select a point cloud first" / "Invalid intensity range" |
| `extract_pointcloud_by_return` | Point cloud type + return selection | "Please select a point cloud first" / "Please select return number" |
| `extract_pointcloud_by_gps_time` | Point cloud type + valid time range | "Please select a point cloud first" / "Invalid time range" |
| `extract_pointcloud_by_additional_attributes` | Point cloud type + additional attribute selection | "Please select a point cloud first" / "Please select additional attribute" |
| `split_pointcloud_by_attribute_label` | Point cloud type + split label attribute | "Please select a point cloud first" / "Missing split label attribute" |
| `segment_by_attribute` | Point cloud type + search_radius > 0 | "Please select a point cloud first" / "Invalid search radius" |

### Normalization

| Tool | Check Items | Failure Message |
|-----|-------------|----------------|
| `normalize_by_ground_points` | Point cloud type + ground points classified -> `preflight_check(check_item=0)`, `has_ground_points == true` -> PASS | "Please select a point cloud first" / "Please classify ground points first" |
| `normalize_by_dem` | Point cloud type + valid DEM -> `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS + range overlap -> `get_data_information` x N, compare `bounds`, intersection area > 0 -> PASS | "Please select a point cloud first" / "DEM does not exist" / "Ranges do not overlap" |
| `denormalize` | Point cloud type (already normalized) | "Please select a normalized point cloud first" |

### Merging/Sampling

| Tool | Check Items | Failure Message |
|-----|-------------|----------------|
| `pointcloud_merge` | >= 2 point clouds + same coordinate system -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS | "Insufficient point cloud count" / "Coordinate systems are inconsistent" |
| `pointcloud_subsampling` | Point cloud type + valid sampling_type | "Please select a point cloud first" / "Invalid sampling type" |

### Attribute Enhancement

| Tool | Check Items | Failure Message |
|-----|-------------|----------------|
| `pointcloud_vegetation_index` | Point cloud type + NIR/RGB attributes | "Please select a point cloud first" / "Missing NIR or RGB attributes" |
| `pointcloud_pcv` | Point cloud type | "Please select a point cloud first" |
| `extract_color_from_ortho_image` | Point cloud type + orthophoto image + range overlap -> `get_data_information` x N, compare `bounds`, intersection area > 0 -> PASS | "Please select a point cloud first" / "Image does not exist" / "Ranges do not overlap" |
| `extract_color_from_image_project` | Point cloud type + image project (liaep) | "Please select a point cloud first" / "Image project does not exist" |
| `brightness_contrast` | Point cloud type + RGB attributes | "Please select a point cloud first" / "Point cloud has no RGB attributes" |
| `extract_spectral_values_from_image` | Point cloud type + multi-band image + range overlap -> `get_data_information` x N, compare `bounds`, intersection area > 0 -> PASS | "Please select a point cloud first" / "Image does not exist" / "Ranges do not overlap" |

### Boundary/Other

| Tool | Check Items | Failure Message |
|-----|-------------|----------------|
| `pointcloud_extract_boundary` | Point cloud type | "Please select a point cloud first" |
| `transform_gps_coordinated_time_to_gps_week_seconds` | Point cloud type + GPSTime attribute | "Please select a point cloud first" / "Point cloud has no GPS time attribute" |
| `transform_gps_week_seconds_to_gps_coordinated_time` | Point cloud type + GPSTime attribute + surveydate | "Please select a point cloud first" / "Point cloud has no GPS time attribute" / "Invalid survey date" |

---

## Other

### Output Path Check

All tools require specifying an output path. It is recommended to check:
- Whether the output directory exists
- Whether disk space is sufficient
- Whether file naming follows conventions
