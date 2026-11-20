# Forestry Terrestrial Tools Registration
---

## Individual Tree Segmentation
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| tls_point_cloud_segmentation | Perform individual tree segmentation based on terrestrial point cloud data | LiData | from_class, cluster_tolerance, minimum_cluster_size, height_above_ground, trunk_height, min_tree_height, optimize_color |
| tls_point_cloud_segmentation_from_seed_points | Perform individual tree segmentation on point cloud based on seed point file | Input data | from_class, cluster_tolerance, minimum_cluster_size, min_tree_height, height_above_ground, optimize_color |
| tls_trunk_based_tree_segmentation | Extract tree trunks from point cloud, and then perform individual tree segmentation based on the trunks | LiData | from_class, trunk_class, height_above_ground, trunk_height, min_tree_height, optimize_color, do_segmentation, foliage_class, segment_from, extract_to_top, use_gpu_first, cluster_size |
| universal_tree_segmentation | A generic individual tree segmentation function. It can identify trunk (available for TLS data but typically not for ALS data) and foliage classes, and directly produce individual tree segmentation results | LiData | from_class, optimize_color, trunk_class, foliage_class, use_gpu_first |

---

## Forest Metrics
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| tls_calculate_forest_metrics_by_grid | Divide the point cloud into grids based on the horizontal grid size, and calculate the point cloud forest parameters for each grid. If a polygon is provided, the grid division is performed only within the polygon | Input data | is_select_canopy_cover, is_select_gap_fraction, is_select_leaf_area_index, x_grid_size, y_grid_size, output_type, voxel_size, coefficient, voxel_size_method |
| tls_calculate_forest_metrics_by_polygon | Divide the point cloud into multiple grids, and calculate the point cloud forest parameters for each grid in polygon | Input data | from_class, is_select_canopy_cover, is_select_gap_fraction, is_select_leaf_area_index, voxel_size, coefficient, voxel_size_method |
| tls_calculate_forest_metrics_by_stands | Using the input LiData as a stand, calculate the overall forest parameters of this stand | LiData | from_class, is_select_canopy_cover, is_select_gap_fraction, is_select_leaf_area_index, voxel_size, coefficient, voxel_size_method |

---

## Tree Attributes and Biomass
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| tls_statistic_tree_attribute | Mainly used for recalculating and adding attributes of individual tree point cloud. **Required attribute IDs: 0,1,2,3** | Input data | select_attribute_to_statistic, height_above_ground, min_tree_height, stem_class, is_updating, delete_unstatistic_tree_when_update, new_file_suffix, als_or_tls_datatype |
| tree_biomass_estimation | Calculate tree biomass from individual tree attribute table using biomass models | Input data | with_progress, method, calculate_result |

---

## Tree Species Identification
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| classify_using_trained_tree_species_model | Identify tree species in segmented point cloud using a custom-trained tree species identification model. Outputs a three-column CSV: tree ID, tree species, and confidence | LiData | input_data, model, confidence_threshold |
| train_tree_species_identification_model | Train a custom deep learning model to identify tree species from individual tree point clouds. Provide point cloud files paired with corresponding tree species label files during training | Input data | input_data, task_name, task_description |

---

## Feature Extraction and Analysis
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| tls_tree_trunk_extraction | Extract trunk from normalized ground-based point cloud data | LiData | from_class, height_above_ground, max_trunk_height, min_trunk_height, buffer_size, max_angle, voxel_size |
| tls_spatial_structure_quantification | Perform quantitative description and analysis of forest or vegetation canopy structure | Input data | from_class, x_grid_size, y_grid_size, output_type, vertical_voxel_size, statistic_method |
| tls_tree_based_fuzzy_matching | Tree-based fuzzy matching for forestry survey. Used for matching trees from different surveys based on geometric features | Input data | point_distance_threshold |

---

## Reports and Data Products
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| tls_extract_tree_image_report | Generate individual tree image reports with tree attributes | Input data | render_img_type, filter_by_tree_id, min_tree_id, max_tree_id, view_type, select_attributes |
| forest_tending_planning | Generate reports and operator design tables from a forest tending plan | LiData + TreeDB + tending plan JSON + optional ROI/panorama data | - |

---

## Common Parameter Explanation

### from_class (point cloud class)
| Value | Class |
|---|------|
| 0 | Created, never classified |
| 1 | Unclassified |
| 2 | Ground |
| 3-5 | Vegetation |
| 6 | Building |
| 23 | Trunk |
| 24 | Foliage |

### Tree segmentation classes
| Parameter | Description | Typical value |
|---|------|------|
| trunk_class | Class code assigned to trunk points | 23 |
| foliage_class | Class code assigned to foliage points | 24 |
| height_above_ground | Minimum height above ground used for segmentation or extraction | 0.3 |
| min_tree_height | Minimum tree height retained in tree outputs | 2.0 |

### Forest metrics outputs
| Value | Output |
|---|------|
| CSV File | Tabular forest metrics |
| TIFF File | Raster forest metrics |

### select_attributes (tls_extract_tree_image_report)
Do not use a fixed or trimmed default list. Read the input `.treedb` first via `platform-get_data_information` and take `TableHeader[].key` as the authoritative field list, then include every field except `Crown Contour` (`TreePosX`/`TreePosY`/`TreePosZ` may be merged into `Position`). Never omit fields such as `TreeSpecies`, `Tree Species Confidence`, or `Biomass Above Ground`, and never include fields that do not exist in the treedb.

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "forestry_terrestrial-toolID"
