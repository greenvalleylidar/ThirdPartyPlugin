# Typical Workflow Examples

## Example 1: Standard Point Cloud Preprocessing Workflow

```
Step 1: Load point cloud -> platform-load_layer
Step 2: Denoise -> pointcloud_processing-pointcloud_outlier_removal (neighbor_points=10)
Step 3: Noise filtering -> pointcloud_processing-pointcloud_noise_filter
Step 4: Smooth -> pointcloud_processing-pointcloud_smooth (search_radius=0.2)
```

**Prerequisite**: Point cloud loaded
**Output**: Cleaned high-quality point cloud

---

## Example 2: Normalization Workflow

```
Step 1: Ground point classification -> pointcloud_classification-classify_ground_by_progressive_tin_densification
Step 2: Normalize -> pointcloud_processing-normalize_by_ground_points
Step 3: (Subsequent) Forestry analysis -> forestry_airborne-individual_tree_segmentation
Step 4: (After completion) Denormalize -> pointcloud_processing-denormalize
```

**Prerequisite**: Ground point classification completed
**Output**: Normalized point cloud (Z=relative height)

---

## Example 3: Point Cloud Clipping and Tiling Workflow

```
Step 1: Load point cloud -> platform-load_layer
Step 2: Load vector boundary -> platform-load_layer (shp)
Step 3: Polygon clipping -> pointcloud_processing-clip_by_polygon
Step 4: Range tiling -> pointcloud_processing-tile_by_range (width=200, length=200)
```

**Prerequisite**: Point cloud + vector boundary loaded
**Output**: Tiled point cloud file set

---

## Example 4: Extract Specific Objects by Class

```
Step 1: Load classified point cloud -> platform-load_layer
Step 2: Extract buildings -> pointcloud_processing-extract_pointcloud_by_class (from_class=[6])
Step 3: Extract vegetation -> pointcloud_processing-extract_pointcloud_by_class (from_class=[3,4,5])
Step 4: Merge extracted results -> pointcloud_processing-pointcloud_merge
```

**Prerequisite**: Point cloud classified
**Output**: Per-class point cloud files

---

## Example 5: Point Cloud Colorization Workflow

```
Step 1: Load point cloud -> platform-load_layer
Step 2: Load orthophoto -> platform-load_layer (tif)
Step 3: Colorize from orthophoto -> pointcloud_processing-extract_color_from_ortho_image
Step 4: Brightness/contrast adjustment -> pointcloud_processing-brightness_contrast (brightness=10)
```

**Prerequisite**: Point cloud + orthophoto loaded with overlapping extent
**Output**: True-color point cloud

---

## Example 6: Point Cloud Subsampling Workflow

```
Step 1: Load point cloud -> platform-load_layer
Step 2: Subsampling -> pointcloud_processing-pointcloud_subsampling (sampling_rate=50)
```

**Prerequisite**: Point cloud loaded
**Output**: Subsampled point cloud

### Different Sampling Method Configurations

#### Minimum Point Spacing Sampling

```
Step 1: Load point cloud -> platform-load_layer
Step 2: Minimum spacing subsampling -> pointcloud_processing-pointcloud_subsampling (sampling_type=0, minimum_points_spacing=0.05)
```

**Call example**:
```
pointcloud_processing-pointcloud_subsampling
Parameters:
  input_data: "/data/point_cloud.lidata"
  output_data: "/output/subsampled_min_dist.lidata"
  sampling_type: 0        # 0=Minimum point spacing
  minimum_points_spacing: 0.05  # Minimum spacing 0.05m
```

**Applicable**: Scenarios with uneven point density requiring precise density control

---

#### Sampling Rate Subsampling

```
Step 1: Load high-density point cloud -> platform-load_layer
Step 2: Subsample by percentage -> pointcloud_processing-pointcloud_subsampling (sampling_type=1, sampling_rate=30)
```

**Call example**:
```
pointcloud_processing-pointcloud_subsampling
Parameters:
  input_data: "/data/dense_cloud.lidata"
  output_data: "/output/subsampled_rate.lidata"
  sampling_type: 1        # 1=Sampling rate
  sampling_rate: 30       # Retain 30% of points
```

**Applicable**: Fast downsampling of massive data

---

#### Octree Subsampling

```
Step 1: Load point cloud -> platform-load_layer
Step 2: Octree subsampling -> pointcloud_processing-pointcloud_subsampling (sampling_type=2, octree=18)
```

**Call example**:
```
pointcloud_processing-pointcloud_subsampling
Parameters:
  input_data: "/data/point_cloud.lidata"
  output_data: "/output/subsampled_octree.lidata"
  sampling_type: 2        # 2=Octree
  octree: 18              # Octree level (1-21), lower values retain fewer points
```

**Applicable**: Structured downsampling, preserving point cloud spatial distribution

---

## Example 7: Point Cloud Merging Workflow

```
Step 1: Load multiple point cloud tiles -> platform-load_layer (multiple lidata)
Step 2: Merge point clouds -> pointcloud_processing-pointcloud_merge
```

