# Terrestrial Forestry Analysis Typical Examples

> Usage examples for terrestrial forestry tools based on schema definitions.

---

## Terrestrial Forestry Examples

### Individual Tree Segmentation Examples

#### Example 1: Seed Point-Based TLS Segmentation

**Scenario**: Use known tree positions for TLS segmentation

**Usage Example**:
```
forestry_terrestrial-tls_point_cloud_segmentation_from_seed_points
Parameters:
  input_data:
    input_data: "/data/tls_plot.lidata"
    input_seed_file: "/data/tls_seeds.treedb"
  output_data: "/output/tls_segmented.treedb"
  from_class: [3, 4, 5, 23, 24]
  height_above_ground: 0.3
  min_tree_height: 2.0
  cluster_tolerance: 0.2
  minimum_cluster_size: 500
  optimize_color: true
```

---

#### Example 2: Trunk-Based TLS Segmentation

**Scenario**: Extract tree trunks from normalized ground-based point cloud and perform individual tree segmentation

**Usage Example**:
```
forestry_terrestrial-tls_trunk_based_tree_segmentation
Parameters:
  input_data: "/data/tls_plot.lidata"
  output_data: "/output/tls_trunk_seg.treedb"
  from_class: [3, 4, 5, 23, 24]
  trunk_class: 23
  foliage_class: 24
  height_above_ground: 0.3
  trunk_height: 8.0
  do_segmentation: true
  segment_from: 1.0
  extract_to_top: true
  cluster_size: 0.2
  use_gpu_first: true
  optimize_color: true
```

---

#### Example 3: Universal Individual Tree Segmentation

**Scenario**: Perform universal individual tree segmentation on terrestrial or airborne normalized point cloud

**Usage Example**:
```
forestry_terrestrial-universal_tree_segmentation
Parameters:
  input_data: "/data/normalized_plot.lidata"
  output_data: "/output/universal_trees.treedb"
  from_class: [5, 23, 24]
  trunk_class: 23
  foliage_class: 24
  min_tree_height: 2.0
  use_gpu_first: true
  optimize_color: true
```

---

### Forest Metrics Calculation Examples

#### Example 4: TLS Grid Metrics Calculation

**Scenario**: Divide TLS plot into grids to calculate canopy cover, gap fraction, and leaf area index

**Usage Example**:
```
forestry_terrestrial-tls_calculate_forest_metrics_by_grid
Parameters:
  input_data:
    lidata_data: "/data/tls_plot.lidata"
    vector_data: "/data/plot_boundary.shp"
  output_data: "/output/tls_grid_metrics"
  from_class: [3, 4, 5, 23, 24]
  x_grid_size: 15.0
  y_grid_size: 15.0
  output_type: "CSV File"
  voxel_size: 0.02
  voxel_size_method: "Voxel Size"
  coefficient: 2.0
  is_select_canopy_cover: true
  is_select_gapFraction: true
  is_select_leafAreaIndex: true
  use_height_range: true
  height_range_min: 2.0
  height_range_max: 25.0
```

---

#### Example 5: TLS Polygon Metrics Calculation

**Scenario**: Calculate forest metrics within polygons using survey plot vectors

**Usage Example**:
```
forestry_terrestrial-tls_calculate_forest_metrics_by_polygon
Parameters:
  input_data:
    lidata_data: "/data/tls_plot.lidata"
    vector_data: "/data/subplots.shp"
  output_data: "/output/tls_subplot_metrics.csv"
  from_class: [3, 4, 5, 23, 24]
  voxel_size: 0.02
  voxel_size_method: "Voxel Size"
  coefficient: 2.0
  is_select_canopy_cover: true
  is_select_gapFraction: true
  is_select_leafAreaIndex: true
```

---

### Individual Tree Attribute Statistics Examples

#### Example 6: Basic Individual Tree Attribute Statistics

**Scenario**: After individual tree segmentation, calculate basic attributes (tree height, DBH, crown width, volume)

