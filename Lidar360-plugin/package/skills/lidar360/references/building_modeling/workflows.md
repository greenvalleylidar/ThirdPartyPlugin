# Building Modeling Workflows

> Based on LiDAR360 Model Builder `Point Cloud & Imagery - Automatic Building Creation Workflow.LiModelBuilder`. This workflow runs the point cloud classification pipeline and the imagery footprint extraction pipeline in parallel, then merges both results into automatic LOD2 building model creation.

---

## Process Overview

| Scenario | Recommended Process | Key Tools | Difficulty |
|-----|---------|---------|------|
| Automatic building creation from point cloud and imagery | Point cloud denoising -> Resampling -> Ground point classification -> Building classification; Imagery building footprint extraction; Both results -> Automatic building creation | `auto_create_buildings` | Medium |
| Extract building footprints from imagery only | DOM/color imagery -> Building footprint extraction -> Manual inspection/cleanup | `extract_building_footprint_from_image` | Low |
| Create LiBIM from existing point cloud classification and footprints | Building/roof points + ground points + footprint -> Automatic building creation | `auto_create_buildings` | Medium |
| Building model post-processing | LiBIM -> Attribute calculation -> Orthophoto or oblique texture mapping | `building_attributes_calculate`, texture mapping tools | Medium |

---

## Model Builder Reference Workflow

```text
Point Cloud File
  -> Point Cloud Denoising
  -> Resampling
  -> Ground Point Classification
  -> Building Classification
  -> Automatic Building Creation

DOM/Three-Channel Color Imagery
  -> Extract Building Footprints from Imagery
  -> Automatic Building Creation
```

**Output**: `.LiBIM` building model.

**Key Connections**:

| Upstream | Downstream | Description |
|-----|------|------|
| `pointcloud_outlier_removal.output_data` | `pointcloud_subsampling.input_data` | Denoised point cloud feeds into resampling |
| `pointcloud_subsampling.output_data` | `classify_ground_by_progressive_tin_densification.input_data` | Resampled result is used for ground point classification |
| `classify_ground_by_progressive_tin_densification.input_data` | `classify_buildings.input_data` | Ground class is identified before building detection |
| `classify_buildings.input_data` | `auto_create_buildings.input_data` | Building classification result is used for modeling |
| `extract_building_footprint_from_image.output_data.output_vector_files` | `auto_create_buildings.input_data.footprint` | Imagery-extracted footprints serve as modeling outline constraints |

---

## Workflow 1: Automatic Building Creation from Point Cloud & Imagery

**Applicable Scenario**: Both point cloud and DOM/three-channel color imagery are available; batch creation of LOD2 building models is needed.

**Flowchart**:

```text
Point Cloud -> Denoising -> Resampling -> Ground Point Classification -> Building Classification ----\
                                                                                                     -> Automatic Building Creation -> LiBIM
Imagery/DOM -> Building Footprint Extraction ------------------------------------------------------/
```

### Step 1: Point Cloud Denoising

This step serves as the entry point of the point cloud pipeline in Model Builder, used to remove outliers and obvious noise.

```json
{
  "step": 1,
  "description": "Point cloud denoising",
  "tool": "pointcloud_processing-pointcloud_outlier_removal",
  "input": {
    "input_data": ["/data/raw.lidata"],
    "neighbor_points": 10,
    "multiples_of_std_deviation": 5,
    "output_data": "/output/denoised.lidata"
  }
}
```

### Step 2: Resampling

```json
{
  "step": 2,
  "description": "Point cloud resampling",
  "tool": "pointcloud_processing-pointcloud_subsampling",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "output_data": "/output/subsampled",
    "sampling_type": 1,
    "from_class": [0, 1, 2, 3, 4, 5, 6],
    "sampling_rate": 50,
    "minimum_points_spacing": 0,
    "octree": 21
  }
}
```

### Step 3: Ground Point Classification

Ground points are identified before building modeling to facilitate subsequent calculation of building base elevation, relative roof height, and non-ground point filtering.

