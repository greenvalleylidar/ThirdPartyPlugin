# Forestry Airborne Tools Registration
---

## Tree Segmentation
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| individual_tree_crown_segmentation | Individual Tree Crown Segmentation | TIFF/TIF/JPG/JPEG/BMP/PNG | overlap_ratio, confidence_threshold |
| trunk_based_tree_segmentation | Extract tree trunks from airborne LiDAR and perform individual tree segmentation based on the trunks, optimized for eucalyptus | LiData | from_class, trunk_class, foliage_class, use_gpu_first, height_above_ground, min_tree_height, optimize_color |
| generate_seed_points_from_chm | Obtain the location information of individual trees through CHM as seed points | TIFF/TIF | maximum_tree_height, minimum_tree_height, buffer_size, is_smooth, sigma, radius_pix |
| pointcloud_segmentation_from_seed_points | Perform individual tree segmentation on point cloud based on seed point file | Input data | from_class, height_above_ground, min_tree_height, optimize_color |
| individual_tree_segmentation | Point cloud segmentation algorithms determine individual trees to be segmented by analyzing the elevation values of points and their distances from other points, obtaining attributes such as individual tree location, tree height, crown diameter, crown area, and crown volume | LiData | from_class, grid_size, buffer_size, height_above_ground, is_smooth, sigma, radius_pix, chm_pits_filling, min_tree_height, optimize_color |

---

## Forest Metrics
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| calculate_forest_metrics_by_grid | Divide the point cloud into multiple grids, and calculate the point cloud forest parameters for each grid | Input data | is_select_elevation_metrics, is_select_intensity_metrics, is_select_canopy_cover, is_select_gap_fraction, is_select_leaf_area_index, from_class, x_grid_size, y_grid_size, height_break, extinction_coefficient, output_type |
| calculate_forest_metrics_by_polygon | Given a polygon extent,compute forest parameters for the points within the polygon | Input data | is_select_elevation_metrics, is_select_intensity_metrics, is_select_canopy_cover, is_select_gap_fraction, is_select_leaf_area_index, from_class, height_break, extinction_coefficient |
| calculate_forest_metrics_by_forest_stands | Treat the whole input point cloud as one forest stand to calculate forest structural parameters | LiData | is_select_elevation_metrics, is_select_intensity_metrics, is_select_canopy_cover, is_select_gap_fraction, is_select_leaf_area_index, from_class, height_break, extinction_coefficient |

---

## Tree Attribute Statistics
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| als_individual_tree_attribute_statistics | Mainly used for recalculating and adding attributes of individual tree point cloud | Input data | select_attribute_to_statistic, height_above_ground, min_tree_height, stem_class, is_updating, delete_unstatistic_tree_when_update, new_file_suffix, als_or_tls_datatype |
| extract_tree_crown_boundaries | Generate crown boundary vectors for individual trees from segmented tree point clouds | LiData | method |

---

## CHM Processing
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| chm_pits_filling | Perform pit filling on CHM without affecting the original non-pit canopy height values | TIFF/TIF | chm_pits_filling_threshold_pix |
| chm_segmentation | Use watershed algorithm to identify and segment individual trees | TIFF/TIF | maximum_tree_height, minimum_tree_height, buffer_size, is_smooth, sigma, radius_pix, chm_pits_filling, crown_base_height_threshold |

---

## Regression and Prediction
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| linear_regression | Linear regression is a linear approach for modeling the relationship between a scalar response and one or more explanatory variables | Input data | dependent_variable, plot_type, radius, x_index, y_index, k_fold, optimize, local_error_buffer, save_model, save_dataset, csv_header_list, report_name, dependent_variable_index |
| random_forest_regression | Random Forest regression is an ensemble learning method that operates by constructing a multitude of decision trees at training time and outputting the mean prediction of the individual trees | Input data | dependent_variable, plot_type, radius, x_index, y_index, k_fold, optimize, local_error_buffer, save_model, save_dataset, csv_header_list, report_name, dependent_variable_index, rf_tree_num, rf_depth, rf_min_split, rf_min_leaf |
| svm_regression | Support Vector Machine regression is a supervised learning algorithm that analyzes data for regression analysis | Input data | dependent_variable, plot_type, radius, x_index, y_index, k_fold, optimize, local_error_buffer, save_model, save_dataset, csv_header_list, report_name, dependent_variable_index, svm_degree, svm_gamma, svm_kernel_type, svm_type |
| fann_regression | Fast Artificial Neural Network regression uses multilayer neural networks for regression analysis | Input data | dependent_variable, plot_type, radius, x_index, y_index, k_fold, optimize, local_error_buffer, save_model, save_dataset, csv_header_list, report_name, dependent_variable_index, fann_momentum, fann_learning_rate |
| regression_prediction | Predicts values using a trained regression model | Input data | plot_type, radius, csv_header_list, report_name |

---

## Forest Stand and Change Analysis
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| forest_stands_delineating | Extract forest stand from Canopy Height Model | TIF/TIFF | method, cell_size, min_stand_area, min_height, max_height |
| forest_structure_change_detection | Quantify forest structural changes at multiple scales | Input data | x_size, y_size, height_break |

---

## TreeID and Data Management
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| generate_tree_model | Generate tree model data based on individual tree attribute data and tree species model | TreeDB | tree_modes_list |
| its_mosaicing | Perform edge matching on several patches after individual tree segmentation | Input data | - |
| auto_registration_forest | Automatically register forest point clouds collected from different platforms,such as airborne UAV,and handled LiDAR | Input data | - |
| clear_tree_id | Clear TreeID under specified conditions | LiData | filter_by_height, min_height, max_height |
| als_clear_treeid_by_file | Input table file containing TreeID values, then clear matching TreeID labels from the point cloud | Input data | - |
| extract_by_tree_id | Extract point cloud under specified conditions by TreeID | Input data | filter_by, extract_to, output_format |

---

## Common Parameter Explanation

### Forest Metrics Types
| Metric | Description | Unit |
|---|------|------|
| DBH | Diameter at Breast Height | cm |
| Height | Tree height | m |
| Crown_Area | Tree crown area | m2 |
| Volume | Tree volume | m3 |
| Biomass | Tree biomass | kg |
| LAI | Leaf Area Index | - |
| Coverage | Canopy coverage | % |

### Segmentation Methods
| Method | Description | Best For |
|---|------|---------|
| CHM | Canopy Height Model based | Dense forests |
| Watershed | Watershed segmentation | Mixed forests |
| Region_Growing | Region growing algorithm | Sparse forests |
| Point_Cloud | Direct point cloud processing | High density data |

### Regression Methods
| Method | Description | Complexity |
|---|------|---------|
| Linear | Simple linear regression | Low |
| Random_Forest | Ensemble of decision trees | Medium |
| SVM | Support Vector Machine | High |
| FANN | Neural network | Very High |

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "forestry_airborne-toolID"
