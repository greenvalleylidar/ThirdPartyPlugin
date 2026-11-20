# UAV Processing Workflow

> Complete processing workflow for UAV airborne LiDAR point cloud data, from raw reconstruction to classification.

---

## Workflow Overview

| Scenario | Recommended Workflow | Key Tools | Difficulty |
|-----|---------|---------|------|
| DJI raw data reconstruction and processing | DJI standard workflow | dji_cloud_reconstruction -> trajectory_adjustment -> auto_split_trajectory -> cut_point_cloud_by_trajectory -> cut_overlap -> pointcloud_smooth -> pointcloud_subsampling -> pointcloud_outlier_removal -> classify_ground_by_progressive_tin_densification -> classify_by_deep_learning | 4/5 |
| Strip adjustment and quality check | Strip adjustment workflow | trajectory_adjustment -> elevation_difference_inspection | 3/5 |
| Trajectory cutting and redundancy removal | Trajectory processing workflow | auto_split_trajectory -> cut_point_cloud_by_trajectory -> cut_overlap -> density_quality_analysis | 3/5 |
| Point cloud preprocessing and classification | Preprocessing and classification workflow | pointcloud_smooth -> pointcloud_subsampling -> pointcloud_outlier_removal -> classify_ground_by_progressive_tin_densification -> classify_by_deep_learning | 2/5 |

---

## General Processing Logic

### UAV Processing Pipeline

```text
DJI raw data -> Point cloud reconstruction -> [Optional: Strip adjustment] -> POS processing (automatic trajectory splitting) -> Cut point cloud by trajectory -> Remove redundancy -> [Optional: Point cloud smoothing] -> [Optional: Resampling] -> Denoising -> Ground point classification -> Deep learning classification
```

### Processing Stages

| Stage | Tool Module | Description |
|------|---------|------|
| **Reconstruction** | `data_preprocessing` | DJI raw data cloud reconstruction to point cloud and POS |
| **Adjustment** | `data_preprocessing` | Trajectory adjustment to correct strip layering |
| **Cutting** | `data_preprocessing` | Automatic trajectory splitting, cut point cloud by trajectory, remove redundancy |
| **Preprocessing** | `pointcloud_processing` | Point cloud smoothing, resampling, denoising |
| **Classification** | `pointcloud_classification` | Ground point classification, deep learning classification |

### Optional Preprocessing Chain

`Point cloud smoothing` and `resampling` are optional preprocessing steps, selected based on point cloud quality and processing requirements:

```text
Point cloud after redundancy removal -> [Optional: Point cloud smoothing] -> [Optional: Resampling] -> Denoising -> Ground point classification -> Deep learning classification
```

| Optional Step | Applicable Situation | Can Skip When |
|---------|---------|-----------|
| Point cloud smoothing | Obvious local elevation jitter, contour line serrations, discontinuous DSM/DEM surface | Original point cloud quality is high and maximum detail preservation is needed |
| Resampling | Point density too high, large data volume, slow processing | Point density is low, or maximum precision and detail preservation is needed |

### General Parameter Recommendations

| Parameter | Recommended Value | Description |
|-----|-------|------|
| `neighbor_points` | 10 | Denoising neighborhood point count |
| `multiples_of_std_deviation` | 5 | Denoising standard deviation multiplier |
| `smoothing_type` | 0 | Point cloud smoothing method (XYZ 3D smoothing) |
| `search_radius` | 0.2 | Smoothing search radius (meters) |
| `max_fix_distance` | 0.1 | Smoothing maximum correction distance (meters) |
| `sampling_type` | 1 | Resampling method (sampling rate) |
| `sampling_rate` | 50 | Resampling percentage (%) |
| `scene_type` | 2 | Ground point classification scene type (gentle slope / general terrain) |
| `to_class` | 2 | Ground point class |

---

## Workflow 1: DJI Standard Processing Workflow

**Applicable Scenario**: DJI L1/L2/L3 raw LiDAR data, complete processing from reconstruction to classification

