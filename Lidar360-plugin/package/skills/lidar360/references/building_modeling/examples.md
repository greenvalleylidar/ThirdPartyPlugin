# Building Modeling Typical Workflow Examples

## Example 1: Automatic Building Creation from Point Cloud & Imagery

```text
Step 1: Prepare a preprocessed and classified point cloud containing at least ground points (2) and building/roof points (6/13/14)
Step 2: Extract building footprints from imagery -> building_modeling-extract_building_footprint_from_image (area=10, regularization=true, simplify=true)
Step 3: Automatically create buildings -> building_modeling-auto_create_buildings (ground_class=[0,1,2], roof_class=[6,13,14])
```

**Prerequisites**: Point cloud is loaded; DOM or three-channel color imagery is ready; both share the same coordinate system and have overlapping extents.
**Output**: LiBIM building model (*.LiBIM).

---

## Example 2: Extract Building Footprints from Imagery Only

```text
Step 1: Load DOM or three-channel color imagery (*.tif, *.tiff, *.jpg, *.png, *.jpeg, *.bmp)
Step 2: Extract building footprints -> building_modeling-extract_building_footprint_from_image (area=10, angle_threshold=10)
Step 3: Inspect and edit footprints
Step 4: Use footprints for automatic modeling or building statistical analysis
```

**Prerequisites**: Input imagery must not be a single-channel elevation raster such as DEM/DSM.
**Output**: Building footprint vector (*.shp, or the footprint format supported by the tool schema).

---

## Example 3: Create LiBIM from Existing Footprints and Classified Point Cloud

```text
Step 1: Prepare a classified point cloud containing at least ground points (2) and building points (6)
Step 2: Prepare building footprints (*.gpkg, *.dxf, *.shp)
Step 3: Automatically create buildings -> building_modeling-auto_create_buildings (ground_class=[2], roof_class=[6,13,14])
```

**Prerequisites**: Footprints and point cloud share the same coordinate system; building outlines are closed and separated per building.
**Output**: LiBIM building model (*.LiBIM).

---

## Example 4: Building Model Attribute Calculation

```text
Step 1: Load LiBIM building model
Step 2: Calculate attributes -> building_modeling-building_attributes_calculate
Step 3: Review attributes such as height, eave height, base elevation, roof orientation, and roof shape
```

**Prerequisites**: The LiBIM file must be writable.
**Output**: Attributes are written back to the input LiBIM file.

---

## Example 5: Orthophoto Texture Mapping

```text
Step 1: Prepare LiBIM building model
Step 2: Prepare DOM orthophoto
Step 3: Orthophoto texture mapping -> building_modeling-ortho_texture_mapper_for_libim
```

**Prerequisites**: DOM and LiBIM must use the same spatial reference, and the DOM must cover the model extent.
**Output**: LiBIM with orthophoto texture.

---

## Example 6: Oblique Imagery Texture Mapping

```text
Step 1: Prepare LiBIM building model
Step 2: Prepare oblique imagery project or image data
Step 3: Oblique texture mapping -> building_modeling-oblique_texture_mapper_for_libim (max_oblique_angle=60)
```

**Prerequisites**: Oblique imagery has completed necessary georeferencing/registration and covers building facades and roofs.
**Output**: LiBIM with oblique imagery texture.

---

## Recommended Parameter Quick Reference

| Stage | Parameter | Recommended Value | Description |
|-----|------|--------|------|
| Footprint extraction | area | 10 | Candidate contours smaller than this area are filtered out |
| Automatic modeling | ground_class | [0, 1, 2] | Model Builder default; use [2] when ground classification is reliable |
| Automatic modeling | roof_class | [6, 13, 14] | Keep consistent with building/roof/wall classification results |

> For detailed workflows, see `references/building_modeling/workflows.md`. For pre-execution checks, see `references/building_modeling/preflight_checks.md`.
