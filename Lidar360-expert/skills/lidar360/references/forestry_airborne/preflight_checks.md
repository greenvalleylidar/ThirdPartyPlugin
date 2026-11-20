# Airborne Forestry Analysis Preflight Check Flow

## Mandatory Checks

The following checks apply to all airborne forestry analysis tools and must be completed before any operation:

1. Confirm input data format is correct (LiData/imagery/CHM, etc.)
2. Check coordinate system consistency -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS
3. Check whether the output directory exists and is writable -> manual confirmation
4. Execute the tool
5. Check whether output files exist; if so, verify that data type, spatial extent, or attribute fields meet expectations

### Normalization Determination Logic

Before executing any airborne forestry tool that depends on normalized point clouds, uniformly apply the following logic to determine whether the point cloud can be considered normalized:

1. First, automatically detect whether the point cloud is already normalized
   - If detected as normalized -> pass the normalization check
2. If auto-detection indicates not normalized or cannot be confirmed, check the point cloud Z value range
   - If the point cloud Z value minimum is 0 (must not be negative, must not be positive, must be exactly 0) and maximum <= 120 -> still considered normalized
   - Otherwise -> determined as not normalized, prompt the user to perform normalization first

**Determination result**: If auto-detection normalization passes, tools depending on normalization may proceed.

---

## Tool Execution

### Individual Tree Segmentation Tools

Before executing any individual tree segmentation tool that takes point cloud as input, only check whether the input point cloud is normalized. Do not use existing `treeID`, point cloud class, seed point content, segmentation parameters, or other data conditions as pre-execution checks; pass the parameters required by the tool according to its interface requirements as usual.

Uniformly use the "Normalization Determination Logic" for checking:

- Determined as normalized -> execute the corresponding individual tree segmentation tool.
- Determined as not normalized -> prompt "Please perform normalization first (pointcloud_processing-normalize_by_ground_points)", do not execute individual tree segmentation.

Image-based or CHM-based individual tree segmentation is not point cloud individual tree segmentation and does not apply this normalization preflight check.

---

#### individual_tree_crown_segmentation (Image-Based Individual Tree Crown Segmentation)

**Prerequisite**: The imagery is single-channel.

**Check Steps**:
1. Check whether an imagery project exists -> `list_loaded_layers`, target URL in `layers[].url` -> PASS
   - No -> prompt "Please load imagery data first"
2. Check whether the imagery is single-channel (not three-channel color imagery)
   - No -> prompt "Imagery must be single-channel"
3. Check whether `confidence_threshold` and `overlap_ratio` are within the 0 to 1 range

**After passing**: Execute `forestry_airborne-individual_tree_crown_segmentation`

---

#### pointcloud_segmentation_from_seed_points (Seed Point-Based Segmentation)

**Prerequisite**: Point cloud is normalized

**Check Steps**:
1. Check whether the input point cloud is normalized according to the "Normalization Determination Logic" -> `preflight_check(check_item=1)`, `is_normalized_point_cloud == true` -> PASS
   - No -> prompt "Please perform normalization first (pointcloud_processing-normalize_by_ground_points)"

**After passing**: Execute `forestry_airborne-pointcloud_segmentation_from_seed_points`

---

#### trunk_based_tree_segmentation (Trunk-Based Segmentation)

**Prerequisite**: Point cloud is normalized

**Check Steps**:
1. Check whether the input point cloud is normalized according to the "Normalization Determination Logic" -> `preflight_check(check_item=1)`, `is_normalized_point_cloud == true` -> PASS
   - No -> prompt "Please perform normalization first (pointcloud_processing-normalize_by_ground_points)"

**After passing**: Execute `forestry_airborne-trunk_based_tree_segmentation`

---

#### individual_tree_segmentation (Point Cloud-Based Individual Tree Segmentation)

**Prerequisite**: Point cloud is normalized

**Check Steps**:
1. Check whether the input point cloud is normalized according to the "Normalization Determination Logic" -> `preflight_check(check_item=1)`, `is_normalized_point_cloud == true` -> PASS
   - No -> prompt "Please perform normalization first (pointcloud_processing-normalize_by_ground_points)"

**After passing**: Execute `forestry_airborne-individual_tree_segmentation`

---

### CHM-Related Tools

#### chm_pits_filling (CHM Pit Filling)

**Prerequisite**: CHM imagery has been generated

**Check Steps**:
1. Check whether the currently selected layer type is raster imagery (CHM) -> `get_data_information`, `data_type == "raster"` -> PASS
   - No -> prompt "Please load CHM imagery first"
2. Check CHM validity (no NoData or invalid values) -> `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS
   - Invalid -> prompt "CHM data is invalid"
3. Check whether `chm_pits_filling_threshold_pix` is greater than 0
4. Check whether the raster imagery is single-channel.

**After passing**: Execute `forestry_airborne-chm_pits_filling`

---

#### chm_segmentation (CHM Segmentation)

**Prerequisite**: CHM imagery has been generated (preferably after pit filling)

**Check Steps**:
1. Check whether CHM exists and is valid -> `get_data_information`, `code == 0` -> PASS; `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS
   - No -> prompt "Please generate CHM imagery first (terrain_analysis-generate_chm)"
