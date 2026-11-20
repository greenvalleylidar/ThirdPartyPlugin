# Terrestrial Forestry Workflows

> Multi-tool collaborative complete processing workflows for terrestrial forestry analysis, including airborne + terrestrial fusion workflows.
>
> **Execution Priority Rule**: The `from_class` arrays appearing in this document are scenario examples only; actual execution must first read the input data's `class_codes` and confirm the target classes. The accuracy and speed improvement ratios in this document are for reference only and do not constitute a result commitment.

---

## Process Overview

| Scenario | Recommended Process | Key Tools | Difficulty |
|-----|---------|---------|------|
| Terrestrial individual tree segmentation | Terrestrial standard workflow | tls_trunk_based_tree_segmentation | Medium |
| Terrestrial universal individual tree segmentation | Universal segmentation workflow | universal_tree_segmentation | Medium |
| Forest resource inventory | Complete inventory workflow | Multi-tool combination | Very High |
| Biomass estimation | Biomass workflow | tree_biomass_estimation | High |
| Terrestrial rainforest analysis | Rainforest analysis workflow | Multi-tool combination | Very High |
| Airborne + terrestrial fusion | Point cloud fusion workflow | Multi-tool collaboration | Expert |

---

## Terrestrial Forestry Workflows

### Workflow 1: Terrestrial Individual Tree Segmentation Standard Workflow

**Applicable Scenario**: Terrestrial TLS data, standard individual tree segmentation

**Flowchart**:
```
Raw TLS -> Denoising -> Ground Point Classification -> Deep Learning Classification -> Normalization -> Clear Tree IDs -> Trunk-Based Individual Tree Segmentation
```

**Configuration Decision Description**:

| Decision Point | Option 1: Use Deep Learning Classification | Option 2: Skip Deep Learning Classification |
|--------|----------------------|----------------------|
| **Step 4**: Deep Learning Classification | **Execute** - Classify into high vegetation (5) and low vegetation (3) | **Skip** - Proceed directly to normalization |
| **Step 7**: Individual tree segmentation from_class | `[5]` - Use only high vegetation class | `[3, 4, 5, 23, 24]` - Use multiple classes |
| **Applicable Scenario** | Dense understory vegetation, requires precise crown extraction, high data quality | Sparse understory vegetation, fast processing, average data quality |
| **Advantages** | Precise crown extraction, avoids understory vegetation interference, good segmentation results | Fast processing, simple configuration, wide adaptability |
| **Disadvantages** | Depends on deep learning model, increased processing time | May include understory vegetation noise, relatively lower accuracy |

**Recommended Decision Flow**:
```
Start
  |
Is understory vegetation dense? (rich shrubs and herbs)
  | Yes
Execute Step 4: Deep Learning Classification -> Step 7 uses from_class: [5]
  | No
Skip Step 4 -> Step 7 uses from_class: [0, 1, 2, 3, 4, 5...255]
  |
Complete
```

**Detailed Steps**:

#### Step 1: TLS Point Cloud Denoising

```json
{
  "step": 1,
  "description": "TLS point cloud denoising",
  "tool": "pointcloud_processing-pointcloud_outlier_removal",
  "input": {
    "input_data": ["/data/raw_tls.lidata"],
    "neighbor_points": 15,
    "multiples_of_std_deviation": 3,
    "output_data": "/output/denoised_tls.lidata"
  }
}
```

#### Step 2: Resampling (Optional)

```json
{
  "step": 2,
  "description": "Remove duplicate points",
  "tool": "pointcloud_processing-pointcloud_subsampling",
  "input": {
    "input_data": ["/data/raw_tls.lidata"],
    "sampling_type": 0,
    "from_class": [0, 1, 2, 3, 4, 5, 23, 24],
    "minimum_points_spacing": 0.02,
    "output_data": "/output/subsampled_tls.lidata"
  }
}
```

#### Step 3: Ground Point Classification (Progressive TIN Densification)

```json
{
  "step": 3,
  "description": "Ground point classification (Progressive TIN Densification)",
  "tool": "pointcloud_classification-classify_ground_by_progressive_tin_densification",
  "input": {
    "input_data": "{{step2.data.output_data}}",
    "scene_type": 2,
    "grid_size": 20,
    "iteration_angle": 8,
    "iteration_distance": 1.2,
    "max_terrain_angle": 88,
    "max_building_size": 30,
    "tolerance_above": 0.15,
    "tolerance_below": 0.15,
    "to_class": 2
  }
}
```

