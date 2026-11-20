# LiDAR360 Tool Plugin Examples

## Example 1: Point Cloud Denoising (Single File Input/Output + Algorithm Parameters)

### metadata.json

```json
{
    "interface": {
        "name": "pointcloud_outlier_removal",
        "title": "Point Cloud Denoising",
        "description": "Remove noise points while preserving point cloud geometric information to improve point cloud data quality",
        "version": "1.0.0",
        "category": "pointcloud_processing",
        "keywords": ["PointCloud", "PointCloud Outlier Removal", "removal noise"]
    },
    "input_schema": {
        "type": "object",
        "description": "Point cloud denoising parameters",
        "properties": {
            "neighbor_points": {
                "type": "integer",
                "title": "Neighborhood Points",
                "description": "number of neighborhood points",
                "default": 10,
                "example": 10
            },
            "standard_deviation_multiples": {
                "type": "number",
                "title": "Standard Deviation Multiples",
                "description": "standard deviation multiples",
                "default": 5.0,
                "example": 5.0
            }
        },
        "required": [],
        "input_data": {
            "type": "file",
            "name": "input_data",
            "title": "Input Point Cloud File",
            "description": "point cloud file path",
            "suffix_name": ["lidata"],
            "required": true
        },
        "output_data": {
            "type": "file",
            "name": "output_data",
            "title": "Output Point Cloud File",
            "description": "Point cloud file path after outlier removal",
            "suffix_name": ["lidata"],
            "required": true
        }
    },
    "output_schema": {
        "type": "object",
        "description": "Point cloud denoising result",
        "properties": {
            "count": {
                "type": "integer",
                "title": "Removed Point Count",
                "description": "Number of outliers removed"
            }
        },
        "required": ["count"],
        "output_data": {
            "type": "file",
            "name": "output_data",
            "title": "Output Point Cloud File",
            "description": "Point cloud file path after outlier removal",
            "suffix_name": ["lidata"],
            "required": true
        }
    }
}
```

### pointcloud_outlier_removal.py

```python
from typing import Callable, Dict, List, Any, Optional, Tuple
import json


def execute(input: dict, progress_callback: Callable[[float, str], bool]) -> Tuple[int, dict, str]:
    """
    Point cloud denoising processing
    Remove noise points while preserving point cloud geometric information to improve data quality
    """
    try:
        # Get input parameters
        input_data = input.get("input_data")
        output_data = input.get("output_data")
        neighbor_points = input.get("neighbor_points", 10)
        std_dev_multiples = input.get("standard_deviation_multiples", 5.0)

        # Step 1: Load point cloud data
        if not progress_callback(0.1, "Loading point cloud data..."):
            return 1, {}, "Operation cancelled by user"
        # TODO: Load point cloud file
        # point_cloud = load_point_cloud(input_data)

        # Step 2: Execute denoising algorithm
        if not progress_callback(0.3, "Executing denoising algorithm..."):
            return 1, {}, "Operation cancelled by user"
        # TODO: Call denoising algorithm
        # result_cloud, removed_count = denoise(point_cloud, neighbor_points, std_dev_multiples)

        # Step 3: Save results
        if not progress_callback(0.8, "Saving result file..."):
            return 1, {}, "Operation cancelled by user"
        # TODO: Save processed point cloud
        # save_point_cloud(result_cloud, output_data)

        # Step 4: Complete
        if not progress_callback(1.0, "Processing complete"):
            return 1, {}, "Operation cancelled by user"

        removed_count = 0  # TODO: Replace with actual removed point count
        return 0, {"count": removed_count, "output_data": output_data}, ""

    except Exception as e:
        return 1, {}, str(e)
```

---

## Example 2: Vector Clipping Raster (Multiple File Input + Directory Output + Multiple File Output)

### metadata.json

