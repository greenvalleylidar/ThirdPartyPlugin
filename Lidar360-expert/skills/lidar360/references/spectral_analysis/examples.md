# Spectral Analysis Typical Workflow Examples

## Example 1: Vegetation Cover Monitoring

```
Step 1: Build mask (optional) -> Build_Mask
Step 2: Calculate NDVI -> NDVI
Step 3: Result analysis
  - >0.6: High coverage vegetation
  - 0.3-0.6: Medium coverage
  - 0-0.3: Sparse vegetation
  - <0: Non-vegetation areas
```

**Call**: `spectral_analysis-ndvi(input_data="image", red_band=1, nir=2, output_data="output")`

---

## Example 2: Urban Expansion Analysis

```
Step 1: Prepare multi-temporal images
Step 2: Calculate NDBI -> NDBI
Step 3: Extract built-up areas (NDBI>0)
Step 4: Multi-temporal comparison analysis
```

**Call**: `spectral_analysis-ndbi(input_data="image", swir_band=1, nir=2, output_data="output")`

---

## Example 3: Water Body Extraction

```
Step 1: Calculate NDWI -> NDWI
Step 2: Extract water bodies (NDWI>0)
Step 3: Vectorize results
```

**Call**: `spectral_analysis-ndwi(input_data="image", green_band=1, nir=2, output_data="output")`

---

## Example 4: Image Dimensionality Reduction and Classification

```
Step 1: Spectral smoothing -> Savitzky_Golay
Step 2: Extract subset -> Extract_Spectral_Subset
Step 3: MNF transformation -> Minimum_Noise_Fraction
Step 4: PCA dimensionality reduction -> Principal_Component_Analysis
Step 5: SAM classification -> Classify_by_Spectral_Angle_Mapper
```

**PCA call**:
```
spectral_analysis-principal_component_analysis(
    input_data="image", output_numbands=3, output_data="output")
```

**SAM call**:
```
spectral_analysis-classify_by_spectral_angle_mapper(
    input_data="PCA result", mode=1, input_spectral_lib="spectral library",
    maximum_angle=0.1, select_bands=[1,2,3], output_data="output")
```

---

## Example 5: Mineral Identification

```
Step 1: Spectral smoothing -> Savitzky_Golay
Step 2: Calculate mineral indices -> Geology_And_Mineral_Index_Calculator
Step 3: MNF dimensionality reduction -> Minimum_Noise_Fraction
Step 4: SAM classification -> Classify_by_Spectral_Angle_Mapper
```

**Mineral index call**:
```
spectral_analysis-geology_and_mineral_index_calculator(
    input_data="image", select_index=["Clay Alteration Index"],
    output_data="output")
```

---

## Example 6: Fire Monitoring

```
Step 1: Pre-fire -> NBR(input_data="pre-fire image")
Step 2: Post-fire -> NBR(input_data="post-fire image")
Step 3: Calculate difference dNBR = NBR_pre - NBR_post
Step 4: Fire severity classification
```

---

## Best Practices

| Step | Recommendation |
|-----|------|
| Data preparation | Ensure atmospheric correction is completed |
| Band selection | Confirm bands according to index requirements |
| Mask application | Exclude clouds, shadows, and other interference |
| Result validation | Validate with ground truth data |
