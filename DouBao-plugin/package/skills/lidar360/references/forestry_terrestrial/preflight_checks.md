# Terrestrial Forestry Analysis Preflight Check Flow

## Mandatory Checks

The following checks apply to all terrestrial forestry analysis tools and must be completed before any operation:

1. Confirm input data format is correct (LiData/TreeDB/CSV, etc.)
2. Check coordinate system consistency -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS
3. Check whether the output directory exists and is writable -> manual confirmation
4. Execute the tool
5. Check whether output files exist; if so, verify that data type, spatial extent, or attribute fields meet expectations

### Normalization Determination Logic

Before executing any terrestrial forestry tool that depends on normalized point clouds, uniformly apply the following logic to determine whether the point cloud can be considered normalized:

1. First, automatically detect whether the point cloud is already normalized
   - If detected as normalized -> pass the normalization check
2. If auto-detection indicates not normalized or cannot be confirmed, check the point cloud Z value range
   - If the point cloud Z value minimum is 0 (must not be negative, must not be positive, must be exactly 0) and maximum <= 120 -> still considered normalized
   - Otherwise -> determined as not normalized, prompt the user to perform normalization first

**Determination result**: If auto-detection normalization passes, or the Z value minimum is 0 and maximum <= 120, tools depending on normalization may proceed.

---

## Tool Execution

### Individual Tree Segmentation Tools

Before executing any individual tree segmentation tool that takes point cloud as input, only check whether the input point cloud is normalized. Do not use existing `treeID`, point cloud class, segmentation parameters, or other data conditions as pre-execution checks; pass the parameters required by the tool according to its interface requirements as usual.

Uniformly use the "Normalization Determination Logic" for checking:

- Determined as normalized -> execute the corresponding individual tree segmentation tool.
- Determined as not normalized -> prompt "Please perform normalization first", do not execute individual tree segmentation.

---

#### tls_point_cloud_segmentation (Terrestrial Point Cloud-Based Segmentation)

**Prerequisite**: Point cloud is normalized

**Check Steps**:
1. Check whether the input LiData is normalized according to the "Normalization Determination Logic" -> `preflight_check(check_item=1)`, `is_normalized_point_cloud == true` -> PASS
   - No -> prompt "Please perform normalization first"

**After passing**: Execute `forestry_terrestrial-tls_point_cloud_segmentation`

---

#### tls_point_cloud_segmentation_from_seed_points (Seed Point-Based Segmentation)

**Prerequisite**: Point cloud is normalized

**Check Steps**:
1. Check whether the input LiData is normalized according to the "Normalization Determination Logic" -> `preflight_check(check_item=1)`, `is_normalized_point_cloud == true` -> PASS
   - No -> prompt "Please perform normalization first"

**After passing**: Execute `forestry_terrestrial-tls_point_cloud_segmentation_from_seed_points`

---

#### tls_trunk_based_tree_segmentation (Trunk-Based Segmentation)

**Prerequisite**: Point cloud is normalized

**Check Steps**:
1. Check whether the input LiData is normalized according to the "Normalization Determination Logic" -> `preflight_check(check_item=1)`, `is_normalized_point_cloud == true` -> PASS
   - No -> prompt "Please perform normalization first"

**After passing**: Execute `forestry_terrestrial-tls_trunk_based_tree_segmentation`

---

#### universal_tree_segmentation (Universal Individual Tree Segmentation)

**Prerequisite**: Point cloud is normalized

**Check Steps**:
1. Check whether the input LiData is normalized according to the "Normalization Determination Logic" -> `preflight_check(check_item=1)`, `is_normalized_point_cloud == true` -> PASS
   - No -> prompt "Please perform normalization first"

**After passing**: Execute `forestry_terrestrial-universal_tree_segmentation`

---

### Forest Metric Calculation Tools

#### tls_calculate_forest_metrics_by_grid

**Prerequisite**: Point cloud is normalized

**Check Steps**:
1. Check whether the point cloud is normalized -> `preflight_check(check_item=1)`, `is_normalized_point_cloud == true` -> PASS
2. Validate `x_grid_size` and `y_grid_size` are greater than 0, typically should be larger than individual tree crown width
3. Check whether `voxel_size`, `voxel_size_method`, `coefficient` are reasonable
4. If `use_height_range=true`, check `height_range_min < height_range_max`
5. Check that at least one statistic is selected: canopy closure, gap fraction, or leaf area index

**After passing**: Execute `forestry_terrestrial-tls_calculate_forest_metrics_by_grid`

---

#### tls_calculate_forest_metrics_by_polygon

**Prerequisite**: Point cloud is normalized + polygon vector exists

