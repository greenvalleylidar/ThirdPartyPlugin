# Airborne Forestry Analysis Typical Examples

> Usage examples for airborne forestry tools based on schema definitions.

---

## Airborne Forestry Examples

### Individual Tree Segmentation Examples

#### Example 1: Image-Based Individual Tree Crown Segmentation

**Scenario**: Automatically identify and segment individual tree crowns using orthophoto imagery

**Prerequisites**:
- Imagery is aligned to the point cloud

**Usage Example**:
```
forestry_airborne-individual_tree_crown_segmentation
Parameters:
  input_data:
    input_data: "/data/ortho.tif"
    mask_file: "/data/study_area.shp"
  confidence_threshold: 0.3
  overlap_ratio: 0.7
  output_data: "/output/tree_crown_segmentation"
```

**Output**:
- Image-based individual tree crown segmentation results

---

#### Example 2: Seed Point-Based Interactive Segmentation

**Scenario**: Use known tree locations as seed points for precise segmentation

**Usage Example**:
```
forestry_airborne-pointcloud_segmentation_from_seed_points
Parameters:
  input_data:
    input_lidata_data: "/data/airborne_lidar.lidata"
    input_table_data: "/data/seed_points.treedb"
  output_data: "/output/seed_segmentation"
  height_above_ground: 2.0
  min_tree_height: 0.0
  optimize_color: false
  from_class: [0, 1, 2, 3, 4, 5]
```

**Output**:
- Seed point-based individual tree segmentation result directory

---

#### Example 3: Trunk-Based Segmentation for Eucalyptus

**Scenario**: Eucalyptus plantation using trunk-priority segmentation method

**Usage Example**:
```
forestry_airborne-trunk_based_tree_segmentation
Parameters:
  input_data: "/data/eucalyptus.lidata"
  output_data: "/output/eucalyptus_trees"
  trunk_class: 23
  foliage_class: 24
  height_above_ground: 0.3
  use_gpu_first: true
  optimize_color: false
  from_class: [0, 1, 2, 3, 4, 5, 23, 24]
```

---

### CHM Processing Examples

#### Example 4: CHM Pit Filling

**Scenario**: CHM has pits that need to be filled

**Usage Example**:
```
forestry_airborne-chm_pits_filling
Parameters:
  input_data: "/data/CHM_raw.tif"
  chm_pits_filling_threshold_pix: 5
  output_data: "/output/CHM_filled.tif"
```

---

#### Example 5: CHM-Based Individual Tree Segmentation

**Scenario**: Use CHM for watershed segmentation

**Usage Example**:
```
forestry_airborne-chm_segmentation
Parameters:
  input_data: "/data/CHM_filled.tif"
  output_data:
    treedb_file: "/output/chm_segmentation.treedb"
    vector_file: "/output/chm_segmentation.shp"
  minimum_tree_height: 1.0
  maximum_tree_height: 80.0
  buffer_size: 50
  is_smooth: true
  sigma: 1.0
  radius_pix: 5
  chm_pits_filling: false
  crown_base_height_threshold: 0.8
```

---

#### Example 6: Generate Seed Points from CHM

**Scenario**: Generate initial seed points for subsequent segmentation

**Usage Example**:
```
forestry_airborne-generate_seed_points_from_chm
Parameters:
  input_data: "/data/CHM_filled.tif"
  output_data: "/output/seed_points.treedb"
  minimum_tree_height: 1.0
  maximum_tree_height: 80.0
  buffer_size: 50
  is_smooth: true
  sigma: 1.0
  radius_pix: 5
```

---

### Forest Metrics Calculation Examples

#### Example 7: Stand-Level Metrics Calculation

**Scenario**: Calculate forest structural parameters for the entire stand

**Usage Example**:
```
forestry_airborne-calculate_forest_metrics_by_forest_stands
Parameters:
  input_data: ["/data/normalized_lidar.lidata"]
  output_data: "/output/stand_metrics.csv"
  extinction_coefficient: 0.5
  height_break: 2.0
  from_class: [3, 4, 5]
  is_select_elevation_metrics: true
  is_select_intensity_metrics: true
  is_select_canopy_cover: true
  is_select_gap_fraction: true
  is_select_leaf_area_index: true
```

---

#### Example 8: Grid-Based Forest Metrics Calculation

**Scenario**: Divide the study area into 15m x 15m grids and calculate metrics for each grid