#### Step 4: Deep Learning Classification

```json
{
  "step": 4,
  "description": "Deep learning classification",
  "tool": "pointcloud_classification-classify_by_deep_learning",
  "input": {
    "input_data": "{{step3.data.output_data}}",
    "scene_type": 2,
    "from_class": [0, 1, 2, 3, 4, 5, 23, 24],
    "high_vegetation_class": 5,
    "low_vegetation_class": 3
  }
}
```

> **Note**: This step uses a deep learning model to classify the point cloud into high vegetation (class 5) and low vegetation (class 3). **If this step is executed, it is recommended to use only the high vegetation class as input for trunk-based individual tree segmentation in Step 7 (from_class: [5]), which can improve segmentation accuracy and efficiency.**

#### Step 5: Point Cloud Normalization

```json
{
  "step": 5,
  "description": "Point cloud normalization",
  "tool": "pointcloud_processing-normalize_by_ground_points",
  "input": {
    "input_data": "{{step4.data.output_data}}",
    "output_data": "/output/normalized_tls.lidata"
  }
}
```

#### Step 6: Clear Tree IDs

```json
{
  "step": 6,
  "description": "Clear tree IDs",
  "tool": "forestry_airborne-clear_tree_id",
  "input": {
    "input_data": "{{step5.data.output_data}}",
    "filter_by_height": false,
    "min_height": 0,
    "max_height": 100
  }
}
```

#### Step 7: Terrestrial Trunk-Based Individual Tree Segmentation

**Configuration Option A - Recommended Configuration (Using Deep Learning Classification Results)**:
```json
{
  "step": 7,
  "description": "Terrestrial trunk-based individual tree segmentation (using high vegetation class)",
  "tool": "forestry_terrestrial-tls_trunk_based_tree_segmentation",
  "input": {
    "input_data": "{{step6.data.output_data}}",
    "output_data": "/output/tls_segmented.treedb",
    "fromClass": [5],
    "trunk_class": 23,
    "foliage_class": 24,
    "height_above_ground": 0.3,
    "trunk_height": 8.0,
    "do_segmentation": true,
    "segment_from": 1.0,
    "extract_to_top": true,
    "cluster_size": 0.2,
    "use_gpu_first": true,
    "optimize_color": false
  }
}
```

**Configuration Option B - Traditional Configuration (Using Multiple Classes)**:
```json
{
  "step": 7,
  "description": "Terrestrial trunk-based individual tree segmentation (using multiple classes)",
  "tool": "forestry_terrestrial-tls_trunk_based_tree_segmentation",
  "input": {
    "input_data": "{{step6.data.output_data}}",
    "output_data": "/output/tls_segmented.treedb",
    "fromClass": [3, 4, 5, 23, 24],
    "trunk_class": 23,
    "foliage_class": 24,
    "height_above_ground": 0.3,
    "trunk_height": 8.0,
    "do_segmentation": true,
    "segment_from": 1.0,
    "extract_to_top": true,
    "cluster_size": 0.2,
    "use_gpu_first": true,
    "optimize_color": false
  }
}
```

> **Configuration Recommendations**:
> - **If Step 4 (Deep Learning Classification) was executed**: Use Configuration Option A, set `from_class: [5]`, segment only high vegetation points to improve accuracy and efficiency
> - **If Step 4 (Deep Learning Classification) was skipped**: Use Configuration Option B, set `from_class: [3, 4, 5, 23, 24]`, segment low vegetation, medium vegetation, high vegetation, trunk, and foliage points

---

### Workflow 2: Terrestrial Universal Individual Tree Segmentation Workflow

**Applicable Scenario**: Terrestrial TLS data, use deep learning universal model for individual tree segmentation

**Flowchart**:
```
Raw TLS -> Denoising -> Ground Point Classification -> Deep Learning Classification -> Normalization -> Clear Tree IDs -> Universal Individual Tree Segmentation
```

**Detailed Steps**:

#### Steps 1-6: Same as Workflow 1 (Preprocessing to Clear Tree IDs)

#### Step 7: Universal Individual Tree Segmentation

```json
{
  "step": 7,
  "description": "Universal individual tree segmentation",
  "tool": "forestry_terrestrial-universal_tree_segmentation",
  "input": {
    "input_data": "{{step6.data.output_data}}",
    "output_data": "/output/tls_universal_segmented.treedb",
    "fromClass": [3, 4, 5, 23, 24],
    "trunk_class": 23,
    "foliage_class": 24,
    "min_tree_height": 2.0,
    "use_gpu_first": true,
    "optimize_color": false
  }
}
```

