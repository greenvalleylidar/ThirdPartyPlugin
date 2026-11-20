# Terrain Analysis Workflows

> Point cloud to TIN, contour, DSM, DEM - four terrain product generation workflows.

---

## Workflow Overview

| Scenario | Recommended Workflow | Key Tools | Difficulty |
|-----|---------|---------|------|
| Point cloud to TIN | Optional preprocessing (smooth/resample/denoise) -> Ground classification -> Generate TIN | `point_cloud_to_tin` | Advanced |
| Point cloud to contours | Optional preprocessing (smooth/resample/denoise) -> Ground classification -> Generate contours from point cloud | `generate_contour_from_pointcloud` | Advanced |
| Point cloud to DSM | Optional preprocessing (smooth/resample/denoise) -> Generate DSM | `generate_general_dsm_from_pointcloud` | Medium |
| Point cloud to DEM | Optional preprocessing (smooth/resample/denoise) -> Ground classification -> Generate DEM | `generate_general_dem_from_pointcloud` | Advanced |
| Generate CHM | DSM + DEM -> Generate CHM | `generate_chm` | Basic |
| Generate DOM | Image alignment + DSM/DEM -> Generate DOM | `generate_dom_by_pixel_mode` | Medium |
| Terrain derivative analysis | DEM -> Slope/Aspect/Roughness/Hillshade/Sky view factor/Viewshed etc. | Terrain derivative toolset | Medium |

---

## General Processing Logic

### General Preprocessing Chain (Optional)

`Point cloud smoothing`, `resampling`, and `denoising` are optional preprocessing steps; not all data requires every step. The actual workflow can execute one, several, or all of these steps depending on point cloud quality, point density, and product accuracy requirements:

```text
Raw Point Cloud -> [Optional: Point Cloud Smoothing] -> [Optional: Resampling] -> [Optional: Denoising] -> (Ground classification as needed) -> Terrain Product Generation
```

**Optional execution recommendations**:

| Optional Step | Applicable When | Can Be Skipped When |
|---------|---------|-----------|
| Point cloud smoothing | Local elevation jitter is obvious, contours have visible jagged edges, DSM/DEM surface is discontinuous | Original point cloud quality is high; need to preserve maximum detail, steep edges, building edges, or micro-terrain |
| Resampling | Point density too high, large data volume, slow processing | Point density is low, or need to preserve highest accuracy and detail |
| Denoising | Outliers, fly-away points, or obvious noise present | Data has passed quality control, or concerned about accidentally removing valid points in sparse areas |

> Note: Model Builder examples typically show "Point cloud smoothing -> Resampling -> Denoising -> Subsequent product tools"; in this workflow skill these three steps are treated as **optional preprocessing**. TIN/contour/DEM workflows typically require ground classification before product generation; the DSM workflow does not mandate ground classification.

### General Parameter Recommendations

| Parameter | Recommended Value | Description |
|-----|-------|------|
| `neighbor_points` | 10 | Denoising neighbor point count |
| `multiples_of_std_deviation` | 5 | Denoising standard deviation multiplier |
| `smoothing_type` | 0 | Point cloud smoothing method |
| `search_radius` | 0.2 | Smoothing search radius |
| `max_fix_distance` | 0.1 | Smoothing maximum correction distance |
| `sampling_type` | 1 | Resampling method, Model Builder default configuration |
| `sampling_rate` | 50 | Resampling percentage |
| `scene_type` | 2 | Ground classification scene type, default gentle slope/general terrain |
| `to_class` | 2 | Ground point class |

---

## Workflow 1: Point Cloud to TIN Generation Workflow

**Applicable scenario**: Generate TIN (`.litin` or `.json`) from raw point cloud, optionally combined with breaklines to control terrain structure.

**Workflow diagram**:

```text
Raw Point Cloud -> [Optional: Point Cloud Smoothing/Resampling/Denoising] -> Ground Classification -> Generate TIN
```

**Key tool**: `terrain_analysis-point_cloud_to_tin`

### Detailed Steps

#### Step 1: Optional Preprocessing - Point Cloud Smoothing

> Optional: Execute when point cloud has local jitter or subsequent contours/raster surfaces are not smooth; skip if steep edges, building edges, or micro-terrain details need to be preserved.