```json
{
    "interface": {
        "name": "raster_clip_by_vector_file",
        "title": "Clip Raster by Vector File",
        "description": "Clip raster data using polygon vector files",
        "version": "v1",
        "category": "raster_clip",
        "keywords": ["RasterTools", "RasterClipByVectorFile", "clip raster"]
    },
    "input_schema": {
        "type": "object",
        "cpp_class": "RasterClipByVectorFileParameter",
        "description": "Vector file clip raster data parameters",
        "properties": {
            "buffer": {
                "type": "number",
                "title": "Buffer Size",
                "description": "Buffer size",
                "default": 5,
                "minimum": 0
            },
            "layer_name": {
                "type": "string",
                "title": "Layer Name",
                "description": "Layer name",
                "example": "polygon"
            },
            "filed_name": {
                "type": "string",
                "title": "Field Name",
                "description": "Field used as output filename, optional",
                "example": "fid"
            }
        },
        "required": ["layer_name"],
        "input_data": [
            {
                "type": "file",
                "name": "raster_file",
                "title": "Input Raster File",
                "description": "Input raster file path",
                "suffix_name": ["tif", "tiff", "img"],
                "required": true
            },
            {
                "type": "file",
                "name": "vector_file",
                "title": "Input Vector File",
                "description": "Input vector file path",
                "suffix_name": ["shp", "kml", "geojson"],
                "required": true
            }
        ],
        "output_data": {
            "type": "dir",
            "name": "output_dir",
            "title": "Output Directory",
            "description": "Output clipped result file directory; if empty, uses the input raster file directory",
            "required": true,
            "example": "D:/test/raster_clip_output"
        }
    },
    "output_schema": {
        "type": "object",
        "cpp_class": "RasterClipByVectorFileResult",
        "description": "Vector file clip raster data execution result",
        "properties": {
            "result": {
                "type": "string",
                "title": "Clip Result",
                "description": "Clip result"
            }
        },
        "required": ["result"],
        "output_data": {
            "type": "multifile",
            "name": "output_data",
            "title": "Output Clipped Result Files",
            "description": "Output clipped result raster file data list",
            "suffix_name": ["tif", "tiff", "img"],
            "required": true
        }
    }
}
```

### raster_clip_by_vector_file.py

```python
from typing import Callable, Dict, List, Any, Optional, Tuple
import json
import os


def execute(input: dict, progress_callback: Callable[[float, str], bool]) -> Tuple[int, dict, str]:
    """
    Vector file clipping raster data
    Clip raster data using polygon vector files
    """
    try:
        # Get input parameters (when input_data is an array, look up by name field)
        input_data_list = input.get("input_data", [])
        raster_file = next((item for item in input_data_list if isinstance(item, dict) and item.get("name") == "raster_file"), {}).get("path")
        vector_file = next((item for item in input_data_list if isinstance(item, dict) and item.get("name") == "vector_file"), {}).get("path")
        output_dir = input.get("output_data")
        layer_name = input.get("layer_name")
        buffer_size = input.get("buffer", 5)
        filed_name = input.get("filed_name", "")

        # If output directory is not specified, use the input raster file directory
        if not output_dir:
            output_dir = os.path.dirname(raster_file)

        # Step 1: Load raster data
        if not progress_callback(0.1, "Loading raster data..."):
            return 1, {}, "Operation cancelled by user"
        # TODO: Load raster file
        # raster_data = load_raster(raster_file)

        # Step 2: Load vector data
        if not progress_callback(0.3, "Loading vector data..."):
            return 1, {}, "Operation cancelled by user"
        # TODO: Load vector file
        # vector_data = load_vector(vector_file, layer_name)

        # Step 3: Execute clipping
        if not progress_callback(0.5, "Executing clipping operation..."):
            return 1, {}, "Operation cancelled by user"
        # TODO: Execute clipping
        # result_files = clip_raster_by_vector(raster_data, vector_data, buffer_size, output_dir)

        # Step 4: Save results
        if not progress_callback(0.8, "Saving result file..."):
            return 1, {}, "Operation cancelled by user"
        # TODO: Result files saved

        # Step 5: Complete
        if not progress_callback(1.0, "Processing complete"):
            return 1, {}, "Operation cancelled by user"

        result_files = []  # TODO: Replace with actual output file list
        return 0, {"result": "Clipping complete", "output_data": result_files}, ""

    except Exception as e:
        return 1, {}, str(e)
```

---

## Example 3: Point Cloud Resampling (Enum Parameters + Conditional Parameters)

### metadata.json

