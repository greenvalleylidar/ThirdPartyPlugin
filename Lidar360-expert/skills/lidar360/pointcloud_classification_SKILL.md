---
name: lidar360-pointcloud-classification
description: LiDAR360 point cloud classification module, updated from references/pointcloud_classification/tools.md, covering Ground Classification, Noise and Outlier Classification, Object-based Classification, Attribute-based Classification, Region and Mask Classification, Machine Learning Classification, Road Extraction and Training.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

In-place write classification tools and model training both execute at L3: show the input, class mapping, impact scope, and training output, suggest a backup, and obtain explicit confirmation; do not promise cancellation, recovery, or a checkpoint when the interface does not declare one.

# Point Cloud Classification Module (pointcloud_classification)

> This skill index is synchronized from the Markdown documents under `references/pointcloud_classification/`; the tool list is defined by `tools.md`.

---

## Detailed Documentation Index

| Document | Content | View |
|---------|---------|------|
| **Tool Registry** | Tool grouping, functions, input formats and key parameters | `read_file('references/pointcloud_classification/tools.md')` |

---

## Tool Group Quick Reference

### Ground Classification
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `classify_ground_by_csf` | CSF ground point classification | LiData | classify_threshold, do_postprocessing, from_class, grid_size, input_data, max_iterations, scene_type, to_class |
| `classify_ground_by_deep_learning` | Deep learning ground point classification | LiData | from_class, input_data, to_class, use_gpu |
| `classify_ground_by_progressive_tin_densification` | Progressive TIN densification ground point classification | LiData | from_class, grid_size, input_data, iteration_angle, iteration_distance, max_building_size, max_terrain_angle, tolerance_above, tolerance_below |
| `extract_median_ground_points` | Extract a smoother median layer from thick ground points | LiData | from_class, grid_size, input_data, maximum_height, minimum_height, standard_deviations, to_class |

### Noise and Outlier Classification
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `classify_noise_points` | Noise point classification | LiData | from_class, input_data, radius, radius_search_method, remove_isolated_points_flag, standard_deviations, to_class |
| `classify_isolated_points` | Isolated point classification | LiData | from_class, minimum_points, radius, to_class |
| `classify_low_points` | Separate low points | LiData | from_class, height_difference, input_data, points_number, radius, to_class |
| `classify_closeby_points` | Classify points close to another selected class | LiData | closeby_class, from_class, input_data, radius, search_method, to_class |

### Object-based Classification
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `classify_buildings` | Building classification | LiData | angle_threshold, buffer_size, building_class, distance_tolerance, from_class, height_above_ground, input_data, max_slope, minimum_building_area, minimum_points_number, search_radius, wall_class |
| `classify_water_points` | Classify water points and extract water boundaries | LiData | density, from_class, grid_size, input_data, min_area, to_class |
| `classify_air_points` | Air noise point classification | LiData | from_class, input_data, neighbor_points_number, standard_deviations, to_class |
| `classify_below_surface_points` | Classify points below the surface | LiData | from_class, input_data, standard_deviations, to_class, z_tolerance |
| `classify_top_surface` | Reclassify the highest surface points for DSM generation | LiData | ground_class, ground_space, input_data, roof_class, roof_space, to_class, vegetation_class, vegetation_space |
| `classify_model_key_points` | Thin classified points while preserving terrain model key points | LiData | from_class, grid_size, input_data, to_class, tolerance_above, tolerance_below |
| `classify_tunnel_points` | Classify tunnel point cloud using deep learning model (tunnel wall/ventilation pipe/cable/debris/noise) | LiData | batch_size, input_data, is_use_gpu, weight_name |