**Usage Example**:
```json
{
  "tool": "forestry_terrestrial-tls_statistic_tree_attribute",
  "input": {
    "input_data": {
      "input_data": "/data/segmented_trees.lidata"
    },
    "output_data": "/output/tree_attributes.treedb",
    "select_attribute_to_statistic": [0, 1, 2, 3],
    "height_above_ground": 0.3,
    "min_tree_height": 2.0,
    "stem_class": 23,
    "is_updating": "New File",
    "als_or_tls_datatype": 1
  }
}
```

#### Example 7: Complete Attribute Statistics Including Tree Species

**Scenario**: Calculate all commonly used attributes, including tree species identification

**Usage Example**:
```json
{
  "tool": "forestry_terrestrial-tls_statistic_tree_attribute",
  "input": {
    "input_data": {
      "input_data": "/data/segmented_trees.lidata",
      "input_dem": "/data/dem.tif",
      "input_slope": "/data/slope.tif",
      "input_reference_point_file": "/data/reference_points.csv"
    },
    "output_data": "/output/full_tree_attributes.treedb",
    "select_attribute_to_statistic": [0, 1, 2, 3, 7, 8, 13, 14, 15, 22, 23],
    "height_above_ground": 0.3,
    "min_tree_height": 2.0,
    "stem_class": 23,
    "is_updating": "New File",
    "als_or_tls_datatype": 1,
    "data_source_for_tree_species_identification": 0,
    "tree_species_confidence": 0.5,
    "tree_species_use_GPU": true,
    "tree_species_use_LLM_fallback": false,
    "recognition_scope_mode": 2,
    "layer_height": 0.2,
    "low_confidence_threshold": 0.5
  }
}
```

---

### Biomass Calculation Examples

> **⚠️ Important Principle**: All biomass information must be obtained through MCP interfaces, it is strictly forbidden to directly read `BiomassModel_zh.db` or any `.db` files
>
> **Language and method Selection Rules**: 
> - Chinese software:
>   - Single species -> Use `method=0`, configure `cal_info`
>   - Multiple species -> Use `method=1`, configure `cal_infos`
>   - All species do not support biomass model -> Fall back to `method=2`
> - English software: Only supports `method=2`
>
> **MCP Interfaces Used**: `QueryBiomassTreeSpeciesInfo` (biomass library interface), `query_tree_species` (tree species library interface)

#### Example 8a: Biomass Calculation (Chinese Software, Single Species, method=0)

**Scenario**: Chinese software, all trees in treedb belong to the same species

**Steps**:
1. Read treedb file, extract "TreeSpecies" column and deduplicate, confirm only one species
2. Use `QueryBiomassTreeSpeciesInfo` to match tree species name, obtain `location`, `tree_species_id`, `model_type`
3. Use `method=0`, configure `cal_info`

**Usage Example**:
```
forestry_terrestrial-tree_biomass_estimation
Parameters:
  input_data:
    input_data: "/data/trees.treedb"
    output_data: "/output/biomass.treedb"
  with_progress: true
  method: 0
  calculate_result: [0, 1, 2, 3, 4]
  valid: true
  cal_info:
    location: "Obtained via QueryBiomassTreeSpeciesInfo"
    model_type: "Obtained via QueryBiomassTreeSpeciesInfo (0=univariate, 1=bivariate)"
    tree_species_id: "Obtained via QueryBiomassTreeSpeciesInfo"
    valid: true
```

**method=0 Example Data**:
```json
{
   "cal_info": {
      "location": "myLocation",
      "model_type": 0,
      "tree_species_id": 1200000003,
      "valid": true
   },
   "method": 0,
   "calculate_result": [0],
   "valid": true
}
```

#### Example 8b: Biomass Calculation (Chinese Software, Multiple Species, method=1)

**Scenario**: Chinese software, treedb contains multiple different species

