# Airborne Forestry Workflows

> Multi-tool collaborative complete processing workflows for airborne forestry analysis.

---

## Process Overview

| Scenario | Recommended Process | Key Tools | Difficulty |
|-----|---------|---------|------|
| Airborne individual tree segmentation | Airborne standard workflow | trunk_based_tree_segmentation | Medium |
| CHM-assisted segmentation | CHM segmentation workflow | chm_segmentation | Medium |
| Image-based segmentation | Image segmentation workflow | individual_tree_crown_segmentation | High |
| Forest resource inventory | Complete inventory workflow | Multi-tool combination | Very High |
| Regression analysis | Model training workflow | Regression toolset | Very High |
| Multi-temporal change detection | Change detection workflow | forest_structure_change_detection | Very High |
| Airborne + terrestrial fusion | Point cloud fusion workflow | Multi-tool collaboration | Expert |

---

## Airborne Forestry Workflows

### Workflow 1: Airborne Individual Tree Segmentation Standard Workflow

**Applicable Scenario**: Standard airborne point cloud, from raw data to individual tree attributes

**Flowchart**:
```
Raw Point Cloud -> Denoising -> Ground Point Classification -> Deep Learning Classification -> Normalization -> Clear Tree IDs -> Individual Tree Segmentation -> Attribute Statistics
```

**Configuration Decision Description**:

| Decision Point | Option 1: Use Deep Learning Classification | Option 2: Skip Deep Learning Classification |
|--------|----------------------|----------------------|
| **Step 3**: Deep Learning Classification | **Execute** - Classify into high vegetation (5) and low vegetation (3) | **Skip** - Proceed directly to normalization |
| **Step 6**: Individual tree segmentation from_class | `[5]` - Use only high vegetation class | `[0, 1, 2, 3, 4, 5, 23, 24]` - Use all classes |
| **Applicable Scenario** | Complex vegetation, requires high accuracy, high point cloud density | Simple vegetation, fast processing, low point cloud density |
| **Advantages** | High segmentation accuracy, fast processing speed, less noise | Simple processing, no dependency on deep learning models |
| **Disadvantages** | Requires deep learning model, slightly increased processing time | May include noise, relatively lower accuracy |

**Recommended Decision Flow**:
```
Start
  |
Is vegetation complex? (severe crown overlap, rich understory)
  | Yes
Execute Step 3: Deep Learning Classification -> Step 6 uses from_class: [5]
  | No
Skip Step 3 -> Step 6 uses from_class: [0, 1, 2, 3, 4, 5, 23, 24]
  |
Complete
```

**Detailed Steps**:

#### Step 1: Point Cloud Preprocessing (Denoising)

```json
{
  "step": 1,
  "description": "Outlier removal",
  "tool": "pointcloud_processing-pointcloud_outlier_removal",
  "input": {
    "input_data": ["/data/raw_als.lidata"],
    "neighbor_points": 10,
    "multiples_of_std_deviation": 5,
    "output_data": "/output/denoised_als.lidata"
  }
}
```

#### Step 2: Ground Point Classification (Progressive TIN Densification)

