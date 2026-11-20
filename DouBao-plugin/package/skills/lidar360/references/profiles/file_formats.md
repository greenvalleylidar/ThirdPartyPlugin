# Data Format Reference

> Loadable formats must be obtained via `get_tool_schema "platform-load_layer"` before execution; for convertible formats, refer to `references/data_conversion/tools.md` to choose a tool, and obtain the target tool's current schema before execution. The two serve different purposes: loadable means `platform-load_layer` can open the file as a layer, while convertible means `data_conversion-*` tools support the format as input or output for format conversion.

---

## Loadable File Formats

### platform-load_layer Data Types

| Data Type | Meaning | Loadable Extensions |
|---------|------|-----------|
| `build_model` | Building Model | `.libim` |
| `dem` | Digital Elevation Model | `.limodel` |
| `gaussian_splats` | Gaussian Splats | `.lisplat`, `.ply`, `.xml` |
| `image_project` | Image Project | `.liaep`, `.limap`, `.ligeo`, `.p4d`, `.xml` |
| `panorama` | Panorama | `.imglist`, `.liscan` |
| `point_cloud` | Point Cloud | `.lidata`, `.las`, `.laz`, `.ply`, `.pcd`, `.e57`, `.asc`, `.neu`, `.xyz`, `.pts`, `.csv`, `.txt` |
| `raster` | Raster | `.tif`, `.tiff`, `.jpg`, `.jpeg`, `.bmp`, `.dat`, `.hdr`, `.img` |
| `table` | Table | `.csv`, `.treedb` |
| `trajectory` | Trajectory | `.traj`, `.pos`, `.txt`, `.out` |
| `tree_model` | Tree Model | `.litree` |
| `vector` | Vector | `.shp`, `.gpkg`, `.lidpkg`, `.kml`, `.dxf` |
| `osg_model` | OSG Model | `.osgb`, `.desc`, `.ive`, `.obj` |
| `surface_mesh` | Surface Mesh / TIN | `.litin` |
| `3dtiles` | 3D Tiles | `tileset.json`, `2dtin.json`, `3dtin.json` |

> `.lisplat` must use `data_type=gaussian_splats`; `.ply` and `.xml` may correspond to multiple data types; confirm the specific `data_type` when the user has not specified one.

---

## Convertible File Formats

### Point Cloud Format Conversion

| Format | Extension/Name | Conversion Direction | Corresponding Tools |
|-----|-----------|---------|---------|
| LiData | `.lidata` | Input/Output | `convert_las_to_lidata`, `convert_lidata_version`, `convert_point_cloud_to_*` |
| LAS | `.las` | Input/Output | `convert_las_to_lidata`, `convert_point_cloud_to_las` |
| ASCII | `.txt`, `.xyz`, `.asc` and other text point clouds | Output | `convert_point_cloud_to_ascii` |
| E57 | `.e57` | Output | `convert_point_cloud_to_e57` |
| PLY | `.ply` | Output | `convert_point_cloud_to_ply` |
| DXF | `.dxf` | Output | `convert_point_cloud_to_dxf` |
| Shapefile | `.shp` | Output | `convert_point_cloud_to_shape` |
| TIF | `.tif` | Output | `convert_point_cloud_to_tif` |
| LandXML | `.xml` / LandXML | Output | `convert_point_cloud_to_landxml` |
| 3D Tiles | `tileset.json` / 3D Tiles | Output | `convert_point_cloud_to_3dtiles` |

### Raster Format Conversion

| Format | Extension/Name | Conversion Direction | Corresponding Tools |
|-----|-----------|---------|---------|
| TIF / GeoTIFF | `.tif`, `.tiff` | Input/Output | `convert_tif_to_ascii`, `convert_tif_to_img`, `convert_img_to_tif`, `convert_usgs_dem_to_tif` |
| ASCII Grid | `.asc` / ASCII | Input/Output | `convert_tif_to_ascii`, `convert_ascii_to_vector` |
| IMG | `.img` | Input/Output | `convert_tif_to_img`, `convert_img_to_tif` |
| LiData | `.lidata` | Output | `convert_tif_to_lidata` |
| LiModel | `.limodel` | Output | `convert_tif_to_limodel` |
| USGS DEM | `.dem` / DEM | Input/Output | `convert_tif_to_usgs_dem`, `convert_usgs_dem_to_tif` |

### Vector Format Conversion

