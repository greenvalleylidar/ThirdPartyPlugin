---
name: tool_plugin_generator
description: Assist users in generating LiDAR360 secondary development tool plugins through interactive Q&A, including metadata.json plugin definition files and {plugin_name}.py code files.
type: code_generation
triggers:
  - Generate tool
  - Create plugin
  - Tool plugin
  - LiDAR360 development
  - Secondary development plugin
  - metadata.json
  - Tool plugin generation
  - Plugin development
---

# LiDAR360 Tool Plugin Generator

> Assist users in generating tool plugins that comply with LiDAR360 secondary development specifications through interactive Q&A.

---

## Applicable Scenarios

- User needs to create a LiDAR360 tool plugin
- User needs to generate a secondary development plugin
- User needs to write tool metadata.json
- User mentions "generate tool", "create plugin", "LiDAR360 development"

## Inapplicable Scenarios

- User only wants to call LiDAR360 MCP tools to process data -> Use module skills
- User needs to write forest tending analysis Hook scripts -> `recipes/forest_tending_script.md`
- User needs automated scripts for batch calling multiple MCP tools -> This feature is not yet implemented; suggest the user refer to `references/profiles/tool_call_conventions.md` to write scripts manually

---

## Execution Specifications

### Generated Files

Each generation produces two files:

1. **metadata.json** -- Plugin definition file
2. **{plugin_name}.py** -- Python code file

### Naming Conventions

| Type | Rule | Example |
|-----|------|---------|
| Plugin name (name) | Lowercase snake_case | `pointcloud_outlier_removal` |
| Parameter field names | Lowercase snake_case | `neighbor_points`, `standard_deviation_multiples` |

**Parameter field naming constraints**:
- Only English letters (a-z, A-Z), digits (0-9), and underscores (_) are allowed
- Must start with an English letter
- No spaces, dots, commas, colons, Chinese characters, or other special symbols

**File parameter naming examples**:
- Input files: `pointcloud_file`, `reference_pointcloud`, `input_pointcloud`, `mask_raster`
- Output files: `classified_pointcloud`, `dem`, `tree_attribute_file`
- Input directories: `input_dir`, `pointcloud_dir`, `tileset_root_dir`
- Output directories: `output_dir`, `pointcloud_dir`, `segmented_dir`

> Note: After the parameter name examples comes the title part. The title usually needs prefixes like "Input" or "Output" to indicate input/output, but the parameter field name itself does not.

**Data field naming rules**:

In `input_schema` / `output_schema`, the JSON keys for data fields follow these rules:

- **The key for input fields must be `input_data`**, whether there is one or multiple inputs
- **The key for output fields must be `output_data`**, whether there is one or multiple outputs
- **For single input/output**, the value is a single object
- **For multiple inputs/outputs**, the value is an array, with each element distinguished by the `name` field
- **Each data field must include a `title` field** for UI display, usually with "Input"/"Output" prefixes

### Data Type Mapping

| JSON Schema Type | Description |
|-----------------|-------------|
| `integer` | Integer (e.g., `10`) |
| `number` | Floating-point number (e.g., `5.0`) |
| `string` | String (e.g., `"polygon"`) |
| `boolean` | Boolean (`true` or `false`) |

| File Type | Description |
|----------|-------------|
| `file` | Single file input/output |
| `multifile` | Multiple file input/output |
| `dir` | Directory input/output |

### Python Code Specification

```python
from typing import Callable, Dict, List, Any, Optional, Tuple
import json


def execute(input: dict, progress_callback: Callable[[float, str], bool]) -> Tuple[int, dict, str]:
    """
    Execute tool functionality

    Args:
        input: Input parameter dictionary
        progress_callback: Progress callback function (progress: float, message: str) -> bool
            - progress: Progress value between 0.0 and 1.0
            - message: Current step description
            - Return value: False means user cancelled, True means continue

    Returns:
        Tuple[int, dict, str]: (status_code, result_dict, error_message)
            - status_code: 0 means success, non-0 means failure
            - result_dict: Contains output fields defined in output_schema
            - error_message: Error description on failure, empty string on success
    """
```

