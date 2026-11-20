# Tool Call Conventions

This document records the general conventions for LiDAR360 MCP tool calls.

---

## 1. Tools and Parameters

- When a complete tool list is needed, first read the corresponding module's `*_SKILL.md`.
- Before each call to a target tool, the current runtime schema must be obtained:

```bash
{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "module-toolID"
```

`tools.md`, `examples.md`, and `*_SKILL.md` are for tool selection, development/maintenance, and static validation only; they must not be used as the execution source or fallback for released runtime. If schema retrieval fails, set `schema_source: unavailable` and `status: blocked`, stop execution, and prompt the user to check the MCP service and tool name; do not construct requests from local documents, snapshots, or memory.

Examples:

```bash
{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "terrain_analysis-generate_general_dem_from_pointcloud"
{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "imagery_processing-orthomosaic"
```

For command-line invocation details, see `references/profiles/mcp_tool_usage.md`.

> **Note**: LiDAR360 does not support parallel tool calls. Multi-step tasks must be executed sequentially, waiting for the previous tool to return results before calling the next one.

---

## 2. Pre-Execution Checks and Workflow Entry

### Mandatory Preflight Gate

Before executing any tool, the following check process **must** be completed:

1. **Read the checklist**: Review the "Pre-Execution Checklist" in the module SKILL.md
2. **Confirm each item**:
   - General checks (file exists, format matches, output is writable)
   - Tool-specific checks (from preflight_checks.md)
3. **In-place modification check**: If the tool is in the "In-Place Modification Tool List", execute the in-place modification gate (see below)
4. **Determine the result**:
   - **PASS**: All checks passed -> Execute the tool
   - **FAIL**: Any check failed -> **Do not execute the tool**; prompt the user to resolve
   - **UNKNOWN**: Cannot verify (e.g., unable to retrieve data information) -> **Do not execute the tool**; ask the user for confirmation

### Check Evidence Retention

Before each tool call, record:
- Which items were checked
- Pass/fail status for each item
- Reasons for failures and resolution suggestions

### Reference Documents

- Checklist template in the module SKILL.md
- Detailed check items in the module `preflight_checks.md`
- For cross-module tasks, see `references/workflow/workflow.md`
- For single-module multi-step tasks, see the module `examples.md` or `workflows.md`

Key pre-execution checks: input existence, output writability, required parameters provided, enum/numeric range validity, consistency of input data formats and coordinate systems.

### Verification Method Reference Table

#### Verification Tool Quick Reference

| Tool | Purpose | Key Return Fields |
|------|------|-------------|
| `platform-preflight_check` | Check point cloud/raster/TIN prerequisites | `has_ground_points`, `is_normalized_point_cloud`, `is_dem_or_dsm`, `is_tin`, `is_valid` |
| `platform-get_data_information` | Get data metadata (coordinate system, extent, classes, bands, etc.) | `coordinate_system`, `bounds`, `point_count`, `class_codes`, `band_count`, `nodata_value`, `resolution`, `data_type` |
| `platform-list_loaded_layers` | List loaded layers | `layers[].id`, `layers[].url`, `layers[].visible` |
| `platform-get_layer_details` | Get detailed properties of a loaded layer | Detailed properties queried by `layer_id` |
| `platform-lidar360_software_information` | Get software information and runtime resources | `runtime_resources[]` (check if dependency models are downloaded) |

#### High-Frequency Condition Verification Mapping

| Condition | Verification Tool | Determination Logic |
|------|---------|---------|
| Coordinate system consistent | `get_data_information` x N | Compare each data's `coordinate_system` field; all identical -> PASS |
| Extent overlap | `get_data_information` x N | Compare each data's `bounds`; intersection area > 0 -> PASS |
| Point cloud normalized | `preflight_check(check_item=1)` | `is_normalized_point_cloud == true` -> PASS |
| Ground points classified | `preflight_check(check_item=0)` | `has_ground_points == true` -> PASS |
| DEM/DSM valid | `preflight_check(check_item=2)` | `is_dem_or_dsm == true` and `is_valid == true` -> PASS |
| TIN valid | `preflight_check(check_item=3)` | `is_tin == true` and `is_valid == true` -> PASS |
| Data loaded | `list_loaded_layers` | Target file URL in `layers[].url` -> PASS |
| Point cloud readable/exists | `get_data_information` | `code == 0` -> PASS |
| Raster band info | `get_data_information` | `band_count >= 1` -> PASS |
| Dependency model installed | `lidar360_software_information` | `runtime_resources[].name` matches and downloaded -> PASS |