**Usage Example**:
```
forestry_airborne-calculate_forest_metrics_by_grid
Parameters:
  input_data:
    lidata_data: "/data/normalized_lidar.lidata"
    vector_data: "/data/study_area.shp"
  output_data: "/output/grid_metrics.tif"
  x_grid_size: 15.0
  y_grid_size: 15.0
  height_break: 2.0
  extinction_coefficient: 0.5
  output_type: "TIFF File"
  is_select_elevation_metrics: true
  is_select_intensity_metrics: true
  is_select_canopy_cover: true
  is_select_gap_fraction: true
  is_select_leaf_area_index: true
```

---

#### Example 9: Plot-Based Metrics Calculation

**Scenario**: Calculate forest metrics for each plot using plot vectors

**Usage Example**:
```
forestry_airborne-calculate_forest_metrics_by_polygon
Parameters:
  input_data:
    lidata_data: "/data/normalized_lidar.lidata"
    vector_data: "/data/sample_plots.shp"
  output_data: "/output/plot_metrics.csv"
  height_break: 2.0
  extinction_coefficient: 0.5
  from_class: [3, 4, 5]
  is_select_elevation_metrics: true
  is_select_intensity_metrics: true
  is_select_canopy_cover: true
  is_select_gap_fraction: true
  is_select_leaf_area_index: true
```

---

### Regression Analysis Examples

#### Example 10: Linear Regression Training

**Scenario**: Build a linear regression model using sample data and parameter files

**Usage Example**:
```
forestry_airborne-linear_regression
Parameters:
  input_data:
    input_data: "/data/predictors.csv"
    sample_data: "/data/samples.csv"
  output_data: "/output/linear_model"
  dependent_variable: "DBH"
  dependent_variable_index: 3
  csv_header_list: ["TreeHeight", "CrownDiameter"]
  plot_type: 0
  radius: 10
  x_index: 0
  y_index: 1
  k_fold: 10
  optimize: false
  local_error_buffer: 0
  save_model: true
  save_dataset: false
  report_name: "linear_dbh"
```

---

#### Example 11: Random Forest Regression Training

**Scenario**: Use multiple features to predict biomass (non-linear relationships)

**Usage Example**:
```
forestry_airborne-random_forest_regression
Parameters:
  input_data:
    input_data: "/data/predictors.csv"
    sample_data: "/data/samples.csv"
  output_data: "/output/rf_model"
  dependent_variable: "Biomass"
  dependent_variable_index: 4
  csv_header_list: ["TreeHeight", "DBH", "CrownDiameter", "CrownArea"]
  plot_type: 0
  radius: 10
  x_index: 0
  y_index: 1
  k_fold: 10
  optimize: false
  local_error_buffer: 0
  save_model: true
  save_dataset: false
  report_name: "rf_biomass"
  rf_tree_num: 10
  rf_depth: 3
  rf_min_split: 3
  rf_min_leaf: 2
```

---

#### Example 12: Prediction Using Trained Model

**Scenario**: Use a trained model to predict biomass for new data

**Usage Example**:
```
forestry_airborne-regression_prediction
Parameters:
  input_data:
    input_data: "/data/new_predictors.csv"
    model_file: "/output/rf_model/model.dat"
  output_data: "/output/predicted_biomass"
  csv_header_list: ["TreeHeight", "DBH", "CrownDiameter", "CrownArea"]
  plot_type: 0
  radius: 10
  report_name: "predict_biomass"
```

---

### Data Processing Examples

#### Example 13: Clear Tree IDs

**Scenario**: Clear previous segmentation results before re-segmentation

**Usage Example**:
```
forestry_airborne-clear_tree_id
Parameters:
  input_data: ["/data/segmented_lidar.lidata"]
  filter_by_height: false
  min_height: 0
  max_height: 1000
```

---

#### Example 14: Extract Point Cloud for Specific Trees

**Scenario**: Extract point cloud for a specific range of tree IDs for detailed analysis

**Usage Example**:
```
forestry_airborne-extract_by_tree_id
Parameters:
  input_data:
    input_data: "/data/segmented_lidar.lidata"
    input_data_table: "/data/tree_attributes.treedb"
  output_data: "/output/selected_trees.lidata"
  filter_by: "TreeID"
  extract_to: "One File"
  output_format: "LiData"
  min_treeID: 1
  max_treeID: 20
```

---

#### Example 15: Forest Structure Change Detection

**Scenario**: Compare forest structure changes between 2015 and 2025

**Usage Example**:
```
forestry_airborne-forest_structure_change_detection
Parameters:
  input_data:
    input_lidata_before_change: "/data/lidar_2015_registered.lidata"
    input_lidata_after_change: "/data/lidar_2025_registered.lidata"
  output_data: "/output/change_detection"
  x_size: 15.0
  y_size: 15.0
  height_break: 0.5
```

---

#### Example 16: Clear Tree IDs by Table