**Steps**:
1. Read treedb file, extract "TreeSpecies" column and deduplicate to get species list (e.g., ["123", "American beech", "Eucalyptus globulus Labill.", "Fagus grandifolia"])
2. Execute tree species matching workflow for each species:
   - Use `QueryBiomassTreeSpeciesInfo` to match
   - Match failed -> Use `query_tree_species` to match
   - If matched and supports biomass model -> Obtain biomass library name -> Then use `QueryBiomassTreeSpeciesInfo` to obtain complete information
3. Use `method=1`, configure `cal_infos` array

**Usage Example**:
```
forestry_terrestrial-tree_biomass_estimation
Parameters:
  input_data:
    input_data: "/data/trees.treedb"
    output_data: "/output/biomass.treedb"
  with_progress: true
  method: 1
  calculate_result: [0, 1, 2, 3, 4]
  valid: true
  cal_infos: [
    {
      location: "Obtained through tree species matching workflow",
      model_type: "Obtained through tree species matching workflow (0=univariate, 1=bivariate)",
      tree_species_id: "Obtained through tree species matching workflow",
      tree_species_name: "Original tree species name from treedb (first after deduplication)",
      valid: true
    },
    {
      location: "Obtained through tree species matching workflow",
      model_type: "Obtained through tree species matching workflow",
      tree_species_id: "Obtained through tree species matching workflow",
      tree_species_name: "Original tree species name from treedb (second after deduplication)",
      valid: true
    }
  ]
```

**method=1 Example Data** (assuming 4 species after deduplication in treedb):
```json
{
   "cal_infos": [
      {
         "location": "Region of 123",
         "model_type": 1,
         "tree_species_id": 1200000002,
         "tree_species_name": "123",
         "valid": true
      },
      {
         "location": "myLocation",
         "model_type": 1,
         "tree_species_id": 1200000004,
         "tree_species_name": "American beech",
         "valid": true
      },
      {
         "location": "myLocation",
         "model_type": 0,
         "tree_species_id": 1200000003,
         "tree_species_name": "Eucalyptus globulus Labill.",
         "valid": true
      },
      {
         "location": "myLocation",
         "model_type": 1,
         "tree_species_id": 1200000004,
         "tree_species_name": "Fagus grandifolia",
         "valid": true
      }
   ],
   "method": 1,
   "calculate_result": [0, 1, 2, 3, 4],
   "valid": true
}
```

> **Notes**: 
> - The length of `cal_infos` array equals the number of deduplicated species in treedb
> - `tree_species_name` always fills in the original tree species name from treedb
> - `location`, `model_type`, `tree_species_id` are obtained through the tree species matching workflow

#### Example 8c: Biomass Calculation (English Software or All Species Not Supported, method=2)

**Scenario**: English software, or all species do not support biomass model

**Usage Example**:
```
forestry_terrestrial-tree_biomass_estimation
Parameters:
  input_data:
    input_data: "/data/us_trees.treedb"
    output_data: "/output/us_biomass.treedb"
  with_progress: true
  method: 2
  calculate_result: []
  valid: true
  cal_info_us: [
    {
      comp_id: 6,
      eqn_no: 400,
      reference_author: "Carpenter 1983",
      region: "09",
      species_name: "tamarack (native)"
    }
  ]
```

---

### Special Analysis Examples

#### Example 9: Rainforest Trunk Extraction

**Scenario**: Tropical rainforest, extract vertical trunks from normalized ground-based point cloud

**Usage Example**:
```
forestry_terrestrial-tls_tree_trunk_extraction
Parameters:
  input_data: "/data/rainforest_tls.lidata"
  from_class: [3, 4, 5, 23, 24]
  height_above_ground: 0.3
  min_trunk_height: 1.5
  max_trunk_height: 4.0
  max_angle: 15.0
  buffer_size: 2.0
  voxel_size: 0.02
```

---

#### Example 10: Spatial Structure Quantification

**Scenario**: Analyze horizontal and vertical distribution of forest canopy structure

