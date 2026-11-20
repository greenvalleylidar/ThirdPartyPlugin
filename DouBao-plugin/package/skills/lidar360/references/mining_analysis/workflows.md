# Mining Analysis Workflows

> Organized based on LiDAR360 Model Builder `PointCloud - Extract Toes and Crests Workflow.LiModelBuilder`. This workflow starts from point cloud preprocessing, generates TIN/OBJ mesh models, and then extracts slope top lines and toe lines of the mine.

---

## Workflow Overview

| Scenario | Recommended Workflow | Key Tools | Difficulty |
|-----|---------|---------|------|
| Point cloud extraction of slope top/toe lines | Denoise -> Resample -> Smooth -> Ground classification -> TIN -> Model smooth -> Extract toes and crests | `extract_toes_and_crests` | Medium |
| Extract slope lines from existing OBJ/LiTin | OBJ/LiTin -> Optional model smoothing -> Extract toes and crests | `extract_toes_and_crests` | Low |
| Point cloud to slope TIN | Point cloud preprocessing -> Ground classification -> Generate TIN | `terrain_analysis-point_cloud_to_tin` | Medium |
| Mining surface reconstruction | Point cloud denoising/clipping -> Surface reconstruction -> OBJ/3D Tiles | `surface_reconstruction` | Medium |
| Tunnel analysis | Tunnel point extraction/cleanup -> Centerline extraction -> Normal vector computation | Tunnel toolset | Medium |

---

## Model Builder Reference Workflow

```text
Point Cloud File
  -> Outlier Removal
  -> Resampling
  -> Point Cloud Smoothing
  -> Classify Ground Points by Triangulation
  -> Generate TIN
  -> Model Smoothing
  -> Extract Toes and Crests
```

**Output**: Slope top line/toe line vectors, supporting `.dxf` or `.shp`.

**Key connections**:

| Upstream | Downstream | Description |
|-----|------|------|
| `pointcloud_outlier_removal.output_data` | `pointcloud_subsampling.input_data` | Denoising result feeds into resampling |
| `pointcloud_subsampling.output_data` | `pointcloud_smooth.input_data` | Resampling result feeds into point cloud smoothing |
| `pointcloud_smooth.output_data` | `classify_ground_by_progressive_tin_densification.input_data` | Smoothed point cloud used for ground classification |
| `classify_ground_by_progressive_tin_densification.input_data` | `point_cloud_to_tin.input_data.input_pointcloud` | Ground classification result used for TIN generation |
| `point_cloud_to_tin.output_data` | `smooth_meshes.input_data` | TIN/mesh feeds into model smoothing |
| `smooth_meshes.output_data` | `extract_toes_and_crests.input_data` | Smoothed mesh used for slope top/toe line extraction |

---

## Workflow 1: Point Cloud Extraction of Slope Top and Toe Lines

**Applicable scenario**: Automatically generate slope triangulated network from mining area point cloud and extract slope top lines and toe lines.

**Workflow diagram**:

```text
Point Cloud -> Denoise -> Resample -> Smooth -> Ground Classification -> TIN -> Model Smooth -> Slope Top/Toe Lines
```

### Step 1: Point Cloud Denoising

```json
{
  "step": 1,
  "description": "Point cloud denoising",
  "tool": "pointcloud_processing-pointcloud_outlier_removal",
  "input": {
    "input_data": ["/data/mine_raw.lidata"],
    "output_data": "/output/denoised.lidata",
    "neighbor_points": 10,
    "multiples_of_std_deviation": 5
  }
}
```

### Step 2: Resampling

```json
{
  "step": 2,
  "description": "Point cloud resampling",
  "tool": "pointcloud_processing-pointcloud_subsampling",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "output_data": "/output/subsampled",
    "sampling_type": 1,
    "from_class": [0, 1, 2, 3, 4, 5, 6],
    "sampling_rate": 50,
    "minimum_points_spacing": 0,
    "octree": 21
  }
}
```

### Step 3: Point Cloud Smoothing

