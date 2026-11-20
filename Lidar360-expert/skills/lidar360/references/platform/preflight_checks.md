# Preflight Check Flow

## Mandatory Checks

The following checks apply to all tools and workflows and must be completed before any operation:

1. Confirm file paths exist and are accessible
2. Confirm input data format matches tool requirements
3. Check input layers, windows, projects, or parameter prerequisites according to the corresponding tool check items in this document
4. Execute the target tool
5. Check whether the output file path exists; if so, call get_data_information to obtain file information and verify that data type, extent, count, bands, or other key fields meet expectations

---

## Tool Execution

### Layer Operations

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `load_layer` | File path is valid + file type matches | "File does not exist" / "File type mismatch" |
| `remove_layer` | Layer is loaded + layer_id is valid | "Layer not loaded" / "Layer ID is invalid" |
| `get_layer_details` | Layer is loaded | "Layer not loaded" |
| `zoom_windows_to_layer` | Layer is loaded + window exists | "Layer not loaded" / "Window does not exist" |

### Window Operations

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `close_window` | Window exists + window ID is valid | "Window does not exist" |
| `camera_roaming` | Window exists + data is loaded -> `list_loaded_layers`, target URL in `layers[].url` -> PASS | "Window does not exist" / "No data" |
| `control_render_window_view` | Window exists | "Window does not exist" |

### Display Settings

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `set_data_render_color_mode` | Data type supports this mode | "Mode not supported" |
| `set_window_data_render_color_mode` | Window exists + data type supports this mode | "Window does not exist" / "Mode not supported" |
| `set_window_polygon_fill_style` | Window exists + data type is vector | "Window does not exist" / "Only vector data is supported" |

### Project Operations

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `lidar360_project_manage` (action=open) | When opening a project, file exists + format is correct | "Project file does not exist" / "Format error" |

---

## Other

### Preflight Check Tools

| Check Item | check_item Value | Applicable Scenario | Verification Method |
|--------|------------|---------|---------|
| Ground points classified | `preflight_check(check_item=0)` | Before DEM generation | `has_ground_points == true` -> PASS |
| Point cloud normalized | `preflight_check(check_item=1)` | Before point cloud segmentation | `is_normalized_point_cloud == true` -> PASS |
| DEM/DSM valid | `preflight_check(check_item=2)` | Before CHM generation | `is_dem_or_dsm == true` && `is_valid == true` -> PASS |
| TIN valid | `preflight_check(check_item=3)` | Before TIN to DEM conversion | `is_tin == true` && `is_valid == true` -> PASS |

### Data Type Reference Table

| data_type Value | Data Type | Common Formats |
|-----------|---------|---------|
| build_model | Building Model | .libim |
| dem | Digital Elevation Model | .limodel |
| image_project | Image Project | .liaep, .limap, .ligeo, .p4d, .xml |
| panorama | Panorama | .imglist, .lipano |
| point_cloud | Point Cloud | .lidata, .las, .laz, .ply, .pcd, .e57, .asc, .neu, .xyz, .pts, .csv, .txt |
| raster | Raster | .tif, .tiff, .jpg, .jpeg, .bmp, .dat, .hdr, .img |
| table | Table | .csv, .treedb |
| trajectory | Trajectory | .traj, .pos, .txt, .out |
| tree_model | Tree Model | .litree |
| vector | Vector | .shp, .gpkg, .lidpkg, .kml, .dxf |
| osg_model | OSG Model | .osgb, .desc, .ive, .obj |
| surface_mesh | Surface Mesh / TIN | .litin |
| 3dtiles | 3D Tiles | tileset.json, 2dtin.json, 3dtin.json |
