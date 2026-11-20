# Typical Workflow Examples

## Example 1: Point Cloud to DEM Generation Workflow

```
Step 1: Point cloud smoothing -> pointcloud_processing-pointcloud_smooth (search_radius=0.2, max_fix_distance=0.1)
Step 2: Resampling -> pointcloud_processing-pointcloud_subsampling (sampling_rate=50, octree=21)
Step 3: Denoising -> pointcloud_processing-pointcloud_outlier_removal (neighbor_points=10, multiples_of_std_deviation=5)
Step 4: Ground point classification -> pointcloud_classification-classify_ground_by_progressive_tin_densification (grid_size=20, to_class=2, scene_type=2)
Step 5: Generate DEM -> terrain_analysis-generate_general_dem_from_pointcloud (x_size, y_size, interpolator, buffer determined by data and scenario)
```

**Prerequisite**: Point cloud loaded
**Output**: DEM raster file (*.tif, *.tiff, *.img, *.dat, *.asc)

---

## Example 2: Point Cloud to DSM Generation Workflow

```
Step 1: Point cloud smoothing -> pointcloud_processing-pointcloud_smooth (search_radius=0.2, max_fix_distance=0.1)
Step 2: Resampling -> pointcloud_processing-pointcloud_subsampling (sampling_rate=50, octree=21)
Step 3: Denoising -> pointcloud_processing-pointcloud_outlier_removal (neighbor_points=10, multiples_of_std_deviation=5)
Step 4: Generate DSM -> terrain_analysis-generate_general_dsm_from_pointcloud (x_size, y_size, buffer determined by data and scenario)
```

**Prerequisite**: Point cloud loaded
**Output**: DSM raster file (*.tif, *.tiff, *.img, *.dat, *.asc)

---

## Example 3: Point Cloud to Contour Generation Workflow

```
Step 1: Point cloud smoothing -> pointcloud_processing-pointcloud_smooth (search_radius=0.2, max_fix_distance=0.1)
Step 2: Resampling -> pointcloud_processing-pointcloud_subsampling (sampling_rate=50, octree=21)
Step 3: Denoising -> pointcloud_processing-pointcloud_outlier_removal (neighbor_points=10, multiples_of_std_deviation=5)
Step 4: Ground point classification -> pointcloud_classification-classify_ground_by_progressive_tin_densification (grid_size=20, to_class=2, scene_type=2)
Step 5: Generate contours -> terrain_analysis-generate_contour_from_pointcloud (from_class=2, max_triangle_length=30)
```

**Prerequisite**: Point cloud loaded
**Output**: Contour vector file (*.shp, *.dxf, *.gpkg)

---

## Example 4: Point Cloud to TIN Generation Workflow

```
Step 1: Point cloud smoothing -> pointcloud_processing-pointcloud_smooth (search_radius=0.2, max_fix_distance=0.1)
Step 2: Resampling -> pointcloud_processing-pointcloud_subsampling (sampling_rate=50, octree=21)
Step 3: Denoising -> pointcloud_processing-pointcloud_outlier_removal (neighbor_points=10, multiples_of_std_deviation=5)
Step 4: Ground point classification -> pointcloud_classification-classify_ground_by_progressive_tin_densification (grid_size=20, to_class=2, scene_type=2)
Step 5: Generate TIN -> terrain_analysis-point_cloud_to_tin (max_triangle_edge=30, buffer_size=10)
```

**Prerequisite**: Point cloud loaded
**Output**: TIN file (*.litin or *.json)

---

## Example 5: Canopy Height Model Generation Workflow

```
Step 1: Generate DEM -> terrain_analysis-generate_general_dem_from_pointcloud (refer to Example 1)
Step 2: Generate DSM -> terrain_analysis-generate_general_dsm_from_pointcloud (refer to Example 2)
Step 3: Generate CHM -> terrain_analysis-generate_chm
```

**Prerequisite**: DEM and DSM generated with identical resolution, coordinate system, and extent
**Output**: CHM raster file (*.tif, *.tiff, *.img, *.dat)

---

## Example 6: Digital Orthophoto (DOM) Generation Workflow

```
Step 1: Image alignment -> imagery_processing-image_alignment (imagery_processing module)
Step 2: Generate DSM -> terrain_analysis-generate_general_dsm_from_pointcloud (refer to Example 2)
Step 3: Generate DOM -> terrain_analysis-generate_dom_by_pixel_mode
```

**Prerequisite**: Image project aligned + DSM generated
**Output**: DOM raster file (*.tif, *.tiff, *.img)

---

## Example 7: Terrain Derivative Analysis Workflow

```
Step 1: Slope analysis -> terrain_analysis-slope_analysis
Step 2: Aspect analysis -> terrain_analysis-aspect_analysis
Step 3: Roughness analysis -> terrain_analysis-roughness_analysis
Step 4: Hillshade generation -> terrain_analysis-generate_hill_shade
```

**Prerequisite**: DEM generated
**Output**: Multiple terrain derivative product raster files

---

## Example 8: Viewshed Analysis Workflow

```
Step 1: Prepare observer point vector -> Create observer point vector file (shp/gpkg)
Step 2: Viewshed analysis -> terrain_analysis-viewshed_analysis
```

**Prerequisite**: DEM + observer point vector
**Output**: Viewshed raster file

---

## Example 9: Hydrological Analysis Workflow

```
Step 1: Drainage analysis -> terrain_analysis-drainage_analysis
Step 2: Flood inundation analysis -> terrain_analysis-flooding_analysis
Step 3: Generate relative elevation model -> terrain_analysis-generate_relative_elevation_model (sample_distance=10)
```

**Prerequisite**: DEM + river centerline vector
**Output**: Hydrological analysis result raster file

---

## Recommended Parameter Quick Reference

| Scenario | DEM Resolution | Contour Scale | Contour Interval |
|-----|----------|------------|-------|
| Building design | 0.3m | 1:500 | 0.5m |
| Urban planning | 0.5-1m | 1:1000 | 1m |
| Engineering survey | 1m | 1:2000 | 2m |
| Forestry survey | 2-3m | 1:10000 | 5m |
| Provincial planning | 5-10m | 1:50000 | 20m |

> For detailed configuration, see `terrain-scale-profiles.yaml`

> **Invocation constraint**: Before generating DEM/DSM, follow the "Parameter Confirmation Gate" in `terrain_analysis_SKILL.md`: ask the user for the scenario and display the table above. The values are recommendations; `x_size`/`y_size` in documentation examples are illustrative only and must not be copied directly, and schema defaults (0.3 m) must not replace the scenario confirmation.

## Tool Parameter Descriptions

### Point Cloud Preprocessing Parameters
- **pointcloud_smooth**: search_radius=0.2m, max_fix_distance=0.1m
- **pointcloud_subsampling**: sampling_rate=50%, octree=21
- **pointcloud_outlier_removal**: neighbor_points=10, multiples_of_std_deviation=5

### Ground Point Classification Parameters
- **classify_ground_by_progressive_tin_densification**: grid_size=20m, to_class=2, scene_type=2, iteration_angle=8, iteration_distance=1.2

### Terrain Model Generation Parameters
- **generate_general_dem_from_pointcloud**: x_size, y_size, interpolator, buffer determined by data and scenario
- **generate_general_dsm_from_pointcloud**: x_size, y_size, buffer determined by data and scenario
- **generate_contour_from_pointcloud**: from_class=2, max_triangle_length=30m
- **point_cloud_to_tin**: max_triangle_edge=30m, buffer_size=10m, free_size_spikefree=1, buffer_size_spikefree=0.5
