---
name: lidar360-spectral-analysis
description: LiDAR360 spectral analysis module, updated from references/spectral_analysis/tools.md, covering Spectral Indices, Image Processing, Advanced Analysis, Mask and Index Tools.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

# Spectral Analysis Module (spectral_analysis)

> This skill index is synchronized from the Markdown documents under `references/spectral_analysis/`; the tool list is defined by `tools.md`.

---

## Detailed Documentation Index

| Document | Content | View |
|---------|---------|------|
| **Tool Registry** | Tool grouping, functions, input formats and key parameters | `read_file('references/spectral_analysis/tools.md')` |
| **Preflight Check Procedures** | Data, parameters, and dependency conditions to verify before executing tools | `read_file('references/spectral_analysis/preflight_checks.md')` |
| **Typical Examples** | Invocation examples and parameter combinations for common tasks | `read_file('references/spectral_analysis/examples.md')` |

---

## Tool Group Quick Reference

### Spectral Indices
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `ndvi` | NDVI | Multispectral images | red_band, nir |
| `ndwi` | NDWI | Multispectral images | green_band, nir |
| `nbr` | NBR | Multispectral images | swir_band, nir |
| `ndbi` | NDBI | Multispectral images | swir_band, nir |
| `savi` | SAVI | Multispectral images | red_band, nir |
| `vegetation_index_calculator` | Vegetation index calculator | Multispectral images | select_index |

### Image Processing
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `composite_multispectral_images` | Multispectral image compositing | Multiple bands | subdirectory_list |
| `extract_spectral_subset` | Extract spectral subset | Hyperspectral images | select_bands |
| `savitzky_golay` | S-G filtering | Spectral data | left_num, right_num, order, degree |
| `minimum_noise_fraction` | Minimum noise fraction | Hyperspectral images | output_numbands |

### Advanced Analysis
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `principal_component_analysis` | Principal component analysis | Multispectral images | output_numbands |
| `classify_by_spectral_angle_mapper` | Spectral angle classification | Spectral images | select_bands, maximum_angle |
| `geology_and_mineral_index_calculator` | Geology and mineral index calculator | Multispectral images | select_index |

### Mask and Index Tools
| Tool ID | Function | Input Format | Key Parameters |
|---------|----------|-------------|---------------|
| `build_mask` | Build mask | Images | select_areas, select_attributes |
| `normalized_index_calculator` | Normalized index calculator | Multispectral images | select_index |
| `spectral_index_calculator` | Spectral index calculator | Spectral data | select_index |

---

## Preflight Check Index

- General preflight checks
- Index calculation checks
- NDVI/SAVI/Vegetation index
- NDBI (building index)
- NDWI (water index)
- NBR (burn index)
- Advanced analysis checks
- PCA/MNF dimensionality reduction
- SAM classification
- Common issue troubleshooting
- Pre-execution confirmation checklist

---

## Example Index

- Example 1: Vegetation cover monitoring
- Example 2: Urban expansion analysis
- Example 3: Water body extraction
- Example 4: Image dimensionality reduction and classification
- Example 5: Mineral identification
- Example 6: Fire monitoring
- Best practices

---

## Common Parameters Index

| Configuration File | Content | View |
|-------------------|---------|------|
| **File Formats** | Point cloud, raster, vector, model format references | `read_file('references/profiles/file_formats.md')` |
| **Point Cloud Class Codes** | ASPRS/LiDAR360 common class codes | `read_file('references/profiles/class_codes.md')` |
| **Interpolation Methods** | DEM/DSM/raster generation common interpolation methods | `read_file('references/profiles/interpolation.md')` |
| **Scale** | Terrain, contour, and mapping scale references | `read_file('references/profiles/scale.md')` |
| **Spectral Indices** | Spectral index rule references | `read_file('references/profiles/spectral_index_use.md')` |

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

- Quick invocation: `spectral_analysis-toolID`
- Detailed parameters: `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "spectral_analysis-toolID"`
- Before execution, you **must** check the corresponding tool's check items in this module's `preflight_checks.md`. If checks fail, **do not execute** and prompt the user. For multi-step tasks, refer to `examples.md` first.