```json
{
  "step": 2,
  "description": "Ground point classification (Progressive TIN Densification)",
  "tool": "pointcloud_classification-classify_ground_by_progressive_tin_densification",
  "input": {
    "input_data": "{{step1.data.output_data}}",
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

#### Step 3: Deep Learning Classification

```json
{
  "step": 3,
  "description": "Deep learning classification",
  "tool": "pointcloud_classification-classify_by_deep_learning",
  "input": {
    "input_data": "{{step2.data.output_data}}",
    "scene_type": 2,
    "from_class": [0, 1, 2, 3, 4, 5, 6],
    "high_vegetation_class": 5,
    "low_vegetation_class": 3
  }
}
```

> **Note**: This step uses a deep learning model to classify the point cloud into high vegetation (class 5) and low vegetation (class 3). **If this step is executed, it is recommended to use only the high vegetation class as input for individual tree segmentation in Step 6 (from_class: [5]), which can improve segmentation accuracy and efficiency.**

#### Step 4: Point Cloud Normalization

```json
{
  "step": 4,
  "description": "Point cloud normalization",
  "tool": "pointcloud_processing-normalize_by_ground_points",
  "input": {
    "input_data": "{{step3.data.output_data}}",
    "output_data": "/output/normalized_als.lidata"
  }
}
```

#### Step 5: Clear Tree IDs

```json
{
  "step": 5,
  "description": "Clear tree IDs (before re-segmentation)",
  "tool": "forestry_airborne-clear_tree_id",
  "input": {
    "input_data": "{{step4.data.output_data}}",
    "filter_by_height": false,
    "min_height": 0,
    "max_height": 100
  }
}
```

#### Step 6: Individual Tree Segmentation

**Configuration Option A - Recommended Configuration (Using Deep Learning Classification Results)**:
```json
{
  "step": 6,
  "description": "Individual tree segmentation (using high vegetation class)",
  "tool": "forestry_airborne-trunk_based_tree_segmentation",
  "input": {
    "input_data": "{{step5.data.output_data}}",
    "output_data": "/output/segmented_trees.treedb",
    "trunk_class": 23,
    "foliage_class": 24,
    "height_above_ground": 0.3,
    "use_gpu_first": true,
    "optimize_color": true,
    "from_class": [5]
  }
}
```

**Configuration Option B - Traditional Configuration (Using All Classes)**:
```json
{
  "step": 6,
  "description": "Individual tree segmentation (using all classes)",
  "tool": "forestry_airborne-trunk_based_tree_segmentation",
  "input": {
    "input_data": "{{step5.data.output_data}}",
    "output_data": "/output/segmented_trees.treedb",
    "trunk_class": 23,
    "foliage_class": 24,
    "height_above_ground": 0.3,
    "use_gpu_first": true,
    "optimize_color": true,
    "from_class": [0, 1, 2, 3, 4, 5, 23, 24]
  }
}
```

> **Configuration Recommendations**:
> - **If Step 3 (Deep Learning Classification) was executed**: Use Configuration Option A, set `from_class: [5]`, segment only high vegetation points to improve accuracy and efficiency
> - **If Step 3 (Deep Learning Classification) was skipped**: Use Configuration Option B, set `from_class: [0, 1, 2, 3, 4, 5, 23, 24]`, segment all non-ground points

#### Step 7: Individual Tree Attribute Statistics

```json
{
  "step": 7,
  "description": "Individual tree attribute statistics",
  "tool": "forestry_airborne-als_individual_tree_attribute_statistics",
  "input": {
    "input_data": "{{step6.data.output_data.derived_output_data_of_input_data}}",
    "output_data": "{{step6.data.output_data.treedb_file}}",
    "select_attribute_to_statistic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    "height_above_ground": 0.3,
    "min_tree_height": 2.0,
    "stem_class": 23,
    "als_or_tls_datatype": 0,
    "is_updating": "Do Not Update",
    "delete_unstatistic_tree_when_update": false,
    "new_file_suffix": "_stat"
  }
}
```

---

### Workflow 2: CHM-Assisted Segmentation Workflow

**Applicable Scenario**: Use CHM to improve segmentation accuracy

**Flowchart**:
```
Point Cloud -> Ground Point Classification -> Normalization -> Generate CHM -> CHM Pit Filling -> CHM Segmentation -> Crown Boundaries
```

**Detailed Steps**:

#### Steps 1-4: Same as Workflow 1 (Denoising, Classification, Deep Learning Classification, Normalization)

#### Step 5: Generate CHM

```json
{
  "step": 5,
  "description": "Generate CHM",
  "tool": "terrain_analysis-generate_chm",
  "input": {
    "input_data": {
      "input_dem": "/output/dem.tif",
      "input_dsm": "/output/dsm.tif"
    },
    "output_data": "/output/chm.tif"
  }
}
```

#### Step 6: CHM Pit Filling

```json
{
  "step": 6,
  "description": "CHM pit filling",
  "tool": "forestry_airborne-chm_pits_filling",
  "input": {
    "input_data": "{{step5.data.output_data}}",
    "chm_pits_filling_threshold_pix": 5,
    "output_data": "/output/chm_filled.tif"
  }
}
```

#### Step 7: CHM Segmentation

```json
{
  "step": 7,
  "description": "CHM individual tree segmentation",
  "tool": "forestry_airborne-chm_segmentation",
  "input": {
    "input_data": "{{step6.data.output_data}}",
    "output_data": "/output/chm_segmentation",
    "minimum_tree_height": 1.0,
    "maximum_tree_height": 80.0,
    "sigma": 1.0,
    "radius_pix": 5,
    "buffer_size": 1.0,
    "is_smooth": true,
    "chm_pits_filling": true,
    "crown_base_height_threshold": 0.8
  }
}
```

#### Step 8: Generate Seed Points (Optional)

```json
{
  "step": 8,
  "description": "Generate seed points from CHM",
  "tool": "forestry_airborne-generate_seed_points_from_chm",
  "input": {
    "input_data": "{{step6.data.output_data}}",
    "output_data": "/output/seed_points.csv",
    "minimum_tree_height": 1.0,
    "maximum_tree_height": 80.0,
    "sigma": 1.0,
    "radius_pix": 5,
    "buffer_size": 1.0,
    "is_smooth": true
  }
}
```

---

### Workflow 3: Image-Based Segmentation Workflow

**Applicable Scenario**: High-resolution orthophoto imagery is available

**Image requirements**:
- **Resolution**: It is recommended that the input orthophoto image resolution is between **0.01m-0.1m**, that is, the actual ground size represented by each pixel is 0.01m-0.1m
- **Image size**: There is no limit to the size of the input image

**Flowchart**:
```
Load Point Cloud -> Load Imagery -> Image Alignment -> Image Segmentation -> Export Results
```

**Detailed Steps**:

#### Step 1: Load Point Cloud (omitted)

#### Step 2: Load Imagery

```json
{
  "step": 2,
  "description": "Load imagery",
  "tool": "platform-load_layer",
  "input": {
    "input_data": ["/data/ortho.tif"],
    "data_type": "Image"
  }
}
```

#### Step 3: Image Alignment

```json
{
  "step": 3,
  "description": "Align imagery to point cloud",
  "tool": "imagery_processing-align_to_point_cloud",
  "input": {
    "input_data": {
      "image_project": "/data/image_project.liaep",
      "point_cloud_list": ["/data/normalized_als.lidata"]
    },
    "output_data": "/output/aligned_image_project.liaep"
  }
}
```

#### Step 4: Individual Tree Crown Segmentation

```json
{
  "step": 4,
  "description": "Image-based individual tree crown segmentation",
  "tool": "forestry_airborne-individual_tree_crown_segmentation",
  "input": {
    "input_data": {
      "input_data": "{{step3.data.output_data}}",
      "mask_file": "/data/study_area.shp"
    },
    "confidence_threshold": 0.3,
    "overlap_ratio": 0.7,
    "output_data": "/output/image_segmentation"
  }
}
```

---

### Workflow 4: Complete Forest Resource Inventory Workflow

**Applicable Scenario**: Systematic forest resource inventory requiring multi-dimensional parameters

**Flowchart**:
```
Point Cloud Preprocessing -> Individual Tree Segmentation -> Stand Metrics Calculation -> Grid Metrics Calculation -> Report Generation
```

**Detailed Steps**:

#### Steps 1-6: Same as Workflow 1 (Denoising to Individual Tree Segmentation)

#### Step 6: Stand-Level Metrics Calculation

```json
{
  "step": 6,
  "description": "Stand-level metrics calculation",
  "tool": "forestry_airborne-calculate_forest_metrics_by_forest_stands",
  "input": {
    "input_data": "{{step3.data.output_data}}",
    "output_data": "/output/stand_metrics.csv",
    "extinction_coefficient": 0.5,
    "height_break": 2.0,
    "from_class": [3, 4, 5],
    "is_select_canopy_cover": true,
    "is_select_gap_fraction": true,
    "is_select_leaf_area_index": true,
    "is_select_elevation_metrics": true,
    "is_select_intensity_metrics": true
  }
}
```

#### Step 7: Grid-Based Metrics Calculation

```json
{
  "step": 7,
  "description": "Grid-based metrics calculation",
  "tool": "forestry_airborne-calculate_forest_metrics_by_grid",
  "input": {
    "input_data": "{{step3.data.output_data}}",
    "output_data": "/output/grid_metrics.tif",
    "x_grid_size": 15.0,
    "y_grid_size": 15.0,
    "height_break": 2.0,
    "extinction_coefficient": 0.5,
    "from_class": [3, 4, 5],
    "is_select_canopy_cover": true,
    "is_select_gap_fraction": true,
    "is_select_leaf_area_index": true,
    "is_select_elevation_metrics": true,
    "is_select_intensity_metrics": true,
    "output_type": "TIFF"
  }
}
```

#### Step 8: Generate Crown Boundaries

```json
{
  "step": 8,
  "description": "Generate crown boundaries",
  "tool": "forestry_airborne-extract_tree_crown_boundaries",
  "input": {
    "input_data": "{{step6.data.output_data.derived_output_data_of_input_data}}",
    "output_data": "/output/crown_contours.shp",
    "method": "Concave",
    "max_edge_length": 1.0
  }
}
```

---

### Workflow 5: Regression Analysis and Model Prediction Workflow

**Applicable Scenario**: Use machine learning to predict forest attributes (e.g., biomass, DBH)

**Flowchart**:
```
Prepare Training Data -> Model Training -> Model Validation -> Model Prediction -> Result Evaluation
```

**Detailed Steps**:

#### Step 1: Prepare Training Data

Assuming an individual tree attribute table with ground truth values is available

```json
{
  "step": 1,
  "description": "Load training data",
  "tool": "platform-load_layer",
  "input": {
    "input_data": ["/data/training_biomass.treedb"],
    "data_type": "Table"
  }
}
```

#### Step 2: Train Random Forest Model

```json
{
  "step": 2,
  "description": "Train random forest regression model",
  "tool": "forestry_airborne-random_forest_regression",
  "input": {
    "dependent_variable": "Biomass",
    "plot_type": 0,
    "radius": 10,
    "x_index": 0,
    "y_index": 1,
    "k_fold": 10,
    "optimize": false,
    "local_error_buffer": 0,
    "save_model": true,
    "save_dataset": false,
    "csv_header_list": ["X", "Y", "TreeHeight", "DBH", "Biomass"],
    "report_name": "Biomass RF Report",
    "dependent_variable_index": 4,
    "rf_tree_num": 100,
    "rf_depth": 10,
    "rf_min_split": 3,
    "rf_min_leaf": 2,
    "input_data": {
      "input_data": "/data/training_biomass.csv",
      "sample_data": "/data/training_biomass.csv"
    },
    "output_data": "/output/rf_biomass"
  }
}
```

#### Step 3: Use Model for Prediction

```json
{
  "step": 3,
  "description": "Use model to predict new data",
  "tool": "forestry_airborne-regression_prediction",
  "input": {
    "plot_type": 0,
    "radius": 10,
    "csv_header_list": ["X", "Y", "TreeHeight", "DBH", "Biomass"],
    "report_name": "Biomass Prediction Report",
    "input_data": {
      "input_data": "/data/new_trees.csv",
      "model_file": "/output/rf_biomass.model"
    },
    "output_data": "/output/predicted_biomass"
  }
}
```

---

### Workflow 6: Multi-Temporal Change Detection Workflow

**Applicable Scenario**: Detect forest changes between two periods (e.g., logging, growth)

**Flowchart**:
```
T1 Period Processing -> T2 Period Processing -> Auto-Registration -> Change Detection -> Result Analysis
```

**Detailed Steps**:

#### Steps 1-7: T1 Period Data Processing (Same as Workflow 1)

```json
{
  "workflow": "Airborne Individual Tree Segmentation Standard Workflow",
  "period": "T1",
  "input": "/data/lidar_2015.lidata",
  "output": "/output/t1_segmented"
}
```

#### Steps 1-7: T2 Period Data Processing (Same as Workflow 1)

```json
{
  "workflow": "Airborne Individual Tree Segmentation Standard Workflow",
  "period": "T2",
  "input": "/data/lidar_2025.lidata",
  "output": "/output/t2_segmented"
}
```

#### Step 11: Forest Point Cloud Auto-Registration

```json
{
  "step": 11,
  "description": "Forest point cloud auto-registration",
  "tool": "forestry_airborne-auto_registration_forest",
  "input": {
    "input_data": {
      "refg_pointcloud_file": "/output/t1_segmented.lidata",
      "align_pointcloud_file": "/output/t2_segmented.lidata"
    },
    "output_data": "/output/t2_registered.lidata",
    "selected_classes": [2],
    "cell_size": 0.3,
    "overlap": 40,
    "icp_optimize": true,
    "iteration": 10,
    "num_samples": 100000,
    "max_search_distance": 1
  }
}
```

#### Step 12: Forest Structure Change Detection

```json
{
  "step": 12,
  "description": "Forest structure change detection",
  "tool": "forestry_airborne-forest_structure_change_detection",
  "input": {
    "input_data": {
      "input_lidata_before_change": "/output/t1_segmented.lidata",
      "input_lidata_after_change": "/output/t2_registered.lidata"
    },
    "output_data": "/output/change_detection.html",
    "x_size": 15.0,
    "y_size": 15.0,
    "height_break": 0.5
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

#### Airborne ALS

| Parameter | Recommended Value | Adjustment Recommendation |
|-----|-------|---------|
| grid_size | 0.5-1.0m | Reduce when point density is high |
| height_above_ground | 2.0m | Lower when stand is short |
| sigma | 0.8-1.2 | Reduce when over-segmentation occurs |
| radius_pix | 3-7 | Must be odd numbers |
| min_tree_height | 0-1m | Based on minimum target tree height |
| **from_class** | **[5] or [0,1,2,3,4,5,23,24]** | **See detailed description below** |

#### from_class Parameter Configuration Guide

**The from_class parameter determines which point cloud classes are used for individual tree segmentation. Based on whether deep learning classification is used, there are two configuration methods:**

| Configuration Scenario | from_class Value | Description | Recommendation Rating |
|---------|------------|------|---------|
| **Using deep learning classification** | `[5]` | Use only high vegetation class (>2m), accurately classified through deep learning | 5 stars |
| **Not using deep learning classification** | `[0, 1, 2, 3, 4, 5, 23, 24]` | Use all non-ground classes, includes noise and low vegetation | 3 stars |

**Configuration Decision Basis**:

1. **Conditions for using from_class: [5] (Recommended)**
   - Step 3 executed: Deep learning classification
   - Vegetation types are complex, crown overlap is severe
   - Point cloud density is high, data quality is good
   - Pursuing high-accuracy segmentation results
   - Want to reduce processing time

2. **Conditions for using from_class: [0, 1, 2, 3, 4, 5, 23, 24]**
   - Step 3 skipped: Deep learning classification
   - Vegetation types are simple, crowns are clearly separated
   - Point cloud density is low, data quality is average
   - Fast processing needs take priority
   - No dependency on deep learning models

**Performance Comparison**:
- **Accuracy**: from_class: [5] > from_class: [0,1,2,3,4,5,23,24] (approximately 15-25% improvement)
- **Speed**: from_class: [5] > from_class: [0,1,2,3,4,5,23,24] (approximately 30-40% faster)
- **Robustness**: from_class: [0,1,2,3,4,5,23,24] > from_class: [5] (stronger adaptability)

### Forest Metrics Calculation Parameters

| Parameter | Recommended Value | Description |
|-----|-------|------|
| extinction_coefficient | 0.5-0.7 | Extinction coefficient, depends on tree species |
| height_break | 1.5-2.0m | Stratification threshold |
| Grid size | 15-30m | Adjust based on research scale |

### Regression Model Selection

| Model | Sample Size | Applicable Scenario | Characteristics |
|-----|-------|---------|------|
| Linear Regression | >30 | Simple linear relationships | Fast, interpretable |
| Random Forest | >50 | Complex non-linear | High accuracy, anti-overfitting |
| SVM Regression | >50 | Medium-sized datasets | Strong generalization ability |
| FANN | >100 | Large datasets | Strong flexibility, requires tuning |

---

## Common Issues and Solutions

### Issue 1: Tree Count After Individual Tree Segmentation is Too Low

**Possible Causes**:
- `grid_size` is too large
- `height_above_ground` is too high
- `sigma` is too large, causing over-smoothing

**Solutions**:
- Reduce `grid_size` to 0.4-0.6m
- Lower `height_above_ground` to 1.5-2.0m
- Reduce `sigma` to 0.8-1.0

---

### Issue 2: Multi-Temporal Data Cannot Be Registered

**Possible Causes**:
- Coordinate systems are inconsistent
- Insufficient overlap
- Large difference in tree counts

**Solutions**:
- Unify the coordinate system for both periods of data
- Ensure overlap is at least 50%
- Increase overlap area or adjust thresholds

---

### Issue 3: CHM Segmentation Boundaries Are Inaccurate

**Possible Causes**:
- CHM resolution is too low
- Pits are not filled
- sigma value is too large

**Solutions**:
- Improve CHM resolution (<1m)
- Perform CHM pit filling first
- Adjust sigma to 0.8-1.0

---

### Issue 4: from_class Parameter Configuration Confusion

**Possible Causes**:
- Uncertain whether deep learning classification should be used
- Unclear which classes from_class should be set to
- Concerned that incorrect configuration will affect segmentation results

**Solutions**:
- **Refer to the configuration decision flowchart**: Choose whether to execute deep learning classification based on vegetation complexity and data quality
- **from_class configuration rules**:
  - Deep learning classification executed -> `from_class: [5]` (use only high vegetation)
  - Deep learning classification skipped -> `from_class: [0, 1, 2, 3, 4, 5, 23, 24]` (use all classes)
- **Effect comparison**: Using `from_class: [5]` typically improves accuracy by 15-25% and speed by 30-40%
- **Testing recommendation**: First test both configurations with small-area data, and choose the best solution

---

## Related Documentation

- Tool registry: `references/forestry_airborne/tools.md`
- Pre-flight checks: `references/forestry_airborne/preflight_checks.md`
- Typical examples: `references/forestry_airborne/examples.md`
- Terrestrial forestry workflows: `references/forestry_terrestrial/workflows.md`
- Airborne + terrestrial fusion: `references/forestry_terrestrial/workflows.md` (Fusion workflow)
