# Imagery Processing Workflows

> Complete multi-tool collaboration workflows for image data processing.

---

## Workflow Overview

| Scenario | Recommended Workflow | Key Tools | Difficulty |
|-----|---------|---------|------|
| DOM generation (point cloud DSM) | Workflow 1 | image_alignment -> generate_dsm_from_pointcloud -> orthomosaic | Medium |
| Image and point cloud alignment | Image project to point cloud alignment workflow | image_alignment -> align_to_point_cloud | Medium |
| Spectral classification | Spectral angle mapper classification workflow | classify_by_Spectral_Angle_Mapper | Advanced |
| Point cloud spectral mapping | Mask classification workflow | classify_by_mask | Medium |
| 3D texture | Texture mapping workflow | texture_mapping_for_3d_mesh | Advanced |
| Point cloud registration | Image alignment to point cloud | align_to_point_cloud | Medium |
| DOM generation (image project DSM) | Workflow 6 | image_alignment -> image_project_generate_dsm -> orthomosaic | Medium |

---

## Imagery Processing Workflows

### Workflow 1: Standard DOM Generation Workflow

**Applicable scenario**: Generate orthophoto (DOM) from raw images

**Workflow diagram**:
```
Load image project -> Image alignment -> [Optional] Denoise -> [Optional] Align to point cloud -> Generate DSM -> Generate DOM
```

**Detailed steps**:

#### Step 1: Image Alignment

```json
{
  "step": 1,
  "description": "Image aerial triangulation (matching, camera parameter calibration)",
  "tool": "imagery_processing-image_alignment",
  "input": {
    "input_data": "/data/image_project.liaep"
  },
  "notes": "All parameters are recommended to use default values; results are written directly into the input image project file"
}
```

#### Step 2: Denoising (Optional)

**Applicable scenario**: When aerial noise points are present

```json
{
  "step": 2,
  "description": "Point cloud denoising (optional)",
  "tool": "pointcloud_processing-pointcloud_outlier_removal",
  "input": {
    "input_data": ["/data/raw_pointcloud.lidata"],
    "neighbor_points": 10,
    "multiples_of_std_deviation": 5,
    "output_data": "/output/denoised_pointcloud.lidata"
  },
  "notes": "Mainly used to address aerial noise point issues"
}
```

#### Step 3: Align to Point Cloud (Optional)

**Applicable scenario**: When the point cloud used for DSM/DEM generation has a large positional deviation from the image project

```json
{
  "step": 3,
  "description": "Image alignment to point cloud (optional)",
  "tool": "imagery_processing-align_to_point_cloud",
  "input": {
    "input_data": {
      "image_project": "/data/image_project.liaep",
      "point_cloud_list": ["{{step2.data.output_data}}"]
    },
    "output_data": "/output/aligned_image_project.prj"
  },
  "notes": "Align the image project and point cloud to improve subsequent processing accuracy"
}
```

#### Step 4: Generate DSM from Point Cloud

```json
{
  "step": 4,
  "description": "Generate DSM from point cloud",
  "tool": "terrain_analysis-generate_general_dsm_from_pointcloud",
  "input": {
    "input_data": ["{{step2.data.output_data}}"],
    "output_data": "/output/dsm.tif",
    "from_class": null,
    "return_number": null,
    "interpolator": 1,
    "x_size": 0.2,
    "y_size": 0.2
  },
  "notes": "DSM is used for geometric correction of orthophoto"
}
```

#### Step 5: Generate Orthophoto

```json
{
  "step": 5,
  "description": "Generate orthophoto (DOM)",
  "tool": "imagery_processing-orthomosaic",
  "input": {
    "input_data": {
      "input_data": "/data/image_project.liaep",
      "raster_file": "/output/dsm.tif"
    },
    "output_data": "/output/dom.tif"
  },
  "notes": "Input image project (result from Step 1; if optional Step 3 was executed, use the aligned image project from Step 3) and DSM file"
}
```

---

### Workflow 2: Spectral Angle Mapper Classification Workflow

**Applicable scenario**: Classify ground features using spectral images

**Workflow diagram**:
```
Load spectral image -> Select mode (spectral library/ROI) -> Spectral angle classification -> Export results
```

**Detailed steps**:

#### Step 1: Load Spectral Image

```json
{
  "step": 1,
  "description": "Load multi-band spectral image",
  "tool": "platform-load_layer",
  "input": {
    "input_data": ["/data/spectral_image.tif"],
    "data_type": "Image"
  }
}
```

#### Step 2A: Spectral Library Mode

**Applicable scenario**: Using txt format spectral library files

```json
{
  "step": "2A",
  "description": "Spectral angle classification (spectral library mode)",
  "tool": "spectral_analysis-classify_by_spectral_angle_mapper",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "select_bands": [1, 2, 3],
    "maximum_angle": 0.1,
    "output_data": "/output/spectral_classification.tif"
  },
  "notes": "Allows selection of image bands for classification"
}
```

#### Step 2B: ROI Mode

**Applicable scenario**: Using ROI files for training

