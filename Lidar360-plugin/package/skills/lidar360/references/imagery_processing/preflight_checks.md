# Preflight Check Flow

## Mandatory Checks

The following checks apply to all imagery processing tools and must be completed before any operation:

1. Confirm imagery project is loaded or input imagery files exist -> `get_data_information`, `code == 0` -> PASS
2. Check imagery overlap (recommended >60%) -> `get_data_information` x N, compare `bounds` to calculate intersection area / union area > 60% -> PASS
3. Check whether POS/GCP data is available -> manual confirmation (no tool directly returns POS/GCP status)
4. Execute the tool
5. Check whether the output file path exists; if so, call get_data_information to obtain file information and verify that data type, spatial extent, band count, or vector feature count meets expectations

---

## Tool Execution

### Image Matching / Aerotriangulation

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `align_to_point_cloud` | Imagery project + point cloud exists | "Please load the imagery project first" / "Please load the point cloud first" |
| `image_alignment` | Imagery project + image count >=2 | "Please load the imagery project first" / "Insufficient image count" |
| `update_alignment` | Imagery project + alignment has been performed | "Please perform image alignment first" |

### Orthomosaic

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `orthomosaic` | Imagery project + aligned + DEM/DSM exists | "Images are not aligned" / "Missing DEM or DSM" |

### Image Enhancement

| Tool | Check Item | Verification Method | Failure Message |
|-----|--------|---------|---------|
| `image_defogging` | Imagery file is valid | `get_data_information` check `code == 0` and `band_count >= 1` | "Imagery file is invalid" |
| `semantic_feature_extraction` | Input imagery exists and format is tif/tiff/img + output vector path is gpkg/shp + confidence_threshold in [0,1] range + image_block_size/inference_scale are schema enum values + **SAM3 model exists** | `get_data_information` check imagery + `lidar360_software_information` check SAM3 model in `runtime_resources` | "Imagery file is invalid" / "Output format not supported" / "Invalid confidence threshold" / "Invalid block or scale parameters" / "SAM3 model missing" |

### Image Management

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `image_divide_group` | Imagery project + image count >=2 | "Insufficient image count" |
| `image_merge_group` | >=2 imagery projects | "Insufficient imagery project count" |

### Texture Mapping

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `texture_mapping_for_3d_mesh` | Imagery project + aligned + 3D model | "Images are not aligned" / "Missing 3D model" |

### Quality Assessment

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `export_quality_report` | Imagery project + alignment or mosaicing has been performed | "Please perform alignment or mosaicing first" |

### Data Export

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `export_image_project` | Imagery project is valid | "Imagery project is invalid" |

---

## Other

### SAM3 Model Check (semantic_feature_extraction Specific)

`semantic_feature_extraction` depends on the SAM3 model file. Before calling, confirm the model exists; if missing, download it first.

#### Check Flow

```
1. Call platform-lidar360_software_information to get the runtime_resources list
2. Search the list for resource items where name contains "sam3"
3. Check whether the corresponding model file exists under the download_dist_dir directory
4. If the model does not exist:
   a. Download the model file from download_url
   b. Save to the directory specified by download_dist_dir
   c. If unzip_it=true, unzip the downloaded file
5. After confirming the model file exists, call semantic_feature_extraction
```

#### runtime_resources Field Description

| Field | Description |
|------|------|
| `name` | Resource file name |
| `description` | Resource file details |
| `download_url` | Download link |
| `download_dist_dir` | Download file save location |
| `unzip_it` | Whether to unzip after download |

### Key Dependencies

| Tool | Depends On |
|-----|---------| 
| orthomosaic | image_alignment + DEM generation |
| texture_mapping_for_3d_mesh | image_alignment + model generation |
| export_quality_report | image_alignment or orthomosaic |
| semantic_feature_extraction | platform-lidar360_software_information (to get SAM3 model download info) |
