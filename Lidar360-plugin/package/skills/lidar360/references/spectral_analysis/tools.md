# Spectral Analysis Tools Registration
---

## Vegetation and Water Indices
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| ndvi | The most widely used vegetation index | Input data | red_band, nir |
| ndwi | NDWI is sensitive to canopy water content variations | Input data | green_band, nir |
| nbr | This index highlights burned areas | Input data | swir_band, nir |
| ndbi | This index highlights urban areas | Input data | swir_band, nir |
| savi | This index is similar to NDVI, but it suppresses the effects of soil pixels | Input data | red_band, nir |
| vegetation_index_calculator | Vegetation Indices are combinations of surface reflectance at two or more wavelengths designed to highlight a particular property of vegetation | Input data | select_index |

---

## Generic Index Calculators
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| normalized_index_calculator | Compilation of normalized indices | Input data | select_index |
| spectral_index_calculator | Spectral indices are combinations of surface reflectance at two or more wavelengths that indicate relative abundance of features of interest | Input data | select_index |
| geology_and_mineral_index_calculator | Compilation of geology and mineral indices | Input data | select_index |

---

## Spectral Image Preprocessing
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| composite_multispectral-images | Fuse images captured by the multi-camera of the LiPlant device into a single multi-band image | Select the root directory of the multispectral images | subdirectory_list |
| extract_spectral_subset | Image band subset extraction | TIF/TIFF/IMG/DAT/HDR | select_bands |
| savitzky_golay | The Savitzky Golay method is a spectral smoothing and derivative calculation technique based on local polynomial fitting | Input data | left_num, right_num, order, degree, resampling_method, threshold_value |
| minimum_noise_fraction | Minimum noise fraction. The MNF transformation effectively separates signal and noise components through two consecutive orthogonal transformations of the image data | Input data | output_numbands |

---

## Dimensionality Reduction and Classification
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| principal_component_analysis | Principal component analysis.PCA is a linear transformation that reorganizes the variance in a multiband image into a new set of image bands | Input data | output_numbands |
| classify_by_spectral_angle_mapper | Classify by spectral angle mapper.This function is a remote sensing image classification method based on spectral similarity, and determines the geographic category by calculating the angle between the cell spectrum and the reference spectrum.The input spectral library files support TXT files exported from the "View Spectral Library" and "Show Spectral Profile" functions, XML-format ROI files exported by ENVI, as well as GPKG vector files. | Input data | select_bands, maximum_angle |

---

## Mask Tools
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| build_mask | Generate a mask based on the vector file extent | Input data | select_areas, select_attributes |

---

## Common Parameter Explanation

### Common Spectral Bands
| Band | Description | Wavelength Range |
|---|------|---------|
| Blue | Blue band | 450-520 nm |
| Green | Green band | 520-600 nm |
| Red | Red band | 630-690 nm |
| NIR | Near Infrared | 770-890 nm |
| SWIR | Short Wave Infrared | 1550-1750 nm |

### Vegetation Index Ranges
| Index | Typical Range | Interpretation |
|---|------|---------|
| NDVI | -1 to 1 | >0.5: dense vegetation |
| NDWI | -1 to 1 | >0: water bodies |
| NBR | -1 to 1 | Negative: burned areas |
| SAVI | -1 to 1 | Adjusted for soil brightness |

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "spectral_analysis-toolID"
