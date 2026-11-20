# Data Preprocessing Workflows

> Complete processing workflows for LiDAR360 data preprocessing, including registration QC, trajectory adjustment QC, trajectory-based cutting, overlap handling, and DJI reconstruction preprocessing. Use these workflows when a preprocessing task requires chaining multiple `data_preprocessing-*` tools to produce and verify downstream-ready results.

---

## Process Overview

| Scenario | Recommended Process | Key Tools | Solves |
|---------|-------------------|-----------|--------|
| Registration QC | Auto registration -> Elevation difference inspection | `auto_registration`, `elevation_difference_inspection` | Align two point clouds and verify registration quality |
| Trajectory Adjustment QC | Trajectory adjustment -> Elevation difference inspection | `trajectory_adjustment`, `elevation_difference_inspection` | Reduce strip layering caused by trajectory errors and verify improvement |
| Trajectory Segmentation and Cutting | Auto split trajectory -> Cut point cloud by trajectory | `auto_split_trajectory`, `cut_point_cloud_by_trajectory` | Split long flight trajectories and output strip/segment point clouds |
| Overlap Handling QC | Cut overlap -> Strip overlap analysis -> Density quality analysis | `cut_overlap`, `strip_overlap_analysis`, `density_quality_analysis` | Classify or delete overlap points, verify strip overlap ratio, and verify density uniformity |
| Trajectory Quality QC | Trajectory quality analysis | `trajectory_quality_analysis` | Check flight height, speed, and attitude quality before downstream strip processing |
| DJI Reconstruction Preprocessing | DJI cloud reconstruction -> Optional trajectory quality analysis -> Optional trajectory adjustment -> Optional density/overlap QC or trajectory cutting | `dji_cloud_reconstruction`, optional `trajectory_quality_analysis`, `trajectory_adjustment`, QC/cutting tools | Generate DJI point cloud/POS outputs, check trajectory quality, optionally correct strip layering, and prepare downstream data |

---

## General Preprocessing Logic

Use preprocessing workflows before terrain, forestry, building, mining, and point cloud classification tasks when raw data needs QC, correction, splitting, overlap handling, or DJI reconstruction.

```text
Input Files -> Preprocessing Tool Chain -> Result Verification -> Downstream Analysis
```

### Common Input Checks

| Check | Required For | Action |
|------|--------------|--------|
| Input files exist and suffixes match tool schema | All workflows | Convert formats with `data_conversion` if unsupported |
| Point cloud is `.lidata` where required | QC, registration, adjustment, cutting, overlap | Convert to `.lidata` before running tools that only accept LiData |
| Coordinate system is known and consistent | Registration, elevation inspection, trajectory adjustment | Transform or define coordinate system first |
| Spatial ranges overlap | Registration, elevation inspection, overlap handling | Select overlapping datasets or clip ROI |
| POS/TRAJ exists | Trajectory adjustment, splitting, cutting, overlap handling, trajectory quality analysis | Provide valid trajectory files matching point clouds |
| Output HTML path is writable | Quality reports, strip overlap analysis, trajectory quality analysis | Choose a writable report path and inspect the generated HTML report after execution |
| DJI `user_token` is valid | DJI reconstruction | Provide a valid runtime token; do not hard-code credentials |

---

## Process 1: Point Cloud Registration QC

**Applicable Scenarios**: Align two scans, strips, or point cloud blocks before merging, comparison, or downstream modeling, then verify the registration quality.

**Flowchart**:

```text
Reference + Align Point Clouds -> Auto Registration -> Elevation Difference Inspection -> Registration Decision
```

### Input Requirements

- `ref_pointcloud_file`: reference `.lidata` point cloud.
- `align_pointcloud_file`: source `.lidata` point cloud to be registered.
- The two point clouds should have sufficient overlap.

### Detailed Steps

#### Step 1: Automatic Registration

```json
{
  "step": 1,
  "description": "Automatically register source point cloud to reference point cloud",
  "tool": "data_preprocessing-auto_registration",
  "input": {
    "input_data": {
      "ref_pointcloud_file": "/data/reference.lidata",
      "align_pointcloud_file": "/data/source.lidata"
    },
    "icp_optimize": true,
    "iteration": 10,
    "overlap": 40,
    "output_data": "/output/registered_source.lidata"
  }
}
```