---

### Workflow 3: Terrestrial Biomass Estimation Workflow

**Applicable Scenario**: Terrestrial TLS data, calculate biomass

**⚠️ Important Principle**: 
- **All biomass information must be obtained through MCP interfaces**, it is strictly forbidden to directly read `BiomassModel_zh.db` or any `.db` files
- MCP interfaces used: `QueryBiomassTreeSpeciesInfo` (biomass library interface), `query_tree_species` (tree species library interface)

**Flowchart**:
```
TLS Segmentation -> Attribute Statistics -> Read treedb tree species (deduplicated)
                                                   |
                                             Count tree species
                                                   |
                                    ┌──────────────┴──────────────┐
                                    ↓                             ↓
                              Single species               Multiple species
                              method=0                     method=1
                              Use cal_info                 Use cal_infos
                                    ↓                             ↓
                                    └──────────────┬──────────────┘
                                                   ↓
                                    Obtain biomass info via MCP interfaces
                                                   ↓
                                    Configuration failed? -> Use method=2
```

**Language and method Selection Rules**:

| Software Language | Available method | Default method | Required Equation Configuration Parameters |
|---------|-----------|-----------|----------------|
| Chinese | 0, 1 or 2 | 0 or 1 | method=0 -> `cal_info`; method=1 -> `cal_infos`; method=2 -> `cal_info_us` |
| English | 2 only | 2 | `cal_info_us` |

**Chinese Software Biomass Calculation Workflow**:

1. **Read treedb file**, extract the "TreeSpecies" column and deduplicate to get the tree species list
2. **Determine tree species count**:
   - Single species -> Use `method=0`, configure `cal_info`
   - Multiple species -> Use `method=1`, configure `cal_infos`
3. **Obtain biomass information through MCP interfaces** (see "Tree Species Matching Workflow" below)
4. **If all species do not support biomass models** -> Fall back to `method=2`, configure `cal_info_us`

**Detailed Steps**:

#### Steps 1-7: Same as Workflow 1 (Denoising to Trunk-based Segmentation)

#### Step 8: Statistics of Individual Tree Attributes

```json
{
   "step": 8,
   "description": "Statistics of individual tree attributes (preparation for biomass calculation)",
   "tool": "forestry_terrestrial-tls_statistic_tree_attribute",
   "input": {
      "input_data": "{{step7.data.output_data}}",
      "output_data": "/output/tls_with_attributes.treedb"
   }
}
```

> **Note**: This step is used to complete the necessary attribute fields in the treedb file to ensure that subsequent biomass calculations can proceed normally.

#### Step 9: Read treedb and Extract Tree Species Information

```json
{
   "step": 9,
   "description": "Read treedb file, extract and deduplicate tree species column",
   "action": "Read treedb file from {{step8.data.output_data}}",
   "extract_field": "TreeSpecies",
   "operation": "Deduplicate to get tree species list",
   "example": "For example, after deduplication: [\"123\", \"American beech\", \"Eucalyptus globulus Labill.\", \"Fagus grandifolia\"]"
}
```

#### Step 9.1: Tree Species Matching Workflow (Obtain Biomass Information via MCP Interfaces)

**⚠️ Core Principle**: All biomass information must be obtained through MCP interfaces, directly reading db files is prohibited

**Tree Species Matching Workflow** (execute for each deduplicated tree species):

```
Start
  ↓
Use QueryBiomassTreeSpeciesInfo to match tree species name
  ↓
Match successful? -> Yes -> Directly obtain location, tree_species_id, model_type
  ↓ No
Use query_tree_species to match tree species name
  ↓
Match successful? -> No -> This species does not support biomass model
  ↓ Yes
Check if biomass model is supported
  ↓
Supported? -> No -> This species does not support biomass model
  ↓ Yes
Obtain the species name in the biomass library
  ↓
Use QueryBiomassTreeSpeciesInfo to match the biomass library name
  ↓
Match successful? -> No -> This species does not support biomass model
  ↓ Yes
Obtain location, tree_species_id, model_type
  ↓
Complete (tree_species_name always fills in the original tree species name from treedb)
```