**Scenario**: Clear only the TreeID labels listed in the table

**Usage Example**:
```
forestry_airborne-als_clear_treeid_by_file
Parameters:
  input_data:
    input_data: "/data/segmented_lidar.lidata"
    input_table: "/data/tree_ids_to_clear.csv"
```

---

#### Example 17: Individual Tree Attribute Statistics

**Scenario**: Recalculate individual tree attributes for segmented point cloud

**Usage Example**:
```
forestry_airborne-als_individual_tree_attribute_statistics
Parameters:
  input_data:
    input_data: "/data/segmented_lidar.lidata"
    input_dem: "/data/dem.tif"
    input_slope: "/data/slope.tif"
    input_reference_point_file: "/data/reference_points.csv"
    input_table: "/data/tree_ids.csv"
  output_data: "/output/tree_attributes.treedb"
  select_attribute_to_statistic: [0, 1, 2, 3, 4, 5]
  height_above_ground: 0.3
  min_tree_height: 2.0
  stem_class: 23
  is_updating: "New File"
  delete_unstatistic_tree_when_update: false
  new_file_suffix: "treedb"
  als_or_tls_datatype: 0
```

---

#### Example 18: Generate Crown Boundaries

**Scenario**: Generate crown boundary vectors from individual tree segmentation point cloud

**Usage Example**:
```
forestry_airborne-extract_tree_crown_boundaries
Parameters:
  input_data: ["/data/segmented_lidar.lidata"]
  output_data: "/output/crown_contours.shp"
  method: "Concave"
  max_edge_length: 1.0
```

---

#### Example 19: SVM Regression Training

**Scenario**: Build a regression model using Support Vector Machine

**Usage Example**:
```
forestry_airborne-svm_regression
Parameters:
  input_data:
    input_data: "/data/predictors.csv"
    sample_data: "/data/samples.csv"
  output_data: "/output/svm_model"
  dependent_variable: "0"
  dependent_variable_index: 4
  csv_header_list: ["TreeHeight", "DBH", "CrownArea"]
  plot_type: 0
  radius: 10
  x_index: 0
  y_index: 1
  k_fold: 10
  optimize: false
  local_error_buffer: 0
  save_model: true
  save_dataset: false
  report_name: "svm_biomass"
  svm_type: 0
  svm_kernel_type: 0
  svm_degree: 3
  svm_gamma: 0.1
```

---

#### Example 20: FANN Regression Training

**Scenario**: Build a regression model using Fast Artificial Neural Network

**Usage Example**:
```
forestry_airborne-fann_regression
Parameters:
  input_data:
    input_data: "/data/predictors.csv"
    sample_data: "/data/samples.csv"
  output_data: "/output/fann_model"
  dependent_variable: "Biomass"
  dependent_variable_index: 4
  csv_header_list: ["TreeHeight", "DBH", "CrownArea"]
  plot_type: 0
  radius: 10
  x_index: 0
  y_index: 1
  k_fold: 10
  optimize: false
  local_error_buffer: 0
  save_model: true
  save_dataset: false
  report_name: "fann_biomass"
  fann_learning_rate: 0.1
  fann_momentum: 0.3
```

---

### Individual Tree Modeling Examples

#### Example 21: Generate Tree Models (generate_tree_model)

**Scenario**: Based on the tree species field in the individual tree attribute table, assign model indices from the 360 tree species model library for each species, and generate LiTree individual tree models.

**Usage Example**:
```json
{
  "tool": "forestry_airborne-generate_tree_model",
  "input": {
    "input_data": "/data/tree_attributes.treedb",
    "output_data": "/output/trees.LiTree",
    "tree_modes_list": [
      {
        "tree_kind": "Default",
        "tree_model": 0
      },
      {
        "tree_kind": "Species 1",
        "tree_model": 1
      },
      {
        "tree_kind": "Species 2",
        "tree_model": 2
      }
    ]
  }
}
```

**tree_kind Generation Rules**:
- `tree_kind` is the tree species name read from the `TreeSpecies` column in the input `treedb` individual tree attribute table after deduplication.
- Output parameters must use standard JSON string values, and the string content itself must not contain leading or trailing double quotes. Even if the `TreeSpecies` cell stores literal double quotes, you must first remove leading/trailing whitespace and the paired single or double quotes wrapping the tree species name before generating `tree_kind`.
- Correct: `{"tree_kind": "Quercus rubra L.", "tree_model": 0}`.
- Incorrect: `{"tree_kind": "\"Quercus rubra L.\"", "tree_model": 32}`. Do not retain or escape these wrapping quotes for literal exact matching with quoted raw text in `treedb`.
- If the cleaned tree species string is empty, `Default` must be used instead.
- For example, if `treedb` has 5 rows with tree species values `Species 1`, `Species 2`, empty, empty, empty, then `tree_modes_list` should contain 3 `tree_kind` values: `Species 1`, `Species 2`, `Default`.