```json
{
  "step": 1,
  "description": "Point cloud smoothing",
  "tool": "pointcloud_processing-pointcloud_smooth",
  "input": {
    "input_data": "/data/raw.lidata",
    "output_data": "/output/smoothed.lidata",
    "smoothing_type": 0,
    "search_radius": 0.2,
    "max_fix_distance": 0.1,
    "select_class": [0, 1, 2, 3, 4, 5, 6]
  }
}
```

#### Step 2: Optional Preprocessing - Resampling

> Optional: Execute when point density is too high, file size is too large, or processing is slow; skip if point density is low or highest accuracy needs to be preserved. If Step 1 is skipped, change input to raw point cloud.

```json
{
  "step": 2,
  "description": "Point cloud resampling",
  "tool": "pointcloud_processing-pointcloud_subsampling",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "output_data": "/output/subsampled.lidata",
    "sampling_type": 1,
    "from_class": [0, 1, 2, 3, 4, 5, 6],
    "sampling_rate": 50,
    "minimum_points_spacing": 0,
    "octree": 21
  }
}
```

#### Step 3: Optional Preprocessing - Point Cloud Denoising

> Optional: Execute when outliers, fly-away points, or obvious noise are present; skip if data has passed quality control or concerned about accidentally removing valid points in sparse areas. If preceding optional steps are skipped, input should be the output of the last executed step or the raw point cloud.

```json
{
  "step": 3,
  "description": "Point cloud denoising",
  "tool": "pointcloud_processing-pointcloud_outlier_removal",
  "input": {
    "input_data": ["{{step2.data.output_data}}"],
    "neighbor_points": 10,
    "multiples_of_std_deviation": 5,
    "output_data": "/output/denoised.lidata"
  }
}
```

#### Step 4: Ground Point Classification (Progressive TIN Densification)

> If some or all of Steps 1-3 optional preprocessing are skipped, `pointcloud_files` should be connected to the output of the last executed step; if all are skipped, use raw point cloud directly.

```json
{
  "step": 4,
  "description": "Ground point classification",
  "tool": "pointcloud_classification-classify_ground_by_progressive_tin_densification",
  "input": {
    "input_data": ["{{step3.data.output_data}}"],
    "scene_type": 2,
    "grid_size": 20,
    "iteration_angle": 8,
    "iteration_distance": 1.2,
    "max_terrain_angle": 88,
    "max_building_size": 30,
    "tolerance_above": 0.15,
    "tolerance_below": 0.15,
    "to_class": 2
  }
}
```

#### Step 5: Generate TIN

```json
{
  "step": 5,
  "description": "Generate TIN",
  "tool": "terrain_analysis-point_cloud_to_tin",
  "input": {
    "input_data": {
      "input_pointcloud": "{{step4.data.output_data}}",
      "breakline_file": "/data/breakline.shp"
    },
    "output_data": "/output/terrain.litin",
    "from_class": [2],
    "tin_type": 0,
    "output_format": 1,
    "max_triangle_edge": 30,
    "buffer_size": 10,
    "scale_type": 2,
    "scale_buffer_size": 10,
    "tile_type": 0,
    "tile_width": 100,
    "tile_height": 100,
    "buffer_size_spikefree": 0.5,
    "free_size_spikefree": 1
  }
}
```

> **Configuration recommendations**:
> - To use only ground points for the terrain TIN, set `from_class` to `[2]`.
> - If breaklines are needed to constrain terrain boundaries or slope edges, provide `breakline_file` (supports `.shp/.dxf/.gpkg`).
> - `max_triangle_edge` controls the maximum triangle edge length; increase when point density is low or there are many voids.

---

## Workflow 2: Point Cloud to Contour Generation Workflow

**Applicable scenario**: Generate contour vector files (`.shp/.dxf/.gpkg`) directly from point cloud, supporting breaklines, ROI, clipping vectors, and automatic annotation.

**Workflow diagram**:

```text
Raw Point Cloud -> [Optional: Point Cloud Smoothing/Resampling/Denoising] -> Ground Classification -> Generate Contours from Point Cloud
```

**Key tool**: `terrain_analysis-generate_contour_from_pointcloud`

### Detailed Steps

#### Steps 1-4: Optional Preprocessing and Ground Classification

Same as Steps 1-4 in "Workflow 1: Point Cloud to TIN Generation Workflow". Steps 1-3 (point cloud smoothing, resampling, denoising) are optional preprocessing and can be selected based on point cloud quality; ground classification is generally recommended for terrain contours, using class 2 to generate contours.