**Key Notes**:
- `query_tree_species` interface can only obtain tree species information and biomass model names from the tree species library, cannot obtain complete biomass library information
- Must use `QueryBiomassTreeSpeciesInfo` interface to obtain complete biomass library information (location, tree_species_id, model_type, etc.)
- `tree_species_name` field always fills in the original tree species name from treedb, even if matched successfully through biomass library name

**Examples**:

**Example 1**: Tree species in treedb is "123"
1. Use `QueryBiomassTreeSpeciesInfo` to match "123" -> Match failed
2. Use `query_tree_species` to match "123" -> Match successful, found to support biomass model, obtained biomass library name as "my123"
3. Use `QueryBiomassTreeSpeciesInfo` to match "my123" -> Match successful, obtained location, tree_species_id, model_type
4. When filling in, `tree_species_name` still fills "123" (original name from treedb)

**Example 2**: Tree species in treedb is "MyAmericanbeech"
1. Use `QueryBiomassTreeSpeciesInfo` to match "MyAmericanbeech" -> Match successful
2. Directly obtain location, tree_species_id, model_type
3. `tree_species_name` fills "MyAmericanbeech"

**Example 3**: Tree species in treedb is "Fagus grandifolia"
1. Use `QueryBiomassTreeSpeciesInfo` to match "Fagus grandifolia" -> Match failed
2. Use `query_tree_species` to match "Fagus grandifolia" -> Match successful, found to support biomass model, obtained biomass library name as "MyAmericanbeech"
3. Use `QueryBiomassTreeSpeciesInfo` to match "MyAmericanbeech" -> Match successful, obtained location, tree_species_id, model_type (tree_species_id is 1200000004)
4. `tree_species_name` still fills "Fagus grandifolia" (original name from treedb)

> **Note**: In Examples 2 and 3, although the tree species names are different, they correspond to the same species in the biomass library, so `tree_species_id` is both 1200000004.

#### Step 9a: Individual Tree Biomass Calculation (method=0, Single Species)

**Applicable Scenario**: All trees in treedb belong to the same species

```json
{
   "step": "9a",
   "description": "Individual tree biomass calculation (method=0)",
   "tool": "forestry_terrestrial-tree_biomass_estimation",
   "input": {
      "input_data": {
         "input_data": "{{step8.data.output_data}}",
         "output_data": "/output/tls_biomass.treedb"
      },
      "with_progress": true,
      "method": 0,
      "calculate_result": [0, 1, 2, 3, 4],
      "valid": true,
      "cal_info": {
         "location": "Obtained via QueryBiomassTreeSpeciesInfo",
         "model_type": "Obtained via QueryBiomassTreeSpeciesInfo (0=univariate, 1=bivariate)",
         "tree_species_id": "Obtained via QueryBiomassTreeSpeciesInfo",
         "valid": true
      }
   }
}
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

> **Note**: For method=0, `location`, `model_type`, `tree_species_id` in `cal_info` all come from the biomass library, must be directly obtained through `QueryBiomassTreeSpeciesInfo` interface, has nothing to do with `query_tree_species`.

#### Step 9b: Individual Tree Biomass Calculation (method=1, Multiple Species)

**Applicable Scenario**: treedb contains multiple different species

**cal_infos Structure Notes**:
- `cal_infos` is an array, each element corresponds to a deduplicated species from treedb
- Each element contains: `location`, `model_type`, `tree_species_id`, `tree_species_name`, `valid`
- `tree_species_name` always fills in the original tree species name from treedb
- Other fields are obtained through the tree species matching workflow

**Handling Multiple locations or Multiple Equations**:
- One species may correspond to multiple regions (location)
- One location may have multiple equations (univariate or bivariate)
- `model_type`: 0=univariate equation, 1=bivariate equation
- **If there are multiple locations or multiple equations, the user needs to specify which one to use**

```json
{
   "step": "9b",
   "description": "Individual tree biomass calculation (method=1)",
   "tool": "forestry_terrestrial-tree_biomass_estimation",
   "input": {
      "input_data": {
         "input_data": "{{step8.data.output_data}}",
         "output_data": "/output/tls_biomass.treedb"
      },
      "with_progress": true,
      "method": 1,
      "calculate_result": [0, 1, 2, 3, 4],
      "valid": true,
      "cal_infos": [
         {
            "location": "Obtained through tree species matching workflow",
            "model_type": "Obtained through tree species matching workflow (0=univariate, 1=bivariate)",
            "tree_species_id": "Obtained through tree species matching workflow",
            "tree_species_name": "Original tree species name from treedb (first after deduplication)",
            "valid": true
         },
         {
            "location": "Obtained through tree species matching workflow",
            "model_type": "Obtained through tree species matching workflow",
            "tree_species_id": "Obtained through tree species matching workflow",
            "tree_species_name": "Original tree species name from treedb (second after deduplication)",
            "valid": true
         }
      ]
   }
}
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
> - `tree_species_name` for each species fills in the original name from treedb
> - `location`, `model_type`, `tree_species_id` are obtained through the tree species matching workflow
> - If a species cannot be found in the biomass library and does not support biomass model, it should not be included in `cal_infos`