**Usage Example**:
```
forestry_terrestrial-tls_spatial_structure_quantification
Parameters:
  input_data:
    lidata_data: "/data/tls_plot.lidata"
    vector_data: "/data/plot_boundary.shp"
  output_data: "/output/spatial_structure"
  from_class: [3, 4, 5, 23, 24]
  x_grid_size: 15.0
  y_grid_size: 15.0
  output_type: "TIFF File"
  vertical_voxel_size: 0.2
  statistic_method: "Point Count"
```

---

#### Example 11: Generate Individual Tree Image Report

**Scenario**: Generate visualization reports for surveyed trees

**Important**: Do not hard-code `select_attributes` from experience or pick only a few fields. First read the actual attribute table of the input treedb (`TableHeader[].key` returned by `platform-get_data_information`), exclude `Crown Contour`, and put **every remaining attribute** into `select_attributes` verbatim. `TreePosX`/`TreePosY`/`TreePosZ` may be merged into `Position`, but nothing else may be dropped.

**Usage Example**:
```
forestry_terrestrial-tls_extract_tree_image_report
Parameters:
  input_data:
    input_lidata: "/data/tls_plot.lidata"
    input_tree_attribute: "/data/tls_trees.treedb"
  output_data: "/output/tree_report.html"
  render_img_type: 0
  filter_by_tree_id: true
  min_tree_id: 1
  max_tree_id: 100
  view_type: 2
  select_attributes: ["TreeID", "Position", "Tree Height", "DBH", "Crown Diameter", "Crown Diameter(S-N)", "Crown Diameter(E-W)", "Crown Area", "Crown Volume", "CBH", "Trunk Volume", "Trunk Curvature(%)", "Altitude", "Slope", "Crown Height", "Crown Height Ratio", "Crown Asymmetry", "TreeSpecies", "Tree Species Confidence", "Biomass Above Ground"]
  report_name: "Tree Report"
  report_description: "TLS individual tree report"
  panorama_enabled: false
```

**Notes**:
- The attribute list above is only an example for one treedb. The actual values must come from that `.treedb`'s `TableHeader`; fields vary by dataset.
- Do not include fields that do not exist in the data (e.g. some treedbs have no `TreeSpecies`). Conversely, fields present in the treedb but absent from the default list (e.g. `CBH`, `TreeSpecies`, `Biomass Above Ground`) must be added.

---

#### Example 12: GPS Control Points and Individual Tree Attribute Fuzzy Matching

**Scenario**: Automatically match field-collected GPS points with individual tree attribute table

**Usage Example**:
```
forestry_terrestrial-tls_tree_based_fuzzy_matching
Parameters:
  input_data:
    input_ref_tree_file: "/data/reference_trees.treedb"
    input_reg_tree_file: "/data/gps_control_points.csv"
  output_data: "/output/tree_matching.csv"
  point_distance_threshold: 0.5
```

---

#### Example 13: Forest Tending Planning

**Scenario**: Generate reports and operational design tables based on registered point cloud, individual tree attributes, and tending plan

**Usage Example**:
```json
{
  "tool": "forestry_terrestrial-forest_tending_planning",
  "input": {
    "input_data": {
      "pointcloud_file": "/data/registered_plot.lidata",
      "treedb_file": "/data/plot_trees.treedb",
      "tending_plan_file": "/data/tending_plan.json",
      "roi_vector_file": "/data/plot_boundary.gpkg",
      "input_panorama_folder": "/data/panoramas",
      "input_panorama_list": "/data/panoramas/plot.imglist"
    },
    "output_data": "/output/tending_planning"
  }
}
```

**Output Check**: Verify that the `/output/tending_planning` directory exists and contains actually generated reports and operational design tables; if spatial data is included, call `platform-get_data_information` to verify `data_type`, `feature_count` or point count, and `bounds`.

---

### Individual Tree Modeling Examples

#### Example 14: Generate Tree Models (generate_tree_model)

> **Note**: `generate_tree_model` belongs to the `forestry_airborne` module tools, but is also applicable to terrestrial forestry scenarios.