**Prerequisite**: Multiple point clouds loaded in the same coordinate system
**Output**: Merged point cloud

---

## Example 8: Vegetation Index Calculation Workflow

```
Step 1: Load point cloud -> platform-load_layer (with NIR attributes)
Step 2: Calculate NDVI -> pointcloud_processing-pointcloud_vegetation_index (index_type=0)
Step 3: Filter by NDVI -> pointcloud_processing-segment_by_attribute (optional)
```

**Prerequisite**: Point cloud contains NIR+R attributes
**Output**: Point cloud with NDVI additional attribute

---

## Example 9: Boundary Extraction Workflow

### Basic Boundary Extraction (Convex Hull)

```
Step 1: Load point cloud -> platform-load_layer
Step 2: Extract boundary -> pointcloud_processing-pointcloud_extract_boundary
```

**Call example**:
```
pointcloud_processing-pointcloud_extract_boundary
Parameters:
  input_data: ["/data/point_cloud.lidata"]
  output_data: "/output/boundary"
  boundary_method: 1  # 0=Convex hull, 1=Convex polygon, 2=Concave polygon
  from_class: [0, 1, 2, 3, 4, 5, 6]
  export: 0  # 0=Single file, 1=Multiple files
  suffix: "shp"
```

**Prerequisite**: Point cloud loaded
**Output**: Point cloud boundary vector (shp/gpkg/dxf)

---

### Hexagonal Grid Boundary Extraction

```
Step 1: Load point cloud -> platform-load_layer
Step 2: Extract hexagonal boundary -> pointcloud_processing-pointcloud_extract_boundary
```

**Call example**:
```
pointcloud_processing-pointcloud_extract_boundary
Parameters:
  input_data: ["/data/point_cloud.lidata"]
  output_data: "/output/hexagon_boundary"
  boundary_method: 0  # Convex hull
  from_class: [2]
  extraction_hexagon_height: 10
  minimum_number_of_points: 10
  export: 0
  suffix: "shp"
```

**Output**: Hexagonal grid boundary vector file

---

### Concave Hull Boundary Extraction (for Irregular Shapes)

```
Step 1: Load point cloud -> platform-load_layer
Step 2: Extract concave hull boundary -> pointcloud_processing-pointcloud_extract_boundary
```

**Call example**:
```
pointcloud_processing-pointcloud_extract_boundary
Parameters:
  input_data: ["/data/point_cloud.lidata"]
  output_data: "/output/concave_boundary"
  boundary_method: 2  # Concave polygon
  from_class: [0, 1, 2, 3, 4, 5]
  max_edge_length: 2.0
  export: 1
  suffix: "gpkg"
```

**Output**: Concave hull boundary vector file (multiple files)

---

## Example 10: Point Cloud Smoothing Workflow

### Basic Smoothing

```
Step 1: Load point cloud -> platform-load_layer
Step 2: Denoise -> pointcloud_processing-pointcloud_outlier_removal
Step 3: Smooth -> pointcloud_processing-pointcloud_smooth
```

**Call example**:
```
pointcloud_processing-pointcloud_smooth
Parameters:
  input_data: ["/data/point_cloud.lidata"]
  output_data: "/output/smoothed.lidata"
  select_class: [0, 1, 2, 3, 4, 5, 6]
  max_fix_distance: 0.1
  search_radius: 0.2
  smoothing_type: 0  # 0=XYZ, 1=Elevation
  smooth_for_multi_cloud: false
```

**Prerequisite**: Point cloud loaded, denoising completed
**Output**: Smoothed point cloud file

---

### Elevation Smoothing (Z-value Only)

```
Step 1: Load point cloud -> platform-load_layer
Step 2: Elevation smoothing -> pointcloud_processing-pointcloud_smooth
```

**Call example**:
```
pointcloud_processing-pointcloud_smooth
Parameters:
  input_data: ["/data/point_cloud.lidata"]
  output_data: "/output/smoothed_elevation.lidata"
  select_class: [2]  # Only smooth ground points
  max_fix_distance: 0.05
  search_radius: 0.3
  smoothing_type: 1  # Elevation smoothing
```

**Output**: Point cloud file with only Z-values adjusted

---

### Multi-Overlap Point Cloud Smoothing

```
Step 1: Load multiple overlapping point clouds -> platform-load_layer (multiple lidata)
Step 2: Simultaneously smooth overlapping point clouds -> pointcloud_processing-pointcloud_smooth
```

**Call example**:
```
pointcloud_processing-pointcloud_smooth
Parameters:
  input_data: ["/data/cloud1.lidata", "/data/cloud2.lidata"]
  output_data: "/output/smoothed_multi.lidata"
  select_class: [0, 1, 2, 3, 4, 5]
  max_fix_distance: 0.15
  search_radius: 0.25
  smoothing_type: 0
  smooth_for_multi_cloud: true
```

**Output**: Simultaneously smoothed overlapping point cloud

