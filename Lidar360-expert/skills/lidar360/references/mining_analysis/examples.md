# Mining Analysis Typical Examples

## Example 1: Point Cloud Extraction of Slope Top and Toe Lines Workflow

```text
Step 1: Point cloud denoising -> pointcloud_processing-pointcloud_outlier_removal (neighbor_points=10, multiples_of_std_deviation=5)
Step 2: Resampling -> pointcloud_processing-pointcloud_subsampling (sampling_rate=50, octree=21)
Step 3: Point cloud smoothing -> pointcloud_processing-pointcloud_smooth (search_radius=0.2, max_fix_distance=0.1)
Step 4: Ground point classification -> pointcloud_classification-classify_ground_by_progressive_tin_densification (grid_size=20, to_class=2, scene_type=2)
Step 5: Generate TIN -> terrain_analysis-point_cloud_to_tin (max_triangle_edge=30, buffer_size=10)
Step 6: Model smoothing -> model_data_processing-smooth_meshes (smooth_iterations=5)
Step 7: Extract slope top and toe lines -> mining_analysis-extract_toes_and_crests (min_slope_angle=20, max_slope_angle=70, min_length=10, save_format=0)
```

**Prerequisite**: LiData point cloud loaded, mine slope area is complete, coordinate and elevation units are correct.
**Output**: Slope top line/toe line vector file, DXF or SHP.

---

## Example 2: Extract Slope Top and Toe Lines from Existing OBJ/LiTin

```text
Step 1: Load OBJ or LiTin triangulated network model
Step 2: Optional model smoothing -> model_data_processing-smooth_meshes (smooth_iterations=5)
Step 3: Extract slope top and toe lines -> mining_analysis-extract_toes_and_crests (min_slope_angle=20, max_slope_angle=70, min_length=10)
```

**Prerequisite**: The triangulated network model can represent real slope terraces, without large-area voids or abnormal spikes.
**Output**: Slope top line/toe line vector file.

---

## Example 3: Large-Scale Surface Reconstruction Workflow for Mining Area

```text
Step 1: Load mining area point cloud -> platform-load_layer
Step 2: Point cloud denoising -> pointcloud_processing-pointcloud_outlier_removal
Step 3: Select classes for modeling -> mining_analysis-surface_reconstruction
Step 4: Output OBJ or 3D Tiles results
```

**Prerequisite**: Point cloud preprocessing is complete, `select_class` has been confirmed.
**Output**: OBJ model or 3D Tiles 1.1 model.

---

## Example 4: Tunnel Centerline and Normal Vector Analysis Workflow

```text
Step 1: Load roadway point cloud and center axis -> platform-load_layer
Step 2: Extract roadway centerline from OBJ model -> mining_analysis-extract_tunnel_centerline
Step 3: Compute roadway normal vector attributes -> mining_analysis-compute_normal_vectors
```

**Prerequisite**: LiData roadway point cloud loaded; if point cloud cleanup is performed, the center axis vector file is required.
**Output**: Denoised roadway point cloud, centerline vector, normal vector attributes.

---

## Example 5: Local High-Precision Surface Reconstruction Workflow

```text
Step 1: Clip target area point cloud -> pointcloud_processing-clip_by_polygon
Step 2: Compute normal vectors with consistent orientation -> mining_analysis-compute_normal_vectors
Step 3: Surface modeling to generate OBJ model -> mining_analysis-surface_reconstruction
Step 4: Optional model smoothing -> model_data_processing-smooth_meshes
```

**Prerequisite**: Input point cloud is LiData, point cloud density is relatively uniform; complete denoising and clipping if necessary.
**Output**: OBJ triangulated network model.

---

## Recommended Parameter Quick Reference

| Scenario | Recommended Tool | Key Parameters |
|-----|---------|---------|
| Slope top/toe line extraction | extract_toes_and_crests | min_slope_angle=20, max_slope_angle=70, min_length=10, save_format=0 |
| Too many slope line fragments | extract_toes_and_crests | Increase min_length, appropriately increase smooth_iterations |
| Missing gentle slope terraces | extract_toes_and_crests | Lower min_slope_angle, lower min_length |
| TIN has overly long triangle edges | point_cloud_to_tin | Lower max_triangle_edge |
| Obvious model noise | smooth_meshes | Start with smooth_iterations=5, adjust gradually |
| Roadway centerline | extract_tunnel_centerline | position 0/1/2, speed_quality controls speed-quality balance |
| Normal vector attributes | compute_normal_vectors | search_radius approximately several times the average point spacing |

---

## Tool Usage Order Recommendations

| Analysis Goal | Recommended Order |
|---------|---------|
| Point cloud extraction of slope top/toe lines | pointcloud_outlier_removal -> pointcloud_subsampling -> pointcloud_smooth -> classify_ground_by_progressive_tin_densification -> point_cloud_to_tin -> smooth_meshes -> extract_toes_and_crests |
| Extract slope lines from existing model | smooth_meshes -> extract_toes_and_crests |
| Large-scale mining area modeling | pointcloud_outlier_removal -> surface_reconstruction |
| Local high-precision model | clip_by_polygon -> compute_normal_vectors -> surface_reconstruction |

> For detailed workflows, see `references/mining_analysis/workflows.md`; for pre-execution checks, see `references/mining_analysis/preflight_checks.md`.