```json
{
  "step": 3,
  "description": "Ground point classification (Progressive TIN Densification)",
  "tool": "pointcloud_classification-classify_ground_by_progressive_tin_densification",
  "input": {
    "input_data": ["{{step2.data.output_data}}"],
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

### Step 4: Building Classification

```json
{
  "step": 4,
  "description": "Building classification",
  "tool": "pointcloud_classification-classify_buildings",
  "input": {
    "input_data": ["{{step3.data.output_data}}"],
    "from_class": null,
    "building_class": 6,
    "wall_class": 14,
    "height_above_ground": 2,
    "minimum_building_area": 20,
    "minimum_points_number": 100,
    "search_radius": 1,
    "angle_threshold": 10,
    "distance_tolerance": 0.2,
    "buffer_size": 10,
    "max_slope": 60
  }
}
```

**Parameter Recommendations**:

| Parameter | Model Builder Default | Description |
|-----|----------------------|------|
| `building_class` | 6 | Building roof/main body point class |
| `wall_class` | 14 | Wall point class; can serve as a supplementary roof class in subsequent modeling |
| `height_above_ground` | 2 | Minimum height above ground (m) for points to participate in building detection |
| `minimum_building_area` | 20 | Candidate buildings smaller than this area are filtered out |
| `minimum_points_number` | 100 | Minimum number of points for a candidate building |
| `search_radius` | 1 | Neighborhood search radius |
| `angle_threshold` | 10 | Plane/boundary angle threshold |
| `distance_tolerance` | 0.2 | Distance tolerance |
| `max_slope` | 60 | Maximum slope threshold |

### Step 5: Extract Building Footprints from Imagery

This step runs in parallel with the point cloud pipeline. Input must be DOM or three-channel color imagery; single-channel rasters such as DEM/DSM cannot be used.

```json
{
  "step": 5,
  "description": "Extract building footprints from imagery",
  "tool": "building_modeling-extract_building_footprint_from_image",
  "input": {
    "input_data": ["/data/dom.tif"],
    "output_data": "/output/building_footprint.shp",
    "area": 10,
    "angle_threshold": 10,
    "delete_contours": true,
    "regularization": true,
    "simplify": true
  }
}
```

**Parameter Recommendations**:

| Parameter | Model Builder Default | Description |
|-----|----------------------|------|
| `area` | 10 | Contours smaller than this area can be filtered |
| `angle_threshold` | 10 | Contour regularization angle threshold |
| `delete_contours` | true | Delete invalid/small contours |
| `regularization` | true | Regularize output building contours |
| `simplify` | true | Simplify contour vertices |

### Step 6: Automatic Building Creation

```json
{
  "step": 6,
  "description": "Automatic building creation",
  "tool": "building_modeling-auto_create_buildings",
  "input": {
    "input_data": {
      "input_data": "{{step4.data.output_data}}",
      "footprint": "{{step5.data.output_data.output_vector_files}}"
    },
    "output_data": "/output/buildings.LiBIM",
    "ground_class": [0, 1, 2],
    "roof_class": [6, 13, 14]
  }
}
```

**Configuration Recommendations**:

| Parameter | Model Builder Default | Description |
|-----|----------------------|------|
| `ground_class` | `[0, 1, 2]` | Used for base elevation estimation and ground constraints; standard ground class is 2 |
| `roof_class` | `[6, 13, 14]` | Used for roof modeling; 6 is building class, 13/14 can cover roof or wall supplementary classes |
| `footprint` | `.gpkg/.dxf/.shp` | Building base outline, from imagery extraction or existing vector |
| `output_data` | `.LiBIM` | Output building model |

---

## Workflow 2: Extract Building Footprints from Imagery Only

**Applicable Scenario**: DOM or aerial photography three-channel imagery is available; need to quickly generate building footprints for modeling or manual editing.

```text
DOM/Color Imagery -> extract_building_footprint_from_image -> output_vector_files(SHP) + output_mask_files(TIF)
```

```json
{
  "step": 1,
  "description": "Extract building footprints",
  "tool": "building_modeling-extract_building_footprint_from_image",
  "input": {
    "input_data": ["/data/dom.tif"],
    "output_data": "/output/footprint.shp",
    "area": 10,
    "angle_threshold": 10,
    "delete_contours": true,
    "regularization": true,
    "simplify": true
  }
}
```

> After output, it is recommended to inspect the results in a vector editing environment for missed buildings, false detections, merged buildings, and boundary deviations caused by eave shadows.

---

## Workflow 3: Create LiBIM from Existing Classified Point Cloud and Footprints

**Applicable Scenario**: Ground point and building point classification have already been completed, and building outline vectors are available.

```text
Classified Point Cloud + Footprint -> auto_create_buildings -> LiBIM
```

```json
{
  "step": 1,
  "description": "Automatic building creation",
  "tool": "building_modeling-auto_create_buildings",
  "input": {
    "input_data": {
      "input_data": "/data/classified.lidata",
      "footprint": "/data/footprint.gpkg"
    },
    "output_data": "/output/buildings.LiBIM",
    "ground_class": [2],
    "roof_class": [6, 13, 14]
  }
}
```

---

## Workflow 4: Building Model Post-Processing

**Applicable Scenario**: A `.LiBIM` file already exists; need to calculate attributes or apply textures.

```text
LiBIM -> Attribute Calculation -> Orthophoto Texture Mapping / Oblique Texture Mapping
```

### Attribute Calculation

```json
{
  "step": 1,
  "description": "Building attribute calculation",
  "tool": "building_modeling-building_attributes_calculate",
  "input": {
    "input_data": "/output/buildings.LiBIM"
  }
}
```

> This tool directly modifies the input LiBIM file and writes attributes such as height, eave height, base elevation, roof orientation, and roof shape. It is recommended to keep a backup before execution.

### Orthophoto Texture Mapping

```json
{
  "step": 2,
  "description": "Orthophoto texture mapping",
  "tool": "building_modeling-ortho_texture_mapper_for_libim",
  "input": {
    "input_data": {
      "building_file": "/output/buildings.LiBIM",
      "dom_file": "/data/dom.tif"
    },
    "output_data": "/output/buildings_orthotextured.LiBIM"
  }
}
```

### Oblique Texture Mapping

```json
{
  "step": 2,
  "description": "Oblique imagery texture mapping",
  "tool": "building_modeling-oblique_texture_mapper_for_libim",
  "input": {
    "input_data": {
      "building_file": "/output/buildings.LiBIM",
      "image_project": "/data/oblique_project.liaep",
      "pointcloud": "/data/oblique_project.lidata"
    },
    "output_data": "/output/buildings_oblique_textured.LiBIM",
    "max_oblique_angle": 60
  }
}
```

---

## Parameter Quick Reference

### Class Configuration

| Class | Meaning | Modeling Usage |
|-----|------|---------|
| 0 | Created/Never classified or default inclusion class in the workflow | Included in Model Builder default ground_class |
| 1 | Unclassified points | Can serve as ground candidate or supplementary points; use with caution |
| 2 | Ground points | Base elevation, ground constraints, building height calculation |
| 6 | Building points | Main roof/building body input |
| 13 | Model Builder default roof supplementary class | Included in default `roof_class` |
| 14 | Wall points or building supplementary class | Can be added to `auto_create_buildings.roof_class` as supplementary |

### Common Issues

| Issue | Possible Cause | Recommended Fix |
|-----|---------|---------|
| LiBIM building base elevation is abnormal | Ground point classification is impure; `ground_class` includes non-ground points | Inspect class 2; consider setting `ground_class: [2]` only |
| Buildings are missing | `minimum_building_area` or `minimum_points_number` is too large; imagery footprints have omissions | Lower filter thresholds; inspect footprint vectors |
| Buildings are merged | Footprints are not split; imagery shadows cause contour merging | Manually edit footprints; enable regularization and simplification, then re-inspect |
| Roof shapes are too coarse | Building point density is insufficient or roof/wall classes are incomplete | Check `roof_class`; avoid excessive resampling |
| Texture misalignment | DOM/image project and LiBIM coordinate systems do not match | Unify spatial references; verify image registration accuracy |

---

## Related Documentation

- Tool registry: `references/building_modeling/tools.md`
- Pre-flight checks: `references/building_modeling/preflight_checks.md`
- Typical examples: `references/building_modeling/examples.md`