#### Step 2: Registration Quality Inspection

```json
{
  "step": 2,
  "description": "Inspect elevation differences after registration",
  "tool": "data_preprocessing-elevation_difference_inspection",
  "input": {
    "input_data": ["/data/reference.lidata", "{{step1.data.output_data}}"],
    "grid_size": 1.0,
    "elevation_difference_threshold": 0.1,
    "output_data": "/output/registration_qc.html"
  }
}
```

**Configuration Recommendations**:
- Enable `icp_optimize` when initial positions are close and overlap is sufficient.
- Increase `overlap` when the two point clouds share a larger common area.
- If elevation differences remain systematic after registration, check coordinate systems and overlap quality before rerunning.

---

## Process 2: Trajectory Adjustment and Strip Layering QC

**Applicable Scenarios**: Correct trajectory-related strip offsets, reduce layering, or improve consistency between point clouds and image projects.

**Flowchart**:

```text
Point Cloud + Trajectory -> Trajectory Adjustment -> Elevation Difference Inspection -> Strip Consistency Decision
```

### Input Requirements

- `pointcloud_files`: one or more `.lidata` point cloud files for each flight.
- `trajectory_file`: matching `.traj`, `.pos`, or `.txt` trajectory file.
- Optional image project can be included when bundle adjustment is required.

### Detailed Steps

#### Step 1: Trajectory Adjustment