**Scenario**: Based on the `treedb` individual tree attribute table generated by terrestrial individual tree segmentation, assign model indices from the 360 tree species model library for each species, and generate LiTree individual tree models.

**Usage Example**:
```json
{
  "tool": "forestry_airborne-generate_tree_model",
  "input": {
    "input_data": "/data/tls_tree_attributes.treedb",
    "output_data": "/output/tls_trees.LiTree",
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

## Parameter Reference

### Individual Tree Segmentation Parameter Recommendations

#### Terrestrial TLS

| Parameter | Recommended Value | Description |
|-----|-------|------|
| height_above_ground | 0.3m | Filter near-ground points |
| min_tree_height | 2.0m | Minimum tree height |
| cluster_tolerance | 0.15-0.25m | Clustering tolerance; larger values increase efficiency but may reduce accuracy |
| minimum_cluster_size | 300-1000 | Adjust based on point density |
| trunk_height | 1.6m | Standard TLS segmentation trunk detection height |
| trunk_class | 23 | Trunk point class |
| foliage_class | 24 | Foliage point class |

---

### Biomass Calculation Result Types (calculate_result)

| Value | Result Type | Abbreviation | Description |
|---|---------|------|------|
| 0 | Aboveground Biomass | AGB | Aboveground Biomass |
| 1 | Underground Biomass | UGB | Underground Biomass |
| 2 | Biomass Conversion Factor | BCF | Biomass Conversion Factor (mg/m³) |
| 3 | Stem Volume | V | Stem Volume |
| 4 | Root-Shoot Ratio | RSR | Root-Shoot Ratio |

> **Default Behavior**: If the user does not specify, all result types `[0, 1, 2, 3, 4]` are selected by default; alternatively, select only specific result types based on user requirements.

---

### Biomass Model Types

| Value | Model Type | Input Variables |
|---|---------|---------|
| 0 | Single-variable equation | Single variable such as tree height or DBH |
| 1 | Two-variable equation | Tree height + DBH |
| 2 | Custom equation | User-defined |
| 3 | Other equation | Multi-variable |

---

## Common Issues

### Q1: TLS Segmentation Results Are Not Ideal

**Possible Causes**:
- `from_class` does not include valid vegetation/trunk/foliage classes
- Normalization has not been completed
- `cluster_tolerance`, `minimum_cluster_size`, or `trunk_height` are set inappropriately

**Solutions**:
- Check whether class 23 (trunk) and class 24 (foliage) or high vegetation classes are included in segmentation
- Confirm that normalization has been performed
- Adjust `cluster_tolerance` (0.15-0.25m) and `minimum_cluster_size` (300-1000)

---

### Q2: Biomass Calculation Results Are Empty

**Possible Causes**:
- The treedb file is missing required fields (tree height, DBH, tree species, etc.)
- `method` and `cal_info`/`cal_infos`/`cal_info_us` configuration do not match
- Equation parameters are not marked as valid (`valid` is not true)
- Species does not exist in biomass library and does not support biomass model
- Biomass information not obtained through MCP interfaces (directly reading db files is prohibited)

**Solutions**:
- Run `tls_statistic_tree_attribute` to complete attributes
- Chinese software:
  - Single species -> Use `method=0`, obtain `cal_info` via `QueryBiomassTreeSpeciesInfo`
  - Multiple species -> Use `method=1`, obtain `cal_infos` through tree species matching workflow
  - All species not supported -> Fall back to `method=2`, configure `cal_info_us`
- English software: Only supports `method=2`, configure `cal_info_us`
- Check `valid`, tree species information and `model_type`
- Ensure all biomass information is obtained through MCP interfaces, it is forbidden to directly read `BiomassModel_zh.db` or any `.db` files

---

## Related Documentation

- Tool registry: `references/forestry_terrestrial/tools.md`
- Pre-flight checks: `references/forestry_terrestrial/preflight_checks.md`
- Complete workflows: `references/forestry_terrestrial/workflows.md`