**Check Steps**:
1. Check whether the point cloud is normalized -> `preflight_check(check_item=1)`, `is_normalized_point_cloud == true` -> PASS
2. Check whether the polygon vector file exists in `input_data` (shp/gpkg/dxf)
3. Validate polygon coordinate system matches point cloud -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS
4. Check whether `fromClass`, `voxel_size`, `coefficient`, `voxel_size_method` are set
5. If height range is enabled, check height upper and lower bounds

**After passing**: Execute `forestry_terrestrial-tls_calculate_forest_metrics_by_polygon`

---

#### tls_calculate_forest_metrics_by_stands

**Prerequisite**: Point cloud is normalized

**Check Steps**:
1. Check whether the input LiData list exists and all are normalized -> `preflight_check(check_item=1)`, `is_normalized_point_cloud == true` -> PASS (each)
2. Check whether `from_class` is selected
3. Check whether `voxel_size`, `coefficient`, `voxel_size_method` are reasonable
4. Check that at least one statistic is selected: canopy closure, gap fraction, or leaf area index
5. If height range is enabled, check height upper and lower bounds

**After passing**: Execute `forestry_terrestrial-tls_calculate_forest_metrics_by_stands`

---

### Biomass Calculation Tools

#### tree_biomass_estimation

**Prerequisite**: treedb individual tree attribute table exists + biomass equation configuration is complete

**⚠️ Important Principle**: All biomass information must be obtained through MCP interfaces, it is strictly forbidden to directly read `BiomassModel_zh.db` or any `.db` files

**Check Steps**:
1. Check whether the treedb file exists in `input_data`
   - No -> prompt "Please generate the individual tree attribute table first"
2. Read treedb file, extract "TreeSpecies" column and deduplicate
3. Determine tree species count:
   - Single species -> Use `method=0`, configure `cal_info`
   - Multiple species -> Use `method=1`, configure `cal_infos`
4. **Obtain biomass information through MCP interfaces** (execute tree species matching workflow for each species):
   - Use `QueryBiomassTreeSpeciesInfo` to match tree species name
   - Match failed -> Use `query_tree_species` to match
   - If matched and supports biomass model -> Obtain biomass library name -> Then use `QueryBiomassTreeSpeciesInfo` to obtain complete information
   - All species do not support -> Fall back to `method=2`
5. Check whether `calculate_result` includes at least one result type
6. For `method=0`, check `cal_info` (location, tree_species_id, model_type must be obtained via QueryBiomassTreeSpeciesInfo)
7. For `method=1`, check `cal_infos` (tree_species_name for each species fills in the original name from treedb)
8. For `method=2`, check `cal_info_us`
9. Check parameter `valid` or equation configuration validity

**After passing**: Execute `forestry_terrestrial-tree_biomass_estimation`

---

#### classify_using_trained_tree_species_model (Custom Model Tree Species Identification)

**Prerequisite**: Individual tree segmentation complete + trained tree species identification model exists

**Check Steps**:
1. Check whether the input LiData is a segmented point cloud (contains treeID)
2. Check the `model` parameter: model name registered in the tree species library or model file path (*.pt)
3. Check `confidence_threshold` is within the 0-1 range

**After passing**: Execute `forestry_terrestrial-classify_using_trained_tree_species_model`

---

#### train_tree_species_identification_model (Train Tree Species Identification Model)

**Prerequisite**: Training data preparation is complete

**Check Steps**:
1. Check `input_data.training_data` directory exists and contains paired point cloud files and tree species label files
2. Check `input_data.validation_data` directory exists and contains paired point cloud files and tree species label files
3. Check `task_name` is non-empty

**After passing**: Execute `forestry_terrestrial-train_tree_species_identification_model`

---

### Attribute Statistics Tools

#### tls_statistic_tree_attribute

**Prerequisite**: Individual tree segmentation complete + point cloud contains treeID

**Check Steps**:
1. Check whether the input LiData is a segmented point cloud
2. Check whether the point cloud has treeID and the maximum value is greater than 0
3. Validate `select_attribute_to_statistic` attribute IDs are within the 0-24 range and **must include 0, 1, 2, 3**
4. If attribute 7 (elevation) is selected, check `input_dem`
5. If attribute 8 (slope) is selected, check `input_slope`
6. If attribute 13 (azimuth and distance) is selected, check `input_reference_point_file`
7. If `is_updating=Update File`, check `input_table` and `updating_table_ascii_file_para`

**After passing**: Execute `forestry_terrestrial-tls_statistic_tree_attribute`

---

### Feature Extraction and Analysis Tools

#### tls_tree_trunk_extraction

**Prerequisite**: Normalized terrestrial point cloud data

**Check Steps**:
1. Check whether the point cloud is normalized -> `preflight_check(check_item=1)`, `is_normalized_point_cloud == true` -> PASS
2. Check whether `from_class` includes the trunk extraction source class
3. Validate `min_trunk_height < max_trunk_height`
4. Check `max_angle` is within the 0-90 range
5. Check `buffer_size` and `voxel_size` are greater than 0