#### Step 9c: Individual Tree Biomass Calculation (method=2, All Species Do Not Support Biomass Model or English Software)

```json
{
   "step": "9c",
   "description": "Individual tree biomass calculation (method=2)",
   "tool": "forestry_terrestrial-tree_biomass_estimation",
   "input": {
      "input_data": {
         "input_data": "{{step8.data.output_data}}",
         "output_data": "/output/tls_biomass.treedb"
      },
      "with_progress": true,
      "method": 2,
      "calculate_result": [],
      "valid": true,
      "cal_info_us": [
         {
            "comp_id": 6,
            "eqn_no": 400,
            "reference_author": "Carpenter 1983",
            "region": "09",
            "species_name": "tamarack (native)"
         }
      ]
   }
}
```

---

### Workflow 4: Terrestrial Rainforest Analysis Workflow

**Applicable Scenario**: Tropical rainforest, extract trunks and spatial structure

**Flowchart**:
```
TLS Preprocessing -> Trunk Extraction -> Spatial Structure Quantification -> Report Generation
```

**Detailed Steps**:

#### Steps 1-5: Same as Workflow 1 (Preprocessing to Normalization)

#### Step 6: Rainforest Trunk Extraction

```json
{
  "step": 6,
  "description": "Rainforest trunk extraction",
  "tool": "forestry_terrestrial-tls_tree_trunk_extraction",
  "input": {
    "input_data": "{{step5.data.output_data}}",
    "fromClass": [3, 4, 5, 23, 24],
    "height_above_ground": 0.3,
    "min_trunk_height": 1.5,
    "max_trunk_height": 4.0,
    "max_angle": 15.0,
    "buffer_size": 2.0,
    "voxel_size": 0.02
  }
}
```

#### Step 7: Spatial Structure Quantification

```json
{
  "step": 7,
  "description": "Spatial structure quantification",
  "tool": "forestry_terrestrial-tls_spatial_structure_quantification",
  "input": {
    "input_data": {
      "lidata_data": "{{step5.data.output_data}}",
      "vector_data": "/data/plot_boundary.shp"
    },
    "output_data": "/output/spatial_structure",
    "fromClass": [3, 4, 5, 23, 24],
    "x_grid_size": 15.0,
    "y_grid_size": 15.0,
    "output_type": "CSV File",
    "vertical_voxel_size": 0.2,
    "statistic_method": "Point Count"
  }
}
```

#### Step 8: Generate Individual Tree Image Report

> `select_attributes` must come from the actual fields of the input treedb: first read `TableHeader[].key` via `platform-get_data_information`, exclude `Crown Contour`, and keep every remaining field (`TreePosX/Y/Z` may be merged into `Position`). Do not use a fixed, trimmed list.

```json
{
  "step": 8,
  "description": "Generate individual tree image report",
  "tool": "forestry_terrestrial-tls_extract_tree_image_report",
  "input": {
    "input_data": {
      "input_lidata": "{{step4.data.output_data}}",
      "input_tree_attribute": "/output/tls_trees.treedb"
    },
    "output_data": "/output/tree_report.html",
    "render_img_type": 0,
    "filter_by_tree_id": true,
    "min_tree_id": 1,
    "max_tree_id": 100,
    "view_type": 2,
    "select_attributes": ["TreeID", "Position", "Tree Height", "DBH", "Crown Diameter", "Crown Diameter(S-N)", "Crown Diameter(E-W)", "Crown Area", "Crown Volume", "CBH", "Trunk Volume", "Trunk Curvature(%)", "Altitude", "Slope", "Crown Height", "Crown Height Ratio", "Crown Asymmetry", "TreeSpecies", "Tree Species Confidence", "Biomass Above Ground"],
    "report_name": "Tree Report",
    "report_description": "TLS individual tree report",
    "panorama_enabled": false
  }
}
```