**Workflow Diagram**:

```text
DJI raw directory + Token -> Point cloud reconstruction -> [Optional: Strip adjustment] -> POS processing (automatic trajectory splitting) -> Cut point cloud by trajectory -> Remove redundancy -> [Optional: Point cloud smoothing] -> [Optional: Resampling] -> Denoising -> Ground point classification -> Deep learning classification
```

**Key Tools**: `data_preprocessing-dji_cloud_reconstruction`, `data_preprocessing-trajectory_adjustment`, `data_preprocessing-auto_split_trajectory`, `data_preprocessing-cut_point_cloud_by_trajectory`, `data_preprocessing-cut_overlap`, `pointcloud_processing-pointcloud_smooth`, `pointcloud_processing-pointcloud_subsampling`, `pointcloud_processing-pointcloud_outlier_removal`, `pointcloud_classification-classify_ground_by_progressive_tin_densification`, `pointcloud_classification-classify_by_deep_learning`

### Detailed Steps

#### Step 1: DJI Cloud Point Cloud Reconstruction

```json
{
  "step": 1,
  "description": "Reconstruct point cloud and POS trajectory from DJI raw LiDAR data",
  "tool": "data_preprocessing-dji_cloud_reconstruction",
  "input": {
    "input_data": "/data/DJI_RAW_DIRECTORY/",
    "user_token": "${DJI_USER_TOKEN}",
    "colorize_point": true,
    "smooth_point": false,
    "icp_optimise": false,
    "lidar_max_distance": 300,
    "output_data": "/output/dji_reconstruction/"
  }
}
```

> **Note**: This step processes DJI L1/L2/L3 raw LiDAR data to generate 3D point cloud data and POS trajectory files. `user_token` is the DJI Terra cloud service token, which must be provided at runtime and should not be hard-coded. If `icp_optimise` is enabled, ICP accuracy optimization will be applied to the point cloud; if `smooth_point` is enabled, point cloud smoothing will be applied.

#### Step 2: Strip Adjustment (Optional)

**Applicable Scenario**: Execute when strip layering or systematic offset is observed after reconstruction

```json
{
  "step": 2,
  "description": "Strip adjustment to correct trajectory errors and reduce strip layering",
  "tool": "data_preprocessing-trajectory_adjustment",
  "input": {
    "input_data": {
      "pointcloud_files": "{{step1.data.output_data.pointcloud_files}}",
      "trajectory_file": "{{step1.data.output_data.pos_files[0]}}"
    },
    "adjust_x": true,
    "adjust_y": true,
    "adjust_z": true,
    "adjust_roll": true,
    "adjust_pitch": true,
    "adjust_heading": true,
    "adjust_time_interval": 5,
    "output_data": "/output/dji_reconstruction/trajectory_adjustment/"
  }
}
```

> **Note**: Strip adjustment corrects systematic offsets and layering between strips by adjusting trajectory parameters (position and attitude). For aerial nadir data, adjusting delta-Z is not recommended. By default, adjusting Roll, Pitch, and Heading parameters yields good results. If no obvious strip layering is observed after reconstruction, this step can be skipped.

#### Step 3: POS Processing (Automatic Trajectory Splitting)

```json
{
  "step": 3,
  "description": "Automatically split trajectory into valid segments",
  "tool": "data_preprocessing-auto_split_trajectory",
  "input": {
    "input_data": "{{step2.data.output_data.traj_files[0] || step1.data.output_data.pos_files[0]}}",
    "max_heading_change": 30,
    "min_duration": 10,
    "min_length": 50,
    "output_data": "/output/split_trajectory/"
  }
}
```

> **Note**: Automatically splits long trajectories into valid segments based on heading change, duration, and length thresholds. `max_heading_change` controls the maximum heading change angle to avoid over-segmentation at curves; `min_duration` and `min_length` filter out overly short invalid segments. If using the adjustment results from Step 2, the input should be changed to the adjusted trajectory file.

