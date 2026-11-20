# Terrain Analysis Tools Registration
---

## Terrain Surface Generation
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| generate_general_dem_from_pointcloud | Generate general DEM (Digital Elevation Model) from point cloud data | LiData | x_size, y_size, interpolator |
| generate_general_dsm_from_pointcloud | Generate general DSM (Digital Surface Model) from point cloud data | LiData | from_class, x_size, y_size, return_number |
| generate_tiled_dem_from_pointcloud | Generate tiled DEM (Digital Elevation Model) from point cloud data | LiData | x_size, y_size, interpolator, scale |
| generate_tiled_dsm_from_pointcloud | Generate tiled DSM (Digital Surface Model) from point cloud data | LiData | from_class, x_size, y_size, interpolator, return_number, scale |
| generate_chm | Generate CHM from DSM and DEM | Input data | - |
| generate_dom_by_pixel_mode | This function uses the results of an aerotriangulation project to generate DOM.Pixel Mode Only (Each pixel individually searches for the most suitable image) | Input data | resolution_mode, auto_gsd, manual_gsd |
| point_cloud_to_tin | Generate TIN (Triangulated Irregular Network) from point cloud | Input data | from_class, tile_type |
| tin_generate_dem | Generate DEM from TIN (Triangulated Irregular Network) | Input data | - |

---

## Contour Generation
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| raster_to_contours | Generate contours from DEM | TIF/TIFF | interval, base |
| generate_contour_from_pointcloud | Generate contour lines from point cloud | Input data | - |
| generate_contour_from_tin | Generate contour lines from TIN | Input data | minor_spacing, basic_spacing, major_spacing, gener_height_spread_point, gen_spread_method |
| generate_elevation_annotation | Generate elevation annotations base on pointcloud and contour | Input data | - |
| merge_tiled_contours | Merge tiled/contour segments | Input data | - |
| merge_breaklines | Merge tiled breaklines into a single file | Input data | - |

---

## Terrain Derivatives
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| slope_analysis | Calculate slope from DEM | TIF/TIFF/IMG/DAT | z_scale |
| aspect_analysis | Calculate aspect from DEM | TIF/TIFF/IMG/DAT | z_scale |
| roughness_analysis | Calculate roughness from DEM | TIF/TIFF/IMG/DAT | - |
| generate_hill_shade | Generate hill shade (shaded relief) from DEM | TIF/TIFF/IMG/DAT | azimuth, altitude, z_scales |
| sky_view_factor | Sky view factor can reflect the degree to which the surrounding terrain obscures the sky | TIF/TIFF | - |
| viewshed_analysis | Viewshed analysis is used to calculate the visibility within a certain range around viewpoints | Input data | - |
| annual_insolation | Annual sunshine is used to estimate the annual sunshine in a certain area and can be used to evaluate the trend of annual sunshine in that area | TIF/TIFF | - |
| solar_radiation | Solar radiation analysis calculates the amount of solar radiation received by the terrain surface based on location, time, and atmospheric conditions | TIF/TIFF | - |

---

## Hydrological Analysis
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| fill_sinks | Eliminates pseudo-depressions and repairs elevation sinks in DEM rasters, producing depression-free DEM data for hydrological and terrain modeling analysis | Input data | - |
| flow_direction | Create a raster of the flow direction from each cell to its downslope neighbor using the D8 method | Input data | - |
| flow_accumulation | Computes upstream drainage accumulation for every cell using a flow direction raster | Input data | - |
| channel_network | Derives a channel network based on gridded digital elevation data | Input data | - |
| drainage_analysis | Drainage analysis based on DEM data | TIF/TIFF | - |
| flooding_analysis | Flooding analysis is a common application of hydrogeological information systems used to simulate and predict areas that may be affected by flooding during flood events | Input data | - |
| generate_relative_elevation_model | Generate relative elevation model from DEM and river centerline vector data | DEM + vector | - |

---

## Multi-temporal Analysis
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| pointcloud_change_detection | Detect changes between two epochs of point cloud data | Input data | cell_size |
| pointcloud_deviation_analysis | Deviation analysis between two point cloud data(3D) | Input data | cell_size, min_distance, max_distance |
| pointcloud_construction_progress_analysis | Construction progress analysis based on point clouds | Input data | - |


---

## Quality Control
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| point_line_contradiction | Detect contradictions between elevation annotation points and contour lines | Input data | - |
| dem_edge_match | Perform edge matching on multiple DEMs to ensure elevation consistency at the boundaries | Input data | - |

---

## Other Terrain Tools
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| terrain_features | Generate multiple terrain feature rasters (slope, aspect, hillshade, roughness) from DEM | TIF/TIFF/IMG/DAT | - |
| create_dem_dsm_for_dom | Automated image workflow for DSM/DEM generation used by DOM processing | Input data | - |

---

## Common Parameter Explanation

### from_class (point cloud class)
| Value | Class |
|---|------|
| 2 | Ground (ground points) - Common for DEM generation |
| 1 | Unclassified |
| 3-5 | Vegetation (vegetation) |
| 6 | Building |
| 38 | Road |

### interpolator (interpolation method)
| Value | Method | Application scenario |
|---|------|---------|
| 0 | IDW | Fast, general precision |
| 1 | Kriging | High precision, smooth |
| 2 | TIN | Preserves terrain features |

### scale (scale level)
| Value | Scale |
|---|-------|
| 0 | 1:500 |
| 1 | 1:1000 |
| 2 | 1:2000 |
| 3 | 1:5000 |

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "terrain_analysis-toolID"