---

### Workflow 5: Forest Tending Planning Workflow

**Applicable Scenario**: Point cloud individual tree segmented and individual tree attribute statistics have been completed; generate reports and operational design tables based on the tending plan.

```text
Individual tree segmented  Point Cloud + TreeDB + Tending Plan JSON + Optional ROI/Panorama -> Forest Tending Planning -> Reports and Operational Design Tables
```

```json
{
  "step": 1,
  "description": "Generate forest tending planning outputs",
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

> After output, verify that reports and operational design table files actually exist in the directory; if spatial products are generated, call `platform-get_data_information` to verify `data_type`, `feature_count` or point count, and `bounds`.

---

## Airborne + Terrestrial Fusion Workflow

### Workflow 5: Airborne + Terrestrial Point Cloud Fusion

**Applicable Scenario**: Combine the advantages of airborne and terrestrial data to improve accuracy

**Flowchart**:
```
Terrestrial Processing -> Trunk Segmentation -> Denormalization
Airborne Processing -> Vegetation Classification
Merge -> Close-by Point Classification -> Trunk Extraction -> Fusion Complete
```

**Detailed Steps**:

#### Terrestrial Part:

##### Steps 1-5: Terrestrial Preprocessing (Same as Workflow 1)

```json
{
  "workflow": "Terrestrial Preprocessing",
  "input": "/data/tls.lidata",
  "output": "/output/tls_normalized.lidata"
}
```

##### Step 7: Terrestrial Trunk-Based Individual Tree Segmentation

```json
{
  "step": 7,
  "description": "Terrestrial trunk-based individual tree segmentation",
  "tool": "forestry_terrestrial-tls_trunk_based_tree_segmentation",
  "input": {
    "input_data": "/output/tls_normalized.lidata",
    "output_data": "/output/tls_trunk.lidata",
    "fromClass": [3, 4, 5, 23, 24],
    "trunk_class": 23,
    "foliage_class": 24,
    "height_above_ground": 0.3,
    "trunk_height": 8.0,
    "do_segmentation": true,
    "segment_from": 1.0,
    "extract_to_top": true,
    "cluster_size": 0.2,
    "use_gpu_first": true,
    "optimize_color": false
  }
}
```

##### Step 8: Denormalization

```json
{
  "step": 8,
  "description": "Denormalization (restore original elevation)",
  "tool": "pointcloud_processing-denormalize",
  "input": {
    "input_data": "{{step7.data.output_data}}",
    "output_data": "/output/tls_original.lidata"
  }
}
```

#### Airborne Part:

##### Step 9: Airborne Vegetation Classification

```json
{
  "step": 9,
  "description": "Classify airborne point cloud to class 5 (high vegetation)",
  "tool": "pointcloud_classification-classify_by_attribute",
  "input": {
    "input_data": "/data/als.lidata",
    "attribute": 0,
    "min_value": 0,
    "max_value": 0,
    "to_class": 5
  }
}
```

#### Fusion Part:

##### Step 10: Data Merge

```json
{
  "step": 10,
  "description": "Merge airborne and terrestrial point clouds",
  "tool": "pointcloud_processing-pointcloud_merge",
  "input": {
    "input_data": ["{{step8.data.output_data}}", "{{step9.data.output_data}}"],
    "output_data": "/output/merged.lidata"
  }
}
```

##### Step 11: Close-by Point Classification (Extract Airborne Trunk Points)

```json
{
  "step": 11,
  "description": "Close-by point classification - extract airborne trunk points",
  "tool": "pointcloud_classification-classify_closeby_points",
  "input": {
    "input_data": "{{step10.data.output_data}}",
    "from_class": [5],
    "closeby_class": [23],
    "to_class": 7
  }
}
```

##### Step 12: Merge Class 7 into Class 23 (Trunk)

```json
{
  "step": 12,
  "description": "Merge class 7 into class 23 (trunk)",
  "tool": "pointcloud_classification-classify_by_attribute",
  "input": {
    "input_data": "{{step11.data.output_data}}",
    "attribute": 0,
    "min_value": 0,
    "max_value": 0,
    "from_class": [7],
    "to_class": 23
  }
}
```

##### Step 13: Universal Individual Tree Segmentation Based on Fused Data

```json
{
  "step": 13,
  "description": "Universal individual tree segmentation based on fused data",
  "tool": "forestry_terrestrial-universal_tree_segmentation",
  "input": {
    "input_data": "{{step12.data.output_data}}",
    "output_data": "/output/fused_segmentation.treedb",
    "fromClass": [5, 23, 24],
    "trunk_class": 23,
    "foliage_class": 24,
    "min_tree_height": 2.0,
    "use_gpu_first": true,
    "optimize_color": false
  }
}
```

---

## Parameter Configuration Quick Reference

### Scene Type (scene_type)

| Value | Type | Applicable Scenario |
|---|------|---------|
| 1 | Steep terrain | Mountainous areas, steep slopes |
| 2 | Gentle slope terrain | Hills, gentle slopes |
| 3 | Flat terrain | Plains, flat areas |

### Interpolation Method (interpolator)

| Value | Method | Characteristics |
|---|------|------|
| 0 | IDW (Inverse Distance Weight) | Fast computation, simple |
| 1 | Kriging | High accuracy, considers spatial autocorrelation |
| 2 | TIN (Triangulated Irregular Network) | Preserves details |

### Key Class Codes (ASPRS Standard)

| Class | Purpose | Description |
|-----|------|------|
| 0 | Unclassified | Never Classified |
| 1 | Unclassified | Unclassified |
| 2 | Ground | Ground |
| 3 | Low Vegetation | Low Vegetation (<0.5m) |
| 4 | Medium Vegetation | Medium Vegetation (0.5-2m) |
| 5 | High Vegetation | High Vegetation (>2m) |
| 23 | Trunk | Trunk (User-defined) |
| 24 | Branches and Leaves | Branches and Leaves (User-defined) |

### Individual Tree Segmentation Parameter Recommendations

#### Terrestrial TLS

| Parameter | Recommended Value | Adjustment Recommendation |
|-----|-------|---------|
| height_above_ground | 0.3m | Filter ground noise |
| min_tree_height | 2.0m | Based on minimum target tree height |
| cluster_tolerance | 0.15-0.25m | Reduce when trees are dense |
| minimum_cluster_size | 300-1000 | Adjust based on point density |
| trunk_height | 1.6m/8.0m | Standard segmentation commonly uses 1.6m; trunk-priority segmentation set to maximum trunk height |
| trunk_class | 23 | Trunk point class |
| foliage_class | 24 | Foliage point class |
| **from_class** | **[5] or [3,4,5,23,24]** | **See detailed description below** |

#### from_class Parameter Configuration Guide

**The `from_class` parameter determines which point cloud classes are used for individual tree segmentation. Based on whether deep learning classification is used, there are two configuration methods:**

| Configuration Scenario | from_class Value | Description | Recommendation Rating |
|---------|------------|------|---------|
| **Using deep learning classification** | `[5]` | Use only high vegetation class (>2m), accurately classified through deep learning | 5 stars |
| **Not using deep learning classification** | `[3, 4, 5, 23, 24]` | Use low vegetation, medium vegetation, high vegetation, trunk, and foliage points | 4 stars |

**Configuration Decision Basis**:

1. **Conditions for using from_class: [5] (Recommended)**
   - Step 4 executed: Deep learning classification
   - Understory vegetation is dense (rich shrubs and herbs)
   - Requires precise crown extraction, avoids understory vegetation interference
   - TLS data quality is high, point cloud density is large
   - Pursuing high-accuracy individual tree segmentation

2. **Conditions for using from_class: [3, 4, 5, 23, 24]**
   - Step 4 skipped: Deep learning classification
   - Understory vegetation is sparse, less interference
   - Need to retain more point cloud information
   - TLS data quality is average, point cloud density is lower
   - Fast processing needs take priority

**Performance Comparison**:
- **Accuracy**: from_class: [5] > from_class: [3,4,5,23,24] (approximately 10-20% improvement)
- **Speed**: from_class: [5] > from_class: [3,4,5,23,24] (approximately 25-35% faster)
- **Understory anti-interference**: from_class: [5] >> from_class: [3,4,5,23,24] (significant improvement)

### Forest Metrics Calculation Parameters

| Parameter | Recommended Value | Description |
|-----|-------|------|
| voxel_size | 0.02m | Voxel size; can be appropriately increased when point density is low |
| voxel_size_method | Voxel Size | Directly use voxel size; can also be set by mean distance coefficient |
| coefficient | 2.0 | Mean distance multiplier when using coefficient method |
| x_grid_size/y_grid_size | 15-30m | Adjust based on research scale |
| vertical_voxel_size | 0.2m | Vertical voxel size for spatial structure quantification |
| use_height_range | false/true | Enable only when calculating statistics for a specified height range |

### Biomass Calculation Result Types (calculate_result)

| Value | Result Type | Abbreviation | Description |
|---|---------|------|------|
| 0 | Aboveground Biomass | AGB | Aboveground Biomass |
| 1 | Underground Biomass | UGB | Underground Biomass |
| 2 | Biomass Conversion Factor | BCF | Biomass Conversion Factor (mg/m³) |
| 3 | Stem Volume | V | Stem Volume |
| 4 | Root-Shoot Ratio | RSR | Root-Shoot Ratio |

> **Default Behavior**: If the user does not specify, all result types `[0, 1, 2, 3, 4]` are selected by default; alternatively, select only specific result types based on user requirements.

### Biomass Model Types

| Value | Model Type | Input Variables |
|---|---------|---------|
| 0 | Single-variable equation | Single variable such as tree height or DBH |
| 1 | Two-variable equation | Tree height + DBH |
| 2 | Custom equation | User-defined |
| 3 | Other equation | Multi-variable |

---

## Common Issues and Solutions

### Issue 1: TLS Segmentation Results Are Not Ideal

**Possible Causes**:
- `fromClass` does not include valid vegetation/trunk/foliage classes
- Normalization has not been completed
- `cluster_tolerance`, `minimum_cluster_size`, or `trunk_height` are set inappropriately

**Solutions**:
- Check whether class 23 (trunk) and class 24 (foliage) or high vegetation classes are included in segmentation
- Confirm that normalization has been performed (has OriginalZ attribute)
- Adjust `cluster_tolerance` to 0.15-0.25m, and adjust `minimum_cluster_size` based on point density

---

### Issue 2: Biomass Calculation Results Are Empty

**Possible Causes**:
- The treedb file is missing required fields
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
- Check `valid`, tree species information, and `model_type`
- Ensure all biomass information is obtained through MCP interfaces, it is forbidden to directly read `BiomassModel_zh.db` or any `.db` files

---

### Issue 3: Poor Segmentation Results After Fusion

**Possible Causes**:
- Terrestrial trunk extraction is incomplete
- Airborne vegetation classification is inaccurate
- Close-by point classification threshold is inappropriate

**Solutions**:
- Improve terrestrial trunk segmentation (use trunk-priority method)
- Check airborne vegetation classification results
- Adjust `distance_threshold` to 0.15-0.25m

---

### Issue 4: Fusion Fails Due to Inconsistent Coordinate Systems

**Possible Causes**:
- Airborne and terrestrial data use different coordinate systems
- Terrestrial data elevation datum after normalization is not suitable for direct fusion

**Solutions**:
- Unify the coordinate system for airborne and terrestrial data
- Denormalize terrestrial data before fusion
- Verify that the spatial range overlap of the two periods of data is at least 30%

---

### Issue 5: Rainforest Trunk Extraction Is Incomplete

**Possible Causes**:
- Tilt angle threshold is set too small
- Trunk height range is set inappropriately
- Buffer size is insufficient

**Solutions**:
- Increase `max_angle` to 15-20 degrees
- Adjust `min_trunk_height` and `max_trunk_height`
- Increase `buffer_size` to 2.0-3.0m

---

### Issue 6: Understory Vegetation Interferes with Segmentation Results

**Possible Causes**:
- Deep learning classification was not used, understory vegetation is included in segmentation
- from_class configuration includes low vegetation classes (3, 4)
- Understory vegetation is dense, affecting crown extraction

**Solutions**:
- **Recommended solution**: Execute Step 4 deep learning classification, use `from_class: [5]` to process only high vegetation
- **Alternative solution**: Adjust the `height_above_ground` parameter to filter low vegetation
- **Parameter tuning**: Increase `cluster_tolerance` to avoid understory vegetation being misclassified as individual trees
- **Data preprocessing**: Manually check and adjust classification results after deep learning classification

---

## Related Documentation

- Tool registry: `references/forestry_terrestrial/tools.md`
- Pre-flight checks: `references/forestry_terrestrial/preflight_checks.md`
- Typical examples: `references/forestry_terrestrial/examples.md`
- Airborne forestry workflows: `references/forestry_airborne/workflows.md`
- Common profiles: `references/profiles/`
