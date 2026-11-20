# Data Conversion Workflows

> Complete processing workflows for LiDAR360 data conversion, including external point cloud ingestion, multi-format point cloud delivery, point-cloud-to-raster delivery, raster standardization, model publishing, and textured terrain model publishing. Use these workflows when a conversion task requires chaining multiple `data_conversion-*` tools or producing a downstream-ready delivery package.

---

## Process Overview

| Scenario | Recommended Process | Key Tools | Solves |
|---------|-------------------|-----------|--------|
| External Point Cloud Ingestion and Web Publishing | LAS/LAZ -> LiData -> 3DTiles | `convert_las_to_lidata`, `convert_point_cloud_to_3dtiles` | Import external point clouds into LiDAR360 format and publish them for web visualization |
| Multi-format Point Cloud Delivery | LiData -> LAS/E57/PLY/ASCII/3DTiles | `convert_point_cloud_to_las`, `convert_point_cloud_to_e57`, `convert_point_cloud_to_ply`, `convert_point_cloud_to_ascii`, `convert_point_cloud_to_3dtiles` | Produce multiple point cloud deliverables from a standard LiData source |
| Point-cloud-to-raster Delivery | LiData -> TIF -> ASCII/IMG/USGS DEM/LiModel | `convert_point_cloud_to_tif`, optional raster conversion tools | Generate raster products from point clouds and export them for GIS/DEM workflows |
| Raster Standardization and Internal Preparation | ASC/IMG/USGS DEM -> TIF -> LiData/LiModel | `convert_asc_to_tif`, `convert_img_to_tif`, `convert_usgs_dem_to_tif`, optional `convert_tif_to_lidata`, `convert_tif_to_limodel` | Normalize external raster formats before LiDAR360 analysis or model use |
| Model Web Publishing and Delivery | LiModel/LiTin/LiTree/LiBIM/OBJ -> 3DTiles or exchange formats | model conversion tools | Publish or deliver terrain, tree, BIM, and general 3D models in target platform formats |
| Textured Terrain Model Publishing | DEM + DOM -> textured LiModel -> 3DTiles/OBJ/OSGB | `convert_to_texture_limodel`, `convert_limodel_to_3dtiles`, `convert_limodel_to_obj`, `convert_limodel_to_osgb` | Create textured terrain models from DEM/DOM and export them for web or modeling platforms |

---

## General Conversion Logic

Use conversion workflows when source formats do not match downstream requirements, when a standard intermediate format is needed, or when one source dataset must be delivered to multiple target platforms.

```text
Source Data -> Standard Intermediate Format -> Target Deliverables -> Verification
```

### Common Input Checks

| Check | Required For | Action |
|------|--------------|--------|
| File suffix matches tool schema | All workflows | Select the matching conversion entry tool |
| Coordinate system and unit are correct | Point cloud, raster, model publishing | Use schema projection/unit parameters or `unit_conversion` when required |
| LiData is available for point cloud exports | Point cloud delivery, point-cloud-to-raster, point cloud 3DTiles | Convert LAS/LAZ to LiData first if needed |
| TIF is available as raster intermediate | Raster delivery and raster-to-model conversion | Convert ASC/IMG/USGS DEM to TIF first |
| Target platform format is known | Delivery workflows | Choose LAS/E57/PLY/ASCII, TIF/IMG/DEM, 3DTiles/OBJ/OSGB/S3M/CityJSON/CityGML/Collada according to recipient requirements |

`unit_conversion` is a reusable optional step before format conversion when source data uses non-target units.

---

## Process 1: External Point Cloud Ingestion and Web Publishing

**Applicable Scenarios**: Import LAS/LAZ point clouds into LiDAR360 internal processing format, then publish the result as 3DTiles for web visualization.

**Flowchart**:

```text
LAS/LAZ -> LiData -> 3DTiles
```

### Input Requirements

- `convert_las_to_lidata.input_data`: `.las` or `.laz` file.
- `convert_point_cloud_to_3dtiles.input_data`: `.lidata` output from Step 1.
- Set coordinate transformation parameters when source and target coordinates differ.

### Detailed Steps

#### Step 1: Convert LAS/LAZ to LiData

```json
{
  "step": 1,
  "description": "Convert external LAS/LAZ point cloud to LiData",
  "tool": "data_conversion-convert_las_to_lidata",
  "input": {
    "input_data": "/data/source.las",
    "output_data": "/output/source.lidata",
    "parse": "xyztiarcuRGBpednNC",
    "transformations_method": 2
  }
}
```