```json
{
  "step": 3,
  "description": "Point cloud smoothing",
  "tool": "pointcloud_processing-pointcloud_smooth",
  "input": {
    "input_data": "{{step2.data.output_data}}",
    "output_data": "/output/smoothed",
    "smoothing_type": 0,
    "search_radius": 0.2,
    "max_fix_distance": 0.1,
    "select_class": [0, 1, 2, 3, 4, 5, 6]
  }
}
```

### Step 4: Ground Point Classification

```json
{
  "step": 4,
  "description": "Ground point classification (progressive TIN densification)",
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

### Step 5: Generate TIN

```json
{
  "step": 5,
  "description": "Generate TIN",
  "tool": "terrain_analysis-point_cloud_to_tin",
  "input": {
    "input_data": {
      "input_pointcloud": "{{step4.data.output_data}}",
      "breakline_file": null
    },
    "output_data": "/output/mine_slope.litin",
    "from_class": null,
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

> If the target is bare mining slope, `from_class` can typically be set to `[2]` to use ground points; if keeping all points better represents terraces, retaining walls, or local facilities, keep it as `null`, but check for interference from non-ground points on slope lines.

### Step 6: Model Smoothing

```json
{
  "step": 6,
  "description": "Model smoothing",
  "tool": "model_data_processing-smooth_meshes",
  "input": {
    "input_data": "{{step5.data.output_data}}",
    "output_data": "/output/mine_slope_smooth.obj",
    "smooth_iterations": 5
  }
}
```

### Step 7: Extract Slope Top and Toe Lines

```json
{
  "step": 7,
  "description": "Extract slope top and toe lines",
  "tool": "mining_analysis-extract_toes_and_crests",
  "input": {
    "input_data": ["{{step6.data.output_data}}"],
    "output_data": "/output/toes_crests.dxf",
    "min_slope_angle": 20,
    "max_slope_angle": 70,
    "min_length": 10,
    "save_format": 0
  }
}
```

**Parameter recommendations**:

| Parameter | Model Builder Default | Description |
|-----|----------------------|------|
| `min_slope_angle` | 20 | Surfaces below this slope angle are not considered slope candidates; can filter platforms and gentle slopes |
| `max_slope_angle` | 70 | Surfaces above this slope angle can be considered anomalous or vertical noise |
| `min_length` | 10 | Remove short line fragments; unit is typically meters |
| `save_format` | 0 | `0` outputs DXF, `1` outputs SHP |

---

## Workflow 2: Extract Slope Top and Toe Lines from Existing OBJ/LiTin

**Applicable scenario**: Already have a mining slope mesh model, only need to extract slope top lines and toe lines.

```text
OBJ/LiTin -> Optional model smoothing -> extract_toes_and_crests -> DXF/SHP
```

```json
{
  "step": 1,
  "description": "Extract slope top and toe lines",
  "tool": "mining_analysis-extract_toes_and_crests",
  "input": {
    "input_data": ["/data/mine_slope.obj"],
    "output_data": "/output/toes_crests.shp",
    "min_slope_angle": 20,
    "max_slope_angle": 70,
    "min_length": 10,
    "save_format": 1
  }
}
```

---

## Workflow 3: Tunnel Point Cloud Cleanup and Centerline Analysis

**Applicable scenario**: Underground roadway or tunnel point cloud, clean noise along the centerline and extract the centerline.

**Workflow diagram**:

```text
Point Cloud -> Denoise/Clip -> Surface Reconstruction (OBJ) -> Extract Centerline -> Centerline Vector
Point Cloud -> Normal Vector Computation -> Normal Vector Attribute Point Cloud
```

### Step 1: Point Cloud Denoising

```json
{
  "step": 1,
  "description": "Tunnel point cloud denoising",
  "tool": "pointcloud_processing-pointcloud_outlier_removal",
  "input": {
    "input_data": ["/data/tunnel_raw.lidata"],
    "output_data": "/output/tunnel_denoised.lidata",
    "neighbor_points": 10,
    "multiples_of_std_deviation": 5
  }
}
```

### Step 2: Surface Reconstruction

```json
{
  "step": 2,
  "description": "Tunnel surface reconstruction",
  "tool": "mining_analysis-surface_reconstruction",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "output_data": "/output/tunnel_surface.obj",
    "export_format": 1,
    "node_size": 32768,
    "minimum_perimeter_of_hole": 10,
    "remove_small_components": true
  }
}
```

### Step 3: Extract Tunnel Centerline

```json
{
  "step": 3,
  "description": "Extract tunnel centerline",
  "tool": "mining_analysis-extract_tunnel_centerline",
  "input": {
    "input_data": "{{step2.data.output_data}}",
    "output_data": "/output/tunnel_centerline.dxf",
    "position": 1,
    "speed_quality": 0.1
  }
}
```

### Step 4: Normal Vector Computation

```json
{
  "step": 4,
  "description": "Compute roadway point cloud normal vectors",
  "tool": "mining_analysis-compute_normal_vectors",
  "input": {
    "input_data": ["{{step1.data.output_data}}"],
    "search_radius": 0.5,
    "orientation": false
  }
}
```

> **Parameter recommendations**:
> - `position`: 0=top line, 1=middle line, 2=bottom line; select based on analysis requirements
> - `speed_quality`: 0.1 is the default balanced value; increasing improves speed but reduces quality
> - `search_radius`: Recommended to set as 5 times the average point spacing

---

## Workflow 4: Mining Surface Reconstruction

**Applicable scenario**: Quickly generate 3D surface models (OBJ or 3D Tiles) from mining area point cloud.

**Workflow diagram**:

```text
Point Cloud -> Denoise/Clip -> Surface Reconstruction -> OBJ/3D Tiles
```

### Step 1: Point Cloud Denoising

```json
{
  "step": 1,
  "description": "Point cloud denoising",
  "tool": "pointcloud_processing-pointcloud_outlier_removal",
  "input": {
    "input_data": ["/data/mine_raw.lidata"],
    "output_data": "/output/mine_denoised.lidata",
    "neighbor_points": 10,
    "multiples_of_std_deviation": 5
  }
}
```

### Step 2: Surface Reconstruction

```json
{
  "step": 2,
  "description": "Mining surface reconstruction",
  "tool": "mining_analysis-surface_reconstruction",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "output_data": "/output/mine_surface.obj",
    "export_format": 1,
    "calculate_vertex_colors": true,
    "node_size": 32768,
    "minimum_perimeter_of_hole": 10,
    "remove_small_components": true
  }
}
```

> **Parameter recommendations**:
> - `export_format`: 0=3D Tiles, 1=OBJ
> - `calculate_vertex_colors`: Preserve original point cloud color as model vertex color
> - `minimum_perimeter_of_hole`: Holes smaller than this value are automatically filled (meters)

---

## Parameter Quick Reference

### Slope Line Extraction Thresholds

| Scenario | `min_slope_angle` | `max_slope_angle` | `min_length` |
|-----|-------------------|-------------------|--------------|
| Conventional open-pit mine slope | 20 | 70 | 10 |
| Weak terrace boundaries, gentler slope face | 12-18 | 65-75 | 5-10 |
| Steep rock walls or high slopes | 25-35 | 80 | 10-20 |
| Too many output fragments | Increase | Maintain or decrease | Increase |
| Missing slope toe/top | Decrease | Increase | Decrease |

### Output Format

| `save_format` | Output | Applicable Scenario |
|---|------|---------|
| 0 | DXF | CAD drafting, mine survey result exchange |
| 1 | SHP | GIS analysis, spatial database import |

---

## Common Issues

| Issue | Possible Cause | Recommended Action |
|-----|---------|---------|
| Too many slope line fragments | TIN noise, `min_length` too small, model not smoothed | Increase model smoothing iterations, raise `min_length` |
| Missing slope top line | `min_slope_angle` too high or TIN over-smoothed | Lower minimum slope angle, reduce smoothing iterations |
| Slope line deviates from real terraces | Point cloud smoothing/resampling excessive, or ground classification errors | Reduce resampling ratio, check ground class and TIN |
| Empty output | Input is not a valid OBJ/LiTin, slope thresholds do not match | Check model file and widen slope range |
| SHP/DXF coordinates abnormal | Input model coordinate system or units incorrect | Check TIN/OBJ source and coordinate units |

---

## Related Documentation

- Tool registry: `references/mining_analysis/tools.md`
- Preflight checks: `references/mining_analysis/preflight_checks.md`
- Typical examples: `references/mining_analysis/examples.md`