```json
{
  "step": 1,
  "description": "Adjust trajectory to correct point cloud strip layering",
  "tool": "data_preprocessing-trajectory_adjustment",
  "input": {
    "input_data": {
      "pointcloud_files": ["/data/strip_01.lidata", "/data/strip_02.lidata"],
      "trajectory_file": "/data/flight.traj"
    },
    "flight_data": [
      {
        "flight_name": "Flight 1",
        "pointcloud_files": ["/data/strip_01.lidata", "/data/strip_02.lidata"],
        "trajectory_file": "/data/flight.traj"
      }
    ],
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

#### Step 2: Adjustment Quality Inspection

```json
{
  "step": 2,
  "description": "Inspect elevation differences after trajectory adjustment",
  "tool": "data_preprocessing-elevation_difference_inspection",
  "input": {
    "input_data": ["/data/reference_strip.lidata", "{{step1.data.output_data.pointcloud_files[0]}}"],
    "grid_size": 1.0,
    "elevation_difference_threshold": 0.1,
    "output_data": "/output/trajectory_adjustment_qc.html"
  }
}
```

**Configuration Recommendations**:
- Start by enabling only necessary adjustment components; avoid solving all components without control evidence.
- Use elevation difference reports and cross-section views to verify improvement.
- For image project bundle adjustment, include image project inputs only after confirming point cloud/trajectory consistency.

---

## Process 3: Trajectory Auto Split and Point Cloud Cutting

**Applicable Scenarios**: Split long trajectories into valid flight segments and cut point clouds by those trajectory segments for strip-based processing or delivery.

**Flowchart**:

```text
POS/TRAJ -> Auto Split Trajectory -> Cut Point Cloud by Trajectory -> Segmented Point Clouds
```

### Input Requirements

- `auto_split_trajectory.input_data`: `.pos` or `.traj` trajectory file.
- `cut_point_cloud_by_trajectory.input_data.pointcloud_file`: `.lidata` point cloud file.
- `cut_point_cloud_by_trajectory.input_data.pos_files`: `.pos` trajectory segment files from Step 1.

### Detailed Steps

#### Step 1: Auto Split Trajectory

```json
{
  "step": 1,
  "description": "Automatically split trajectory by heading, duration, and length thresholds",
  "tool": "data_preprocessing-auto_split_trajectory",
  "input": {
    "input_data": "/data/flight.traj",
    "max_heading_change": 30,
    "min_duration": 10,
    "min_length": 50,
    "output_data": "/output/split_trajectory/"
  }
}
```

#### Step 2: Cut Point Cloud by Trajectory

```json
{
  "step": 2,
  "description": "Cut point cloud along trajectory segments",
  "tool": "data_preprocessing-cut_point_cloud_by_trajectory",
  "input": {
    "input_data": {
      "pointcloud_file": "/data/raw.lidata",
      "pos_files": "{{step1.data.output_data}}"
    },
    "enable_buffer": true,
    "buffer": 20,
    "output_data": "/output/trajectory_cut/"
  }
}
```

**Configuration Recommendations**:
- Increase `max_heading_change` to avoid over-splitting curved routes.
- Increase `min_duration` and `min_length` to filter short invalid segments.
- Set `buffer` based on scan width and required strip overlap.

---

## Process 4: Overlap Point Handling and Density QC

**Applicable Scenarios**: Classify or delete overlap points between flight strips to reduce duplicate points, improve density uniformity, and prepare data for DEM/DSM generation.

**Flowchart**:

```text
Flight Strip Point Clouds + POS Files -> Cut Overlap -> Density Quality Analysis -> Density Uniformity Decision
```

### Input Requirements

- `pointcloud_files`: at least two `.lidata` strip point clouds.
- `pos_files`: matching `.pos` files for each strip.
- Select `type` and `method_type` according to whether overlap points should be classified or deleted.

### Detailed Steps

#### Step 1: Cut Overlap

```json
{
  "step": 1,
  "description": "Classify or delete overlap points",
  "tool": "data_preprocessing-cut_overlap",
  "input": {
    "input_data": {
      "pointcloud_files": ["/data/strip_01.lidata", "/data/strip_02.lidata"],
      "pos_files": ["/data/strip_01.pos", "/data/strip_02.pos"]
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

#### Step 2: Strip Overlap Analysis

```json
{
  "step": 2,
  "description": "Analyze overlap ratio between adjacent flight strips",
  "tool": "data_preprocessing-strip_overlap_analysis",
  "input": {
    "input_data": {
      "pointcloud_files": ["/data/strip_01.lidata", "/data/strip_02.lidata"],
      "traj_files": ["/data/strip_01.pos", "/data/strip_02.pos"]
    },
    "overlap_threshold": 5,
    "report_title": "Strip Overlap Analysis Report",
    "output_data": "/output/strip_overlap_report.html"
  }
}
```

#### Step 3: Density Quality Analysis After Overlap Handling

```json
{
  "step": 3,
  "description": "Check point cloud density after overlap handling",
  "tool": "data_preprocessing-density_quality_analysis",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "grid_size": 1.0,
    "upper_values": [10, 50, 100, 200],
    "report_title": "Overlap Handling Density Report",
    "render_colors": [[255, 0, 0], [255, 255, 0], [0, 255, 0], [0, 0, 255]],
    "output_data": "/output/overlap_density_report.html"
  }
}
```

**Configuration Recommendations**:
- Use `type: 0` to classify overlap points to `to_class`; use `type: 1` to delete overlap points only after QC approval.
- Use `method_type: 0` with `offset` for trajectory-angle detection; use `method_type: 1` with `scan_angle` for scan-angle detection.
- Adjust `edge` to control the density grid size for overlap detection.
- Run strip overlap analysis to confirm adjacent strip overlap ratios before delivery or downstream DEM/DSM generation.
- Run density quality analysis after overlap handling to confirm density uniformity.

---

## Process 5: DJI L1/L2/L3 Reconstruction Preprocessing

**Applicable Scenarios**: Convert DJI Zenmuse raw LiDAR data into point cloud and POS trajectory outputs, optionally run trajectory adjustment to reduce strip layering, then perform density QC or trajectory-based cutting.

**Flowchart**:

```text
DJI Raw Directory + Token -> DJI Cloud Reconstruction -> [Optional Trajectory Adjustment] -> Optional Density QC / Trajectory Cutting -> Downstream Processing
```

### Input Requirements

- `input_data`: DJI raw LiDAR data directory.
- `user_token`: valid DJI cloud service token supplied at runtime.
- DJI reconstruction outputs include `pointcloud_files` and `pos_files`; point cloud outputs may need conversion to `.lidata` before tools that only support LiData.
- Run optional trajectory adjustment when reconstructed strips show layering or systematic offsets.

### Detailed Steps

#### Step 1: DJI Cloud Reconstruction

```json
{
  "step": 1,
  "description": "Reconstruct point cloud from DJI raw LiDAR data",
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

#### Step 2A: Optional Trajectory Quality Analysis

```json
{
  "step": "2A",
  "description": "Check DJI reconstructed trajectory height, speed, and attitude quality",
  "tool": "data_preprocessing-trajectory_quality_analysis",
  "input": {
    "input_data": "{{step1.data.output_data.pos_files}}",
    "report_type": 3,
    "design_height": 100,
    "design_speed": 8,
    "height_tolerance": 5,
    "speed_consistency": 5,
    "strip_deformation": 3,
    "output_data": "/output/dji_reconstruction/trajectory_quality_report.html"
  }
}
```

#### Step 2B: Optional Trajectory Adjustment

```json
{
  "step": "2B",
  "description": "Optionally adjust DJI reconstructed point clouds and POS trajectories",
  "tool": "data_preprocessing-trajectory_adjustment",
  "input": {
    "input_data": {
      "pointcloud_files": "{{step1.data.output_data.pointcloud_files}}",
      "trajectory_file": "{{step1.data.output_data.pos_files[0]}}"
    },
    "flight_data": [
      {
        "flight_name": "DJI Flight 1",
        "pointcloud_files": "{{step1.data.output_data.pointcloud_files}}",
        "trajectory_file": "{{step1.data.output_data.pos_files[0]}}"
      }
    ],
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

#### Step 2C: Optional Density Quality Analysis

```json
{
  "step": "2C",
  "description": "Check reconstructed or adjusted point cloud density",
  "tool": "data_preprocessing-density_quality_analysis",
  "input": {
    "input_data": "{{step2B.data.output_data.pointcloud_files || step1.data.output_data.pointcloud_files}}",
    "grid_size": 1.0,
    "upper_values": [10, 50, 100, 200],
    "report_title": "DJI Reconstruction Density Report",
    "render_colors": [[255, 0, 0], [255, 255, 0], [0, 255, 0], [0, 0, 255]],
    "output_data": "/output/dji_reconstruction/density_report.html"
  }
}
```

#### Step 2D: Optional Point Cloud Cutting by POS

```json
{
  "step": "2D",
  "description": "Cut reconstructed or adjusted point cloud by POS outputs",
  "tool": "data_preprocessing-cut_point_cloud_by_trajectory",
  "input": {
    "input_data": {
      "pointcloud_file": "{{step2B.data.output_data.pointcloud_files[0] || step1.data.output_data.pointcloud_files[0]}}",
      "pos_files": "{{step2B.data.output_data.traj_files || step1.data.output_data.pos_files}}"
    },
    "enable_buffer": true,
    "buffer": 20,
    "output_data": "/output/dji_reconstruction/trajectory_cut/"
  }
}
```

**Configuration Recommendations**:
- Do not hard-code DJI credentials in workflow files or scripts; use environment variables or secure runtime inputs.
- Confirm raw data directory integrity before execution.
- Run trajectory quality analysis when POS/TRAJ outputs need height, speed, or attitude QA before downstream strip processing.
- Run trajectory adjustment only when strip layering or systematic offsets are visible.
- Convert point cloud outputs to `.lidata` before density quality analysis, strip overlap analysis, trajectory adjustment, or trajectory cutting if DJI reconstruction returns other formats.

---

## Result Verification Checklist

| Workflow | Verification |
|---------|--------------|
| Registration QC | Registered point cloud exists; elevation report is within tolerance |
| Trajectory adjustment QC | Strip layering decreases; no new systematic offset is introduced |
| Trajectory cutting | Output segments match trajectory direction and expected buffer |
| Overlap handling QC | Strip overlap HTML report exists and overlap ratios meet threshold; density becomes more uniform; valid edge data is not over-trimmed |
| Trajectory quality QC | Trajectory quality HTML report exists and height, speed, and attitude statistics are within project tolerance |
| DJI reconstruction preprocessing | Point cloud/POS outputs exist; optional trajectory report, adjustment, QC, overlap, or cutting outputs are valid |