### Referencing the pylidar360 Package

Secondary development tool plugins run in LiDAR360's built-in Python environment. The `pylidar360` package is pre-installed and can be imported directly without additional installation.

#### Package Structure

`pylidar360` is organized into the following submodules by functional domain:

| Submodule | Functional Domain |
|----------|------------------|
| `PointCloudTools` | Point cloud processing (denoising, clipping, resampling, extraction, etc.) |
| `PointCloudClassificationTools` | Point cloud classification |
| `RasterTools` | Raster processing |
| `VectorTools` | Vector processing |
| `TerrainAnalysisTools` | Terrain analysis |
| `Conversion` | Format conversion |
| `Preprocessing` | Data preprocessing |
| `ALSForestTools` | Airborne forestry tools |
| `TLSForestTools` | Terrestrial forestry tools |
| `Building` | Building modeling |
| `ModelTools` | Model tools |
| `Mine` | Mining analysis |
| `Spectral` | Spectral analysis |
| `Photo` | Image processing |
| `Common` | Common tools (attribute tables, etc.) |
| `UAVLiDARQC` | UAV LiDAR quality control |

#### Core Base Classes

| Class | Source | Purpose |
|-------|--------|---------|
| `SchemaBase` | `pylidar360.Base` | Base class for all Parameter / Result, provides `from_json()` / `to_json()` |
| `ToolInterface` | `pylidar360.Base` | Tool interface base class, provides `name()` / `title()` / `get_input_schema()` and other metadata methods |
| `IOData` | `pylidar360.IOData` | File path wrapper, `get_path()` / `set_path()` for single file, `get_paths()` / `set_paths()` for multiple files |

#### Tool Invocation Pattern

Each built-in tool consists of three classes: `{ToolName}Parameter`, `{ToolName}Result`, `{ToolName}ToolInterface`.

Instantiate Parameter to invoke; use when custom pre/post-processing logic is needed:

```python
from pylidar360.PointCloudTools.PointCloudOutlierRemoval import (
    PointCloudOutlierRemovalParameter,
    PointCloudOutlierRemovalToolInterface,
)
from pylidar360.IOData import IOData

def execute(input: dict, progress_callback) -> tuple[int, dict, str]:
    param = PointCloudOutlierRemovalParameter()
    param.from_json(input)
    # from_json handles regular parameters in properties, but does not handle file/dir type fields
    # Manually create IOData objects for input_data / output_data and set paths
    param.input_data = IOData(type="file")
    param.input_data.set_path(input["input_data"])
    param.output_data = IOData(type="file")
    param.output_data.set_path(input["output_data"])

    tool = PointCloudOutlierRemovalToolInterface()
    status, result, error = tool(param, progress_callback)
    return status, result.to_json(), error
```

**Note: Before test invocation, you must set the LIDAR360_HOME environment variable to the parent directory of the python310 folder.**

#### Consulting the API

- When you need to confirm whether a built-in tool exists, or check parameter names and types, read the `.pyi` type stub files in the `pylidar360` package directly. Use the actually exported interfaces as the source of truth.
- Each submodule directory contains `.pyi` files for the corresponding tools, with complete Parameter / Result field definitions.
- When generating invocation code, parameters must be handled strictly according to the tool interface's schema definition.

### Important Notes

1. **Naming uniqueness**: Plugin names and class names must be unique; do not duplicate other plugins
2. **Default values**: Non-required parameters must have default values
3. **Required constraints**: Declare mandatory fields through the `required` array
4. **File suffixes**: File type parameters must explicitly specify suffix lists (lowercase)
5. **Version number**: Use `v1` or `v1.0.0`
6. **Progress callback**: Code should use `progress_callback` appropriately to report progress
7. **Exception handling**: Code should include complete exception handling logic
8. **Status codes**: The status code returned by `execute`, refer to `references/profiles/error_message_handle.md`
9. **Generation location**: Generate under the `custom tools directory`, in a folder named by the `name` field value. The custom tools directory can be obtained via the `platform-lidar360_software_information` tool.

---

## Reference Documents