#### UNKNOWN Handling Rules

When a verification tool call fails:
1. Tool returns `code != 0` -> Record error, mark UNKNOWN
2. Return field is missing or empty -> Mark UNKNOWN
3. UNKNOWN items -> **Do not execute the target tool**; show the user verified/unverified items and request manual confirmation

### In-Place Modification Gate

Some tools **modify input files in place** (output path is the same as input path); calling with incorrect parameters may irreversibly corrupt data. Before executing such tools, additional checks **must** be completed.

#### Identification Rules

The following 5 schema patterns identify a tool as in-place modification:

1. Schema `description` contains "source dataset will be updated", "in-place write", "in-place update", "source file will be overwritten"
2. `outputSchema.output_data.description` contains "output file is the same as input file"
3. `inputSchema.input_data.description` contains "directly modifies source data in place"
4. `outputSchema.output_data.description` contains "path is the same as input path"
5. Tool has no independent output path parameter; results are written back to the input file

#### In-Place Modification Tool List

| Module | Tool ID | Modification Content |
|------|--------|---------|
| pointcloud_classification | `classify_ground_by_csf` | Ground point classification (CSF method) |
| pointcloud_classification | `classify_ground_by_deep_learning` | Ground point classification (deep learning) |
| pointcloud_classification | `classify_ground_by_progressive_tin_densification` | Ground point classification (Progressive TIN Densification) |
| pointcloud_classification | `extract_median_ground_points` | Extract median ground points (source file will be overwritten) |
| pointcloud_classification | `classify_noise_points` | Noise point classification |
| pointcloud_classification | `classify_isolated_points` | Isolated point classification |
| pointcloud_classification | `classify_low_points` | Low point classification |
| pointcloud_classification | `classify_closeby_points` | Close-by point classification |
| pointcloud_classification | `classify_buildings` | Building classification |
| pointcloud_classification | `classify_air_points` | Air point classification |
| pointcloud_classification | `classify_below_surface_points` | Below-surface point classification |
| pointcloud_classification | `classify_top_surface` | Top surface classification |
| pointcloud_classification | `classify_model_key_points` | Model key point classification |
| pointcloud_classification | `classify_by_attribute` | Classification by attribute |
| pointcloud_classification | `classify_by_additional_attribute` | Classification by additional attribute |
| pointcloud_classification | `classify_by_height_above_ground` | Classification by height above ground |
| pointcloud_classification | `classify_by_tree_attributes` | Classification by tree attributes |
| pointcloud_classification | `classify_by_region` | Classification by region |
| pointcloud_classification | `classify_by_mask` | Classification by mask |
| pointcloud_classification | `classify_by_deep_learning` | Deep learning classification |
| pointcloud_classification | `classify_by_machine_learning` | Machine learning classification |
| pointcloud_classification | `classify_by_trained_ml_model` | Classification by trained model |
| pointcloud_classification | `classify_water_points` | Water point classification and update source dataset |
| pointcloud_classification | `classify_by_min_elevation_difference` | Classification by minimum elevation difference and update source dataset |
| pointcloud_classification | `classify_tunnel_points` | No independent output path; conservatively treated as L3 in-place write |
| pointcloud_classification | `classify_low_and_high_vegetation` | Low and high vegetation classification |
| pointcloud_classification | `train_point_cloud_classification_model` | Point cloud classification model training (long-running task) |
| pointcloud_classification | `train_image_classification_model` | Image classification model training (long-running task) |
| pointcloud_processing | `extract_color_from_ortho_image` | Extract color from ortho image |
| pointcloud_processing | `extract_color_from_image_project` | Extract color from image project |
| pointcloud_processing | `pointcloud_pcv` | Position Contrast Visualization |
| mining_analysis | `compute_normal_vectors` | Normal vector computation |
| building_modeling | `building_attributes_calculate` | Building attribute calculation |
| imagery_processing | `image_alignment` | Image aerial triangulation |
| imagery_processing | `update_alignment` | Update image alignment |
| forestry_airborne | `clear_tree_id` | Clear tree ID |
| forestry_airborne | `trunk_based_tree_segmentation` | Trunk-based individual tree segmentation |
| forestry_airborne | `its_mosaicing` | Individual tree segmentation mosaicing |
| forestry_terrestrial | `universal_tree_segmentation` | Universal individual tree segmentation |
| forestry_terrestrial | `tls_trunk_based_tree_segmentation` | Terrestrial trunk-based segmentation |
| forestry_terrestrial | `tls_point_cloud_segmentation` | Terrestrial point cloud segmentation |
| forestry_terrestrial | `tls_point_cloud_segmentation_from_seed_points` | Terrestrial seed point segmentation |

