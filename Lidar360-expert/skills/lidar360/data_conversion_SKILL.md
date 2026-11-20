---
name: lidar360-data-conversion
description: LiDAR360 data conversion module, updated from references/data_conversion/tools.md, covering Point Cloud Format Conversion, Raster Format Conversion, Vector Format Conversion, Model Format Conversion, Other Tools.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

# Data Conversion Module (data_conversion)

> This skill index is synchronized from the Markdown documents under `references/data_conversion/`; the tool list follows `tools.md`.

---

## Detailed Documentation Index

| Document | Content | View |
|---------|---------|------|
| **Tool Registry** | Tool groups, functions, input formats, and key parameters | `read_file('references/data_conversion/tools.md')` |
| **Detailed Workflows** | External point cloud ingestion, multi-format point cloud delivery, point cloud rasterization, raster standardization, model publishing, and textured terrain model publishing workflows | `read_file('references/data_conversion/workflows.md')` |

---

## Tool Group Quick Reference

### Point Cloud Format Conversion
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `convert_las_to_lidata` | LAS to LiData | LAS | - |
| `convert_point_cloud_to_ascii` | Point cloud to ASCII | LiData | ascii_type, parse |
| `convert_point_cloud_to_e57` | Point cloud to E57 | LiData | from_class, parse |
| `convert_point_cloud_to_las` | Point cloud to LAS | LiData | - |
| `convert_point_cloud_to_ply` | Point cloud to PLY | LiData | - |
| `convert_point_cloud_to_dxf` | Point cloud to DXF | LiData | - |
| `convert_point_cloud_to_shape` | Point cloud to Shapefile | LiData | - |
| `convert_point_cloud_to_tif` | Point cloud to TIF | LiData | x_size, y_size |
| `convert_point_cloud_to_landxml` | Point cloud to LandXML | LiData | - |
| `convert_point_cloud_to_3dtiles` | Point cloud to 3DTiles | LiData | - |

### Raster Format Conversion
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `convert_tif_to_ascii` | TIF to ASCII | TIF | - |
| `convert_asc_to_tif` | ASC to TIF | ASC | - |
| `convert_tif_to_img` | TIF to IMG | TIF | - |
| `convert_img_to_tif` | IMG to TIF | IMG | - |
| `convert_tif_to_lidata` | TIF to LiData | TIF | - |
| `convert_tif_to_limodel` | TIF to LiModel | TIF | - |
| `convert_tif_to_usgs_dem` | TIF to USGS DEM | TIF | - |
| `convert_usgs_dem_to_tif` | USGS DEM to TIF | DEM | - |

### Vector Format Conversion
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `convert_shape_to_kml` | Shapefile to KML | Shapefile | - |
| `convert_kml_to_shape` | KML to Shapefile | KML | - |
| `convert_vector_to_ascii` | Vector to ASCII | GPKG/DXF/SHP | - |
| `convert_vector_to_landxml` | Vector to LandXML | GPKG/SHP/DXF/KML | input_data, output_data |
| `convert_ascii_to_vector` | ASCII to vector | TXT/CSV/TreeDB | - |
| `vector_format_conversion` | Vector format conversion | GPKG/DXF/SHP/KML/XML | export_format, merge |

### Model Format Conversion
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `convert_limodel_to_3dtiles` | LiModel to 3DTiles | LiModel | - |
| `convert_limodel_to_obj` | LiModel to OBJ | LiModel | - |
| `convert_limodel_to_osgb` | LiModel to OSGB | LiModel | - |
| `convert_limodel_to_s3m` | LiModel to S3M | LiModel | - |
| `convert_limodel_to_tif` | LiModel to TIF | LiModel | - |
| `convert_to_texture_limodel` | Convert to texture LiModel | LiModel | - |
| `convert_litin_to_3dtiles` | LiTin to 3DTiles | LiTin | - |
| `convert_litin_to_obj` | LiTin to OBJ | LiTin | - |
| `convert_litin_to_osgb` | LiTin to OSGB | LiTin | - |
| `convert_litin_to_fbx` | LiTin to FBX | LiTin | - |
| `convert_litin_to_dxf` | LiTin to DXF | LiTin | - |
| `convert_litin_to_lidata` | LiTin to LiData | LiTin | - |
| `convert_litin_to_landxml` | LiTin to LandXML | LiTin | - |
| `convert_litree_to_3dtiles` | LiTree to 3DTiles | LiTree | - |
| `convert_litree_to_obj` | LiTree to OBJ | LiTree | - |
| `convert_litree_to_osgb` | LiTree to OSGB | LiTree | - |
| `convert_litree_to_cityjson` | LiTree to CityJSON | LiTree | - |
| `convert_libim_to_3dtiles` | LiBIM to 3DTiles | LiBIM | - |
| `convert_libim_to_obj` | LiBIM to OBJ | LiBIM | - |
| `convert_libim_to_osgb` | LiBIM to OSGB | LiBIM | - |
| `convert_libim_to_fbx` | LiBIM to FBX | LiBIM | - |
| `convert_libim_to_cityjson` | LiBIM to CityJSON | LiBIM | - |
| `convert_libim_to_citygml` | LiBIM to CityGML | LiBIM | export_content, export_attributes |
| `convert_libim_to_collada` | LiBIM to Collada | LiBIM | - |
| `convert_3dtiles_to_obj` | 3DTiles to OBJ | 3DTiles | - |
| `convert_3dtiles_to_osgb` | 3DTiles to OSGB | 3DTiles | - |
| `convert_3dtiles_to_s3m` | 3DTiles to S3M | 3DTiles | - |
| `convert_obj_to_3dtiles` | OBJ to 3DTiles | OBJ | - |
| `convert_lidata_version` | LiData version conversion | LiData | - |

### Other Tools
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `unit_conversion` | Unit conversion | Various formats | - |
| `attribute_table_data_exporter` | Export rows from attribute table to data file | gpkg/dxf/shp/kml/csv/treedb/libim | output_format, row_selection_mode, input_data, output_data |

---

## Workflow Index

- Workflow 1: External point cloud ingestion and web publishing
- Workflow 2: Multi-format point cloud delivery
- Workflow 3: Point cloud rasterization and raster delivery
- Workflow 4: External raster standardization and ingestion
- Workflow 5: Model web publishing and multi-format delivery
- Workflow 6: DOM textured terrain model generation and publishing

---

## Common Parameters Index

| Configuration File | Content | View |
|-------------------|---------|------|
| **File Formats** | Point cloud, raster, vector, model format references | `read_file('references/profiles/file_formats.md')` |
| **Point Cloud Class Codes** | ASPRS/LiDAR360 common class codes | `read_file('references/profiles/class_codes.md')` |
| **Interpolation Methods** | Common interpolation methods for DEM/DSM/raster generation | `read_file('references/profiles/interpolation.md')` |
| **Scale** | Terrain, contour, and mapping scale references | `read_file('references/profiles/scale.md')` |

---

## Invocation Convention

- Quick invocation: `data_conversion-toolID`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "data_conversion-toolID"`
- For multi-step tasks, refer to `workflows.md` first.
