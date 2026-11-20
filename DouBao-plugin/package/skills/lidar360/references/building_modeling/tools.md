# Building Modeling Tools Registration

---

## Building Creation and Extraction

| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| auto_create_buildings | Automatic batch creation of LOD2 building models from classified point cloud and building footprint | LiData + GPKG/DXF/SHP | roof_class, ground_class |
| extract_building_footprint_from_image | This function uses deep learning to extract building footprints from images. The input file must be a DOM (Digital Orthophoto Image) or a three-channel color image produced by aerial photography, such as an orthophoto image. It cannot be a single-channel image such as a DEM or DSM. The output includes building footprint vector files (SHP) and optional mask files (TIF). The runtime schema description and outputSchema suffix may be inconsistent; verify the current outputSchema before execution. | TIF/TIFF/JPG/PNG/JPEG/BMP | - |

---

## Building Analysis

| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| building_attributes_calculate | The Attribute Calculation function automatically calculates the attributes of building models, such as building height, eave height, base elevation, roof orientation and roof shape based on the input data.The input LiBIM file will be modified and attributes will be written to it | Input data | - |

---

## Texture Mapping

| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| ortho_texture_mapper_for_libim | Texture mapping of the building model (LiBIM) using orthophotos.DOM and LiBIM must be in the same spatial reference system | Input data | - |
| oblique_texture_mapper_for_libim | Texture mapping of the building model (LiBIM) using oblique images | Input data | max_oblique_angle |

---

## Model Builder Default Parameters

### extract_building_footprint_from_image

| Parameter | Default | Description |
|-----|---------|-------------|
| area | 10 | Minimum footprint area |
| angle_threshold | 10 | Regularization angle threshold |
| delete_contours | true | Delete small or invalid contours |
| regularization | true | Regularize extracted contours |
| simplify | true | Simplify output geometry |

### auto_create_buildings

| Parameter | Default | Description |
|-----|---------|-------------|
| ground_class | [0, 1, 2] | Ground classes used for base elevation estimation |
| roof_class | [6, 13, 14] | Roof/building classes used for model generation |

---

## Common Parameter Explanation

### Building class codes

| Value | Class | Usage |
|---|------|-------|
| 1 | Unclassified | Input or fallback class |
| 2 | Ground | Base elevation and height reference |
| 6 | Building | Main building/roof class |
| 13 | Roof supplementary class | Included by Model Builder `roof_class` |
| 14 | Wall | Can be included in `auto_create_buildings.roof_class` when wall points are available |

### Building detection and modeling parameters

| Parameter | Meaning | Tuning advice |
|---|------|---------|
| roof_class | Classes used by `auto_create_buildings` as roof/building evidence | Keep consistent with the input point cloud classification |
| ground_class | Classes used as ground reference | Prefer `[2]` when ground classification is reliable |

### Building Attributes
| Attribute | Description | Unit |
|---|------|------|
| Height | Building height | m |
| Area | Building footprint area | m2 |
| Volume | Building volume | m3 |
| Floor_Area | Floor area | m2 |
| Roof_Type | Roof type | - |

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "building_modeling-toolID"