#### Pre-Execution Requirements

Before calling any tool in the above table, the following steps **must** be executed:

1. **Detect in-place modification**: Compare `input_data` and `output_data` paths; if identical or tool is in the above table -> confirm as in-place modification
2. **Notify the user**: Explicitly inform the user that "this tool will modify the input file in place; the modification is irreversible"
3. **Suggest backup**: Prompt the user to "back up the original data first, or confirm that a copy of the data already exists"
4. **Obtain confirmation**: Wait for explicit user confirmation before executing; if the user does not confirm, **do not execute the tool**

> **Note**: All 24 classification tools in the `pointcloud_classification` module are in-place modifications. This module has no independent `preflight_checks.md`; the above gate process must be executed before calling.

---

## 3. Output Path Generation

When a tool call requires an output path, generate the default path according to the following rules.

### 3.1 Tool Title Source

"Tool title" uses the `title` field from the schema returned by `get_tool_schema` / `get_mcp_schema`, not the tool `name`, tool ID, or `module-toolID`.

If `title` contains Windows invalid filename characters (`< > : " / \ | ? *`), replace them with `_` when used in paths.

### 3.2 Output as File

Rule: Use the directory and filename of the first input file, appending the tool title before the extension.

```text
Input: D:/data/site01.lidata
Actual tool: terrain_analysis-generate_general_dem_from_pointcloud
schema.title: Digital Elevation Model
Output: D:/data/site01_Digital Elevation Model.tif
```

### 3.3 Output as Folder

Rule: Use the parent folder of the first input path, appending the tool title as the output folder name.

```text
Input: D:/uav/raw/DJI_001/L1_raw
Actual tool: data_preprocessing-dji_cloud_reconstruction
schema.title: DJI L1/L2/L3 Reconstruction
Path title: DJI L1_L2_L3 Reconstruction
Output: D:/uav/raw/DJI_001/L1_raw_DJI L1_L2_L3 Reconstruction
```

### 3.4 Multiple Input Paths

Rule: When inputs contain multiple files or directories, use the first input path.

```text
Input:
- D:/data/strip01.lidata
- D:/data/strip02.lidata
Actual tool: data_preprocessing-strip_overlap_analysis
schema.title: Strip Overlap Analysis
Output: D:/data/strip01_Strip Overlap Analysis.html
```

### 3.5 Path Length

The total output path length must not exceed the Windows system path length limit. When the limit may be exceeded, shorten the input filename or choose a shorter output directory; if other tool titles are already in the path, remove them from right to left until the limit is satisfied.

---

## 4. Error Handling

When a tool call returns an error, read the error message first; do not retry blindly. Focus on checking input paths, output paths, parameter types, enum values, file count, format, coordinate system, and spatial extent.

For detailed error handling, see `references/profiles/error_message_handle.md`.

---

## 5. Shared Safety and Result Contract

### Side Effect Levels and Confirmation Gates

| Level | Operation Type | Default Strategy |
|---|---|---|
| L0 | Read-only queries, information retrieval, pre-checks | Can be executed directly |
| L1 | Create new output without overwriting existing content | Execute after preflight passes |
| L2 | Overwrite output, update fields, modify classification | Show the target and impact scope and obtain explicit confirmation; suggest a backup when feasible |
| L3 | In-place modification, deletion, persistent configuration, installation, sending feedback externally, classification training | Mandatory backup suggestion and explicit confirmation, and honestly state recovery/cancellation capability |

When the target already exists, stop and let the user choose a new name, explicitly overwrite, or cancel. Without a real interface that supports it, do not claim automatic backup, automatic rollback, or cancel-anytime.

### Standard Result Contract

```yaml
status: success | partial | failed | blocked | cancelled
tool_id: module-tool_id
schema_source: runtime | unavailable
preflight:
  status: passed | failed | unknown
outputs: []
validation:
  status: passed | failed | unknown
warnings: []
errors: []
next_action: null
```

Only report `success` when the tool returns success and output validation passes; partial success in batch processing must be reported as `partial` with each item listed. Fill unknown information as `unknown`; do not fabricate.