2. Check whether CHM resolution is appropriate (recommended <1m)
3. Check `minimum_tree_height` is less than `maximum_tree_height`
4. Check whether `radius_pix` is an odd number
5. If `chm_pits_filling` is enabled, check whether the pit filling threshold is reasonable
6. Check whether the raster imagery is single-channel.

**After passing**: Execute `forestry_airborne-chm_segmentation`

---

#### generate_seed_points_from_chm (Generate Seed Points from CHM)

**Prerequisite**: CHM imagery exists

**Check Steps**:
1. Check whether CHM exists -> `get_data_information`, `code == 0` -> PASS
2. Check whether CHM resolution is appropriate (recommended <1m)
3. Check `minimum_tree_height` is less than `maximum_tree_height`
4. Check whether `radius_pix` is an odd number

**After passing**: Execute `forestry_airborne-generate_seed_points_from_chm`

---

### Forest Metric Calculation Tools

#### calculate_forest_metrics_by_forest_stands (Calculate by Forest Stands)

**Prerequisite**: Point cloud is normalized

**Check Steps**:
1. Check whether the point cloud is normalized -> `preflight_check(check_item=1)`, `is_normalized_point_cloud == true` -> PASS
2. Check whether the point cloud has classes available for computation
3. Check `fromClass` includes at least one valid class
4. Check whether `height_break` is greater than or equal to 0
5. Check that at least one metric is selected: height, intensity, canopy closure, gap fraction, or leaf area index

**After passing**: Execute `forestry_airborne-calculate_forest_metrics_by_forest_stands`

---

#### calculate_forest_metrics_by_grid (Calculate by Grid)

**Prerequisite**: Point cloud is normalized

**Check Steps**:
1. Check whether the point cloud is normalized -> `preflight_check(check_item=1)`, `is_normalized_point_cloud == true` -> PASS
2. Validate `x_grid_size` and `y_grid_size` are greater than 0, and preferably larger than individual tree crown width
3. If a clipping vector is specified, check whether the vector file is valid
4. Check `output_type` is `CSV File` or `TIFF File`
5. Check that at least one metric is selected

**After passing**: Execute `forestry_airborne-calculate_forest_metrics_by_grid`

---

#### calculate_forest_metrics_by_polygon (Calculate by Polygon)

**Prerequisite**: Point cloud is normalized + polygon vector exists

**Check Steps**:
1. Check whether the point cloud is normalized -> `preflight_check(check_item=1)`, `is_normalized_point_cloud == true` -> PASS
2. Check whether the polygon vector file exists
   - No -> prompt "Please provide a polygon vector file"
3. Validate polygon coordinate system matches point cloud -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS
4. Check whether `height_break` and `extinction_coefficient` are reasonable
5. Check that at least one metric is selected

**After passing**: Execute `forestry_airborne-calculate_forest_metrics_by_polygon`

---

### Regression Analysis Tools

#### linear_regression / random_forest_regression / fann_regression / svm_regression

**Prerequisite**: Independent variable data and sample data exist

**Check Steps**:
1. Check whether `input_data.input_data` exists (CSV or TIF)
   - No -> prompt "Please provide independent variable data"
2. Check whether `input_data.sample_data` exists
   - No -> prompt "Please provide sample data"
3. Check whether dependent variable field names or column numbers are valid
4. Check whether `csv_header_list` is non-empty
5. Check whether sample coordinate field index and K-fold parameters are reasonable

**After passing**: Execute the corresponding regression tool

---

#### regression_prediction

**Prerequisite**: Model file exists + data to predict is valid

**Check Steps**:
1. Check whether `input_data.model_file` exists
   - No -> prompt "Please train the model first"
2. Check whether `input_data.input_data` exists
3. Check whether the data to predict contains all feature fields required by the model
4. Validate `csv_header_list` matches the training model features

**After passing**: Execute `forestry_airborne-regression_prediction`

---

### Data Processing Tools

#### clear_tree_id / als_clear_treeid_by_file

**Prerequisite**: Point cloud is loaded

**Check Steps**:
1. Check whether the currently selected layer type is point cloud
   - No -> prompt "Please select the point cloud layer first"
2. Check whether the point cloud is opened in the project
3. For `clear_tree_id`, check `min_height` is less than `max_height`
4. For `als_clear_treeid_by_file`, check the input TreeID table exists

**After passing**: Execute the corresponding clearing tool

---

#### extract_by_tree_id

**Prerequisite**: Individual tree segmentation is complete

**Check Steps**:
1. Check whether the currently selected layer type is point cloud
2. Check whether the point cloud has treeID (>0)
   - No -> prompt "Please perform individual tree segmentation first"