```json
{
    "interface": {
        "name": "point_cloud_resampling",
        "title": "Point Cloud Resampling",
        "cpp_class": "PointCloudResampling",
        "category": "pointcloud_processing",
        "description": "Resample point cloud using a chosen method to reduce unnecessary point count and lower computational burden for other functions",
        "version": "1.0.0",
        "keywords": []
    },
    "input_schema": {
        "type": "object",
        "cpp_class": "PointCloudResamplingParameter",
        "properties": {
            "sampling_type": {
                "type": "integer",
                "title": "Sampling Type",
                "description": "Sampling type: 1=minimum spatial spacing; 2=random by sampling rate; 3=octree",
                "default": 1,
                "example": 1,
                "enum": [1, 2, 3]
            },
            "point_spacing": {
                "type": "number",
                "title": "Minimum Spacing",
                "description": "Minimum spacing (valid when sampling_type=1)",
                "default": 0.0,
                "example": 0.0
            },
            "sampling_rate": {
                "type": "number",
                "title": "Sampling Rate",
                "description": "Sampling rate (0.0 - 1.0, valid when sampling_type=2)",
                "default": 0.9999
            },
            "octree_level": {
                "type": "integer",
                "title": "Octree Level",
                "description": "Octree subdivision level (valid when sampling_type=3)",
                "default": 21,
                "example": 21,
                "minimum": 1,
                "maximum": 21
            }
        },
        "required": ["sampling_type"],
        "input_data": {
            "type": "file",
            "name": "input_data",
            "title": "Input Point Cloud File",
            "description": "Point cloud file path for resampling",
            "required": false,
            "suffix_name": ["lidata"]
        },
        "output_data": {
            "type": "file",
            "name": "output_data",
            "title": "Output Point Cloud File",
            "description": "Output resampled point cloud file",
            "required": false,
            "suffix_name": ["lidata"]
        }
    },
    "output_schema": {
        "type": "object",
        "cpp_class": "PointCloudResamplingResult",
        "properties": {},
        "required": [],
        "output_data": {
            "type": "file",
            "name": "output_data",
            "title": "Output Point Cloud File",
            "description": "Output resampled point cloud file",
            "required": false,
            "suffix_name": ["lidata"]
        }
    }
}
```

### point_cloud_resampling.py

```python
from typing import Callable, Dict, List, Any, Optional, Tuple
import json


def execute(input: dict, progress_callback: Callable[[float, str], bool]) -> Tuple[int, dict, str]:
    """
    Point cloud resampling
    Resample point cloud using a chosen method to reduce unnecessary point count and lower computational burden
    """
    try:
        # Get input parameters
        input_file = input.get("input_data")
        output_file = input.get("output_data")
        sampling_type = input.get("sampling_type", 1)
        point_spacing = input.get("point_spacing", 0.0)
        sampling_rate = input.get("sampling_rate", 0.9999)
        octree_level = input.get("octree_level", 21)

        # Step 1: Load point cloud data
        if not progress_callback(0.1, "Loading point cloud data..."):
            return 1, {}, "Operation cancelled by user"
        # TODO: Load point cloud file
        # point_cloud = load_point_cloud(input_file)

        # Step 2: Execute resampling based on sampling type
        if sampling_type == 1:
            if not progress_callback(0.3, f"Executing minimum spacing sampling (spacing={point_spacing})..."):
                return 1, {}, "Operation cancelled by user"
            # TODO: Minimum spatial spacing sampling
            # result_cloud = resample_by_spacing(point_cloud, point_spacing)
        elif sampling_type == 2:
            if not progress_callback(0.3, f"Executing random sampling by rate (rate={sampling_rate})..."):
                return 1, {}, "Operation cancelled by user"
            # TODO: Random sampling by rate
            # result_cloud = resample_by_rate(point_cloud, sampling_rate)
        elif sampling_type == 3:
            if not progress_callback(0.3, f"Executing octree sampling (level={octree_level})..."):
                return 1, {}, "Operation cancelled by user"
            # TODO: Octree sampling
            # result_cloud = resample_by_octree(point_cloud, octree_level)
        else:
            return 1, {}, f"Invalid sampling type: {sampling_type}"

        # Step 3: Save results
        if not progress_callback(0.8, "Saving result file..."):
            return 1, {}, "Operation cancelled by user"
        # TODO: Save resampled point cloud
        # save_point_cloud(result_cloud, output_file)

        # Step 4: Complete
        if not progress_callback(1.0, "Processing complete"):
            return 1, {}, "Operation cancelled by user"

        return 0, {"output_data": output_file}, ""

    except Exception as e:
        return 1, {}, str(e)
```