**After passing**: Execute `forestry_terrestrial-tls_tree_trunk_extraction`

---

#### tls_spatial_structure_quantification

**Prerequisite**: Point cloud is normalized

**Check Steps**:
1. Check whether the input LiData is normalized
2. If an ROI vector is provided, check the file exists and coordinate systems match -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS
3. Check `x_grid_size`, `y_grid_size`, `vertical_voxel_size` are greater than 0
4. Check `statistic_method` is `Point Count` or `Area`
5. If `statistic_method=Area`, check `area_summary_type` is `Sum` or `Average`

**After passing**: Execute `forestry_terrestrial-tls_spatial_structure_quantification`

---

#### tls_tree_based_fuzzy_matching

**Prerequisite**: Reference and target individual tree attribute files exist

**Check Steps**:
1. Check whether the reference individual tree attribute file exists (csv/treedb)
2. Check whether the target file exists (csv/treedb)
3. Validate both files contain `TreeID`, `TreePosX`, `TreePosY`
4. Validate `point_distance_threshold` is greater than 0

**After passing**: Execute `forestry_terrestrial-tls_tree_based_fuzzy_matching`

---

### Report Generation Tools

#### tls_extract_tree_image_report

**Prerequisite**: Individual tree segmentation / attribute statistics complete

**Check Steps**:
1. Check whether `input_data.input_lidata` and `input_data.input_tree_attribute` exist
2. Read `input_tree_attribute` (`.treedb`) via `platform-get_data_information` and take `TableHeader[].key` as the actual field list
3. Validate `select_attributes`: it must contain **every** treedb field except `Crown Contour` (`TreePosX`/`TreePosY`/`TreePosZ` may be merged into `Position`). Do not omit non-default fields such as `TreeSpecies`, `Tree Species Confidence`, or `Biomass Above Ground`, and do not include fields absent from the data
4. Check `render_img_type` is 0, 1, or 2
5. Check `view_type` is 0, 1, or 2
6. If `filter_by_tree_id=true`, check `min_tree_id <= max_tree_id`
7. If panorama is enabled, validate the panorama list is valid

**After passing**: Execute `forestry_terrestrial-tls_extract_tree_image_report`

---

#### forest_tending_planning (Forest Tending Planning)

**Prerequisite**: Registered point cloud, TreeDB, and tending plan JSON exist

**Check Steps**:
1. Check `input_data.pointcloud_file` (`.lidata`), `input_data.treedb_file` (`.treedb`), and `input_data.tending_plan_file` (`.json`) paths exist
2. If `roi_vector_file` is provided, check the file is `.shp/.gpkg` and coordinate system matches the point cloud -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS
3. If panorama data is provided, check `input_panorama_folder` directory exists and `input_panorama_list` is a readable `.imglist`
4. Check `output_data` output directory exists or can be created and is writable
5. After execution, check the reports and operation design table files actually generated in the output directory; if necessary, call `platform-get_data_information` on generated spatial data to verify `data_type`, `feature_count` or point count, and `bounds` match the input ROI / point cloud extent

**After passing**: Execute `forestry_terrestrial-forest_tending_planning`

---

## Other

### Quick Reference Table

| Tool | Key Check |
|------|----------|
| tls_point_cloud_segmentation | Normalization |
| tls_point_cloud_segmentation_from_seed_points | Normalization |
| tls_trunk_based_tree_segmentation | Normalization |
| universal_tree_segmentation | Normalization |
| tls_calculate_forest_metrics_by_grid | Normalization + grid size + voxel parameters + statistics |
| tls_calculate_forest_metrics_by_polygon | Normalization + polygon file + voxel parameters |
| tls_calculate_forest_metrics_by_stands | Normalization + LiData list + statistics |
| tree_biomass_estimation | treedb exists + method-specific equation configuration |
| classify_using_trained_tree_species_model | Segmented point cloud + model name or path + confidence threshold |
| train_tree_species_identification_model | Training data directory + validation data directory + task name |
| tls_statistic_tree_attribute | Segmented point cloud + treeID + attribute dependency data |
| tls_tree_trunk_extraction | Normalization + trunk height range + tilt angle + voxel |
| tls_spatial_structure_quantification | Normalization + grid/vertical voxel + statistic method |
| tls_tree_based_fuzzy_matching | Two attribute files + TreeID/TreePosX/TreePosY + distance threshold |
| tls_extract_tree_image_report | Individual tree data + render type + view type + attribute list |
| forest_tending_planning | LiData + TreeDB + tending plan JSON + writable output directory; output files exist and verify spatial fields |
