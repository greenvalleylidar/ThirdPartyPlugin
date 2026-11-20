# Platform Tools Registration

---

## Project Management
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| lidar360_project_manage | Manage the LiDAR360 project document: open, save, save as, close, or create a new project | liprjx | action |
| get_project_context | Get current project context, including project state, loaded layers, render windows, and related workspace information | - | - |
| recent_files_or_projects | LiDAR360's recently opened files list or project list | - | - |

---

## Layer Management
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| load_layer | Load layer files into the platform and specify a window for rendering and display | layer file path list | data_type |
| remove_layer | Remove specified layers from a target render window, or from all windows when no window is specified | - | layer_ids |
| rename_layer | Rename a loaded layer by layer ID and return the updated layer information(you can only modify the name; the path and file extension cannot be changed) | - | layer_id, new_name |
| list_loaded_layers | List layers currently loaded in the project, including layer identifiers and basic layer information | - | - |
| get_layer_details | Get detailed properties and state for a loaded layer by layer ID | - | layer_id |
| set_selected_layers | Set the current selected layers and return selection status information | - | layer_ids |
| get_data_information | Get data information, the data can be point cloud/raster/vector/treedb/model/trajectory etc.The information includes coordinate system name, classifications, corrdinate extent, band count, wavelength, statistics etc | LiData/LiTin/TIF/IMG/TIFF/LiModel/LiBIM/LiTree/TreeDB/SHP/GPKG/LIAEP | - |

---

## Window Management
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| list_render_windows | List all render scenes in the active project, including scenes whose window views are closed. The opened field indicates whether each scene currently has an open render window view | - | - |
| close_window | Close render window views selected by scope without deleting their project scenes. Closed scenes remain in the project tree and can be reopened. Use applied_to to close selected, all, or current views; window_ids is used when applied_to is selected | - | applied_to |
| zoom_windows_to_layer | Zoom target render windows to the full extent of a specified layer | - | layer_id |
| control_render_window_view | Control render window view actions, including view direction, projection mode, 2D/3D mode, visual effects, window layout, and display options | - | action, applied_to |

---

## Display Settings
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| set_window_point_size | Set point size for layers of a selected data type in target render windows | - | applied_to, data_type, point_size, window_ids |
| set_window_line_width | Set line width for layers of a selected data type in target render windows | - | applied_to, data_type, line_width, window_ids |
| set_window_polygon_fill_style | Set polygon fill, random color, and transparency options for layers of a selected data type in target render windows | - | applied_to, data_type |
| set_data_render_color_mode | Set the render color mode for an input data file by data type. Color modes are validated against the selected data type; point cloud classification mode can optionally apply per-class render rules | LiData/SHP/DXF/LiModel/TIF/IMG/TIFF/CSV/TreeDB | data_type, color_mode |
| set_window_data_render_color_mode | Set the render color mode for layers of a selected data type in target windows. Target windows are controlled by applied_to and window_ids; color modes are validated against the selected data type. Point cloud classification mode can optionally apply per-class render rules | - | applied_to, data_type, color_mode |
| set_window_layer_visibility | Show or hide loaded layers in specified render windows without removing layers or closing windows | - | window_ids, layer_ids, visible |
| set_viewer_background_color | Set the viewer background color using a color string such as a named color or hexadecimal value | - | color |
| set_viewer_background_gradient | Enable or disable gradient rendering for the viewer background | - | - |

---

## Navigation Tools
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| goto_coordinate | Move target render windows to a specified 3D coordinate using X, Y, and Z values | - | applied_to, x, y, z |
| camera_roaming | Roaming allows the virtual camera to move along a route, angle, and speed set by the user, simulating a real-world shooting or walking perspective. It supports drawing, loading camera paths, and adding camera paths by viewport. Optionally records video (mp4) | - | output_data |

---

## System Functions
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| lidar360_software_information | Get LiDAR360 software information, including version number, interface language, and GPU in use | - | - |
| lidar360_updates | Start the LiDAR360 software update workflow. Use `check_for_software_updates` to query available versions and release notes without starting an update | - | - |
| check_for_software_updates | Check whether a newer LiDAR360 software version is available and return current version, latest version, and update notes | - | - |
| lidar360_ui_style | Set the LiDAR360 user interface style | - | style |
| set_ui_panel_visibility | Show or hide LiDAR360 UI panels and keep the ribbon Show/Hide checkbox state synchronized | - | panel_ids, visible |
| submit_feedback_report | Submit a bug report or enhancement request with contact information, problem type, and detailed description | - | name, company, email, problem_type, description, type |

---

## Advanced Tools
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| preflight_check | To Check if task requirements are satisfied, such as requiring input point clouds to contain ground point classifications when extracting DEM from point clouds, and requiring input point clouds to have been normalized for point cloud segmentation, etc | LiData/TIF/TIFF/IMG/LiTin | - |
| control_snapping_settings | Enable, disable, or configure snapping options used by editing and measurement operations | - | operation |
| start_master_node | Start the LiDAR360 distributed-processing master node, connect to configured compute nodes, and schedule processing tasks | Input data | slave_list, input_data |
| start_compute_node | Start the current computer as a LiDAR360 distributed compute node that accepts connections and tasks from the master | - | ip, responser_port, commander_port, receiver_port, sender_port, cache |

---

## Addon Management
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| reload_user_addons | Reload all user-defined addon tools from disk and return the loading result of each addon | - | - |
| list_toolbox_tools | List tools in the toolbox, filtered by category path and tool source (all/user addon/system). Tools without a toolbox path are excluded | - | category, stem_path |

---

## Common Parameter Explanation

### data_type (layer type)
| Value | Type |
|---|------|
| build_model | Building Model (.libim) |
| dem | Digital Elevation Model (.limodel) |
| image_project | Image Project (.liaep/.limap/.ligeo/.p4d/.xml) |
| panorama | Panorama (.imglist/.lipano) |
| point_cloud | Point Cloud (.lidata/.las/.laz/.ply/.pcd/.e57/.asc/.neu/.xyz/.pts/.csv/.txt) |
| raster | Raster (.tif/.tiff/.jpg/.jpeg/.bmp/.dat/.hdr/.img) |
| table | Table (.csv/.treedb) |
| trajectory | Trajectory (.traj/.pos/.txt/.out) |
| tree_model | Tree Model (.litree) |
| vector | Vector (.shp/.gpkg/.lidpkg/.kml/.dxf) |
| osg_model | OSG Model (.osgb/.desc/.ive/.obj) |
| surface_mesh | Surface Mesh / TIN (.litin) |
| 3dtiles | 3D Tiles (tileset.json/2dtin.json/3dtin.json) |

### applied_to (window scope)
| Value | Meaning |
|---|------|
| selected | Selected windows |
| all | All windows |
| current | Current window |

### action (render window view actions)
| Value | Meaning |
|---|------|
| view_direction | Set view direction |
| projection_mode | Set projection mode |
| mode_2d_3d | Switch 2D/3D mode |
| visual_effects | Apply visual effects |
| window_layout | Set window layout |
| display_options | Set display options |

### background_type (viewer background type)
| Value | Type |
|---|------|
| 0 | Solid color |
| 1 | Gradient |
| 2 | Image |
| 3 | Skybox |

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "platform-toolID"