#### Step 4: Cut Point Cloud by Trajectory

```json
{
  "step": 4,
  "description": "Cut point cloud by trajectory segments",
  "tool": "data_preprocessing-cut_point_cloud_by_trajectory",
  "input": {
    "input_data": {
      "pointcloud_file": "{{step2.data.output_data.pointcloud_files[0] || step1.data.output_data.pointcloud_files[0]}}",
      "pos_files": "{{step3.data.output_data}}"
    },
    "enable_buffer": true,
    "buffer": 20,
    "output_data": "/output/trajectory_cut/"
  }
}
```

> **Note**: Cuts the point cloud according to the trajectory segments from Step 3, generating an independent point cloud file for each segment. `buffer` sets the distance (meters) to preserve on both sides of the trajectory for cutting; adjust based on scan width and desired strip overlap. If Step 2 is skipped, the input point cloud should use the output from Step 1.

#### Step 5: Remove Redundancy

```json
{
  "step": 5,
  "description": "Remove redundant points between overlapping strips",
  "tool": "data_preprocessing-cut_overlap",
  "input": {
    "input_data": {
      "pointcloud_files": ["/output/trajectory_cut/strip_01.lidata", "/output/trajectory_cut/strip_02.lidata"],
      "pos_files": ["/output/split_trajectory/segment_01.pos", "/output/split_trajectory/segment_02.pos"]
    },
    "type": 0,
    "method_type": 0,
    "edge": 5,
    "density": 100,
    "offset": 25,
    "from_class": [0, 1, 2, 3, 4, 5, 6],
    "to_class": 12,
    "output_data": "/output/cut_overlap.lidata"
  }
}
```

> **Note**: Classifies (`type: 0`) or deletes (`type: 1`) redundant points between overlapping strips. `method_type: 0` detects by angle to trajectory; `method_type: 1` detects by scan angle. `to_class` is the target class for redundant points (default 12). It is recommended to classify first and then verify before deleting. This step requires at least two pairs of matched point cloud and POS files. `pointcloud_files` are the trajectory-cut point clouds from Step 4, and `pos_files` are the segment POS files from Step 3; replace with actual output file paths.

#### Step 6: Point Cloud Smoothing (Optional)

**Applicable Scenario**: Execute when obvious local elevation jitter or contour line serrations are present; skip if steep edges, building edges, or micro-terrain details need to be preserved.

```json
{
  "step": 6,
  "description": "Point cloud smoothing",
  "tool": "pointcloud_processing-pointcloud_smooth",
  "input": {
    "input_data": "{{step5.data.output_data}}",
    "output_data": "/output/smoothed.lidata",
    "smoothing_type": 0,
    "search_radius": 0.2,
    "max_fix_distance": 0.1,
    "select_class": [0, 1, 2, 3, 4, 5, 6]
  }
}
```

> **Note**: `smoothing_type: 0` is XYZ 3D smoothing, where points on vertical surfaces are smoothed in XY and points on horizontal surfaces are smoothed in Z. `max_fix_distance` controls the maximum adjustment distance for a single point; points exceeding this value will not be adjusted. If this step is skipped, subsequent step inputs should be changed to the output from Step 5.

#### Step 7: Resampling (Optional)

**Applicable Scenario**: Execute when point density is too high, file size is too large, or processing is slow; skip if point density is low or maximum precision needs to be preserved.

```json
{
  "step": 7,
  "description": "Point cloud resampling",
  "tool": "pointcloud_processing-pointcloud_subsampling",
  "input": {
    "input_data": "{{step6.data.output_data}}",
    "output_data": "/output/subsampled.lidata",
    "sampling_type": 1,
    "sampling_rate": 50,
    "minimum_points_spacing": 0,
    "octree": 21
  }
}
```

> **Note**: `sampling_type: 1` is sampling rate mode, retaining a specified percentage of points. `sampling_rate: 50` means retaining 50% of points. If Step 6 is skipped, the input should be changed to the output from Step 5.