#### Step 2: Convert LiData to 3DTiles

```json
{
  "step": 2,
  "description": "Publish LiData point cloud as 3DTiles",
  "tool": "data_conversion-convert_point_cloud_to_3dtiles",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "from_class": [0, 1, 2, 3, 4, 5, 6],
    "output_data": "/output/source_3dtiles/"
  }
}
```

**Configuration Recommendations**:
- Preserve RGB and classification attributes in `parse` when downstream visualization needs them.
- Use `from_class` to exclude noise or temporary classes from 3DTiles delivery.
- Verify that the 3DTiles folder contains the required tileset entry before publishing.

---

## Process 2: Multi-format Point Cloud Delivery

**Applicable Scenarios**: Produce multiple point cloud delivery formats from one LiData source for different software platforms.

**Flowchart**:

```text
LiData -> LAS / E57 / PLY / ASCII / 3DTiles
```

### Input Requirements

- A processed `.lidata` file.
- Target format list from the recipient or delivery specification.

### Detailed Steps

#### Step 1A: Export LAS

```json
{
  "step": "1A",
  "description": "Export LiData to LAS",
  "tool": "data_conversion-convert_point_cloud_to_las",
  "input": {
    "input_data": "/data/final.lidata",
    "output_data": "/delivery/final.las"
  }
}
```

#### Step 1B: Export E57

```json
{
  "step": "1B",
  "description": "Export LiData to E57",
  "tool": "data_conversion-convert_point_cloud_to_e57",
  "input": {
    "input_data": "/data/final.lidata",
    "from_class": [0, 1, 2, 3, 4, 5, 6],
    "parse": "xyzRGB",
    "output_data": "/delivery/final.e57"
  }
}
```

#### Step 1C: Export PLY

```json
{
  "step": "1C",
  "description": "Export LiData to PLY",
  "tool": "data_conversion-convert_point_cloud_to_ply",
  "input": {
    "input_data": "/data/final.lidata",
    "output_data": "/delivery/final.ply"
  }
}
```

#### Step 1D: Export ASCII

```json
{
  "step": "1D",
  "description": "Export LiData to ASCII",
  "tool": "data_conversion-convert_point_cloud_to_ascii",
  "input": {
    "input_data": "/data/final.lidata",
    "ascii_type": 0,
    "parse": "xyzRGB",
    "output_data": "/delivery/final.txt"
  }
}
```

#### Step 1E: Export 3DTiles

```json
{
  "step": "1E",
  "description": "Export LiData to 3DTiles",
  "tool": "data_conversion-convert_point_cloud_to_3dtiles",
  "input": {
    "input_data": "/data/final.lidata",
    "output_data": "/delivery/final_3dtiles/"
  }
}
```

**Configuration Recommendations**:
- Treat these exports as parallel branches from the same LiData source.
- Use class filters consistently across formats when delivery requires identical point subsets.
- Use ASCII only when a text-based exchange format is explicitly required.

---

## Process 3: Point-cloud-to-raster Delivery

**Applicable Scenarios**: Convert point cloud attributes or elevation values to TIF, then create GIS/DEM/model deliverables from the raster output.

**Flowchart**:

```text
LiData -> TIF -> ASCII / IMG / USGS DEM / LiModel
```

### Input Requirements

- `convert_point_cloud_to_tif.input_data`: `.lidata` file.
- Choose `raster_style`, `cell_value_type`, `x_size`, `y_size`, and `radius` according to the raster product.

### Detailed Steps

#### Step 1: Convert Point Cloud to TIF

```json
{
  "step": 1,
  "description": "Rasterize LiData point cloud to TIF",
  "tool": "data_conversion-convert_point_cloud_to_tif",
  "input": {
    "input_data": "/data/final.lidata",
    "x_size": 1.0,
    "y_size": 1.0,
    "raster_style": 0,
    "cell_value_type": 0,
    "radius": 6,
    "from_class": [2],
    "output_data": "/output/final_dem.tif"
  }
}
```

#### Step 2A: Optional TIF to ASCII

```json
{
  "step": "2A",
  "description": "Export TIF raster to ASCII",
  "tool": "data_conversion-convert_tif_to_ascii",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "output_data": "/delivery/final_dem.asc"
  }
}
```

#### Step 2B: Optional TIF to IMG