**tree_model Meaning**:
- `tree_model` is the tree species index in the current LiDAR360 tree species model library, and must be output as an integer, not as a string.
- Currently supports 70 tree species, with index range `0~69`.
- For the Chinese-English comparison of tree species models, see `references/profiles/model_library_tree_species_chinese_english_comparison_table.md`.
- Use the corresponding index only when the user explicitly specifies the tree species model, or when the tree species name can be uniquely matched according to the Chinese-English comparison table in the model library; when it cannot be uniquely confirmed, you must ask the user and cannot guess.
- The canonical parameters for `Quercus rubra L.` are `{"tree_kind": "Quercus rubra L.", "tree_model": 0}`.

---

#### Example 22: Forest Point Cloud Auto-Registration

**Scenario**: Register forest point clouds collected from two different periods or platforms

**Usage Example**:
```
forestry_airborne-auto_registration_forest
Parameters:
  input_data:
    refg_pointcloud_file: "/data/reference.lidata"
    align_pointcloud_file: "/data/target.lidata"
  output_data: "/output/target_registered.lidata"
  selected_classes: [2]
  cell_size: 0.3
  overlap: 40
  icp_optimize: true
  iteration: 10
  num_samples: 100000
  max_search_distance: 1
  normal_filter: 60
  rms_diff: -1
```

---

#### Example 23: ITS Mosaicing

**Scenario**: Edge-match multiple individual tree segmentation patches

**Usage Example**:
```
forestry_airborne-its_mosaicing
Parameters:
  input_data:
    input_lidata_data:
      - "/data/tile_01.lidata"
      - "/data/tile_02.lidata"
    input_table_data:
      - "/data/tile_01.treedb"
      - "/data/tile_02.treedb"
    input_vector_data: "/data/tiles.shp"
  tile_buffer: 5
  recalculate_tree_id: true
```

---

#### Example 24: Forest Stand Delineation

**Scenario**: Automatically extract stand boundaries from CHM

**Usage Example**:
```
forestry_airborne-forest_stands_delineating
Parameters:
  input_data: "/data/chm.tif"
  output_data: "/output/forest_stands.shp"
  method: "Region Growing"
  cell_size: 10
  min_stand_area: 10000
  min_height: 0.5
  max_height: 40
```

---

## Parameter Reference

### Individual Tree Segmentation Parameter Recommendations

#### Airborne ALS

| Parameter | Recommended Value | Description |
|-----|-------|------|
| grid_size | 0.5-1.0m | Grid size, adjust based on point cloud density |
| height_above_ground | 1.5-2.0m | Filter low vegetation; can be reduced for short stands |
| sigma | 0.8-1.2 | Gaussian smoothing factor; reduce when under-segmentation occurs |
| radius_pix | 3-7 | Window size (odd numbers) |
| min_tree_height | 0-1m | Minimum tree height threshold |

---

### Forest Metrics Calculation Parameter Recommendations

| Parameter | Recommended Value | Description |
|-----|-------|------|
| extinction_coefficient | 0.5-0.7 | Extinction coefficient, depends on tree species and leaf angle distribution |
| height_break | 1.5-2.0m | Height stratification threshold |
| Grid size | 15-30m | `x_grid_size` / `y_grid_size`, should be larger than individual tree crown width |
| output_type | CSV File / TIFF File | Grid result output format |

---

### Regression Analysis Parameter Recommendations

| Method | Sample Size Recommendation | Applicable Scenario |
|-----|-----------|---------|
| Linear Regression | >30 | Simple linear relationships |
| Random Forest | >50 | Complex non-linear relationships |
| SVM Regression | >50 | Medium-sized datasets |
| FANN | >100 | Large datasets, complex relationships |

---

## Common Issues

### Q1: Tree Count After Individual Tree Segmentation is Too Low

**Possible Causes**:
- `grid_size` is too large
- `height_above_ground` is too high
- `sigma` is too large, causing over-smoothing

**Solutions**:
- Reduce `grid_size` (0.4-0.6m)
- Lower `height_above_ground` (1.5-2.0m)
- Reduce `sigma` (0.8-1.0)

---

## Related Documentation

- Tool registry: `references/forestry_airborne/tools.md`
- Pre-flight checks: `references/forestry_airborne/preflight_checks.md`
- Complete workflows: `references/forestry_airborne/workflows.md`
