# Data Preprocessing Tools Registration
---

## Data Registration and Adjustment
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| auto_registration | Automatically register and align point cloud data from two scans using feature matching and optional ICP refinement | Input data | - |
| auto_image_registration | Automatically match image features, build a parameter fitting model, and register the align image to the reference image | Input data | - |
| trajectory_adjustment | Corrects trajectory to reduce layering between point clouds and improve their quality. Additionally supports bundle adjustment that integrates image projects with point clouds to enhance overall data accuracy. Outputs refined point clouds and/or image project files | Input data | adjust_x, adjust_y, adjust_z, adjust_roll, adjust_pitch, adjust_heading, flight_data, adjust_time_interval |

---

## Data Splitting and Cutting
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| auto_split_trajectory | Automatically split the trajectory into segments based on heading change, duration, and length thresholds | POS/TRAJ | max_heading_change, min_duration, min_length |
| cut_overlap | Classify or delete overlap points based on scan angle or offset angle relative to the trajectory line | Input data | type, method_type, edge, density, to_class, from_class |
| cut_point_cloud_by_trajectory | Cut point cloud data along the trajectory line with an optional buffer width | Input data | enable_buffer |

---

## Quality Analysis and Reconstruction
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| density_quality_analysis | For analyzing the density distribution of the point cloud data. There are four density levels by default, and density threshold ranges can be added or deleted as needed.analysis report will output | LiData | grid_size, upper_values, report_title, render_colors |
| strip_overlap_analysis | Analyze the overlap ratio between point cloud datasets and export an HTML report | Point cloud files and trajectory files | overlap_threshold |
| trajectory_quality_analysis | Check flight trajectory quality, including flight height, speed and attitude analysis, and export an HTML report | TRAJ/POS/OUT | - |
| dji_cloud_reconstruction | DJI Cloud Reconstruction supports data processing for the Zenmuse L1/L2/L3. It can convert raw LiDAR files from the L1/L2/L3 into 3D point cloud data in multiple formats, including PNTS, LAS, PLY, PCD, and S3MB. The tool also offers point cloud classification and digital elevation model (DEM) generation. Users can import the resulting datasets into downstream analysis software for surveying, power line inspection, and other industry applications | DJI Raw LiDAR Data Directory | user_token |

---

## Data Inspection
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| elevation_difference_inspection | For analyzing elevation differences between point cloud data,outputting analysis reports | LiData | grid_size, elevation_difference_threshold |

---

## Common Parameter Explanation

### Registration Methods
| Method | Description | Accuracy |
|---|------|---------|
| ICP | Iterative Closest Point | High |
| Feature_Based | Feature matching | Medium |
| Point_Cloud | Point cloud registration | High |
| Trajectory | Trajectory based | Medium |

### Quality Metrics
| Metric | Description | Good Range |
|---|------|---------|
| Point_Density | Points per square meter | >100 pts/m2 |
| Overlap | Overlap percentage | 30-60% |
| Elevation_Diff | Elevation difference | <10 cm |
| Trajectory_Accuracy | GPS accuracy | <5 cm |

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "data_preprocessing-toolID"