```json
{
  "step": "2B",
  "description": "Export TIF raster to IMG",
  "tool": "data_conversion-convert_tif_to_img",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "output_data": "/delivery/final_dem.img"
  }
}
```

#### Step 2C: Optional TIF to USGS DEM

```json
{
  "step": "2C",
  "description": "Export TIF raster to USGS DEM",
  "tool": "data_conversion-convert_tif_to_usgs_dem",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "output_data": "/delivery/final.dem"
  }
}
```

#### Step 2D: Optional TIF to LiModel

```json
{
  "step": "2D",
  "description": "Convert TIF raster to LiModel",
  "tool": "data_conversion-convert_tif_to_limodel",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "output_data": "/delivery/final_dem.limodel"
  }
}
```

**Configuration Recommendations**:
- Use ground class `[2]` for DEM-like raster outputs when available.
- Set smaller `x_size` and `y_size` for finer raster resolution; increase them for faster regional output.
- Run optional export branches only for formats required by the recipient.

---

## Process 4: Raster Standardization and Internal Preparation

**Applicable Scenarios**: Convert external ASC/IMG/USGS DEM rasters to TIF, then prepare LiData or LiModel for LiDAR360 analysis and model workflows.

**Flowchart**:

```text
ASC / IMG / USGS DEM -> TIF -> LiData / LiModel
```

### Input Requirements

- Source raster must be ASC, IMG, or USGS DEM.
- TIF output is the standard intermediate for subsequent raster-to-internal conversion.

### Detailed Steps

#### Step 1A: Convert ASC to TIF

```json
{
  "step": "1A",
  "description": "Convert ASC raster to TIF",
  "tool": "data_conversion-convert_asc_to_tif",
  "input": {
    "input_data": ["/data/source.asc"],
    "output_data": "/output/raster_tif/"
  }
}
```

#### Step 1B: Convert IMG to TIF

```json
{
  "step": "1B",
  "description": "Convert IMG raster to TIF",
  "tool": "data_conversion-convert_img_to_tif",
  "input": {
    "input_data": ["/data/source.img"],
    "output_data": "/output/raster_tif/"
  }
}
```

#### Step 1C: Convert USGS DEM to TIF

```json
{
  "step": "1C",
  "description": "Convert USGS DEM to TIF",
  "tool": "data_conversion-convert_usgs_dem_to_tif",
  "input": {
    "input_data": "/data/source.dem",
    "output_data": "/output/source.tif"
  }
}
```

#### Step 2A: Optional TIF to LiData

Use the TIF highlighted by the selected Step 1 branch:
- ASC branch: `{{step1A.data.output_data[0]}}`
- IMG branch: `{{step1B.data.output_data[0]}}`
- USGS DEM branch: `{{step1C.data.output_data}}`

```json
{
  "step": "2A",
  "description": "Convert standardized TIF to LiData",
  "tool": "data_conversion-convert_tif_to_lidata",
  "input": {
    "input_data": "{{selected_tif}}",
    "select_sampling_center": 1,
    "output_data": "/output/source.lidata"
  }
}
```

#### Step 2B: Optional TIF to LiModel

Use the same `{{selected_tif}}` from the selected Step 1 branch.

```json
{
  "step": "2B",
  "description": "Convert standardized TIF to LiModel",
  "tool": "data_conversion-convert_tif_to_limodel",
  "input": {
    "input_data": "{{selected_tif}}",
    "output_data": "/output/source.limodel"
  }
}
```

**Configuration Recommendations**:
- Choose only one Step 1 branch according to the source raster format.
- Use LiData output when downstream tools expect point-like raster-derived data.
- Use LiModel output when downstream workflows require terrain/model visualization.

---

## Process 5: Model Web Publishing and Multi-format Delivery

**Applicable Scenarios**: Convert LiDAR360 internal models or OBJ models to web publishing formats and target exchange formats.

**Flowchart**:

```text
LiModel / LiTin / LiTree / LiBIM / OBJ -> 3DTiles / OBJ / OSGB / S3M / FBX / CityJSON / Collada
```

### Input Requirements

- Source model type determines the valid conversion tools.
- Choose target formats according to the target platform or delivery specification.

### Common Branches