```json
{
  "step": "2B",
  "description": "Spectral angle classification (ROI mode)",
  "tool": "spectral_analysis-classify_by_spectral_angle_mapper",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "select_bands": [1, 2, 3],
    "maximum_angle": 0.1,
    "output_data": "/output/spectral_classification.tif"
  },
  "notes": "Supports gpkg or ENVI exported xml format ROI files"
}
```

---

### Workflow 3: Spectral Classification Mapping to Point Cloud Workflow

**Applicable scenario**: Map spectral classification results to point cloud

**Workflow diagram**:
```
Point cloud loading -> Spectral classification -> Classify by mask -> Point cloud classification result
```

**Detailed steps**:

#### Step 1: Load Point Cloud

```json
{
  "step": 1,
  "description": "Load point cloud",
  "tool": "platform-load_layer",
  "input": {
    "input_data": ["/data/pointcloud.lidata"],
    "data_type": "PointCloud"
  }
}
```

#### Step 2: Spectral Angle Classification

```json
{
  "step": 2,
  "description": "Spectral angle classification (same as Workflow 2)",
  "tool": "spectral_analysis-classify_by_spectral_angle_mapper",
  "input": {
    "input_data": "/data/spectral_image.tif",
    "select_bands": [1, 2, 3],
    "maximum_angle": 0.1,
    "output_data": "/output/spectral_classification.tif"
  }
}
```

#### Step 3: Classify by Mask

```json
{
  "step": 3,
  "description": "Classify by mask (map to point cloud)",
  "tool": "pointcloud_classification-classify_by_mask",
  "input": {
    "input_data": {
      "pointcloud_files": ["/data/pointcloud.lidata"],
      "mask_file": "{{step2.data.output_data}}"
    },
    "mask_class": [1, 2, 3],
    "target_class": [2, 5, 6]
  },
  "notes": "The mask file must be a classification mask generated by LiDAR360"
}
```

---

### Workflow 4: 3D Model Texture Mapping Workflow

**Applicable scenario**: Add textures to 3D models

**Workflow diagram**:
```
3D model + image project -> Texture mapping -> Textured 3D model
```

**Detailed steps**:

#### Step 1: Load 3D Model

```json
{
  "step": 1,
  "description": "Load 3D model",
  "tool": "platform-load_layer",
  "input": {
    "input_data": ["/data/3d_model.obj"],
    "data_type": "Model"
  }
}
```

#### Step 2: Image Alignment (if not yet completed)

```json
{
  "step": 2,
  "description": "Image aerial triangulation",
  "tool": "imagery_processing-image_alignment",
  "input": {
    "input_data": "/data/image_project.liaep"
  }
}
```

#### Step 3: Texture Mapping

```json
{
  "step": 3,
  "description": "Texture mapping to 3D model",
  "tool": "imagery_processing-texture_mapping_for_3d_mesh",
  "input": {
    "input_data": {
      "input_model": "/data/3d_model.obj",
      "input_liaep": "/data/image_project.liaep"
    },
    "precision": 1
  },
  "notes": "Requires the image project to be aligned"
}
```

---

### Workflow 5: Image Project and Point Cloud Alignment Workflow

**Applicable scenario**: Spatially align the image project with the point cloud so that both share consistent coordinates

**Workflow diagram**:
```
Image alignment -> Align to point cloud
```

**Detailed steps**:

#### Step 1: Image Alignment

```json
{
  "step": 1,
  "description": "Image aerial triangulation (matching, camera parameter calibration)",
  "tool": "imagery_processing-image_alignment",
  "input": {
    "input_data": "/data/image_project.liaep"
  },
  "notes": "All parameters are recommended to use default values; results are written directly into the input image project file"
}
```

#### Step 2: Align to Point Cloud

```json
{
  "step": 2,
  "description": "Align image project to point cloud",
  "tool": "imagery_processing-align_to_point_cloud",
  "input": {
    "input_data": {
      "image_project": "/data/image_project.liaep",
      "point_cloud_list": ["/data/pointcloud.lidata"]
    },
    "output_data": "/output/aligned_image_project.prj"
  },
  "notes": "Input is the aligned image project from Step 1 and the point cloud file; output is the aligned image project file. This function can be used to align the image project and point cloud"
}
```

---

### Workflow 6: Image Project DOM Generation Workflow (Image Project Generates DSM)

**Applicable scenario**: Generate DSM directly from the image project and produce orthophoto (DOM) without relying on external point cloud for DSM generation

**Difference from Workflow 1**: Workflow 1 uses `terrain_analysis-generate_general_dsm_from_pointcloud` to generate DSM from point cloud; this workflow uses `imagery_processing-image_project_generate_dsm` to generate DSM directly from the image project

**Workflow diagram**:
```
Image alignment -> Image project generates DSM -> Generate orthophoto
```

**Detailed steps**:

#### Step 1: Image Alignment

```json
{
  "step": 1,
  "description": "Image aerial triangulation (matching, camera parameter calibration)",
  "tool": "imagery_processing-image_alignment",
  "input": {
    "input_data": "/data/image_project.liaep"
  },
  "notes": "All parameters are recommended to use default values; results are written directly into the input image project file"
}
```

