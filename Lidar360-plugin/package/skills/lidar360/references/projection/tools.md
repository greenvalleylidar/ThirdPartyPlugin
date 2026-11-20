# Projection Tools Registration
---

## Coordinate Reference System Definition and Transformation
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| define_projection | Define a coordinate reference system for supported data without changing actual coordinate values. Use reproject when coordinate transformation is needed | lidata/tif/tiff/dat/img/shp/gpkg/libim/litree/obj | coordinate_name, h_authority_code, v_authority_code, is_use_seven_param, seven_param, wkt |
| reproject | Transform data with an existing coordinate reference system to the target coordinate system and generate new output files | lidata/tif/tiff/dat/img/shp/gpkg/libim/litree/obj | coordinate_name, h_authority_code, v_authority_code, is_use_seven_param, seven_param, wkt, output_data |

---

## Coordinate Query and Transformation
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| query_crs | Query official, custom, or preset coordinate reference systems, supporting filtering by authority code, definition, name, type, source, or geoid | - | authority_code, crs_type, definition, definition_format, geoid, include_deprecated, include_projjson, include_wkt, keyword, limit, match_mode, offset, source |
| transform_coordinates | Transform one or more coordinate points between coordinate reference systems. For geographic coordinates: x=longitude, y=latitude; for projected coordinates: x=easting, y=northing | - | source_crs, source_crs_format, target_crs, target_crs_format, points, is_use_seven_param, seven_param, linear_unit_as_meter, operation |

---

## Coordinate Transformation Management
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| get_coordinate_transformations | Get all stored coordinate transformation parameters, including 4-parameter, 7-parameter, 3D affine, XY multiplier, linear, known-point, and height-fitting transformations | - | - |
| define_transformation | Define a new coordinate transformation and permanently save it to the transformation manager for use by coordinate transformation/reprojection tools | - | name, type, dx, dy, dz, rx, ry, rz, scale_ppm, theta, scale_factor, mx, my, mz, x1, x2, x3, y1, y2, y3, z1, z2, z3, a1, a2, a3, b1, b2, b3, h0-h9, h_fitting_name |
| fit_geoid_transformation | Read geoid fitting points from TXT or CSV files, solve the selected height anomaly model, and save it as an auto-named coordinate transformation | txt/csv | input_data, method |
| transformation_file_coordinates | Apply a named coordinate transformation to an input file and create an output file | lidata/shp/gpkg/dxf/treedb/libim/obj | input_data, output_data, transformation_name |

---

## Common Parameter Explanation

### Coordinate System Parameters

| Parameter | Description | Example |
|------|------|------|
| coordinate_name | Coordinate system name | WGS84/49N, CGCS2000/3DEG |
| h_authority_code | Horizontal coordinate system EPSG code | EPSG:4326, EPSG:4490 |
| v_authority_code | Vertical coordinate system EPSG code | EPSG:4326, EPSG:5737 |
| wkt | Coordinate system definition in Well-Known Text format | Custom WKT string |

### Seven-Parameter Transformation

| Parameter | Description |
|------|------|
| is_use_seven_param | Whether to use seven parameters for coordinate transformation |
| seven_param | Seven-parameter array [dx, dy, dz, rx, ry, rz, scale], default all zeros |

### Supported Data Formats

| Type | Formats |
|------|------|
| Point Cloud | lidata |
| Raster | tif, tiff, dat, img |
| Vector | shp, gpkg |
| Model | libim, litree, obj |

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "projection-toolID"