| Source | Web Publishing | Modeling / Exchange | City / BIM Standards |
|--------|----------------|---------------------|----------------------|
| LiModel | `convert_limodel_to_3dtiles` | `convert_limodel_to_obj`, `convert_limodel_to_osgb`, `convert_limodel_to_s3m`, `convert_limodel_to_tif` | - |
| LiTin | `convert_litin_to_3dtiles` | `convert_litin_to_obj`, `convert_litin_to_osgb`, `convert_litin_to_fbx`, `convert_litin_to_dxf`, `convert_litin_to_landxml` | - |
| LiTree | `convert_litree_to_3dtiles` | `convert_litree_to_obj`, `convert_litree_to_osgb` | `convert_litree_to_cityjson` |
| LiBIM | `convert_libim_to_3dtiles` | `convert_libim_to_obj`, `convert_libim_to_osgb`, `convert_libim_to_fbx`, `convert_libim_to_collada` | `convert_libim_to_cityjson` |
| OBJ | `convert_obj_to_3dtiles` | - | - |

### Example: LiModel to 3DTiles and OBJ

```json
{
  "step": "1A",
  "description": "Convert LiModel to 3DTiles for web publishing",
  "tool": "data_conversion-convert_limodel_to_3dtiles",
  "input": {
    "input_data": "/data/model.limodel",
    "output_data": "/delivery/model_3dtiles/"
  }
}
```

```json
{
  "step": "1B",
  "description": "Convert LiModel to OBJ for modeling software",
  "tool": "data_conversion-convert_limodel_to_obj",
  "input": {
    "input_data": "/data/model.limodel",
    "output_data": "/delivery/model.obj"
  }
}
```

**Configuration Recommendations**:
- Treat model delivery branches as parallel exports from the same source model.
- Use 3DTiles for web/Cesium-style publishing.
- Use OBJ/FBX/Collada for modeling tools; use CityJSON for city model standards.

---

## Process 6: Textured Terrain Model Publishing

**Applicable Scenarios**: Build a textured terrain model from DEM and DOM, then publish or export it to web/modeling formats.

**Flowchart**:

```text
DEM + DOM -> Textured LiModel -> 3DTiles / OBJ / OSGB
```

### Input Requirements

- `input_dem`: DEM `.tif` or `.tiff`.
- `input_dom`: DOM `.tif` or `.tiff` aligned with the DEM.
- Output textured model is `.limodel`.

### Detailed Steps

#### Step 1: Generate Textured LiModel

```json
{
  "step": 1,
  "description": "Map DOM texture to DEM and generate textured LiModel",
  "tool": "data_conversion-convert_to_texture_limodel",
  "input": {
    "input_data": {
      "input_dem": "/data/dem.tif",
      "input_dom": "/data/dom.tif"
    },
    "output_data": "/output/textured_terrain.limodel"
  }
}
```

#### Step 2A: Optional Textured LiModel to 3DTiles

```json
{
  "step": "2A",
  "description": "Publish textured LiModel as 3DTiles",
  "tool": "data_conversion-convert_limodel_to_3dtiles",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "output_data": "/delivery/textured_terrain_3dtiles/"
  }
}
```

#### Step 2B: Optional Textured LiModel to OBJ

```json
{
  "step": "2B",
  "description": "Export textured LiModel to OBJ",
  "tool": "data_conversion-convert_limodel_to_obj",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "output_data": "/delivery/textured_terrain.obj"
  }
}
```

#### Step 2C: Optional Textured LiModel to OSGB

```json
{
  "step": "2C",
  "description": "Export textured LiModel to OSGB",
  "tool": "data_conversion-convert_limodel_to_osgb",
  "input": {
    "input_data": "{{step1.data.output_data}}",
    "output_data": "/delivery/textured_terrain.osgb"
  }
}
```

**Configuration Recommendations**:
- Confirm DEM and DOM coordinate systems and extents match before generating the textured model.
- Use 3DTiles for web publishing and OBJ/OSGB for modeling or 3D platform delivery.

---

## Result Verification Checklist

| Workflow | Verification |
|---------|-------------|
| External point cloud ingestion and web publishing | LiData exists; 3DTiles output folder is complete |
| Multi-format point cloud delivery | All requested output formats exist and use consistent point classes/attributes |
| Point-cloud-to-raster delivery | TIF exists; optional raster/model outputs match requested resolution and format |
| Raster standardization | TIF intermediate exists; LiData/LiModel internal outputs are generated when requested |
| Model web publishing and delivery | Target model formats exist and can be opened by the recipient platform |
| Textured terrain model publishing | Textured LiModel exists; exported web/model formats preserve texture alignment |
