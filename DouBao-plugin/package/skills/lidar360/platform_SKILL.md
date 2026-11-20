---
name: lidar360-platform
description: LiDAR360 platform management module, updated from references/platform/tools.md, covering Project Management, Layer Management, Window Management, Display Settings, Navigation Tools, System Functions, Advanced Tools.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

`lidar360_updates` (installing updates), closing a project with unsaved changes, and `submit_feedback_report` (sending feedback externally) all require explicit L3 confirmation; before submitting feedback, display the outgoing content and remove sensitive information.

# Platform Management Module (platform)

> This skill index is synchronized from the Markdown documents under `references/platform/`; the tool list follows `tools.md`.

---

## Detailed Documentation Index

| Document | Content | View |
|---------|---------|------|
| **Tool Registry** | Tool groups, functions, input formats, and key parameters | `read_file('references/platform/tools.md')` |
| **Preflight Check Workflows** | Data, parameter, and dependency conditions to verify before executing tools | `read_file('references/platform/preflight_checks.md')` |
| **Typical Examples** | Invocation examples and parameter combinations for common tasks | `read_file('references/platform/examples.md')` |

---

## Tool Group Quick Reference

### Project Management
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `lidar360_project_manage` | Manage LiDAR360 project documents: open, save, save as, close, or create new project | liprjx | action, path, save_opened_project |
| `get_project_context` | Get current project context, including project state, loaded layers, render windows, and related workspace information | - | - |
| `recent_files_or_projects` | List of recently opened files or projects in LiDAR360 | - | - |

### Layer Management
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `load_layer` | Load layer files to the platform, specifying render window and display | layer file path list | data_type |
| `remove_layer` | Remove specified layer from target render window (remove from all windows when no window is specified) | - | layer_ids |
| `rename_layer` | Rename a loaded layer by layer ID (can only modify name; path and file extension cannot be changed) | - | layer_id, new_name |
| `list_loaded_layers` | List currently loaded layers in the project, including layer identifiers and basic layer information | - | - |
| `get_layer_details` | Get detailed properties and state of a loaded layer by layer ID | - | layer_id |
| `set_selected_layers` | Set currently selected layers and return selection state information | - | layer_ids |
| `get_data_information` | Get data information (point cloud/raster/vector/treedb/model/trajectory etc.), including coordinate system name, classification, coordinate extent, band count, wavelength, statistics, etc. | LiData/LiTin/TIF/IMG/TIFF/LiModel/LiBIM/LiTree/TreeDB/SHP/GPKG/LIAEP | - |

### Window Management
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `list_render_windows` | List all render scenes in the active project, including scenes with closed window views. The opened field indicates whether each scene currently has an open render window view | - | - |
| `close_window` | Close render window views by scope without deleting their project scenes. Closed scenes remain in the project tree for reopening (use applied_to to close selected, all, or current view; window_ids used when applied_to is selected) | - | applied_to |
| `zoom_windows_to_layer` | Zoom target render windows to the full extent of the specified layer | - | layer_id |
| `control_render_window_view` | Control render window view operations, including view direction, projection mode, 2D/3D mode, visual effects, window layout, and display options | - | action, applied_to |

### Display Settings
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `set_window_point_size` | Set point size for selected data type layers in target render windows | - | applied_to, data_type |
| `set_window_line_width` | Set line width for selected data type layers in target render windows | - | applied_to, data_type |
| `set_window_polygon_fill_style` | Set polygon fill, random color, and transparency options for selected data type layers in target render windows | - | applied_to, data_type |
| `set_data_render_color_mode` | Set render color mode for input data files by data type (color mode is validated against selected data type; point cloud classification mode can optionally apply per-class render rules) | LiData/SHP/DXF/LiModel/TIF/IMG/TIFF/CSV/TreeDB | data_type, color_mode |
| `set_window_data_render_color_mode` | Set render color mode for selected data type layers in target windows (target windows controlled by applied_to and window_ids; color mode is validated against selected data type) | - | applied_to, data_type, color_mode |
| `set_window_layer_visibility` | Show or hide loaded layers in specified render windows without removing layers or closing windows | - | window_ids, layer_ids, visible |
| `set_viewer_background_color` | Set viewer background color using color string (e.g., named color or hex value) | - | color |
| `set_viewer_background_gradient` | Enable or disable gradient rendering for viewer background | - | - |

### Navigation Tools
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `goto_coordinate` | Move target render window to specified 3D coordinates using X, Y, and Z values | - | applied_to, x, y, z |
| `camera_roaming` | Roaming allows virtual camera to move along user-defined path, angle, and speed, simulating real shooting or walking viewpoints. Supports drawing, loading camera paths, and adding camera paths via viewport. Optionally record video (mp4) | - | output_data |

