# Preflight Check Flow

## Mandatory Checks

The following checks apply to all terrain analysis tools and must be completed before any operation:

1. Confirm the selected layer type is correct
2. Check prerequisites: ground points classified -> `preflight_check(check_item=0)`, `has_ground_points == true` -> PASS; DEM/DSM valid -> `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS; TIN valid -> `preflight_check(check_item=3)`, `is_tin == true` && `is_valid == true` -> PASS
3. Check parameter validity (resolution / contour interval, etc.)
4. Execute the tool
5. Check whether the output terrain file exists; if so, call get_data_information to obtain file information and verify that data type, spatial extent, resolution, or feature count meets expectations

---

## Tool Execution

### Surface Generation

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `generate_general_dem_from_pointcloud` | Point cloud type + ground points classified -> `preflight_check(check_item=0)`, `has_ground_points == true` -> PASS | "Please select the point cloud first" / "Please perform ground point classification first" |
| `generate_general_dsm_from_pointcloud` | Point cloud type | "Please select the point cloud first" |
| `generate_tiled_dem_from_pointcloud` | Point cloud type + ground points classified -> `preflight_check(check_item=0)`, `has_ground_points == true` -> PASS | "Please select the point cloud first" / "Please perform ground point classification first" |
| `generate_tiled_dsm_from_pointcloud` | Point cloud type | "Please select the point cloud first" |
| `generate_chm` | DEM valid -> `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS + DSM valid -> `preflight_check(check_item=2)` + overlap >= 90% + resolution/coordinate system consistent -> `get_data_information` x N, compare `coordinate_system` + `resolution_x`/`resolution_y` | "DEM/DSM does not exist" / "Insufficient extent overlap" / "Resolution or coordinate system mismatch" |
| `generate_dom_by_pixel_mode` | Imagery project + aligned + DSM/DEM valid -> `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS | "Please load the imagery project first" / "Images are not aligned" / "Missing DSM or DEM" |
| `point_cloud_to_tin` | Point cloud type + ground points classified -> `preflight_check(check_item=0)`, `has_ground_points == true` -> PASS | "Please select the point cloud first" / "Please perform ground point classification first" |
| `tin_generate_dem` | TIN valid -> `preflight_check(check_item=3)`, `is_tin == true` && `is_valid == true` -> PASS | "Please select the TIN first" |

### Contours

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `raster_to_contours` | DEM raster | "Please select the DEM first" |
| `generate_contour_from_pointcloud` | Point cloud + ground points classified -> `preflight_check(check_item=0)`, `has_ground_points == true` -> PASS | "Please select the point cloud first" / "Please perform ground point classification first" |
| `generate_contour_from_tin` | TIN valid -> `preflight_check(check_item=3)`, `is_tin == true` && `is_valid == true` -> PASS | "Please select the TIN first" |
| `generate_elevation_annotation` | Contours exist | "Please select contours first" |
| `merge_tiled_contours` | >=2 contour sheets | "Insufficient contour sheets" |
| `merge_breaklines` | >=2 breakline sheets | "Insufficient breakline sheets" |

### Terrain Derivatives (All Require DEM)

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `slope_analysis` | DEM valid -> `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS | "Please select the DEM first" / "DEM data is invalid" |
| `aspect_analysis` | DEM valid -> `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS | "Please select the DEM first" / "DEM data is invalid" |
| `roughness_analysis` | DEM valid -> `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS | "Please select the DEM first" / "DEM data is invalid" |
| `generate_hill_shade` | DEM valid -> `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS | "Please select the DEM first" / "DEM data is invalid" |
| `sky_view_factor` | DEM valid -> `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS | "Please select the DEM first" / "DEM data is invalid" |
| `viewshed_analysis` | DEM valid -> `preflight_check(check_item=2)` + observer point vector | "Please select the DEM first" / "Missing observer point vector" / "DEM data is invalid" |
| `annual_insolation` | DEM valid -> `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS | "Please select the DEM first" / "DEM data is invalid" |
| `solar_radiation` | DEM valid -> `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS | "Please select the DEM first" / "DEM data is invalid" |

### Hydrological Analysis (All Require Valid DEM)

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `drainage_analysis` | DEM valid -> `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS + NoData valid | "Please select the DEM first" / "DEM data is invalid" / "NoData value has issues" |
| `flooding_analysis` | DEM valid -> `preflight_check(check_item=2)` + river centerline vector + NoData valid | "Please select the DEM first" / "Missing river centerline" / "DEM data is invalid" / "NoData value has issues" |
| `generate_relative_elevation_model` | DEM valid -> `preflight_check(check_item=2)` + river centerline vector + sample_distance in 0.1~1000 range | "Please select the DEM first" / "Missing river centerline" / "DEM data is invalid" / "Sampling distance is invalid" |

### Multi-Temporal Analysis

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `pointcloud_change_detection` | 2 epoch point clouds + same coordinate system -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS + overlap >= 50% | "Insufficient data" / "Coordinate system mismatch" / "Insufficient extent overlap" |
| `pointcloud_deviation_analysis` | 2 epoch point clouds + same coordinate system -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS | "Insufficient data" / "Coordinate system mismatch" |
| `pointcloud_construction_progress_analysis` | 2 epoch point clouds + same coordinate system -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS | "Insufficient data" / "Coordinate system mismatch" |

### Other Terrain Tools

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `terrain_features` | DEM valid -> `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS | "Please select the DEM first" / "DEM data is invalid" |

### Quality Control

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `point_line_contradiction` | Contours + elevation annotations | "Missing contours or annotations" |
| `dem_edge_match` | >=2 DEM sheets + same coordinate system -> `get_data_information` x N, compare `coordinate_system` + same resolution -> `get_data_information` x N, compare `resolution_x`/`resolution_y` | "Insufficient DEM sheets" / "Coordinate system mismatch" / "Resolution mismatch" |