#### Step 5: Generate Contours from Point Cloud

```json
{
  "step": 5,
  "description": "Generate contours from point cloud",
  "tool": "terrain_analysis-generate_contour_from_pointcloud",
  "input": {
    "input_data": {
      "pointcloud_file": "{{step4.data.output_data}}",
      "input_breakline": "/data/breakline.shp",
      "roi_vector_file": "/data/roi.shp",
      "trimming_vector_file": "/data/trim.shp"
    },
    "output_data": "/output/contours.shp",
    "from_class": [2],
    "scale": 3,
    "base": 0,
    "gener_major": true,
    "gener_basic": true,
    "gener_minor": true,
    "major_spacing": 25,
    "basic_spacing": 5,
    "minor_spacing": 2.5,
    "major_line_width": 30,
    "basic_line_width": 15,
    "minor_line_width": 15,
    "terrain_smooth": true,
    "terrain_smooth_iter": 5,
    "mean_smooth_k": 5,
    "smooth_method": 0,
    "smooth_span": 0.005,
    "simplify_method": 0,
    "simply_dist": 3,
    "max_triangle_length": 30,
    "auto_label_contour": true,
    "label_accuracy": 2,
    "label_interval": 35,
    "delete_min_area": true,
    "min_area": 10,
    "delete_min_length": true,
    "min_length": 5,
    "handle_contradictions": 1,
    "contour25D": false,
    "file_type": 11
  }
}
```

> **Configuration recommendations**:
> - `from_class: [2]` means using ground points for contour generation, the most common configuration for DEM/terrain contours.
> - `major_spacing/basic_spacing/minor_spacing` control the index contour, basic contour, and intermediate contour spacing respectively; adjust based on mapping scale.
> - `scale` defaults to `3` (commonly used for 1:5000 scenarios); for larger scales, refer to tool parameter descriptions.
> - If contours have obvious jagged edges, keep `terrain_smooth: true` and appropriately increase `terrain_smooth_iter`.

---

## Workflow 3: Point Cloud to Digital Surface Model (DSM) Generation Workflow

**Applicable scenario**: Generate DSM raster (`.tif/.tiff/.img/.dat/.asc`) from point cloud, representing surface elevation including buildings, vegetation, etc.

**Workflow diagram**:

```text
Raw Point Cloud -> [Optional: Point Cloud Smoothing/Resampling/Denoising] -> Generate DSM
```

**Key tool**: `terrain_analysis-generate_general_dsm_from_pointcloud`

### Detailed Steps

#### Steps 1-3: Optional Preprocessing

Same as Steps 1-3 in "Workflow 1" (point cloud smoothing, resampling, denoising), all optional. DSM typically needs to preserve feature surface elevation; if the original point cloud quality is good, DSM can be generated directly from raw point cloud; execute corresponding preprocessing only if the point cloud has noise, excessive data volume, or local jitter.

#### Step 4: Generate DSM

> If some or all of Steps 1-3 optional preprocessing are skipped, `pointcloud_files` should be connected to the output of the last executed step; if all are skipped, use raw point cloud directly.

```json
{
  "step": 4,
  "description": "Generate Digital Surface Model DSM",
  "tool": "terrain_analysis-generate_general_dsm_from_pointcloud",
  "input": {
    "input_data": ["{{step3.data.output_data}}"],
    "output_data": "/output/dsm.tif",
    "from_class": null,
    "return_number": null,
    "interpolator": null,
    "x_size": null,
    "y_size": null,
    "elevation_prec": null,
    "fill_holes": null,
    "radius_type": null,
    "number_of_points": null,
    "distance": null,
    "power": null,
    "buffer": null,
    "buffer_size": null,
    "free_size": null,
    "merge": null,
    "with_cloud_name": null,
    "use_sheet_frame": null,
    "use_spike": null,
    "optimize_roof_class": null,
    "optimize_vegetation_class": null,
    "scale": null
  }
}
```

> **Configuration recommendations**:
> - DSM typically does not restrict `from_class`, to preserve the highest surface information including buildings and vegetation; if only specific classes are needed, set the corresponding class array.
> - `x_size/y_size` is the raster resolution; determined by data and scenario; increase appropriately when point density is low.
> - `interpolator` sets the interpolation method (e.g. IDW, Kriging, TIN), to be determined from the tool schema and the data.

---

## Workflow 4: Point Cloud to Digital Elevation Model (DEM) Generation Workflow