### System Functions
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `lidar360_software_information` | Get LiDAR360 software information, including version number, UI language, and GPU in use | - | - |
| `lidar360_updates` | Launch LiDAR360 software update workflow. Use `check_for_software_updates` to query available versions and release notes | - | - |
| `check_for_software_updates` | Check if a newer LiDAR360 software version is available, returns current version, latest version, and update notes | - | - |
| `lidar360_ui_style` | Set LiDAR360 user interface style | - | style |
| `set_ui_panel_visibility` | Show or hide LiDAR360 interface panels and sync ribbon show/hide checkbox state | - | panel_ids, visible |
| `submit_feedback_report` | Submit error reports or enhancement requests with contact information, problem type, and detailed description | - | name, company, email, problem_type, description, type |

### Advanced Tools
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `preflight_check` | Check if task requirements are met, e.g., extracting DEM from point cloud requires input point cloud to contain ground point classification; point cloud segmentation requires input point cloud to be normalized | LiData/TIF/TIFF/IMG/LiTin | - |
| `control_snapping_settings` | Enable, disable, or configure snapping options used by editing and measuring operations | - | operation |
| `start_master_node` | Start master node | Input data | slave_list, input_data |
| `start_compute_node` | Start slave node | - | ip, responser_port, commander_port, receiver_port, sender_port, cache |

### Addon Management
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `reload_user_addons` | Reload all user-defined plugin tools from disk, returns loading result for each plugin | - | - |
| `list_toolbox_tools` | List tools in the toolbox, filterable by category path and tool source (all/user plugins/system) | - | category, stem_path |

---

## Data Tree Semantics and Tool Selection

- "LiDAR360 directory tree", "data tree", "layer tree", "project tree" as well as `layer tree`, `project tree`, `Data Management tree` refer to the loaded objects in the current LiDAR360 project by default, and are not equivalent to the disk directory.
- To query currently loaded, selected or visible layers, prefer calling `list_loaded_layers`, and follow its runtime schema and returned fields; when querying details of a single loaded layer, call `get_layer_details`.
- `get_project_context` is only used for tasks that require project-level comprehensive context; you must not assume its opaque `data` object contains tree node fields not declared in the runtime schema.
- `set_selected_layers` is only used when the user explicitly requests to change selection state, and must not be used as a query tool or called to fulfill read-only requests.
- Existing tools can only reliably describe the objects they actually return; if the user requests the complete UI tree structure, unloaded nodes, node hierarchy or expansion state while the runtime schema does not provide them, you should clearly state the capability boundary, and must not complete by scanning the disk, guessing paths or invoking Shell.

---

## Preflight Check Index

- Check workflow table
- Layer operations
- Window operations
- Display settings
- Project operations
- Preflight check tools
- Pre-execution check template
- Data type reference table
- Window naming rules

---

## Example Index

- Example 1: Data loading and display workflow
- Example 2: Multi-window comparison analysis
- Example 3: Project management workflow
- Example 4: DEM generation preflight check
- Example 5: Vector data display settings
- Example 6: Distributed processing startup
- Recommended parameter values quick reference
- Common issue troubleshooting

---

## Common Parameters Index

| Configuration File | Content | View |
|-------------------|---------|------|
| **File Formats** | Point cloud, raster, vector, model format references | `read_file('references/profiles/file_formats.md')` |
| **Point Cloud Class Codes** | ASPRS/LiDAR360 common class codes | `read_file('references/profiles/class_codes.md')` |
| **Interpolation Methods** | Common interpolation methods for DEM/DSM/raster generation | `read_file('references/profiles/interpolation.md')` |
| **Scale** | Terrain, contour, and mapping scale references | `read_file('references/profiles/scale.md')` |

---

## Pre-Execution Checklist

> Before invoking a tool, confirm each of the following checks. If any check fails, **do not execute the tool** — prompt the user to resolve first.

### General Checks

| # | Check Item | Verification Method | Pass |
|---|-----------|-------------------|------|
| 1 | Input file path exists and is accessible | `get_data_information` -> `code == 0` | [ ] |
| 2 | Input data format matches tool requirements | schema `suffix_name` comparison | [ ] |
| 3 | Output path is writable | Manual confirmation | [ ] |

### Result

- [ ] All passed -> Execute tool
- [ ] Some items failed -> **Do not execute**, prompt user on which checks failed and resolution suggestions

---

## Invocation Convention

- Quick invocation: `platform-toolID`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "platform-toolID"`
- Before execution, you **must** check the corresponding tool's check items in this module's `preflight_checks.md`. If checks fail, **do not execute** and prompt the user; for multi-step tasks, refer to `examples.md` first.