#### Step 8: Denoising

```json
{
  "step": 8,
  "description": "Outlier removal",
  "tool": "pointcloud_processing-pointcloud_outlier_removal",
  "input": {
    "input_data": ["{{step7.data.output_data}}"],
    "neighbor_points": 10,
    "multiples_of_std_deviation": 5,
    "output_data": "/output/denoised.lidata"
  }
}
```

> **Note**: Removes outliers based on neighborhood distance statistics. The smaller `multiples_of_std_deviation` is, the stronger the denoising. It may not work well for dense noise; run multiple times for better results. If Steps 6 and 7 are skipped, the input should be changed to the output from Step 5.

#### Step 9: Ground Point Classification (Progressive TIN Densification)

```json
{
  "step": 9,
  "description": "Ground point classification (Progressive TIN Densification)",
  "tool": "pointcloud_classification-classify_ground_by_progressive_tin_densification",
  "input": {
    "input_data": "{{step8.data.output_data}}",
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

> **Note**: Uses Progressive TIN Densification for ground point classification. `scene_type` is selected based on terrain: 1=steep terrain, 2=gentle slope terrain, 3=flat terrain. `max_terrain_angle` controls the maximum terrain slope angle. Ground point classification results provide reference for subsequent deep learning classification and are the basis for terrain products such as DEM/contour lines.

#### Step 10: Deep Learning Classification

```json
{
  "step": 10,
  "description": "Deep learning classification",
  "tool": "pointcloud_classification-classify_by_deep_learning",
  "input": {
    "input_data": "{{step8.data.output_data}}",
    "scene_type": 2,
    "high_vegetation_class": 5,
    "low_vegetation_class": 3
  }
}
```

> **Note**: Uses deep learning segmentation models to classify the point cloud. `scene_type` selects the scene type (airborne urban / airborne rural, etc.), and the software automatically loads the corresponding pre-trained model. Supports classification into ground, vegetation, building, pole, powerline, car, and other classes. This step output will overwrite the original data file.

---

## Workflow 2: Strip Adjustment and Quality Check Workflow

**Applicable Scenario**: Existing point cloud and trajectory data that need strip layering correction and quality verification

**Workflow Diagram**:

```text
Point cloud + trajectory -> Strip adjustment -> Elevation difference check -> Quality determination
```

### Detailed Steps

#### Step 1: Strip Adjustment

```json
{
  "step": 1,
  "description": "Strip adjustment to correct trajectory errors",
  "tool": "data_preprocessing-trajectory_adjustment",
  "input": {
    "input_data": {
      "pointcloud_files": ["/data/strip_01.lidata", "/data/strip_02.lidata"],
      "trajectory_file": "/data/flight.traj"
    },
    "adjust_x": true,
    "adjust_y": true,
    "adjust_z": true,
    "adjust_roll": true,
    "adjust_pitch": true,
    "adjust_heading": true,
    "adjust_time_interval": 5,
    "output_data": "/output/trajectory_adjustment/"
  }
}
```

#### Step 2: Elevation Difference Check

```json
{
  "step": 2,
  "description": "Elevation difference check after strip adjustment",
  "tool": "data_preprocessing-elevation_difference_inspection",
  "input": {
    "input_data": ["/data/strip_01.lidata", "{{step1.data.output_data.pointcloud_files[0]}}"],
    "grid_size": 1.0,
    "elevation_difference_threshold": 0.1,
    "output_data": "/output/adjustment_qc.html"
  }
}
```

---

## Workflow 3: Trajectory Cutting and Redundancy Removal Workflow

**Applicable Scenario**: Existing point cloud and POS data that need to be cut by trajectory and have redundancy removed

**Workflow Diagram**:

```text
POS + point cloud -> Automatic trajectory splitting -> Cut by trajectory -> Remove redundancy -> Density quality check
```

### Detailed Steps

#### Steps 1-3: Same as Steps 3-5 in Workflow 1

---

## Parameter Configuration Quick Reference

### DJI Reconstruction Parameters

| Parameter | Recommended Value | Description |
|------|--------|------|
| `colorize_point` | true | Colorize point cloud |
| `smooth_point` | false | Do not smooth during reconstruction; handle separately later |
| `icp_optimise` | false | Do not perform ICP optimization during reconstruction; handle separately later |
| `lidar_max_distance` | 300 | Maximum valid distance (meters); excess is trimmed |

### Strip Adjustment Parameters

| Parameter | Recommended Value | Description |
|------|--------|------|
| `adjust_x/y/z` | true | Position correction |
| `adjust_roll/pitch/heading` | true | Attitude correction |
| `adjust_time_interval` | 5 | Trajectory correction time interval (seconds); shorter interval means higher fluctuation frequency |

### Trajectory Splitting Parameters

| Parameter | Recommended Value | Description |
|------|--------|------|
| `max_heading_change` | 30 | Maximum heading change angle (degrees); avoids over-segmentation at curves |
| `min_duration` | 10 | Minimum duration (seconds); filters overly short segments |
| `min_length` | 50 | Minimum length (meters); filters overly short segments |

### Trajectory Cutting Parameters

| Parameter | Recommended Value | Description |
|------|--------|------|
| `enable_buffer` | true | Enable buffer zone cutting |
| `buffer` | 20 | Distance preserved on both sides of trajectory for cutting (meters); adjust based on scan width |

### Redundancy Removal Parameters

| Parameter | Recommended Value | Description |
|------|--------|------|
| `type` | 0 | 0=classify redundant points, 1=delete redundant points |
| `method_type` | 0 | 0=by angle to trajectory, 1=by scan angle |
| `edge` | 5 | Overlap area grid cell size |
| `density` | 100 | Grid cell minimum point density threshold |
| `offset` | 25 | Angle threshold to trajectory (degrees) |
| `to_class` | 12 | Redundant point target class |

### Point Cloud Smoothing Parameters

| Parameter | Recommended Value | Description |
|------|--------|------|
| `smoothing_type` | 0 | XYZ 3D smoothing |
| `search_radius` | 0.2 | Search radius for nearby points (meters) |
| `max_fix_distance` | 0.1 | Maximum adjustment distance per point (meters) |
| `select_class` | [0,1,2,3,4,5,6] | Classes participating in smoothing |

### Resampling Parameters

| Parameter | Recommended Value | Description |
|------|--------|------|
| `sampling_type` | 1 | Sampling rate mode |
| `sampling_rate` | 50 | Percentage of points to retain (%) |
| `minimum_points_spacing` | 0 | Minimum point spacing (meters); only effective in minimum spacing mode |
| `octree` | 21 | Octree subdivision level; only effective in octree mode (1-21) |

### Denoising Parameters

| Parameter | Recommended Value | Description |
|------|--------|------|
| `neighbor_points` | 10 | Required number of points in neighborhood |
| `multiples_of_std_deviation` | 5 | Standard deviation multiplier; smaller value means stronger denoising |

### Ground Point Classification Parameters

| Parameter | Recommended Value | Description |
|------|--------|------|
| `scene_type` | 2 | 1=steep terrain, 2=gentle slope terrain, 3=flat terrain |
| `grid_size` | 20 | Grid size (meters) |
| `iteration_angle` | 8 | Iteration angle (degrees) |
| `iteration_distance` | 1.2 | Iteration distance (meters) |
| `max_terrain_angle` | 88 | Maximum terrain slope angle (degrees) |
| `max_building_size` | 30 | Maximum building size (meters) |
| `tolerance_above` | 0.15 | Above tolerance (meters) |
| `tolerance_below` | 0.15 | Below tolerance (meters) |
| `to_class` | 2 | Ground point class |

### Deep Learning Classification Parameters

| Parameter | Recommended Value | Description |
|------|--------|------|
| `scene_type` | 2 | Scene type; select based on data |
| `high_vegetation_class` | 5 | High vegetation class code |
| `low_vegetation_class` | 3 | Low vegetation class code |

### Common Class Codes

| Class | Meaning | Description |
|-----|------|------|
| 0 | Never Classified | Never Classified |
| 1 | Unclassified | Unclassified |
| 2 | Ground | Ground |
| 3 | Low Vegetation | Low Vegetation (<0.5m) |
| 4 | Medium Vegetation | Medium Vegetation (0.5-2m) |
| 5 | High Vegetation | High Vegetation (>2m) |
| 6 | Building | Building |
| 9 | Water | Water |
| 12 | Overlap | Overlap points (redundancy removal target class) |

---

## Common Issues and Solutions

### Issue 1: DJI Reconstruction Failed or Poor Point Cloud Quality

**Possible Causes**:
- `user_token` is invalid or expired
- Raw data directory is incomplete
- `lidar_max_distance` is set too small

**Solutions**:
- Check and update the DJI Terra cloud service token
- Confirm the raw data directory contains complete DJI raw files
- Increase `lidar_max_distance` to 300-500 meters

### Issue 2: Strip Layering Not Eliminated

**Possible Causes**:
- Trajectory error is too large for a single adjustment to fully correct
- Adjustment parameters are not comprehensive enough
- Necessary adjustment components were not enabled

**Solutions**:
- Execute strip adjustment multiple times to progressively correct
- Enable all position and attitude adjustment components
- Check if `adjust_time_interval` is appropriate; reduce it to correct local jitter
- Use the profile tool to view layering before and after correction

### Issue 3: Trajectory Splitting Too Fine or Too Coarse

**Possible Causes**:
- `max_heading_change` is set too small, causing over-segmentation at curves
- `min_duration` or `min_length` is too small, filtering out too many short segments

**Solutions**:
- Increase `max_heading_change` to 45-60 degrees
- Increase `min_duration` to 15-30 seconds
- Increase `min_length` to 100-200 meters

### Issue 4: Uneven Density After Redundancy Removal

**Possible Causes**:
- `edge` is set inappropriately
- `density` threshold is too high or too low
- `offset` angle threshold is inappropriate

**Solutions**:
- Adjust `edge` to 3-10 meters
- Adjust `density` threshold based on actual point density
- Adjust `offset` to 20-30 degrees
- Use the density quality analysis tool to verify density uniformity

### Issue 5: Ground Point Classification Includes Buildings or Vegetation

**Possible Causes**:
- `scene_type` does not match the actual terrain
- `max_terrain_angle` is set too large
- `max_building_size` is too large

**Solutions**:
- Select the correct `scene_type` based on actual terrain
- Reduce `max_terrain_angle` to 75-85 degrees
- Reduce `max_building_size` to 15-25 meters
- Check `tolerance_above` and `tolerance_below` parameters

### Issue 6: Deep Learning Classification Results Are Unsatisfactory

**Possible Causes**:
- Scene type selection is inappropriate
- Classification class configuration is incorrect
- Point cloud has not been ground-point classified

**Solutions**:
- Select a scene type that matches the data
- Check `high_vegetation_class` and `low_vegetation_class` configuration
- Ensure ground point classification is completed in Step 9
- For unsatisfactory areas, use other classification tools for correction

---

## Related Documents

- Data preprocessing tool registry: `references/data_preprocessing/tools.md`
- Data preprocessing preflight checks: `references/data_preprocessing/preflight_checks.md`
- Point cloud processing tool registry: `references/pointcloud_processing/tools.md`
- Point cloud processing preflight checks: `references/pointcloud_processing/preflight_checks.md`
- Point cloud classification tool registry: `references/pointcloud_classification/tools.md`
- Terrain analysis tool registry: `references/terrain/tools.md`
- Common profiles: `references/profiles/`
