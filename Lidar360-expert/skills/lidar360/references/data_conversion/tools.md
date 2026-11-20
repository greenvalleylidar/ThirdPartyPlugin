# Data Conversion Tools Registration
> Grouped by conversion type

---

## Point Cloud Format Conversion
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| convert_las_to_lidata | Converting LAS files to LiData files | LAS/LAZ | - |
| convert_point_cloud_to_ascii | Convert LiData point clouds to ASCII format files | LiData | ascii_type, parse |
| convert_point_cloud_to_e57 | Convert LiData point clouds to E57 format files | LiData | from_class, parse |
| convert_point_cloud_to_las | Convert LiData point clouds to LAS format files | LiData | - |
| convert_point_cloud_to_ply | Convert LiData point clouds to PLY format files | LiData | - |
| convert_point_cloud_to_dxf | Convert LiData point clouds to DXF format files | LiData | - |
| convert_point_cloud_to_shape | Convert LiData point clouds to shape format files | LiData | - |
| convert_point_cloud_to_tif | Convert LiData point clouds to TIF format files | LiData | x_size, y_size, raster_style, cell_value_type, radius |
| convert_point_cloud_to_landxml | Convert LiData Point Clouds to LandXML format files | LiData | - |
| convert_point_cloud_to_3dtiles | Convert LiData Point Clouds to 3DTiles format files | LiData | - |

---

## Raster Format Conversion
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| convert_tif_to_ascii | Convert a raster image in TIF format to ASCII format | TIF/TIFF | - |
| convert_asc_to_tif | Convert ASC files to TIF files | ASC | - |
| convert_tif_to_img | Convert a raster image in TIF format to IMG format | TIF/TIFF | - |
| convert_img_to_tif | Convert a raster image in IMG format to TIF format | IMG | - |
| convert_tif_to_lidata | Convert single-band raster data (DEM, DSM, CHM, etc.) to LiData format | TIF/TIFF | - |
| convert_tif_to_limodel | TIF to LiModel file conversion | TIF/TIFF | - |
| convert_tif_to_usgs_dem | Convert a raster image in TIF format to USGS DEM format | TIF/TIFF | - |
| convert_usgs_dem_to_tif | Convert USGS DEM format files to TIF format files | DEM | - |

---

## Vector Format Conversion
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| convert_shape_to_kml | Convert Shapefile format files to KML format files | SHP | - |
| convert_kml_to_shape | Convert KML format files to shape format files | KML | - |
| convert_vector_to_ascii | Convert vector files to ascii files | GPKG/DXF/SHP | - |
| convert_vector_to_landxml | Convert vector files to LandXML format files | GPKG/SHP/DXF/KML | - |
| convert_ascii_to_vector | Convert ascii files to vector files | TXT/CSV/TreeDB | - |
| vector_format_conversion | Convert vector files to vector files in other format | GPKG/DXF/SHP/KML/XML | - |

---

## LiModel Conversion
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| convert_limodel_to_3dtiles | Convert LiModel format files to 3DTiles format files | LiModel | - |
| convert_limodel_to_obj | Convert LiModel format files to OBJ format files | LiModel | - |
| convert_limodel_to_osgb | Convert LiModel format files to OSGB format files | LiModel | - |
| convert_limodel_to_s3m | Convert LiModel format files to S3M format files | LiModel | - |
| convert_limodel_to_tif | Convert LiModel format files to TIF format raster images | LiModel | - |
| convert_to_texture_limodel | Mapping DOM data color values to the LiModel for display | Input data | - |

---

## LiTin Conversion
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| convert_litin_to_3dtiles | Convert LiTin format files to 3DTiles format files | LiTin | - |
| convert_litin_to_obj | Convert LiTin format files to OBJ format files | LiTin | - |
| convert_litin_to_osgb | Convert LiTin format files to OSGB format files | LiTin | - |
| convert_litin_to_fbx | Convert LiTin format files to FBX format files | LiTin | - |
| convert_litin_to_dxf | Convert LiTin format files to DXF format files | LiTin | - |
| convert_litin_to_lidata | Convert LiTin format files to LiData format files | LiTin | - |
| convert_litin_to_landxml | Convert LiTin Clouds to LandXML format files | LiTin | - |

---

## LiTree Conversion
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| convert_litree_to_3dtiles | Convert LiTree format files to 3DTiles format files | LiTree | - |
| convert_litree_to_obj | Convert LiTree format files to OBJ format files | LiTree | - |
| convert_litree_to_osgb | Convert LiTree format files to OSGB format files | LiTree | - |
| convert_litree_to_cityjson | Convert LiTree format files to CityJson format files | LiTree | - |

---

## LiBIM Conversion
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| convert_libim_to_3dtiles | Convert LiBIM format files to 3DTiles format files | LiBIM | - |
| convert_libim_to_obj | Convert LiBIM files to OBJ format model | LiBIM | - |
| convert_libim_to_osgb | Convert LiBIM files to OSGB format model | LiBIM | - |
| convert_libim_to_fbx | Convert LiBIM files to FBX format model | LiBIM | - |
| convert_libim_to_cityjson | Convert LiBIM files to CityJson format model | LiBIM | - |
| convert_libim_to_citygml | Convert LiBIM files to CityGML format model. | LiBIM | export_content, export_attributes |
| convert_libim_to_collada | Convert LiBIM files to Collada format model | LiBIM | - |

---

## 3D Model Format Conversion
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| convert_3dtiles_to_obj | Convert 3DTiles format files to OBJ format files | JSON | - |
| convert_3dtiles_to_osgb | Convert 3DTiles format files to OSGB format files | JSON | - |
| convert_3dtiles_to_s3m | Convert 3DTiles format files to S3M format files | JSON | - |
| convert_obj_to_3dtiles | Convert OBJ format files to 3DTiles format files | OBJ | - |

---

## LiData Version Conversion
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| convert_lidata_version | Convert a LiData file between point cloud versions | LiData | - |

---

## Other Conversion Tools
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| unit_conversion | Unit conversion | LiData/PCD/LAS/LAZ/E57/PLY/SHP/GPKG/DXF/KML/TreeDB/CSV/LIAEP/LiModel/LiTin/LiBIM/LiTree/OBJ/TIF/TIFF/POS/TRAJ | - |
| attribute_table_data_exporter | Export rows from attribute table to data file | gpkg/dxf/shp/kml/csv/treedb/libim | output_format, row_selection_mode, input_data, output_data |

---

## Common Parameter Explanation

## Usage Recommendations

### Format Selection Guide

| Target Platform | Recommended Format | Conversion Tool |
|---------|---------|---------|
| LiDAR360 internal processing | LiData | convert_xxx_to_lidata |
| Other point cloud software | LAS | convert_point_cloud_to_las |
| Web 3D display | 3DTiles | convert_point_cloud_to_3dtiles / model-specific `*_to_3dtiles` tools |
| CAD software | DXF | convert_point_cloud_to_dxf |
| GIS software | Shape/TIF | convert_point_cloud_to_shape / convert_point_cloud_to_tif |
| 3D modeling software | OBJ/FBX | convert_xxx_to_obj/fbx |
| City 3D standard | CityJSON | convert_xxx_to_cityjson |

### Common Conversion Path

` 
External data -> LAS/E57 -> LiData -> Processing -> LiData -> Target format -> 3DTiles -> Web publishing
` 

---

Quick call: data_conversion-toolID
Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "data_conversion-toolID"
