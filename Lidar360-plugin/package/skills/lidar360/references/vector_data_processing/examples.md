# Vector Data Processing Usage Examples

## Clipping Examples

### Scenario: Extract Data by Administrative Region

```json
{
  "tool": "clip_vector_by_polygon",
  "params": {
    "input_data": {
      "input_vector_file": "D:/data/national_roads.shp",
      "overlay_vector_file": "D:/data/administrative_divisions.gpkg"
    },
    "clip_layer_name": "Beijing",
    "output_data": "D:/output/beijing_roads.gpkg"
  }
}
```

**Description**: Extract roads within Beijing from national road data

---

## Merging Examples

### Scenario: Merge Multi-Phase Survey Data

```json
{
  "tool": "merge_vectors",
  "params": {
    "input_data": [
      "D:/data/2020_survey.shp",
      "D:/data/2021_survey.shp",
      "D:/data/2022_survey.shp"
    ],
    "output_data": "D:/output/survey_summary.gpkg"
  }
}
```

**Description**: Merge three years of survey data into a single file

---

## Editing Examples

### Scenario: Contour Optimization Processing

Step 1: Line smoothing

```json
{
  "tool": "vector_smooth_lines",
  "params": {
    "input_data": "D:/data/raw_contours.shp",
    "method": 2,
    "output_data": "D:/temp/smoothed_contours.shp"
  }
}
```

Step 2: Remove duplicate vertices

```json
{
  "tool": "remove_duplicate_vertices",
  "params": {
    "input_data": "D:/temp/smoothed_contours.gpkg",
    "output_data": "D:/output/optimized_contours.gpkg"
  }
}
```

**Description**: Contours become more aesthetically pleasing after smoothing and vertex cleanup

---

## Terrain Conformance Examples

### Scenario: 2D Road to 3D Conversion

```json
{
  "tool": "set_z_from_raster",
  "params": {
    "input_data": {
      "vector_file": "D:/data/road_centerline.shp",
      "raster_file": "D:/dem/regional_dem.tif"
    },
    "band_number": 1,
    "scale": 1.0,
    "offset": 0,
    "no_data": -9999,
    "output_data": "D:/output/3d_road.gpkg"
  }
}
```

**Description**: Conform 2D roads to the terrain surface to generate 3D roads

### Scenario: Elevation Datum Conversion

```json
{
  "tool": "set_z_from_raster",
  "params": {
    "input_data": {
      "vector_file": "D:/data/pipeline.shp",
      "raster_file": "D:/dem/dem_1985_elevation.tif"
    },
    "band_number": 1,
    "scale": 1.0,
    "offset": -0.5,
    "no_data": 0,
    "output_data": "D:/output/pipeline_2000_elevation.gpkg"
  }
}
```

**Description**: Use the offset parameter for elevation datum conversion

---

## Splitting and Extraction Examples

### Scenario: Split Data by Land Use Type

```json
{
  "tool": "split_by_attribute",
  "params": {
    "input_data": "D:/data/land_use_survey.shp",
    "layer_name": "land_use_survey",
    "split_fields": ["land_use_name"],
    "output_data": "D:/output/split_by_land_use/"
  }
}
```

**Description**: Generate a separate file for each land use type

### Scenario: Multi-Factor Sampling Analysis

```json
{
  "tool": "extract_multi_values_to_points",
  "params": {
    "bilinear_interpolation": false,
    "input_data": {
      "vector_file": "D:/data/sampling_points.shp",
      "image_files": [
        "D:/raster/dem.tif",
        "D:/raster/slope.tif",
        "D:/raster/vegetation_index.tif"
      ]
    }
  }
}
```

**Description**: Extract values from multiple rasters into the sampling point attribute table

---

## Best Practices

### Workflow Suggestions

1. **Data Preparation**: Ensure coordinate systems are consistent
2. **Quality Check**: Run the preflight checklist
3. **Parameter Configuration**: Start with default values and adjust
4. **Result Verification**: Check output data integrity

### Parameter Optimization Suggestions

| Parameter | Optimization Suggestion |
|----------|----------------------|
| method | Test from low to high to avoid over-smoothing |
| scale | Set according to raster units (e.g., meters -> centimeters x 100) |
| offset | Set according to elevation datum difference |
| no_data | Use obviously abnormal values for easy identification |
