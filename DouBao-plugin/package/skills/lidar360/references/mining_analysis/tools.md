# Mining Analysis Tools Registration

---

## Tunnel Analysis

| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| extract_tunnel_centerline | Automatic extraction of tunnel centerline based on triangular network model | OBJ | speed_quality, position |

---

## Surface Analysis

| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| extract_toes_and_crests | Automatic extraction of mine slope line based on triangular network model | OBJ/LiTin | min_slope_angle, max_slope_angle, min_length, save_format |
| compute_normal_vectors | The roadway normal vector is calculated and stored as an additional attribute.Additional attributes will be written to the input file | LiData | search_radius |

---

## Modeling

| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| surface_reconstruction | Use point cloud for surface reconstruction, and generate 3D model file in obj or 3D Tiles format | LiData | minimum_perimeter_of_hole, simplify_to, smooth_iteration, tiling_method, type, node_size, export_format, select_class |
| triangulation_modeling | Use Poisson implicit surface reconstruction to generate OBJ triangulated model from LiData point cloud | LiData | resolution, every_node_sample, density |

---

## Model Builder Default Parameters

### extract_toes_and_crests

| Parameter | Default | Description |
|-----|---------|-------------|
| min_slope_angle | 20 | Minimum slope angle in degrees |
| max_slope_angle | 70 | Maximum slope angle in degrees |
| min_length | 10 | Minimum output line length |
| save_format | 0 | 0 = DXF, 1 = SHP |

---

## Common Parameter Explanation

### Slope Line Extraction

| Parameter | Description | Output impact |
|---|------|---------|
| min_slope_angle | Minimum slope angle in degrees | Higher value removes gentle slope/platform edges but may miss weak benches |
| max_slope_angle | Maximum slope angle in degrees | Lower value suppresses near-vertical noise but may miss steep walls |
| min_length | Minimum toe/crest line length in meters | Higher value removes fragments; lower value keeps small benches |
| save_format | 0 dxf, 1 shp | Selects CAD or GIS output |

### Surface Reconstruction

| Parameter | Values | Description |
|---|------|---------|
| export_format | 0/1 | Outputs OBJ or 3D Tiles 1.1 format |
| tiling_method | 0 point count, 1 side length | Controls large-scene tiling strategy |
| type | 0 adaptive quadtree, 1 adaptive octree | Quadtree suits terrain-like data; octree suits volumetric data |
| select_class | 0-255 class array | Selects point classes participating in reconstruction |

### Centerline Extraction
| Parameter | Values | Description |
|---|------|---------|
| position | 0 Top, 1 Middle, 2 Bottom | Controls whether the output line adheres to the upper, middle, or lower tunnel surface |
| speed_quality | Number | Balance between extraction speed and quality |
---

Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "mining_analysis-toolID"`
