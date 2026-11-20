# MCP Tool Usage Guide

This document details the usage of the `mcp-tool.exe` tool, including command examples and programming language invocation methods.



## Basic Usage

### Command Syntax

```bash
mcp-tool.exe <command> [arguments]
```

---

## Available Commands

### 1. detect_mcp - Detect MCP Service

**Function**: Detect the currently available LiDAR360 MCP service

#### Usage Example

```bash
mcp-tool.exe detect_mcp
```

#### Output Example

```json
http://127.8.9.10:30000/mcp
```



### 2. list_tools - List All Tools

**Function**: List all available tools on the MCP server with their basic descriptions

#### Usage Example

```bash
# Use default server address
mcp-tool.exe -url "http://127.8.9.10:30000/mcp" list_tools
```

#### Output Example

```json
{
  "tools": [
    {
      "name": "terrain_analysis-generate_general_dem_from_pointcloud",
      "description": "Generate Digital Elevation Model (DEM) from point cloud",
      "inputSchema": {
        "type": "object",
        "properties": {...}
      }
    },
    {
      "name": "pointcloud_classification-classify_ground_by_progressive_tin_densification",
      "description": "Point cloud ground point classification (Progressive TIN Densification)",
      "inputSchema": {...}
    }
  ]
}
```

---

### 3. get_tool_schema - Get Detailed Tool Schema

**Function**: Get the complete parameter definitions, data types, required parameters, etc. for a specific tool

#### Usage Examples

```bash
# Get DEM generation tool schema
mcp-tool.exe -url "http://127.8.9.10:30000/mcp" get_tool_schema "terrain_analysis-generate_general_dem_from_pointcloud"

# Get point cloud classification tool schema
mcp-tool.exe -url "http://127.8.9.10:30000/mcp" get_tool_schema "pointcloud_classification-classify_ground_by_progressive_tin_densification"
```

#### Output Example

```json
{
  "name": "terrain_analysis-generate_general_dem_from_pointcloud",
  "description": "Generate Digital Elevation Model (DEM) from point cloud",
  "inputSchema": {
    "type": "object",
    "properties": {
      "input_data": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Input point cloud file path"
      },
      "output_data": {
        "type": "string",
        "description": "DEM output file path"
      },
      "from_class": {
        "type": "array",
        "items": {"type": "integer"},
        "description": "Point cloud class codes (ground points)"
      },
      "x_size": {
        "type": "number",
        "description": "X direction resolution"
      },
      "y_size": {
        "type": "number",
        "description": "Y direction resolution"
      },
      "interpolator": {
        "type": "integer",
        "description": "Interpolation method: 0-IDW, 1-Kriging, 2-TIN",
        "enum": [0, 1, 2]
      },
      "fill_holes": {
        "type": "boolean",
        "description": "Whether to fill holes"
      }
    },
    "required": ["input_data", "output_data"]
  }
}
```

#### Typical Uses

- View all parameters supported by a tool
- Understand parameter data types and value ranges
- Identify required and optional parameters
- Get detailed parameter descriptions

---

### 4. call_tool - Invoke a Tool

**Function**: Actually invoke a specified tool to execute a data processing task

#### Basic Syntax

```bash
mcp-tool.exe  -url "http://127.8.9.10:30000/mcp" call_tool <tool_name> '<JSON_parameters>'
```

#### Usage Examples

**Example 1: Generate DEM from point cloud**

```bash
mcp-tool.exe  -url "http://127.8.9.10:30000/mcp" call_tool "terrain_analysis-pointcloud_to_dem" '{
  "pointcloud_files": ["/data/raw.lidata"],
  "dem_files": "/output/dem.tif",
  "from_class": 2,
  "x_size": 0.5,
  "y_size": 0.5,
  "interpolator": 1,
  "fill_holes": true
}'
```

**Example 2: Point cloud ground point classification**

```bash
mcp-tool.exe  -url "http://127.8.9.10:30000/mcp" call_tool "pointcloud_classification-classify_ground_points" '{
  "input_data": "/data/raw.lidata",
  "output_data": "/data/classified.lidata",
  "filter_method": 0
}'
```

**Example 3: Generate contours**

```bash
mcp-tool.exe  -url "http://127.8.9.10:30000/mcp" call_tool "terrain_analysis-generate_contour_from_pointcloud" '{
  "input_data": "/data/classified.lidata",
  "output_data": "/output/contours.shp",
  "from_class": 2,
  "scale": "1:5000",
  "major_spacing": 10,
  "basic_spacing": 5,
  "minor_spacing": 1
}'
```

#### Output Example

```json
{
  "code": 0,
  "message": "Tool executed successfully",
  "output": {
    "dem_file": "/output/dem.tif",
    "statistics": {
      "width": 1000,
      "height": 1000,
      "cell_size": 0.5,
      "data_range": [100.5, 200.3]
    }
  }
}
```

#### Error Response Example

```json
{
  "code": -1,
  "message": "Execution failed: file does not exist /data/raw.lidata",
  "output": null
}
```

---

## Advanced Usage

### Batch Processing

#### 1. View and Save All Available Tools

```bash
# Save tool list to file
mcp-tool.exe -url "http://127.8.9.10:30000/mcp" list_tools > available_tools.json

# Format output (if jq is installed)
mcp-tool.exe -url "http://127.8.9.10:30000/mcp" list_tools | jq . > available_tools_formatted.json
```

#### 2. Get and Save Tool Schema

```bash
# Save schema to file
mcp-tool.exe -url "http://127.8.9.10:30000/mcp" get_tool_schema "terrain_analysis-generate_general_dem_from_pointcloud" > dem_tool_schema.json

# View specific tool parameters
mcp-tool.exe -url "http://127.8.9.10:30000/mcp" get_tool_schema "terrain_analysis-generate_general_dem_from_pointcloud" | jq '.inputSchema.properties'
```
