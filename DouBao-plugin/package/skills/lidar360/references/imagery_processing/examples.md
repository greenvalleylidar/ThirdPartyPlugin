# Typical Workflow Examples

## Example 1: Standard Orthophoto Production Workflow

```
Step 1: Create image project -> Import images
Step 2: Image alignment -> imagery_processing-image_alignment
Step 3: Accuracy check -> imagery_processing-export_quality_report
Step 4: Generate DEM -> terrain_analysis-generate_general_dem_from_pointcloud (requires point cloud)
Step 5: Orthomosaic -> imagery_processing-orthomosaic
Step 6: Image defogging (optional) -> imagery_processing-image_defogging
```

**Prerequisite**: Image overlap >60%
**Output**: Orthophoto DOM

---

## Example 2: Image and Point Cloud Fusion Workflow

```
Step 1: Load point cloud -> platform-load_layer
Step 2: Load image project -> platform-load_layer
Step 3: Align images to point cloud -> imagery_processing-align_to_point_cloud
Step 4: Orthomosaic -> imagery_processing-orthomosaic
Step 5: Extract color for point cloud -> pointcloud_processing related tools
```

**Prerequisite**: Point cloud + image project
**Output**: Colored point cloud

---

## Example 3: 3D Model Texture Mapping Workflow

```
Step 1: Generate 3D model -> building_modeling related tools
Step 2: Image alignment -> imagery_processing-image_alignment
Step 3: Texture mapping -> imagery_processing-texture_mapping_for_3d_mesh
```

**Prerequisite**: 3D model + aligned image project
**Output**: Textured 3D model

---

## Example 4: Large Area Image Block Processing Workflow

```
Step 1: Create image project -> Import images
Step 2: Divide image groups -> imagery_processing-image_divide_group
Step 3: Group alignment -> imagery_processing-image_alignment (each group)
Step 4: Group orthomosaic -> imagery_processing-orthomosaic (each group)
Step 5: Merge images -> imagery_processing-image_merge_group
Step 6: Quality report -> imagery_processing-export_quality_report
```

**Prerequisite**: Large volume of image data
**Output**: Merged orthophoto

---

## Example 5: Image Semantic Feature Extraction Workflow

```json
{
  "tool": "imagery_processing-semantic_feature_extraction",
  "input": {
    "input_data": "/data/orthomosaic.tif",
    "output_data": "/output/semantic_features.gpkg",
    "input_prompts": "road,building,water",
    "confidence_threshold": 0.3,
    "image_block_size": 512,
    "inference_scale": 1,
    "regularize_enabled": false,
    "simplify_enabled": false,
    "smooth_enabled": false
  }
}
```

**Prerequisite**: Input image exists in tif/tiff/jpg/png format, output path is gpkg or shp; **SAM3 model must be available** (if missing, call `platform-lidar360_software_information` first to get the download link and download it)
**Output verification**: Check if the output vector file exists; if it does, call `get_data_information` to retrieve file information and verify the number of vector features and spatial extent

---

## Recommended Parameter Quick Reference

| Scenario | max_feature | max_tie_points | Image Overlap Requirement |
|-----|------------|----------------|-------------|
| UAV aerial photography | 8192 | 1024 | >60% |
| Aerial imagery | 12000 | 2048 | >60% |
| Close-range photogrammetry | 16000 | 4096 | >70% |