| Document | Content | View |
|---------|---------|------|
| JSON Schema Specification | Complete metadata.json structure specification, field descriptions, naming rules | `read_file('references/recipes/tool_plugin_generator/json_schema_spec.md')` |
| Code Template | {plugin_name}.py code skeleton template | `read_file('references/recipes/tool_plugin_generator/tool_template.py')` |
| Complete Examples | Multiple actual plugin metadata.json + code examples | `read_file('references/recipes/tool_plugin_generator/examples.md')` |
| Validation Script | metadata.json validity validation tool | `read_file('references/recipes/tool_plugin_generator/validate_metadata.py')` |

---

## Execution Workflow

### Step 1: Collect Basic Information

Ask the user for the following information:

1. **Plugin name** (English, lowercase snake_case, e.g., `pointcloud_denoise`)
2. **Plugin display name** (e.g., `PointCloud Denoise`)
3. **Function description** (e.g., `Point cloud denoising is mainly achieved through statistical filtering, radius filtering, etc., to remove outliers, reduce noise, and preserve key geometric features`)
4. **Function category** (e.g., `pointcloud_processing`, `raster_processing`)

### Step 2: Define Input Parameters

Ask the user about input parameter information:

1. **Input file type**: Single file (file), multiple files (multifile), directory (dir)
2. **Input file suffixes** (e.g., `lidata`, `tif`, `shp`)
3. **Algorithm parameters** (optional): Parameter name, title, type, default value, required, description

### Step 3: Define Output Parameters

Ask the user about output parameter information:

1. **Output file type** (file, multifile, dir)
2. **Output file suffixes**
3. **Output result fields** (optional, e.g., processing statistics)

### Step 4: Generate Files

1. Read `references/recipes/tool_plugin_generator/json_schema_spec.md` to confirm metadata.json structure
2. Read `references/recipes/tool_plugin_generator/tool_template.py` to get the code skeleton
3. Reference patterns in `references/recipes/tool_plugin_generator/examples.md`
4. Generate `metadata.json` and `{plugin_name}.py`
5. Validate against the checklist

### Step 5: Validate metadata.json

**After generating metadata.json, you must run the validation script to check validity**:

```bash
python references/recipes/tool_plugin_generator/validate_metadata.py <metadata.json path>
```

The validation script checks:
- Required fields are complete (interface/input_schema/output_schema)
- Naming conventions (name in lowercase snake_case, valid characters for parameter field names)
- Version number format (must be `v1` or `v1.0.0`)
- Data field naming rules (input_data/output_data as fixed keys)
- Data field title existence
- Whether suffix_name for file type parameters is a lowercase array

If validation fails, fix according to the error messages and re-validate until it passes.

### Step 6: Confirm and Deliver

Confirm the generation results with the user, explain the file locations, then call `platform-reload_user_addons` to reload user custom plugins.

**Reload workflow**:
1. Call `platform-reload_user_addons` to reload all user custom plugins
2. Check the `success` field and `results` array in the return value
3. If loading fails, prompt the user to check plugin format or parameter definitions based on the `message`
4. After successful loading, call `platform-list_toolbox_tools` with `category: "user_addon"` to confirm the new tool is registered in the toolbox

---

## Post-Generation Checklist

- [ ] metadata.json format is correct and passes JSON validation
- [ ] All naming follows conventions (snake_case / camelCase)
- [ ] Non-required parameters have default values
- [ ] File suffixes are all lowercase
- [ ] Python code includes complete exception handling
- [ ] Python code correctly uses progress_callback
- [ ] Return value format is correct (triplet)

---

## Example Index

- **Example 1: Point Cloud Denoising** -- Single file input/output + algorithm parameters -> `references/recipes/tool_plugin_generator/examples.md`
- **Example 2: Vector Clipping Raster** -- Multiple file input + directory output + multiple file output -> `references/recipes/tool_plugin_generator/examples.md`
- **Example 3: Point Cloud Resampling** -- Enum parameters + conditional parameters -> `references/recipes/tool_plugin_generator/examples.md`
- **Example 4: Test Tool** -- Simplified metadata.json format -> `references/recipes/tool_plugin_generator/examples.md`
