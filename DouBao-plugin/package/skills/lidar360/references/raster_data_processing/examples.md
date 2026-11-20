# Raster Data Processing Typical Examples

## Example 1: Raster Clipping and Extraction Workflow

**Scenario**: Extract a study area from a large-extent DEM

```
Step 1: Load DEM data
-> platform-load_layer

Step 2: Load study area vector boundary
-> platform-load_layer

Step 3: Clip by polygon
-> raster_data_processing-clip_raster_by_polygon
  - input_data: dem.tif
  - polygon_file: boundary.shp

Step 4: Extract elevation range by attribute (optional)
-> raster_data_processing-extract_by_attributes
  - expression: "value >= 100 AND value <= 500"

Step 5: Define NoData value
-> raster_data_processing-define_raster_nodata_value
  - nodata_value: -9999
```

---

## Example 2: Raster Mosaicking Workflow

**Scenario**: Mosaic multiple DEM map sheets

```
Step 1: Check all DEM coordinate systems
-> Ensure projections are consistent

Step 2: Check resolution
-> Ensure pixel sizes are consistent

Step 3: Execute mosaicking
-> raster_data_processing-raster_mosaic
  - input_data: [dem1.tif, dem2.tif, dem3.tif]
  - sample_type: 5 (average sampling)

Step 4: Define NoData value
-> raster_data_processing-define_raster_nodata_value
```

---

## Example 3: Raster Band Compositing and Index Calculation

**Scenario**: Create multi-band imagery and calculate vegetation index

```
Step 1: Composite raster bands
-> raster_data_processing-composite_raster_bands
  - input_data: [red.tif, green.tif, blue.tif, nir.tif]

Step 2: Create true color composite
-> raster_data_processing-create_color_composite
  - red_expression: "B1"
  - green_expression: "B2"
  - blue_expression: "B3"

Step 3: Calculate NDVI (using raster calculator)
-> raster_data_processing-raster_calculator
  - expression: "(nir - red) / (nir + red)"

Step 4: Export results
```

---

## Example 4: Raster Map Sheet Subdivision

**Scenario**: Subdivide a large-extent raster into map sheets

```
Step 1: Load large-extent raster
-> platform-load_layer

Step 2: Execute subdivision
-> raster_data_processing-raster_subdivision
  - input_data: large_dem.tif
  - scale: 2 (1:2000 scale)

Step 3: Batch process each map sheet (optional)
```

---

## Common Raster Calculator Expressions

| Calculation Goal | Expression Example |
|---------|-----------|
| Normalization | "(raster - min) / (max - min)" |
| Elevation difference | "dem1 - dem2" |
| Conditional extraction | "dem > 100" |
| Slope to degrees | "atan(slope) * 180 / 3.14159" |
| Vegetation index | "(nir - red) / (nir + red)" |

---

**Tip**: Use `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "raster_data_processing-toolID"` to get detailed parameter descriptions