#### Step 2: Image Project Generates DSM

```json
{
  "step": 2,
  "description": "Generate DSM directly from image project",
  "tool": "imagery_processing-image_project_generate_dsm",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "output_data": "/output/dsm_from_image.tif"
  },
  "notes": "Generate DSM directly from the image project without external point cloud. Different from the generate_dsm_from_pointcloud used in Workflow 1"
}
```

#### Step 3: Generate Orthophoto

```json
{
  "step": 3,
  "description": "Generate orthophoto (DOM)",
  "tool": "imagery_processing-orthomosaic",
  "input": {
    "input_data": {
      "input_data": "/data/image_project.liaep",
      "raster_file": "/output/dsm_from_image.tif"
    },
    "output_data": "/output/dom.tif"
  },
  "notes": "Input is the image project from Step 1 and the DSM file from Step 2; parameters can use default values"
}
```

**Parameter configuration**:

| Step | Tool | Parameter | Recommended Value | Description |
|------|------|------|--------|------|
| 1 | `image_alignment` | Default parameters | - | All use default values |
| 2 | `align_to_point_cloud` | Default parameters | - | Align image project and point cloud |

---

## Parameter Configuration Quick Reference

### DOM Generation Parameter Recommendations

| Tool | Parameter | Recommended Value | Description |
|------|------|--------|------|
| image_alignment | Default parameters | - | All recommended to use default values |
| pointcloud_outlier_removal | neighbor_points | 10 | Number of neighbor points |
| | multiples_of_std_deviation | 5 | Standard deviation multiplier |
| align_to_point_cloud | - | - | Adjust based on deviation |
| generate_dsm_from_pointcloud | interpolator | 1 (Kriging) | Interpolation method |
| | resolution | 0.2 | DSM resolution (meters) |
| orthomosaic | Default parameters | - | All recommended to use default values |

### Spectral Angle Mapper Classification Parameter Recommendations

| Parameter | Recommended Value | Description |
|------|--------|------|
| maximum_angle | 0.1 | Maximum spectral angle threshold |
| select_bands | Based on data | Select bands for classification |

### Point Cloud Mask Classification Mapping

| Mask Value | Point Cloud Class | Class Name |
|--------|----------|---------|
| 1 | 2 | Ground |
| 2 | 5 | Vegetation |
| 3 | 6 | Building |
| 4 | 9 | Water |

---

## Common Issues and Solutions

### Issue 1: Image Alignment Failure

**Possible causes**:
- Insufficient image overlap (<60%)
- Poor image quality
- Insufficient feature points

**Solutions**:
- Ensure image overlap >60%
- Check image quality and remove blurry images
- Increase number of images or adjust flight altitude

---

### Issue 2: DOM Geometric Distortion

**Possible causes**:
- DSM resolution too low
- Images and point cloud not aligned
- Insufficient DEM accuracy

**Solutions**:
- Improve DSM resolution (<0.5m)
- Execute align_to_point_cloud to align images and point cloud
- Use high-precision DEM

---

### Issue 3: Low Spectral Angle Classification Accuracy

**Possible causes**:
- Spectral angle threshold set too high
- Insufficient representativeness of spectral library/ROI
- Poor band selection for spectral image

**Solutions**:
- Reduce maximum_angle to 0.05-0.1
- Increase training sample quantity and representativeness
- Select band combinations with high discriminability

---

### Issue 4: Poor Mask Mapping Results

**Possible causes**:
- Mask file and point cloud coordinates are inconsistent
- Incorrect mask class mapping configuration
- Inaccurate mask classification results

**Solutions**:
- Ensure mask file and point cloud share the same coordinate system
- Check mask_class_mapping configuration
- Improve spectral angle classification parameters

---

### Issue 5: Missing Texture Mapping

**Possible causes**:
- Image project not aligned
- Large positional deviation between images and model
- Incomplete image coverage

**Solutions**:
- Complete image aerial triangulation first
- Use align_to_point_cloud for alignment
- Ensure images cover the model area

---

## Workflow Selection Recommendations

| Requirement | Recommended Workflow | Required Steps |
|------|---------|---------|
| Generate standard DOM (with high-quality point cloud) | Workflow 1 | 1->4->5 |
| Precise DOM (large point cloud deviation) | Workflow 1 | 1->2->3->4->5 |
| Feature classification | Workflow 2 | 1->2A/2B |
| Spectral classification to point cloud | Workflow 3 | 1->2->3 |
| 3D model beautification | Workflow 4 | 1->2->3 |
| Image and point cloud alignment | Workflow 5 | 1->2 |
| Generate standard DOM (no point cloud or poor quality) | Workflow 6 | 1->4->5 |
---

## Related Documentation

- Tool registry: `references/imagery_processing/tools.md`
- Preflight checks: `references/imagery_processing/preflight_checks.md`
- Typical examples: `references/imagery_processing/examples.md`
- Spectral analysis: `references/spectral_analysis/`