3. If filtering by TreeID, check `min_treeID` is less than or equal to `max_treeID`
4. If filtering by attribute file, check the individual tree attribute file exists
5. Check `output_format` is LiData, CSV, LAS, or LAZ

**After passing**: Execute `forestry_airborne-extract_by_tree_id`

---

#### generate_tree_model

**Prerequisite**: Individual tree attribute table and tree species model configuration exist

**Check Steps**:
1. Check whether the input table file exists
   - No -> prompt "Please generate the individual tree attribute table first"
2. Check whether `tree_modes_list` is configured
   - `tree_kind` must have leading/trailing whitespace and surrounding paired single or double quotes stripped; do not generate string content in the form of `\"tree_species_name\"`
   - `tree_model` must be an integer in the range `0~69`; only fill in when the user specifies or the model library can uniquely match; otherwise, ask the user first
3. Check whether the output LiTree path is writable

**After passing**: Execute `forestry_airborne-generate_tree_model`

---

#### auto_registration_forest

**Prerequisite**: Reference point cloud and point cloud to register exist

**Check Steps**:
1. Check whether `input_data.refg_pointcloud_file` exists
2. Check whether `input_data.align_pointcloud_file` exists
3. Check whether the two point clouds have overlapping areas
4. Check `selected_classes` exist in the point cloud
5. If ICP is enabled, check whether iteration count, sampling point count, and search distance are reasonable

**After passing**: Execute `forestry_airborne-auto_registration_forest`

---

#### its_mosaicing

**Prerequisite**: Multiple individual tree segmentation results and corresponding tables exist

**Check Steps**:
1. Check whether `input_data.input_lidata_data` is a non-empty array
2. Check whether `input_data.input_table_data` is a non-empty array
3. Check point cloud array and table array have matching counts and order
4. Check the input vector file exists
5. Check `tile_buffer` is greater than 0

**After passing**: Execute `forestry_airborne-its_mosaicing`

---

#### forest_structure_change_detection

**Prerequisite**: Before and after point clouds are registered to the same coordinate system

**Check Steps**:
1. Check whether the before-change LiData exists
2. Check whether the after-change LiData exists
3. Validate the two epochs have the same coordinate system, elevation datum, and units -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS
4. Check spatial extent overlap of the two epochs -> `get_data_information` x N, compare `bounds`, intersection area > 0 -> PASS
5. Check whether `x_size`, `y_size`, and `height_break` are reasonable

**After passing**: Execute `forestry_airborne-forest_structure_change_detection`

---

#### forest_stands_delineating

**Prerequisite**: CHM imagery exists

**Check Steps**:
1. Check whether the input CHM exists and is valid -> `get_data_information`, `code == 0` -> PASS; `preflight_check(check_item=2)`, `is_dem_or_dsm == true` && `is_valid == true` -> PASS
2. Check `method` is `Region Growing` or `Cell Automation`
3. Check `cell_size` and `min_stand_area` are greater than 0
4. Check `min_height` is less than `max_height`

**After passing**: Execute `forestry_airborne-forest_stands_delineating`

---

## Other

### Quick Reference Table

| Tool | Key Check |
|------|----------|
| individual_tree_crown_segmentation | Imagery aligned to point cloud |
| pointcloud_segmentation_from_seed_points | Normalization |
| trunk_based_tree_segmentation | Normalization |
| individual_tree_segmentation | Normalization |
| chm_pits_filling | CHM exists + pit filling threshold |
| chm_segmentation | CHM exists + tree height range + odd window |
| generate_seed_points_from_chm | CHM exists + tree height range + odd window |
| calculate_forest_metrics_by_forest_stands | Normalization + metric selection |
| calculate_forest_metrics_by_grid | Normalization + grid size + output type |
| calculate_forest_metrics_by_polygon | Normalization + polygon file |
| als_individual_tree_attribute_statistics | Individual tree segmentation complete + attribute selection |
| extract_tree_crown_boundaries | Individual tree segmentation complete + crown method |
| linear_regression | Independent variable data + sample data |
| random_forest_regression | Independent variable data + sample data + RF parameters |
| fann_regression | Independent variable data + sample data + FANN parameters |
| svm_regression | Independent variable data + sample data + SVM parameters |
| regression_prediction | Model file + data to predict |
| als_clear_treeid_by_file | Point cloud + TreeID table |
| clear_tree_id | Point cloud loaded + height range |
| extract_by_tree_id | Individual tree segmentation complete + filter criteria |
| generate_tree_model | Individual tree attribute table + tree species model |
| auto_registration_forest | Reference point cloud + point cloud to register + overlap area |
| its_mosaicing | Multiple point clouds + corresponding tables + vector |
| forest_structure_change_detection | Before/after point clouds same coordinate/elevation/units |
| forest_stands_delineating | CHM exists + stand delineation parameters |
