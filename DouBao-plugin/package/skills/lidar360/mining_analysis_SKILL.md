---
name: lidar360-mining-analysis
description: LiDAR360 mining analysis module, updated from references/mining_analysis/tools.md, covering Tunnel Analysis, Surface Analysis, Modeling.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

# Mining Analysis Module (mining_analysis)

> This skill index is synchronized from the Markdown documents under `references/mining_analysis/`; the tool list is defined by `tools.md`.

---

## Detailed Documentation Index

| Document | Content | View |
|---------|---------|------|
| **Tool Registry** | Tool grouping, functions, input formats and key parameters | `read_file('references/mining_analysis/tools.md')` |
| **Preflight Check Procedures** | Data, parameters, and dependency conditions to verify before executing tools | `read_file('references/mining_analysis/preflight_checks.md')` |
| **Typical Examples** | Invocation examples and parameter combinations for common tasks | `read_file('references/mining_analysis/examples.md')` |
| **Detailed Workflows** | Complete business workflows with multi-tool collaboration | `read_file('references/mining_analysis/workflows.md')` |

---

## Tool Group Quick Reference

### Tunnel Analysis
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `extract_tunnel_centerline` | Extract tunnel centerline | TIN model | position, speed_quality |

### Surface Analysis
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `extract_toes_and_crests` | Extract slope toe and crest lines | TIN model | max_slope_angle, min_length, min_slope_angle, save_format |
| `compute_normal_vectors` | Normal vector computation | LiData | orientation, search_radius |

### Modeling
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `surface_reconstruction` | Surface reconstruction | LiData | calculate_vertex_colors, export_format, select_class, tiling_method, type |
| `triangulation_modeling` | Poisson modeling | LiData | resolution, every_node_sample, density |

---

## Preflight Check Index

- Check procedure table
- Tunnel analysis
- Slope analysis
- Modeling and reconstruction
- Vector computation
- Pre-execution check template
- Common error handling

---

## Example Index

- Example 1: Tunnel point cloud cleanup and centerline analysis workflow
- Example 2: Large-scale surface reconstruction workflow for mining areas
- Example 3: Mine slope toe and crest line extraction workflow
- Example 4: Local high-precision surface reconstruction workflow
- Recommended parameter values quick reference
- Suggested tool execution order

---

## Common Parameters Index

| Configuration File | Content | View |
|-------------------|---------|------|
| **File Formats** | Point cloud, raster, vector, model format references | `read_file('references/profiles/file_formats.md')` |
| **Point Cloud Class Codes** | ASPRS/LiDAR360 common class codes | `read_file('references/profiles/class_codes.md')` |
| **Interpolation Methods** | DEM/DSM/raster generation common interpolation methods | `read_file('references/profiles/interpolation.md')` |
| **Scale** | Terrain, contour, and mapping scale references | `read_file('references/profiles/scale.md')` |

---

## Pre-Execution Checklist

> Before invoking a tool, confirm each check below. If any check fails, **do not execute the tool** — prompt the user to resolve the issue first.

### General Checks

| # | Check Item | Verification Method | Pass |
|---|-----------|-------------------|------|
| 1 | Input file path exists and is accessible | `get_data_information` -> `code == 0` | [ ] |
| 2 | Input data format matches tool requirements | Schema `suffix_name` comparison | [ ] |
| 3 | Output path is writable | Manual confirmation | [ ] |

### Results

- [ ] All passed -> Execute tool
- [ ] Some checks failed -> **Do not execute**, prompt user on which checks failed and provide resolution suggestions

---

## Invocation Conventions

- Quick invocation: `mining_analysis-toolID`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "mining_analysis-toolID"`
- Before execution, you **must** check the corresponding tool's check items in this module's `preflight_checks.md`. If checks fail, **do not execute** and prompt the user. For multi-step tasks, refer to `examples.md` first.
