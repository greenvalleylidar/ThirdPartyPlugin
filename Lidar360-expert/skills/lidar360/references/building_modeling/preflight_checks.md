# Building Modeling Preflight Check Flow

## Mandatory Checks

The following checks apply to all building modeling tools and must be completed before any operation:

1. Confirm input point cloud, imagery, and footprint are all readable -> `get_data_information` x 3, `code == 0` -> PASS
2. Confirm point cloud, imagery, and footprint use the same coordinate system and have overlapping extents -> `get_data_information` x 3, compare `coordinate_system` and `bounds` -> PASS
3. Check point cloud classification: whether ground point class, building point class, wall/roof supplementary classes exist -> `preflight_check(check_item=0)` check `has_ground_points` and `present_classes`
4. Check imagery type: building footprint extraction must use DOM or three-channel color imagery -> `get_data_information` check `band_count` (DOM=1, color=3)
5. Check whether the output directory exists and is writable -> manual confirmation
6. Execute the modeling tool
7. Validate LiBIM: base height, roof shape, contour fit, attributes and textures -> manual confirmation

---

## Tool Execution

### Auto Create Buildings

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `auto_create_buildings` | Point cloud exists and is readable | "Please select a point cloud file first" |
| `auto_create_buildings` | Footprint exists, format is `.gpkg/.dxf/.shp` | "Missing building footprint file" |
| `auto_create_buildings` | Output path is `.LiBIM` | "Output file format should be LiBIM" |
| `auto_create_buildings` | `ground_class` is non-empty | "Please set the ground class" |
| `auto_create_buildings` | `roof_class` is non-empty | "Please set the roof/building class" |
| `auto_create_buildings` | Point cloud and footprint coordinate systems match, extents overlap | "Point cloud and building footprint coordinate system or extent mismatch" |

### Extract Building Footprint from Image

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `extract_building_footprint_from_image` | Input is DOM or three-channel color imagery | "Input imagery must be DOM or three-channel color imagery" |
| `extract_building_footprint_from_image` | Input format is `.tif/.tiff/.jpg/.png/.jpeg/.bmp` | "Unsupported imagery format" |
| `extract_building_footprint_from_image` | Cannot input single-channel rasters such as DEM/DSM | "Building footprint extraction cannot use single-channel elevation raster" |
| `extract_building_footprint_from_image` | Output path is writable | "Output path is not writable" |
| `extract_building_footprint_from_image` | `area` and `angle_threshold` are valid positive numbers | "Contour filtering or regularization parameters are invalid" |

### Point Cloud Classification Chain

| Check Item | Verification Method | Failure Message |
|--------|---------|---------|
| Point cloud has completed necessary preprocessing; noise and density meet building modeling requirements | `get_data_information` check `point_count > 0` and Z value range is reasonable; manually confirm noise level | "Point cloud quality does not meet modeling requirements" |
| Ground class exists in point cloud, typically class 2 | `preflight_check(check_item=0)` check `has_ground_points == true` | "Missing ground class" |
| Building/roof class exists in point cloud and matches `auto_create_buildings.roof_class` | `get_data_information` check `present_classes` contains target class | "Building or roof class configuration mismatch" |

### Building Model Post-Processing

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `building_attributes_calculate` | LiBIM exists and is writable | "Please select a writable LiBIM file first" |
| `ortho_texture_mapper_for_libim` | LiBIM and DOM coordinate systems match | "Model and DOM coordinate system mismatch" |
| `ortho_texture_mapper_for_libim` | DOM covers building extent | "DOM does not cover building model extent" |
| `oblique_texture_mapper_for_libim` | Oblique imagery project or imagery data exists | "Missing oblique imagery data" |
| `oblique_texture_mapper_for_libim` | `max_oblique_angle` is valid | "Maximum oblique angle parameter is invalid" |

---

## Other

### Quality Check Recommendations

| Stage | Focus | Acceptance Criteria |
|-----|---------|---------| 
| Point cloud denoising | Whether roof sparse points were mistakenly deleted | Roof edges and ridges still retain sufficient points |
| Resampling | Whether building point density was excessively reduced | Small buildings still meet `minimum_points_number` |
| Ground point classification | Whether buildings or trees were mixed into ground | Class 2 represents only bare ground, roads, etc. |
| Building classification | Whether building points are complete | Roof main planes, ridges, wall candidate points are visible |
| Footprint extraction | Whether footprints were missed, incorrectly extracted, or merged | Building outlines are closed, individual buildings are separated, boundaries align with imagery |
| LiBIM output | Whether base height, roof, and contours are reasonable | Model is basically consistent with point cloud and footprint |
| Texture mapping | Whether textures are misaligned, stretched, or missing | Textures cover completely and align with geometry |