---

## Example 4: Test Tool (Simplified metadata.json Format)

> **Note**: This example is a simplified format for internal testing, containing the following non-standard fields. Do not use these in production development:
> - `interface.icon`, `interface.toolbox_paths` -- non-standard interface fields
> - `data_type` -- non-standard data field property
>
> This format may not pass `validate_metadata.py` validation and is for reference only.

### metadata.json (Simplified Format)

```json
{
    "input_schema": {
        "input_data": {
            "data_type": "PointCloud",
            "description": "Input point cloud file to process",
            "name": "input_data",
            "required": true,
            "suffix_name": ["lidata"],
            "title": "Point Cloud",
            "type": "file"
        },
        "output_data": {
            "description": "Result folder for algorithm processing output",
            "name": "output_dir",
            "required": true,
            "title": "Output Directory",
            "type": "dir"
        },
        "properties": {
            "algorithm": {
                "description": "Algorithm to use",
                "enum": ["a1", "a2", "a3"],
                "title": "Algorithm",
                "type": "string"
            }
        },
        "required": ["algorithm"],
        "type": "object"
    },
    "interface": {
        "description": "Test tool for verifying plugin loading workflow",
        "icon": "",
        "name": "test_tool",
        "title": "Test Tool",
        "toolbox_paths": ["Data Management/Model Tools"],
        "version": "v1"
    },
    "output_schema": {
        "output_data": {
            "data_type": "Raster",
            "description": "Output result file list",
            "name": "output_raster_files",
            "required": true,
            "suffix_name": ["tif", "tiff", "img"],
            "title": "Output Result Files",
            "type": "multifile"
        },
        "properties": {},
        "required": [],
        "type": "object"
    }
}
```

### test_tool.py

```python
from typing import Callable, Dict, List, Any, Optional, Tuple
import json


def execute(input: dict, progress_callback: Callable[[float, str], bool]) -> Tuple[int, dict, str]:
    try:
        for i in range(1, 11):
            if not progress_callback(i * 0.1, f"Step {i} processing..."):
                return 1, {}, "Cancelled by user"
        return 0, {"result": "success"}, ""
    except Exception as e:
        return 1, {}, str(e)
```

---

## Key Pattern Summary

### Pattern 1: Single File Input -> Single File Output

Applicable to: Point cloud denoising, point cloud resampling, format conversion, etc.

```
input_data: { type: "file", name: "input_data", title: "Input Point Cloud File", suffix_name: ["lidata"] }
output_data: { type: "file", name: "output_data", title: "Output Point Cloud File", suffix_name: ["lidata"] }
```

### Pattern 2: Multiple File Input -> Directory Output + Multiple File Output

Applicable to: Vector clipping raster, batch processing, etc.

```
input_data: [
    { type: "file", name: "raster_file", title: "Input Raster File", suffix_name: ["tif"] },
    { type: "file", name: "vector_file", title: "Input Vector File", suffix_name: ["shp"] }
]
output_data (input): { type: "dir", name: "output_data", title: "Output Directory" }
output_data (output): { type: "multifile", name: "output_data", title: "Output Result Files" }
```

### Pattern 3: Enum Parameters

Applicable to: Multiple algorithm choices, mode switching, etc.

```json
"sampling_type": {
    "type": "integer",
    "title": "Sampling Type",
    "enum": [1, 2, 3],
    "default": 1,
    "description": "1=Method A; 2=Method B; 3=Method C"
}
```

### Pattern 4: Conditional Parameters

Applicable to: Parameters only valid under specific conditions

```json
"point_spacing": {
    "type": "number",
    "title": "Point Spacing",
    "description": "Minimum spacing (valid when sampling_type=1)",
    "default": 0.0
}
```