**Applicable scenario**: Generate DEM raster (`.tif/.tiff/.img/.dat/.asc`) from point cloud, representing bare ground terrain elevation.

**Workflow diagram**:

```text
Raw Point Cloud -> [Optional: Point Cloud Smoothing/Resampling/Denoising] -> Ground Classification -> Generate DEM
```

**Key tool**: `terrain_analysis-generate_general_dem_from_pointcloud`

### Detailed Steps

#### Steps 1-4: Optional Preprocessing and Ground Classification

Same as Steps 1-4 in "Workflow 1: Point Cloud to TIN Generation Workflow". Steps 1-3 (point cloud smoothing, resampling, denoising) are optional preprocessing; ground classification is generally recommended for DEM, using class 2 to generate the bare ground elevation model.

#### Step 5: Generate DEM

```json
{
  "step": 5,
  "description": "Generate Digital Elevation Model DEM",
  "tool": "terrain_analysis-generate_general_dem_from_pointcloud",
  "input": {
    "input_data": ["{{step4.data.output_data}}"],
    "output_data": "/output/dem.tif",
    "from_class": null,
    "interpolator": null,
    "x_size": null,
    "y_size": null,
    "elevation_prec": null,
    "fill_holes": null,
    "radius_type": null,
    "number_of_points": null,
    "distance": null,
    "power": null,
    "buffer": null,
    "buffer_size": null,
    "free_size": null,
    "merge": null,
    "with_cloud_name": null,
    "use_sheet_frame": null,
    "use_spike": null,
    "scale": null
  }
}
```

