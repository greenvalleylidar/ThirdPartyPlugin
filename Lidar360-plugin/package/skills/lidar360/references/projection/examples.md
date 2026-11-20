# Projection Examples

## Example 1: Define WGS84 Coordinate System for Point Cloud Data

**Scenario**: Point cloud data has no coordinate system definition; need to assign WGS84 coordinate system

**Preflight Checks**:
- [x] Point cloud file exists and is accessible
- [x] File format is lidata (supported format)
- [x] Using EPSG:4326 (WGS84)

**Invocation Flow**:
```
1. Call projection-define_projection
   - input_data: ["path/to/pointcloud.lidata"]
   - h_authority_code: "EPSG:4326"
   - v_authority_code: "EPSG:4326"
   - is_use_seven_param: false
```

**Expected Result**: Point cloud data is defined with WGS84 coordinate system; coordinate values remain unchanged

---

## Example 2: Reproject Point Cloud from WGS84 to CGCS2000

**Scenario**: Transform point cloud from WGS84 coordinate system to CGCS2000 coordinate system

**Preflight Checks**:
- [x] Point cloud file has WGS84 coordinate system defined
- [x] Target coordinate system EPSG:4490 (CGCS2000) is valid
- [x] Output directory exists and is writable

**Invocation Flow**:
```
1. Call projection-reproject
   - input_data: ["path/to/pointcloud.lidata"]
   - h_authority_code: "EPSG:4490"
   - v_authority_code: "EPSG:5737"
   - output_data: "path/to/output/"
   - is_use_seven_param: false
```

**Expected Result**: New point cloud file generated with CGCS2000 coordinate system

---

## Example 3: Precise Coordinate Transformation Using Seven Parameters

**Scenario**: High-precision coordinate transformation required; using custom seven parameters

**Preflight Checks**:
- [x] Accurate seven parameters obtained [dx, dy, dz, rx, ry, rz, scale]
- [x] Input data coordinate system is defined
- [x] Output path is writable

**Invocation Flow**:
```
1. Call projection-reproject
   - input_data: ["path/to/data.lidata"]
   - h_authority_code: "EPSG:4326"
   - v_authority_code: "EPSG:4326"
   - is_use_seven_param: true
   - seven_param: [100.5, -50.2, 30.1, 0.001, 0.002, -0.001, 1.00001]
   - output_data: "path/to/output/"
```

**Expected Result**: Precise coordinate transformation using seven parameters; new file generated

---

## Example 4: Define and Transform Coordinate Systems for Raster Data

**Scenario**: DEM data needs coordinate system definition and transformation to another coordinate system

**Preflight Checks**:
- [x] Raster file (tif) exists
- [x] Source and target coordinate systems determined

**Invocation Flow**:
```
1. Define coordinate system
   Call projection-define_projection
   - input_data: ["path/to/dem.tif"]
   - h_authority_code: "EPSG:4326"
   - v_authority_code: "EPSG:4326"

2. Reproject
   Call projection-reproject
   - input_data: ["path/to/dem.tif"]
   - h_authority_code: "EPSG:4490"
   - output_data: "path/to/output/"
```

**Expected Result**: DEM data coordinate system transformed from WGS84 to CGCS2000

---

## Example 5: Define and Transform Coordinate Systems for Vector Data

**Scenario**: Shapefile needs coordinate system definition and transformation

**Preflight Checks**:
- [x] Vector file (shp) exists
- [x] Coordinate system parameters determined

**Invocation Flow**:
```
1. Define coordinate system
   Call projection-define_projection
   - input_data: ["path/to/data.shp"]
   - h_authority_code: "EPSG:4326"
   - v_authority_code: "EPSG:4326"

2. Reproject
   Call projection-reproject
   - input_data: ["path/to/data.shp"]
   - h_authority_code: "EPSG:4490"
   - output_data: "path/to/output/"
```

**Expected Result**: Vector data coordinate system transformation completed

---

## Recommended Parameter Values Quick Reference

### Common EPSG Codes

| Code | Coordinate System | Use Case |
|------|--------|----------|
| EPSG:4326 | WGS84 | Global standard; GPS data |
| EPSG:4490 | CGCS2000 | China national standard |
| EPSG:3857 | Web Mercator | Web map display |
| EPSG:326XX | UTM Northern Hemisphere | By longitude zone (XX=zone number) |
| EPSG:327XX | UTM Southern Hemisphere | By longitude zone (XX=zone number) |

### Seven-Parameter Default Values

Use when no transformation is needed: `[0, 0, 0, 0, 0, 0, 1]`
- First three: Translation parameters (meters)
- Middle three: Rotation parameters (arc seconds)
- Last one: Scale factor

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "projection-toolID"
