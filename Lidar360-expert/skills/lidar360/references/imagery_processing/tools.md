# Imagery Processing Tools Registration
---

## Image Alignment and Registration
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| new_image_project | Import images to create new image project (.liaep) | images | - |
| image_alignment | Run the camera alignment(image alignment) to get the camera's parameters and restore image positions.The output file is same as the input file.Align results are written back into the input image project | LIAEP | - |
| align_to_point_cloud | Align to point cloud.Match image project to pointcloud | Input data | - |
| update_alignment | Update alignment.Update camera alignment result based on pos or ground control points.Directly update the input image project | LIAEP | - |

---

## Image Processing
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| image_defogging | Run defogging to enhance images | select the folder corresponding to the image sequence to be processed | block, radius |
| image_project_generate_dsm | Generate a DSM from image projects when the point cloud required for DSM generation is missing | Input data | - |
| orthomosaic | Orthophoto,Image mosac,Generate DOM. Mosaic images using camera alignment result and dem/dsm | Input data | - |
| semantic_feature_extraction | Extract semantic features such as roads, buildings, water, vegetation and bare land from images using SAM prompts | TIF/TIFF/IMG | - |

---

## Image Group Management
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| image_divide_group | Divide image project into several projects | LIAEP | - |
| image_merge_group | Merge several image projects into one project | LIAEP | - |

---

## Export and Texture
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| export_image_project | Export image project to exchange format | LIAEP | - |
| export_quality_report | Export Quality Report after alignment and mosaic | LIAEP | - |
| texture_mapping_for_3d_mesh | Texture Mapping for 3D Mesh.Use the image project to perform texture mapping on the model file, and save the texture into the input model file. | Input data | precision |

---

## Common Parameter Explanation

### Alignment Methods
| Method | Description | Accuracy |
|---|------|---------|
| Feature_Based | Feature point matching | High |
| Area_Based | Area correlation | Medium |
| Rigid | Rigid transformation | Medium |
| Similarity | Similarity transformation | Medium |

### Image Quality Metrics
| Metric | Description | Good Range |
|---|------|---------|
| Resolution | Ground sample distance | <10 cm |
| Overlap | Image overlap percentage | 60-80% |
| GSD | Ground sampling distance | Consistent |
| RMS | Root mean square error | <1 pixel |

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "imagery_processing-toolID"
