# Point Cloud Processing Tools Registration
---

## Clipping/Splitting
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| clip_by_polygon | Extract all point cloud data within each polygon and save in one file or multiple files | Input data | - |
| clip_by_rectangle | Extract all point cloud data within each rectangle and save in one file or multiple files | LiData | coordinate_array |
| clip_by_circle | Extract all point cloud data within each 2D circle and save in one file or multiple files | LiData | coordinate_array |
| clip_by_draw_polygon | This function only allows extracting all point cloud data within each polygon drawn interactively in the viewer, and saving them to one or more files | LiData | polygon_list |
| tile_by_line | Draw a straight line on the Viewer, and divide the point cloud data into 2 data with this line as the boundary | LiData | start_point_x, start_point_y, end_point_x, end_point_y |

---

## Tiling/Division
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| tile_by_polygon | Read polygon information in vector data to generate a new point cloud file | Input data | buffer |
| tile_by_range | The point cloud data is divided into data of a certain size according to the set width and length and buffer size | LiData | width, length, merge |
| tile_by_point_number | Divide the point cloud data into data of a certain number of points according to the set number of points | LiData | point_number |
| pointcloud_subdivision | According to different scales, the point cloud can be divided into different picture frames by the rectangular framing method or the latitude and longitude framing method | LiData | subdivision_type, scale, buffer |

---

## Denoising/Smoothing
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| pointcloud_outlier_removal | Based on neighborhood distance statistics to eliminate outliers. A smaller threshold results in stronger denoising, suitable for removing isolated points, flyers, and sparse noise points | LiData | neighbor_points, multiples_of_std_deviation |
| pointcloud_noise_filter | By choosing appropriate parameters, noise can be removed and data quality improved | LiData | - |
| pointcloud_smooth | The laser point cloud can be smoothed based on the point's neighbors. Can make the appearance of the point cloud more consistent | LiData | select_class, max_fix_distance, search_radius, smoothing_type |

---

## Extraction/Filtering
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| extract_pointcloud_by_class | Extract point cloud by class | LiData | - |
| extract_pointcloud_by_elevation | Extract point cloud by elevation | LiData | - |
| extract_pointcloud_by_intensity | Extract point cloud by intensity | LiData | - |
| extract_pointcloud_by_return | Extract point cloud by return | LiData | - |
| extract_pointcloud_by_gps_time | Extract point cloud by gps time | LiData | - |
| extract_pointcloud_by_additional_attributes | Extract point cloud by additional attributes | LiData | - |
| split_pointcloud_by_attribute_label | Split a point cloud into separate files based on identical integer label values in a selected additional attribute | LiData | - |

---

## Normalization
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| normalize_by_ground_points | Point cloud normalization by ground points | LiData | - |
| normalize_by_dem | Point cloud normalization by dem | Input data | - |
| denormalize | Point cloud denormalization | LiData | - |


---

## Merging/Sampling
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| pointcloud_merge | Merge multiple point cloud files into one point cloud file | LiData | - |
| pointcloud_subsampling | Resample the point cloud to reduce the number of point clouds | LiData | sampling_type, from_class |

---

## Attribute Enhancement
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| pointcloud_vegetation_index | The vegetation index function does not generate new files. The generated normalized vegetation index or visible-band vegetation index information will be stored in the additional attributes of the point cloud.The normalized difference vegetation index(NDVI) requires near-infrared (NIR) and red (R) attributes in point cloud data.The visual band difference vegetation index requires that red (R), green (G) and blue (B) attributes exist in the point cloud data and are not all 0 | LiData | index_type |
| pointcloud_pcv | This feature generates PCV additional attributes of the point cloud, displayed according to the additional attributes PCV, which can be used to improve the point cloud visualization effect | LiData | - |
| extract_color_from_ortho_image | Using the extract color from ortho image function does not generate new data, map the color value RGB of the multi-band image data to the color value attribute of the corresponding point cloud data | Input data | - |
| extract_color_from_image_project | Using the extract color from image project function does not generate new data, map the color value RGB of the image project to the color value attribute of the corresponding point cloud data | Input data | - |
| brightness_contrast | Adjust the brightness and contrast of point cloud color | LiData | brightness, contrast |
| extract_spectral_values_from_image | Extract spectral values from multi-band images (including near-infrared) and map them to point cloud attributes. Supports selecting specific bands to save as additional attributes and outputting near-infrared bands | Input data | - |

---

## Boundary/Other
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| pointcloud_extract_boundary | Extract the boundary of the point cloud on the XY plane | LiData | - |
| transform_gps_time | Converting GPS time does not generate a new file; it only modifies the GPSTime attribute information.Converted from GPS-coordinated time to GPS-week-seconds, or GPS-week-seconds to GPS-coordinated time | LiData | - |
| segment_by_attribute | Segment point cloud into clusters based on spatial distance (Euclidean distance clustering). Each cluster is assigned a unique Group ID. Optional filters include classification and additional attributes. Statistics can be calculated for each cluster | LiData | search_radius, dimension, from_class |

---

## Common Parameter Explanation

### sampling_type (sampling type)
| Value | Method | Application scenario |
|---|------|---------|
| 0 | Minimum point spacing | Precise density control |
| 1 | Sampling rate (%) | Fast downsampling |
| 2 | Octree level | Structured downsampling(1-21) |

### scale (scale level)
| Value | Scale |
|---|-------|
| 0 | 1:500 |
| 1 | 1:1000 |
| 2 | 1:2000 |
| 3 | 1:5000 |
| 4 | 1:10000 |

### boundary_method (boundary extraction method)
| Value | Method | Characteristics |
|---|------|------|
| 0 | Convex hull | Grid-based boundary |
| 1 | Convex polygon | Minimum outer enclosing polygon |
| 2 | Concave polygon | Concave aggregation boundary |

### dimension (segmentation dimension)
| Value | Dimension | Explanation |
|---|------|------|
| 2 | 2D | Only horizontal(X-Y) distance |
| 3 | 3D | Full three-dimensional spatial distance |

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "pointcloud_processing-toolID"