### Attribute-based Classification
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `classify_by_attribute` | Classify points by built-in attributes such as elevation, intensity, GPS time, scan angle, or return number | LiData | attribute, from_class, input_data, max_value, min_value, to_class |
| `classify_by_additional_attribute` | Classify points by additional_attributes (input point cloud must contain additional attributes; min_value/max_value are required with min_value <= max_value; from_class defaults to all classes) | LiData | additional_attribute, from_class, input_data, max_value, min_value, to_class |
| `classify_by_height_above_ground` | Classify points by height above terrain surface | LiData | from_class, input_data, max_height, min_height, to_class |
| `classify_by_min_elevation_difference` | Classify points by elevation difference to the local minimum point | LiData | from_class, input_data, max_elevation_difference, min_elevation_difference, radius, to_class |
| `classify_by_tree_attributes` | Classify by tree attributes | LiData + tree attribute file | from_class, input_data, pointcloud_files, query_string, to_class, tree_attribute_file |

### Region and Mask Classification
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `classify_by_region` | Classify points within polygons from source class to target class | LiData + polygon region | calculate_polygon_topological_flag, from_class, input_data, pointcloud_files, to_class, vector_file |
| `classify_by_mask` | Classify by mask | LiData + mask raster | from_class, input_data, mask_class, mask_file, pointcloud_files, target_class |
| `classify_by_trained_ml_model` | Classify by machine learning model | LiData + VCM model | from_class, input_data, model_file, pointcloud_files |

### Machine Learning Classification
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `classify_by_deep_learning` | Classify point clouds using built-in deep learning segmentation models for multiple scenes | LiData | billboard_class, building_class, car_class, dynamic_car_class, from_class, guardrail_class, height_above_ground, high_vegetation_class, input_data, low_vegetation_class, pole_class, powerline_class, scene_type, static_car_class, tower_class, use_gpu, vegetation_class |
| `classify_low_and_high_vegetation` | Classify low and high vegetation from TLS forest point cloud data using a deep learning segmentation model | LiData | from_class |
| `classify_by_machine_learning` | Classify point cloud by random forest and generate classified data and model output | LiData | from_class, input_data, max_building_size, min_building_height, output_data, pointcloud_files, training_class, training_files |
| `classify_using_trained_point_cloud_model` | Classify using trained point cloud model | LiData + model | batch_size, input_data, model, task_name, weight_name |
| `classify_using_trained_pano_image_tree_classification_model` | Classify tree species from panoramic images using a trained model | Panoramic images | batch_size, input_data, model, task_name, weight_name |

### Model Training
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `train_point_cloud_classification_model` | Train point cloud classification model using deep learning | LiData | batch_size, epochs, learning_rate, model, model_type, output_data, task_name, training_data, validation_data |
| `train_pano_image_tree_classification_model` | Train panoramic image tree species classification model | Panoramic images | batch_size, epochs, learning_rate, model, model_type, output_data, task_name, training_data, validation_data |

### Road Extraction and Training
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `extract_roads_by_deep_learning` | Extract road polygons and road mask images by deep learning | LiData | douglas_distance_threshold, douglas_simplification_flag, input_data, output_data, road_length_threshold |
| `train_image_classification_model` | Train image classification model | training images | input_data, model_list, training, data_enhancement, class_conversion_setting, preprocess_transform, task_name, task_description |

---

## Common Parameters Index

| Configuration File | Content | View |
|-------------------|---------|------|
| **File Formats** | Point cloud, raster, vector, model format references | `read_file('references/profiles/file_formats.md')` |
| **Point Cloud Class Codes** | ASPRS/LiDAR360 common class codes | `read_file('references/profiles/class_codes.md')` |
| **Interpolation Methods** | DEM/DSM/raster generation common interpolation methods | `read_file('references/profiles/interpolation.md')` |
| **Scale** | Terrain, contour, and mapping scale references | `read_file('references/profiles/scale.md')` |

---

## Invocation Conventions

- Quick invocation: `pointcloud_classification-toolID`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "pointcloud_classification-toolID"`
- Detailed parameters are subject to the tool schema. Before execution, verify input data format and coordinate system.