| Format | Extension/Name | Conversion Direction | Corresponding Tools |
|-----|-----------|---------|---------|
| Shapefile | `.shp` | Input/Output | `convert_shape_to_kml`, `convert_kml_to_shape`, `convert_vector_to_ascii`, `convert_vector_to_landxml`, `vector_format_conversion` |
| KML | `.kml` | Input/Output | `convert_shape_to_kml`, `convert_kml_to_shape`, `convert_vector_to_landxml`, `vector_format_conversion` |
| DXF | `.dxf` | Input/Output | `convert_vector_to_landxml`, `vector_format_conversion` |
| GPKG | `.gpkg` | Input/Output | `convert_vector_to_ascii`, `convert_vector_to_landxml`, `vector_format_conversion` |
| ASCII | `.txt`, `.csv` and other text | Output | `convert_vector_to_ascii` |
| LandXML | `.xml` / LandXML | Output | `convert_vector_to_landxml` |

### Model Format Conversion

| Format | Extension/Name | Conversion Direction | Corresponding Tools |
|-----|-----------|---------|---------|
| LiModel | `.limodel` | Input/Output | `convert_limodel_to_*`, `convert_tif_to_limodel`, `convert_to_texture_limodel` |
| LiTin | `.litin` | Input | `convert_litin_to_*` |
| LiTree | `.litree` | Input | `convert_litree_to_*` |
| LiBIM | `.libim` | Input | `convert_libim_to_*` |
| OBJ | `.obj` | Input/Output | `convert_limodel_to_obj`, `convert_litin_to_obj`, `convert_litree_to_obj`, `convert_libim_to_obj`, `convert_3dtiles_to_obj`, `convert_obj_to_3dtiles` |
| OSGB | `.osgb` | Input/Output | `convert_limodel_to_osgb`, `convert_litin_to_osgb`, `convert_litree_to_osgb`, `convert_libim_to_osgb`, `convert_3dtiles_to_osgb` |
| FBX | `.fbx` | Output | `convert_litin_to_fbx`, `convert_libim_to_fbx` |
| S3M | `.s3m` | Output | `convert_limodel_to_s3m`, `convert_3dtiles_to_s3m` |
| 3D Tiles | `tileset.json` / 3D Tiles | Input/Output | `convert_limodel_to_3dtiles`, `convert_litin_to_3dtiles`, `convert_litree_to_3dtiles`, `convert_libim_to_3dtiles`, `convert_3dtiles_to_obj`, `convert_3dtiles_to_osgb`, `convert_3dtiles_to_s3m`, `convert_obj_to_3dtiles` |
| CityJSON | `.cityjson`, `.json` | Output | `convert_litree_to_cityjson`, `convert_libim_to_cityjson` |
| Collada | `.dae` / Collada | Output | `convert_libim_to_collada` |
| LandXML | `.xml` / LandXML | Output | `convert_litin_to_landxml` |
| TIF | `.tif` | Output | `convert_limodel_to_tif` |
| DXF | `.dxf` | Output | `convert_litin_to_dxf` |
| LiData | `.lidata` | Output | `convert_litin_to_lidata` |

---

## Loading vs. Conversion

| Scenario | Entry Point | Description |
|-----|---------|------|
| Open data and display as a layer | `platform-load_layer` | File extension must belong to the loadable extensions for the corresponding `data_type` |
| Convert external format to LiDAR360 internal format | `data_conversion-*` | Common entries include `convert_las_to_lidata`, `convert_tif_to_lidata` |
| Export processing results to external software | `data_conversion-*` | Choose LAS, TIF, Shape, OBJ, FBX, 3D Tiles, CityJSON, etc. based on target platform |
| Web 3D publishing | `data_conversion-*` | Common target formats are 3D Tiles or S3M |

---

## Common Conversion Scenarios

### Point Cloud Import
```text
LAS -> LiData: data_conversion-convert_las_to_lidata
```

### Point Cloud Export
```text
LiData -> LAS/E57/PLY/DXF/Shape/TIF/LandXML/3D Tiles: data_conversion-convert_point_cloud_to_*
```

### Raster Conversion
```text
TIF -> ASCII/IMG/LiData/LiModel/USGS DEM: data_conversion-convert_tif_to_*
IMG -> TIF: data_conversion-convert_img_to_tif
USGS DEM -> TIF: data_conversion-convert_usgs_dem_to_tif
```

### Vector Conversion
```text
Shapefile <-> KML: data_conversion-convert_shape_to_kml / data_conversion-convert_kml_to_shape
Shape/KML/DXF -> target vector format: data_conversion-vector_format_conversion
```

### 3D Model Conversion
```text
LiBIM/LiTin/LiTree/LiModel -> OBJ/OSGB/3D Tiles: data_conversion-convert_*_to_*
OBJ -> 3D Tiles: data_conversion-convert_obj_to_3dtiles
3D Tiles -> OBJ/OSGB/S3M: data_conversion-convert_3dtiles_to_*
```
