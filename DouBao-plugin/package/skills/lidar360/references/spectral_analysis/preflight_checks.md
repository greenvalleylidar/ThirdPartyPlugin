# Preflight Check Flow

## Mandatory Checks

The following checks apply to all spectral analysis tools and must be completed before any operation:

| Check Item | Requirement | Verification Method | Notes |
|-------|------|---------|------|
| Imagery format | tif/tiff/img/dat/hdr | Schema `suffix_name` comparison | Supported raster formats |
| Band information | Metadata complete | `get_data_information` check `band_count >= 1` | Band numbers, wavelength info readable |
| Coordinate system | Defined | `get_data_information` check `coordinate_system` is non-empty | Projection information complete |
| Cloud coverage | <20% | Manual confirmation (no tool directly returns cloud coverage) | Or cloud effects already removed |

---

## Tool Execution

### Vegetation / Water / Building / Burn Indices

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `ndvi` | Multi-band imagery + red band + near-infrared band | "Please load imagery first" / "Band does not exist" |
| `savi` | Multi-band imagery + red band + near-infrared band | "Please load imagery first" / "Band does not exist" |
| `ndwi` | Multi-band imagery + green band + near-infrared band | "Please load imagery first" / "Band does not exist" |
| `ndbi` | Multi-band imagery + near-infrared band + shortwave infrared band | "Please load imagery first" / "Band does not exist" |
| `nbr` | Multi-band imagery + near-infrared band + shortwave infrared band | "Please load imagery first" / "Band does not exist" |
| `vegetation_index_calculator` | Multi-band imagery + index selection + required bands | "Please load imagery first" / "Band mismatch" |

### General Index Calculators

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `normalized_index_calculator` | Multi-band imagery + index selection + required bands | "Please load imagery first" / "Band mismatch" |
| `spectral_index_calculator` | Multi-band imagery + index selection + required bands | "Please load imagery first" / "Band mismatch" |
| `geology_and_mineral_index_calculator` | Multi-band imagery + index selection + required bands | "Please load imagery first" / "Band mismatch" |

### Spectral Preprocessing

| Tool | Check Item | Verification Method | Failure Message |
|-----|--------|---------|---------|
| `composite_multispectral_images` | Multispectral imagery root directory + subdirectory list | File system check | "Directory does not exist" / "Subdirectory is invalid" |
| `extract_spectral_subset` | Multi-band imagery + band numbers valid | `get_data_information` check `band_count` | "Please load imagery first" / "Band number out of range" |
| `savitzky_golay` | Imagery valid + window parameters reasonable | `get_data_information` check `code == 0` + schema numeric range validation | "Imagery is invalid" / "Parameters out of range" |
| `minimum_noise_fraction` | Multi-band imagery + band count >= 3 | `get_data_information` check `band_count >= 3` | "Please load imagery first" / "Insufficient band count" |

### Dimensionality Reduction and Classification

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `principal_component_analysis` | Multi-band imagery + band count >= 3 + NoData handled | "Please load imagery first" / "Insufficient band count" |
| `classify_by_spectral_angle_mapper` | Multi-band imagery + spectral library + band matching + maximum_angle > 0 | "Please load imagery first" / "Spectral library does not exist" / "Band mismatch" |

### Mask Tools

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `build_mask` | Vector file exists + region/attribute selection valid | "Vector file does not exist" / "Attribute is invalid" |

---

## Other

### Common Error Handling

| Error | Cause | Solution |
|-----|------|---------| 
| Result is all NoData | Band mismatch | Check band numbers |
| Abnormal values | Not corrected | Check preprocessing steps |
| Poor classification results | Improper angle threshold | Adjust maximum_angle |
| Out of memory | Data too large | Reduce sampling rate |