> **Configuration recommendations**:
> - In Model Builder, ground classification has been executed before DEM generation; when producing DEM, it is recommended to set `from_class` to the ground point class (determined from the data's classification result) to ensure only ground points are used.
> - `radius_type` sets the search radius type; DEM and DSM workflows suit different values, to be determined by data and scenario.
> - DEM is very sensitive to ground classification quality; if the generated result has building/vegetation residuals, first check whether class 2 is clean.

---

## Workflow 5: Canopy Height Model (CHM) Generation Workflow

**Applicable scenario**: Generate CHM (Canopy Height Model) from DSM and DEM, for forestry analysis, vegetation height estimation, etc.

**Workflow diagram**:

```text
DSM + DEM -> Generate CHM
```

**Key tool**: `terrain_analysis-generate_chm`

### Detailed Steps

#### Step 1: Generate CHM

> Prerequisite: DSM and DEM must be generated first; refer to Workflow 3 (DSM generation) and Workflow 4 (DEM generation).

```json
{
  "step": 1,
  "description": "Generate Canopy Height Model CHM",
  "tool": "terrain_analysis-generate_chm",
  "input": {
    "input_data": {
      "input_dem": "/output/dem.tif",
      "input_dsm": "/output/dsm.tif"
    },
    "output_data": "/output/chm.tif"
  }
}
```

> **Configuration recommendations**:
> - Ensure DSM and DEM have identical resolution, coordinate system, and extent
> - CHM = DSM - DEM, yielding vegetation and building height information
> - Output can be used for forestry individual tree segmentation (forestry_airborne module)

---

## Workflow 6: DOM Generation Workflow

**Applicable scenario**: Generate Digital Orthophoto (DOM) from image project and DSM/DEM, for map making, feature identification, etc.

**Workflow diagram**:

```text
Image Project + DSM/DEM -> Generate DOM
```

**Key tool**: `terrain_analysis-generate_dom_by_pixel_mode`

### Detailed Steps

#### Step 1: Image Alignment (Prerequisite)

> Must first use the image alignment tool from the imagery_processing module to complete aerial triangulation.

```json
{
  "step": 1,
  "description": "Image aerial triangulation (imagery_processing module)",
  "tool": "imagery_processing-image_alignment",
  "input": {
    "input_data": "/data/image_project.liaep"
  },
  "notes": "Results are written directly into the image project file"
}
```

#### Step 2: Generate DSM (Prerequisite)

> Refer to "Workflow 3: Point Cloud to Digital Surface Model (DSM) Generation Workflow"

```json
{
  "step": 2,
  "description": "Generate DSM (refer to Workflow 3)",
  "tool": "terrain_analysis-generate_general_dsm_from_pointcloud",
  "input": {
    "input_data": ["/data/raw.lidata"],
    "output_data": "/output/dsm.tif",
    "from_class": null,
    "return_number": null,
    "x_size": null,
    "y_size": null,
    "buffer": null
  }
}
```

#### Step 3: Generate DOM

```json
{
  "step": 3,
  "description": "Generate Digital Orthophoto DOM",
  "tool": "terrain_analysis-generate_dom_by_pixel_mode",
  "input": {
    "input_data": {
      "input_data": "/data/image_project.liaep",
      "dem_dsm_path": "/output/dsm.tif"
    },
    "output_data": "/output/dom.tif",
    "resolution_mode": 0,
    "auto_gsd": false,
    "manual_gsd": 0.2
  }
}
```

> **Configuration recommendations**:
> - `resolution_mode`: 0=manually specify resolution, 1=automatically calculate GSD
> - `auto_gsd`: when true, automatically calculate ground sample distance
> - `manual_gsd`: set DOM output resolution (meters) in manual mode
> - DOM can be used for feature identification, map making, forestry analysis, etc.

---

## Workflow 7: Terrain Derivative Analysis Workflow

**Applicable scenario**: Calculate multiple terrain derivative products based on DEM, for geomorphological analysis, engineering planning, hydrological analysis, etc.

**Workflow diagram**:

```text
DEM -> Slope/Aspect/Roughness/Hillshade/Sky View Factor/Viewshed/Solar Radiation/Hydrological Analysis
```

**Key tools**: Terrain derivative toolset (`slope_analysis`, `aspect_analysis`, `roughness_analysis`, `generate_hill_shade`, `sky_view_factor`, `viewshed_analysis`, `annual_insolation`, `solar_radiation`, `drainage_analysis`, `flooding_analysis`, `generate_relative_elevation_model`)

### Detailed Steps

#### Step 1: Slope Analysis

**Applicable scenario**: Analyze terrain slope for soil erosion assessment, engineering planning, etc.

```json
{
  "step": 1,
  "description": "Slope analysis",
  "tool": "terrain_analysis-slope_analysis",
  "input": {
    "input_data": "/output/dem.tif",
    "output_data": "/output/slope.tif",
    "z_scale": 1
  }
}
```

#### Step 2: Aspect Analysis

**Applicable scenario**: Analyze terrain aspect orientation for ecological research, solar energy planning, etc.

```json
{
  "step": 2,
  "description": "Aspect analysis",
  "tool": "terrain_analysis-aspect_analysis",
  "input": {
    "input_data": "/output/dem.tif",
    "output_data": "/output/aspect.tif",
    "z_scale": 1
  }
}
```

#### Step 3: Roughness Analysis

**Applicable scenario**: Analyze terrain roughness for geomorphological classification, landscape analysis, etc.

```json
{
  "step": 3,
  "description": "Roughness analysis",
  "tool": "terrain_analysis-roughness_analysis",
  "input": {
    "input_data": "/output/dem.tif",
    "output_data": "/output/roughness.tif"
  }
}
```

#### Step 4: Hillshade Generation

**Applicable scenario**: Generate hillshade map for terrain visualization, cartography, etc.

```json
{
  "step": 4,
  "description": "Generate hillshade",
  "tool": "terrain_analysis-generate_hill_shade",
  "input": {
    "input_data": "/output/dem.tif",
    "output_data": "/output/hillshade.tif",
    "azimuth": 315,
    "altitude": 45,
    "z_scales": 1
  }
}
```

> **Configuration recommendations**:
> - `azimuth`: Sun azimuth angle (degrees), 315=northwest direction
> - `altitude`: Sun altitude angle (degrees), 45=45-degree altitude
> - `z_scales`: Elevation scale factor, exaggerates or compresses terrain relief

#### Step 5: Sky View Factor Analysis

**Applicable scenario**: Assess the degree to which terrain obscures the sky, for urban ventilation, radiation analysis, etc.

```json
{
  "step": 5,
  "description": "Sky view factor analysis",
  "tool": "terrain_analysis-sky_view_factor",
  "input": {
    "input_data": "/output/dem.tif",
    "output_data": "/output/sky_view_factor.tif",
    "max_radius": 100
  }
}
```

#### Step 6: Viewshed Analysis

**Applicable scenario**: Calculate visible range from specified observation points, for landscape planning, lookout tower siting, etc.

```json
{
  "step": 6,
  "description": "Viewshed analysis",
  "tool": "terrain_analysis-viewshed_analysis",
  "input": {
    "input_data": {
      "input_dem": "/output/dem.tif",
      "observer_points": "/data/observer_points.shp"
    },
    "output_data": "/output/viewshed.tif",
    "observer_height": 1.7,
    "target_height": 0
  }
}
```

#### Step 7: Annual Insolation Analysis

**Applicable scenario**: Estimate annual sunshine duration, for urban planning, ecological research, etc.

```json
{
  "step": 7,
  "description": "Annual insolation analysis",
  "tool": "terrain_analysis-annual_insolation",
  "input": {
    "input_data": "/output/dem.tif",
    "output_data": "/output/annual_insolation.tif",
    "year": 2026,
    "interval": 30
  }
}
```

#### Step 8: Solar Radiation Analysis

**Applicable scenario**: Calculate solar radiation received by terrain surface, for solar energy planning, ecological research, etc.

```json
{
  "step": 8,
  "description": "Solar radiation analysis",
  "tool": "terrain_analysis-solar_radiation",
  "input": {
    "input_data": "/output/dem.tif",
    "output_data": "/output/solar_radiation.tif",
    "latitude": 30.0,
    "time_period": "Day",
    "start_day": "2026-06-29",
    "stop_day": "2026-06-29",
    "moment": 12
  }
}
```

#### Step 9: Hydrological Analysis (Drainage Analysis)

**Applicable scenario**: Perform hydrological analysis based on DEM, extract flow direction, flow accumulation, etc.

```json
{
  "step": 9,
  "description": "Hydrological analysis - drainage analysis",
  "tool": "terrain_analysis-drainage_analysis",
  "input": {
    "input_data": "/output/dem.tif",
    "output_data": "/output/drainage.tif",
    "flow_thre": 1000
  }
}
```

#### Step 10: Flood Inundation Analysis

**Applicable scenario**: Simulate flood inundation extent, for disaster assessment, flood prevention planning, etc.

```json
{
  "step": 10,
  "description": "Flood inundation analysis",
  "tool": "terrain_analysis-flooding_analysis",
  "input": {
    "input_data": {
      "dem_file": "/output/dem.tif",
      "roi_file": "/data/flood_roi.shp",
      "building_file": "/data/buildings.shp"
    },
    "output_data": "/output/flooding.tif",
    "water_level_base_elevation": 10.0
  }
}
```

> **Configuration recommendations**:
> - Can simulate different inundation scenarios at different water levels
> - Combine with hydrological data for flood risk assessment

#### Step 11: Generate Relative Elevation Model (REM)

**Applicable scenario**: Generate elevation model relative to riverbed, for riverbed analysis, river engineering, etc.

```json
{
  "step": 11,
  "description": "Generate Relative Elevation Model REM",
  "tool": "terrain_analysis-generate_relative_elevation_model",
  "input": {
    "input_data": {
      "input_dem": "/output/dem.tif",
      "input_vector": "/data/river_centerline.shp"
    },
    "output_data": "/output/rem.tif",
    "sample_distance": 10
  }
}
```

> **Configuration recommendations**:
> - REM = DEM - riverbed elevation, used for analyzing river terrain
> - Commonly used for river management, ecological restoration, etc.

---

## Parameter Configuration Quick Reference

### Terrain Product Tools

| Product | Tool | Main Input | Main Output | Key Parameters |
|-----|------|---------|---------|---------|
| TIN | `terrain_analysis-point_cloud_to_tin` | `.lidata` + optional breaklines | `.litin/.json` | `from_class`, `max_triangle_edge`, `tin_type` |
| Contours | `terrain_analysis-generate_contour_from_pointcloud` | `.lidata` + optional breaklines/ROI/clip vectors | `.shp/.dxf/.gpkg` | `from_class`, `scale`, `major_spacing`, `basic_spacing`, `minor_spacing` |
| DSM | `terrain_analysis-generate_general_dsm_from_pointcloud` | `.lidata` | Raster | `x_size`, `y_size`, `interpolator`, `fill_holes` |
| DEM | `terrain_analysis-generate_general_dem_from_pointcloud` | `.lidata` | Raster | `from_class`, `x_size`, `y_size`, `interpolator`, `fill_holes` |
| CHM | `terrain_analysis-generate_chm` | DEM + DSM | Raster | Ensure DEM and DSM are fully aligned |
| DOM | `terrain_analysis-generate_dom_by_pixel_mode` | Image project + DSM/DEM | Raster | `resolution_mode`, `auto_gsd`, `manual_gsd` |
| Slope | `terrain_analysis-slope_analysis` | DEM | Raster | `z_scale` |
| Aspect | `terrain_analysis-aspect_analysis` | DEM | Raster | - |
| Roughness | `terrain_analysis-roughness_analysis` | DEM | Raster | - |
| Hillshade | `terrain_analysis-generate_hill_shade` | DEM | Raster | `azimuth`, `altitude`, `z_scales` |
| Sky View Factor | `terrain_analysis-sky_view_factor` | DEM | Raster | `max_radius` |
| Viewshed | `terrain_analysis-viewshed_analysis` | DEM + observer points | Raster | `observer_height`, `target_height` |
| Annual Insolation | `terrain_analysis-annual_insolation` | DEM | Raster | `latitude`, `start_month`, `end_month` |
| Solar Radiation | `terrain_analysis-solar_radiation` | DEM | Raster | `latitude`, `day_of_year`, `hour` |
| Drainage Analysis | `terrain_analysis-drainage_analysis` | DEM | Raster | `threshold` |
| Flood Analysis | `terrain_analysis-flooding_analysis` | DEM + river centerline | Raster | `flood_level` |
| Relative Elevation | `terrain_analysis-generate_relative_elevation_model` | DEM + river centerline | Raster | `sample_distance` |

### from_class Configuration Recommendations

| Product | Recommended Class | Description |
|-----|---------|------|
| TIN | `[2]` or `null` | Ground points recommended for terrain TIN; can leave unrestricted to preserve full-point detail |
| Contours | `[2]` | Standard terrain contours should use ground points |
| DSM | `null` | DSM represents surfaces; typically no class restriction |
| DEM | `[2]` | DEM should use ground points |

### Interpolation Method (interpolator)

| Value | Method | Applicable Scenario |
|---|------|---------|
| 0 | IDW | Fast generation, standard precision, Model Builder default |
| 1 | Kriging | Smoother, higher precision requirements |
| 2 | TIN | Preserves terrain details, obvious features like slope edges |

### Common Class Codes

| Class | Meaning | Usage |
|-----|------|------|
| 1 | Unclassified | Raw/unprocessed points |
| 2 | Ground | Main input for DEM, TIN, contours |
| 3/4/5 | Low/Medium/High Vegetation | Can be retained for DSM surface analysis |
| 6 | Building | Can be retained for DSM surface analysis |
| 38 | Road | Urban terrain/feature analysis |

---

## Common Issues and Solutions

### Issue 1: DEM or Contours Contain Building/Vegetation Noise

**Possible causes**:
- Insufficient ground point classification
- `from_class` not restricted to ground points during DEM/contour generation
- Denoising and smoothing parameters not suitable for current point density

**Solutions**:
- Check and correct class 2 ground points
- Set `from_class: [2]` in DEM/contour tools
- Adjust `scene_type`, `iteration_angle`, `iteration_distance`, and tolerance parameters for ground classification based on terrain relief

### Issue 2: TIN Has Elongated Triangle Edges or Crosses Voids

**Possible causes**:
- `max_triangle_edge` set too large
- Point cloud voids or over-resampling
- No breaklines/boundary constraints used

**Solutions**:
- Reduce `max_triangle_edge`
- Lower resampling ratio or increase point cloud density
- Use `breakline_file` or ROI to control boundaries

### Issue 3: DSM/DEM Raster Has Voids

**Possible causes**:
- Insufficient point density
- Resolution `x_size/y_size` set too small
- Insufficient interpolation neighborhood parameters

**Solutions**:
- Keep `fill_holes: true`
- Appropriately increase `x_size/y_size`
- Increase `number_of_points` or `distance`

### Issue 4: Contours Too Jagged or Over-Smoothed

**Possible causes**:
- Smoothing iterations and simplification distance not set appropriately
- Original point cloud has significant noise
- Contour interval does not match data precision

**Solutions**:
- When jagged, increase `terrain_smooth_iter` or `mean_smooth_k`
- When over-smoothed, reduce `smooth_span`, `simply_dist`
- Adjust `major_spacing/basic_spacing/minor_spacing` based on scale and terrain relief

---

## Related Documentation

- Tool registry: `references/terrain/tools.md`
- Preflight checks: `references/terrain/preflight_checks.md`
- Typical examples: `references/terrain/examples.md`