---

## Example 11: Spatial Clustering Segmentation Workflow

### Basic 2D Clustering

```
Step 1: Load point cloud -> platform-load_layer
Step 2: Spatial clustering -> pointcloud_processing-segment_by_attribute
```

**Call example**:
```
pointcloud_processing-segment_by_attribute
Parameters:
  input_data: "/data/point_cloud.lidata"
  output_data: "/output/segments"
  search_radius: 0.5
  dimension: 2  # 2D clustering (X-Y distance only)
  from_class: [0, 1, 2, 3, 4, 5]
  use_min_cluster_pts: true
  min_cluster_pts: 10
  use_max_cluster_pts: false
  use_min_area_threshold: false
```

**Prerequisite**: Point cloud loaded
**Output**: Segmented point cloud file set (one cluster per file)

---

### 3D Clustering with Statistics

```
Step 1: Load point cloud -> platform-load_layer
Step 2: 3D clustering + statistics -> pointcloud_processing-segment_by_attribute
```

**Call example**:
```
pointcloud_processing-segment_by_attribute
Parameters:
  input_data: "/data/point_cloud.lidata"
  output_data: "/output/segments_3d"
  search_radius: 0.3
  dimension: 3  # 3D clustering (full spatial distance)
  from_class: [0, 1, 2, 3, 4, 5, 6, 7]
  use_min_cluster_pts: true
  min_cluster_pts: 100
  use_max_cluster_pts: true
  max_cluster_pts: 100000
  use_min_area_threshold: true
  min_area_threshold: 0.5
  statistic_additional_attribute: true
  statistic_attribute_name: "Height"
  statistic_info: "minmaxmeanstd"
```

**Output**: Segmented point cloud file set + statistics CSV file

---

### Filter Clustering by Additional Attribute

```
Step 1: Load point cloud with additional attributes -> platform-load_layer
Step 2: Filter by attribute then cluster -> pointcloud_processing-segment_by_attribute
```

**Call example**:
```
pointcloud_processing-segment_by_attribute
Parameters:
  input_data: "/data/point_cloud.lidata"
  output_data: "/output/segments_filtered"
  search_radius: 0.4
  dimension: 2
  from_class: [3, 4, 5]
  filter_by_additional_attribute:
    attribute_name: "NDVI"
    is_addition_attribute_filter: true
  use_min_cluster_pts: true
  min_cluster_pts: 50
```

**Output**: Clustering results filtered by NDVI attribute

---

## Example 12: Tiling by Point Count Workflow

### Basic Point Count Tiling

```
Step 1: Load large point cloud -> platform-load_layer
Step 2: Tile by point count -> pointcloud_processing-tile_by_point_number
```

**Call example**:
```
pointcloud_processing-tile_by_point_number
Parameters:
  input_data: ["/data/large_pointcloud.lidata"]
  output_data: "/output/tiles"
  point_number: 50000
```

**Prerequisite**: Point cloud loaded
**Output**: Tiled point cloud file set (approximately 50,000 points per tile)

---

### Small Point Count Dense Tiling

```
Step 1: Load point cloud -> platform-load_layer
Step 2: Small point count tiling -> pointcloud_processing-tile_by_point_number
```

**Call example**:
```
pointcloud_processing-tile_by_point_number
Parameters:
  input_data: ["/data/point_cloud.lidata"]
  output_data: "/output/small_tiles"
  point_number: 10000
```

**Output**: Densely tiled point cloud file set (approximately 10,000 points per tile)

---

## Example 13: Map Sheet Subdivision Workflow

```
Step 1: Load large-extent point cloud -> platform-load_layer
Step 2: Map sheet subdivision -> pointcloud_processing-pointcloud_subdivision (scale=2, buffer=0)
```

**Prerequisite**: Point cloud loaded
**Output**: Point cloud set subdivided by 1:2000 standard map sheets + boundary vector

---

## Recommended Parameter Quick Reference

| Scenario | Denoise Neighbor Points | Smoothing Radius | Subsampling Rate | Tile Size |
|-----|----------|---------|-------|---------|
| Urban buildings | 10 | 0.2m | 30% | 200m |
| Forestry survey | 8 | 0.3m | 50% | 500m |
| Engineering survey | 15 | 0.1m | 80% | 100m |
| Power line inspection | 10 | 0.15m | 40% | By tower location |

### Subsampling Method Selection Guide

| Sampling Type | Parameter Value | Applicable Scenario | Recommended Parameter Range |
|---------|-------|---------|-------------|
| Minimum point spacing | `sampling_type=0` | Uneven point density, precise density control | `minimum_points_spacing`: 0.02-0.1m |
| Sampling rate | `sampling_type=1` | Fast downsampling of massive data | `sampling_rate`: 10-80% |
| Octree | `sampling_type=2` | Structured downsampling, preserving spatial distribution | `octree`: 15-21 (lower values retain fewer) |

> For detailed configuration, see the public configuration files in the `references/profiles/` directory
