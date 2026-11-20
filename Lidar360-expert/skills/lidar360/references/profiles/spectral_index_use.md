# Spectral Index Selection Rules

> This rule base is used by AI Agents to automatically match the most appropriate spectral index based on user requirements.

---

## I. Decision Index (Quick Lookup by Requirement Keywords)

| User Requirement Keywords | Recommended Index Group |
|---|---|
| Vegetation cover / Greenness / Biomass | NDVI, EVI, SAVI, GNDVI, VARI, GLI |
| Chlorophyll content | GCI, LCI, MCARI, MCARI2, TCARI, CRI1, CRI2 |
| Vegetation water / Water stress | MSI, NDII, NDWI, WBI, LWVI1, LWVI2, NDMSI |
| Nitrogen content | NDNI, RENDVI, MRESR |
| Anthocyanin / Carotenoid | ARI1, ARI2, CRI1, CRI2, SIPI, NPCI |
| Vegetation stress / Senescence / Disease | PSRI, PRI, SIPI, VREI1, VREI2, REPI |
| Leaf Area Index | LAI, EVI |
| Forest cover | FCI1, FCI2, NDVI |
| Fire / Burned area | BAI, NBR, NBRT1 |
| Water body extraction | NDWI, MNDWI, SWI, WRI, WV-WI |
| Snow and ice monitoring | NDSI |
| Built-up area / Urban | NDBI, WV-BI, WV-NHFD |
| Drought monitoring | NMDI, MSI, NDMSI |
| Soil adjustment / Sparse vegetation | SAVI, OSAVI, MSAVI2, GSAVI, GOSAVI |
| Mineral exploration - Alunite/Clay | ALUI, CLAI, KAI1, KAI2, KAI3, MONI |
| Mineral exploration - Carbonate | CALI, CARI, DOLI, MGAI |
| Mineral exploration - Iron minerals | FEAI, FEI, FMR, IOR, WV-II |
| Mineral exploration - Hydroxyl alteration | OHI1, OHI2, OHI3, PHAI, PRAI |
| Mineral exploration - Sulfate | SULI |
| Mineral exploration - Siliceous/Quartz | QSRI, QRRI, SIDI |
| Mineral exploration - Muscovite | MUSI, PHEI |
| Mineral exploration - Magnesite | MAGI |
| Mineral exploration - Montmorillonite | MONI |
| Laterization / Weathering crust | LATI |
| Lignin / Cellulose / Litter | CAI, LCAI, NDLI |
| Residue / Stubble cover | CAI |
| Aquaculture pond / Mudflat | NDPI, NDMI |
| Photosynthesis efficiency | PRI |
| WorldView sensor-specific | WV-BI, WV-VI, WV-II, WV-NHFD, WV-SI, WV-WI |
| Atmosphere-resistant | ARVI, GARI, EVI, VARI |
| High biomass / Anti-saturation | EVI, WDRVI, MSR, MRESR |
| Red-edge band analysis | RENDVI, MRENDVI, MRESR, REPI, VREI1, VREI2 |
| Global-scale monitoring | GEMI |
| Urban sparse vegetation | TDVI, MTVI, MTVI2 |
| Visible light RGB imagery | VARI, GLI |

---

## II. Detailed Index Rules

### A. Vegetation Monitoring

#### A1. General Vegetation Indices

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Normalized Difference Vegetation Index | NDVI | nir, red | Vegetation monitoring (most common) | -1 to 1; >0.6 dense vegetation; 0.2-0.6 moderate; 0-0.2 sparse; <0 water/bare soil |
| Enhanced Vegetation Index | EVI | nir, red, blue | Vegetation monitoring (high biomass areas) | >0.5 high coverage, 0.2-0.5 moderate, <0.2 sparse/bare soil; atmosphere-resistant, less prone to saturation |
| Difference Vegetation Index | DVI | nir, red | Vegetation monitoring (general) | High values indicate lush vegetation; sensitive to soil background; no fixed threshold |
| Simple Ratio | SR | nir, red | Vegetation monitoring (simple ratio) | >2.0 dense vegetation, 1.0-2.0 moderate, <1.0 sparse/non-vegetation |
| Infrared Percentage Vegetation Index | IPVI | nir, red | Vegetation monitoring (percentage form) | 0-1; >0.5 vegetation dominant |
| Non-Linear Index | NLI | nir, red | Vegetation monitoring (non-linear) | >0.5 high, 0.2-0.5 moderate |
| Renormalized Difference Vegetation Index | RDVI | nir, red | Vegetation monitoring (renormalized) | >0.5 high, 0.2-0.5 moderate; between DVI and NDVI |
| Modified Simple Ratio | MSR | nir, red | Vegetation monitoring (modified ratio) | >1.0 vegetation; high coverage can exceed 5; improves SR saturation issues |
| Modified Non-Linear Index | MNLI | nir, red | Vegetation monitoring (non-linear) | >0.5 high coverage, 0.2-0.5 moderate |
| Global Environmental Monitoring Index | GEMI | red, nir | Global vegetation monitoring | >0.4 good vegetation coverage; global scale with reduced atmospheric influence |
| Wide Dynamic Range Vegetation Index | WDRVI | nir, red | Vegetation monitoring (wide dynamic range) | >0.2 high coverage, 0-0.2 moderate, <0 non-vegetation |
| Forest Cover Index 1 | FCI1 | red, rededge | Forestry (forest cover) | Proportional to canopy density; uses red-edge features to enhance vegetation signal |
| Forest Cover Index 2 | FCI2 | red, nir | Forestry (forest cover) | Proportional to canopy density; combines near-infrared to enhance canopy response |

#### A2. Soil-Adjusted (For Sparse Vegetation / Bare Soil Background)

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Soil Adjusted Vegetation Index | SAVI | nir, red | Arid area vegetation (soil-adjusted) | >0.5 high coverage, 0.2-0.5 moderate, <0.2 sparse/bare soil; L=0.5 |
| Optimized Soil Adjusted Vegetation Index | OSAVI | nir, red | Agriculture (optimized soil-adjusted) | >0.5 high coverage, 0.16-0.5 moderate, <0.16 sparse/bare soil |
| Modified Soil Adjusted Vegetation Index 2 | MSAVI2 | nir, red | Arid area vegetation (soil-adjusted) | >0.5 good, 0.2-0.5 moderate, <0.2 sparse; adaptive L factor |
| Green Soil Adjusted Vegetation Index | GSAVI | nir, green | Agriculture/Ecology (soil-adjusted) | >0.5 high coverage |
| Green Optimized Soil Adjusted Vegetation Index | GOSAVI | nir, green | Agriculture (sparse vegetation) | >0.5 high coverage, 0.2-0.5 moderate, <0.2 sparse |

#### A3. Green Band Vegetation Indices (More Sensitive to Chlorophyll)

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Green Normalized Difference Vegetation Index | GNDVI | nir, green | Vegetation monitoring (green band normalized) | >0.5 lush, 0.2-0.5 moderate, <0.2 sparse/bare soil |
| Green Difference Vegetation Index | GDVI | nir, green | Vegetation monitoring (green band) | Increases with vegetation coverage |
| Green Ratio Vegetation Index | GRVI | nir, green | Vegetation monitoring (simple ratio) | >1.0 green vegetation; high vegetation can exceed 5 |
| Green Leaf Index | GLI | red, green, blue | Agriculture (green leaf coverage) | >0 green leaves, approximately 0 bare soil, <0 non-green |
| Green Vegetation Index | GVI | tm1-tm7 | Geology/Vegetation (K-T transform) | Positive = vegetation; soil/water approximately 0 or negative |
| Sum Green Index | SGI | sumgreen, nbandsgreen | Vegetation monitoring (green band sum) | Proportional to green coverage |

#### A4. Atmosphere-Resistant

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Atmospherically Resistant Vegetation Index | ARVI | w800w, w680, w450 | Vegetation monitoring (atmosphere-resistant) | >0.5 lush, 0.2-0.5 moderate, 0-0.2 sparse, <0 bare soil/water |
| Green Atmospherically Resistant Index | GARI | nir, red, green, blue | Vegetation monitoring (atmosphere-resistant + green band) | >0.5 high vegetation, 0.2-0.5 moderate, <0.1 bare soil/water |
| Visible Atmospherically Resistant Index | VARI | red, green, blue | Vegetation monitoring (visible light) | >0 vegetation, <0 non-vegetation; >0.1 prominent green vegetation; applicable to RGB imagery |

#### A5. Triangular Method / Modified

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Triangular Vegetation Index | TVI | w550, w680, w750w | Vegetation monitoring (triangular method) | >10 healthy, 5-10 moderate, <5 sparse/stressed |
| Modified Triangular Vegetation Index | MTVI | nir, red, green | Vegetation monitoring (triangular method) | >0.3 good |
| Modified Triangular Vegetation Index - Improved | MTVI2 | nir, red, green | Vegetation monitoring (improved triangular method) | >0.5 high, 0.2-0.5 moderate |
| Transformed Difference Vegetation Index | TDVI | nir, red | Urban vegetation (transformed DVI) | 0-1; >0.5 high, 0.2-0.5 moderate; sensitive to urban sparse vegetation |

#### A6. Red-Edge Vegetation Indices (Highly Sensitive to Chlorophyll and Nitrogen)

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Red Edge Normalized Difference Vegetation Index | RENDVI | w750n, w705 | Precision agriculture (red-edge NDVI) | >0.5 high, 0.3-0.5 moderate, <0.3 low |
| Modified Red Edge NDVI | MRENDVI | w750w, w705, w445 | Vegetation monitoring (red-edge improved) | >0.5 high, 0.2-0.5 moderate; includes blue band correction |
| Modified Red Edge Simple Ratio | MRESR | w750w, w445, w705 | Vegetation monitoring (red-edge ratio) | >2.0 high health, <1.5 possible stress |
| Red Edge Position Index | REPI | w670, w795, rededge, w740 | Vegetation physiology (red-edge position) | Healthy approximately 0.72um; <0.715 indicates stress (blue shift) |
| Vogelmann Red Edge Index 1 | VREI1 | w740, w720 | Vegetation stress (red-edge) | >1.5 healthy, <1.0 possible stress |
| Vogelmann Red Edge Index 2 | VREI2 | w734, w747, w715w, w726 | Vegetation stress (red-edge) | >0 indicates health, negative values indicate stress |

---

### B. Vegetation Physiology and Biochemistry

#### B1. Chlorophyll Content

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Green Chlorophyll Index | GCI | nir, green | Agriculture (chlorophyll content) | >1.5 high chlorophyll, 1.0-1.5 moderate, <1.0 low |
| Leaf Chlorophyll Index | LCI | w850, w710, w680 | Agriculture (leaf chlorophyll) | >0.5 high, 0.2-0.5 moderate, <0.2 low |
| Modified Chlorophyll Absorption Ratio Index | MCARI | w700, w680, w550 | Agriculture (chlorophyll absorption) | >0 indicates chlorophyll; higher values indicate greater concentration |
| Modified Chlorophyll Absorption Ratio Index - Improved | MCARI2 | w800n, w680, w550 | Agriculture (improved chlorophyll) | >0.2 high, 0.1-0.2 moderate, <0.1 low |
| Transformed Chlorophyll Absorption Reflectance Index | TCARI | w550, w680, w700 | Precision agriculture (chlorophyll) | >0.1 high chlorophyll; TCARI/OSAVI >0.7 high chlorophyll |
| Triangular Greenness Index | TGI | centerred, centergreen, centerblue, red, green, blue | Vegetation physiology (chlorophyll) | >0 chlorophyll present, negative values non-vegetation |

#### B2. Anthocyanin and Carotenoid

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Anthocyanin Reflectance Index 1 | ARI1 | w550, w700 | Vegetation physiology (anthocyanin content) | >0.001 indicates anthocyanin accumulation |
| Anthocyanin Reflectance Index 2 | ARI2 | w800n, w550, w700 | Vegetation physiology (anthocyanin content) | >0 indicates anthocyanin accumulation |
| Carotenoid Reflectance Index 1 | CRI1 | w510, w550 | Vegetation physiology (carotenoid) | >0 indicates stress |
| Carotenoid Reflectance Index 2 | CRI2 | w510, w700 | Vegetation physiology (carotenoid) | >0 indicates stress |
| Normalized Pigment Chlorophyll Index | NPCI | w680, w430 | Agriculture (pigment-chlorophyll ratio) | >0.1 may indicate stress/senescence |
| Structure Independent Pigment Index | SIPI | w800n, w445, w680 | Vegetation physiology (pigment) | >1.0 stress/senescence; <1.0 healthy; insensitive to canopy structure |

#### B3. Nitrogen Content

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Normalized Difference Nitrogen Index | NDNI | w1510, w1680 | Agriculture (nitrogen content) | >0 indicates abundant nitrogen |

#### B4. Photosynthesis Efficiency

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Photochemical Reflectance Index | PRI | w531, w570 | Vegetation photosynthesis efficiency | >0.02 high photosynthetic efficiency; <0 stress |

#### B5. Vegetation Senescence / Stress

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Plant Senescence Reflectance Index | PSRI | w680, w500, w750w | Agriculture/Ecology (vegetation senescence) | >0.5 obvious senescence/maturity; <0.2 healthy green |
| Red Green Ratio Index | RGRI | sumred, sumgreen, nbandsgreen, nbandsred | Vegetation/Geology (red-green ratio) | >1 indicates iron oxide or yellowing vegetation dominance |

#### B6. Leaf Area Index

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Leaf Area Index | LAI | nir, red, blue | Agriculture/Ecology (leaf area index) | <1 sparse, 1-3 moderate, >3 closed canopy, >7 very rare; unit m2/m2 |

---

### C. Vegetation Water

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Moisture Stress Index | MSI | w1599, w819 | Vegetation water stress | >1.0 water stress, <1.0 sufficient water |
| Normalized Difference Infrared Index | NDII | w819, w1649 | Vegetation water (NIR-SWIR) | >0.3 sufficient water, 0-0.3 moderate, <0 stress |
| Normalized Difference Moisture Index | NDMSI | nir, swir1 | Soil/Vegetation moisture | >0 sufficient water, <0 drought |
| Leaf Water Vegetation Index 1 | LWVI1 | w1094, w983 | Vegetation water (leaf water content) | >0 normal water, approximately 0 or negative = drought |
| Leaf Water Vegetation Index 2 | LWVI2 | w1094, w1205 | Vegetation water (leaf water content) | Same as LWVI1 |
| Water Band Index | WBI | w970, w900 | Vegetation water (water absorption band) | >0.95 sufficient water, <0.9 possible stress |
| Normalized Multiband Drought Index | NMDI | w860, w1640, w2130 | Drought monitoring (multiband) | >0.4 sufficient water, 0.2-0.4 moderate drought, <0.2 severe drought |
| Disease Water Stress Index | DWSI | nir, green, swir1, red | Agriculture (disease/water stress) | Increases with stress; no unified threshold |

---

### D. Water Bodies and Snow/Ice

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Normalized Difference Water Index | NDWI | w857, midir | Water body extraction / Vegetation moisture | >0 water/high moisture; >0.2 pure water body; <0 vegetation/bare soil |
| Modified Normalized Difference Water Index | MNDWI | green, swir1 | Water body extraction / Urban water systems | >0 water; >0.2 confirmed water body; buildings <0; suppresses building noise |
| Simple Water Index | SWI | blue, swir1 | Water body extraction (simplified) | >0.5 may indicate clean water |
| Water Ratio Index | WRI | green, red, nir, swir1 | Water/Wetland (water ratio) | >1.0 indicates open water/wetland |
| Normalized Difference Snow Index | NDSI | green, swir1 | Snow and ice monitoring | >0.4 snow/ice; 0.2-0.4 ice-water mix; <0.2 no snow |
| Normalized Difference Pond Index | NDPI | green, swir1 | Aquaculture/Wetland (aquaculture ponds) | >0.1 possible aquaculture pond; >0.2 confirmed water body |
| Normalized Difference Mud Index | NDMI | w795, w990 | Coast/Beach (sediment) | >0 indicates turbid water/mudflat |
| WorldView Water Index | WV-WI | wv2coastal, wv2nir2 | Water body extraction (WorldView water) | >0 indicates water |

---

### E. Fire Monitoring

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Burn Area Index | BAI | nir, red | Fire monitoring (burned area mapping) | >0 burned area; burned areas typically >10, unburned <0 |
| Normalized Burn Ratio | NBR | tm4, tm7 | Fire monitoring (burn severity) | Healthy vegetation >0.3; after fire <0.1; dNBR >0.66 high severity |
| Normalized Burn Ratio Thermal 1 | NBRT1 | nir, swir1, thermal | Fire monitoring (with thermal infrared) | Reference NBR; incorporates thermal infrared to improve detection of residual combustion |

---

### F. Urban and Built-Up

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Normalized Difference Built-Up Index | NDBI | tm5, tm4 | Urban remote sensing (built-up area) | >0 built-up area, <0 vegetation; urban core >0.1 |
| WorldView Built-Up Index | WV-BI | wv2coastal, wv2rededge | Urban remote sensing (WorldView built-up) | >0 indicates built-up area; designed for WorldView-2 |
| WorldView Non-Homogeneous Feature Difference | WV-NHFD | wv2rededge, wv2coastal | Urban/Land use (heterogeneity) | >0 high heterogeneity, <0 homogeneous |

---

### G. Mineral Exploration and Geology

#### G1. Hydroxyl-Bearing Minerals / Clay Alteration

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Alunite Index | ALUI | w2165, w2260, w2330 | Mineral exploration (alunite identification) | >1.0 may indicate alunite |
| Clay Alteration Index | CLAI | w1650, w2165, w2205 | Mineral exploration (clay alteration) | >1.0 may indicate clay minerals |
| Kaolinite Index 1 | KAI1 | w2300, w2165 | Mineral exploration (kaolinite) | >1.0 may indicate kaolinite |
| Kaolinite Index 2 | KAI2 | w1650, w2165, w2205, w2330 | Mineral exploration (kaolinite) | >0.5 may indicate kaolinite |
| Kaolinite Index 3 | KAI3 | w1650, w2205, w2260 | Mineral exploration (kaolinite) | >1.0 may indicate kaolinite |
| Montmorillonite Index | MONI | w1650, w2205, w2260 | Mineral exploration (montmorillonite) | >1.0 may indicate montmorillonite |
| Hydroxyl-Bearing Altered Minerals Index 1 | OHI1 | w1650, w2205, w2260 | Mineral exploration (hydroxyl alteration) | >1.0 may indicate hydroxyl alteration |
| Hydroxyl-Bearing Altered Minerals Index 2 | OHI2 | w1650, w2205, w2260 | Mineral exploration (hydroxyl alteration) | >0 may indicate hydroxyl alteration |
| Hydroxyl-Bearing Altered Minerals Index 3 | OHI3 | w1650, w2165, w2260 | Mineral exploration (hydroxyl alteration) | >0 may indicate hydroxyl alteration |
| Phyllic Alteration Index | PHAI | w2165, w2205, w2260 | Mineral exploration (phyllic alteration) | >1.0 may indicate phyllic alteration |
| Propylitic Alteration Index | PRAI | w2260, w2330, w2395 | Mineral exploration (propylitic alteration) | >1.0 may indicate propylitic alteration zone |
| Muscovite Index | MUSI | w2205, w2300 | Mineral exploration (muscovite) | >1.0 may indicate muscovite |
| Phengitic Index | PHEI | w2165, w2205 | Mineral exploration (phengitic muscovite) | >1.0 may indicate phengitic muscovite |

#### G2. Carbonate Minerals

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Calcite Index | CALI | w2205, w2330, w2395 | Mineral exploration (calcite identification) | >1.0 may indicate calcite |
| Carbonate Index | CARI | w10600, w11300 | Mineral exploration (carbonate rock identification) | >1.0 may indicate carbonate rock |
| Dolomite Index | DOLI | w2205, w2300, w2330 | Mineral exploration (dolomite identification) | >1.0 may indicate dolomite |
| Magnesite Index | MAGI | w2205, w2260, w2330, w2395 | Mineral exploration (magnesite) | >1.0 may indicate magnesite |
| MgOH-Carbonate Abundance Index | MGAI | w2205, w2330, w2395 | Mineral exploration (magnesium-bearing carbonate) | >1.0 may indicate magnesium-bearing carbonate |

#### G3. Iron Minerals

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Ferric Iron Alteration Index | FEAI | w560, tm3, w820, w2165 | Mineral exploration (ferric iron alteration) | >1.0 may indicate Fe3+ alteration |
| Ferrous Iron (Fe2+) Index | FEI | w560, tm3, w820, w2165 | Mineral exploration (ferrous iron minerals) | >1.0 may indicate Fe2+ minerals |
| Ferrous Minerals Ratio | FMR | tm5, tm4 | Mineral exploration (iron-bearing minerals) | >1.0 indicates iron-bearing minerals may be enriched |
| Ferrous Silicates Index | FESI | w1650, w2165 | Mineral exploration (iron-bearing silicates) | >1.0 indicates iron-bearing silicates |
| Iron Oxide Ratio | IOR | tm3, tm1 | Geological survey (iron oxides) | >1.0 indicates iron oxide enrichment |
| Clay Minerals Ratio | CMR | tm5, tm7 | Geological survey (clay minerals) | >1.0 indicates higher clay content |

#### G4. Siliceous / Quartz Minerals

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Quartz/Siliceous Rocks Index | QSRI | w8300, w8650, w9100 | Mineral exploration (quartz/siliceous rock) | >1.0 may indicate quartz/siliceous rock |
| Quartz Rich Rocks Index | QRRI | w9100, w11300 | Mineral exploration (quartzite) | >1.0 may indicate quartz enrichment |
| Silica Dioxide Index | SIDI | w9100, w10600 | Mineral exploration (silicon dioxide) | >1.0 may indicate siliceous rock/acidic rock |

#### G5. Sulfate Minerals

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Sulfate Index | SULI | w8300, w8650, w9100 | Mineral exploration (sulfate) | >1.0 may indicate sulfate minerals |

#### G6. Other Geological Indices

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Epidote/Chlorite/Amphibole Index | ECAI | w2205, w2300, w2330, w2395 | Mineral exploration (epidote/chlorite/amphibole) | >1.0 may indicate mineral assemblage |
| Laterite Index | LATI | w560, w1650 | Geology/Soil (laterization) | >1.0 may indicate laterization |

---

### H. Vegetation Residue / Organic Matter

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| Cellulose Absorption Index | CAI | w2000, w2200, w2100 | Vegetation residue / Soil organic matter | >0.5 indicates residue cover |
| Lignin Cellulose Absorption Index | LCAI | w2205, w2165, w2330 | Vegetation residue (lignin/cellulose) | >0 indicates dry vegetation/woody residue |
| Normalized Difference Lignin Index | NDLI | w1754, w1680 | Vegetation residue (lignin) | >0 indicates high lignin content |

---

### I. WorldView Sensor-Specific Indices

| Full Name | Abbreviation | Required Bands | Application | Value Meaning and Thresholds |
|---|---|---|---|---|
| WorldView Built-Up Index | WV-BI | wv2coastal, wv2rededge | Urban remote sensing (WorldView built-up) | >0 indicates built-up area |
| WorldView Improved Vegetative Index | WV-VI | wv2nir2, wv2redcenter | Vegetation monitoring (WorldView improved) | >0.3 high vegetation coverage |
| WorldView New Iron Index | WV-II | wv2green, wv2yellow, wv2blue | Mineral exploration (WorldView iron index) | >0.001 may indicate iron minerals |
| WorldView Non-Homogeneous Feature Difference | WV-NHFD | wv2rededge, wv2coastal | Urban/Land use (heterogeneity) | >0 high heterogeneity, <0 homogeneous |
| WorldView Soil Index | WV-SI | wv2green, wv2yellow | Soil monitoring (WorldView soil) | >0 indicates bare soil |
| WorldView Water Index | WV-WI | wv2coastal, wv2nir2 | Water body extraction (WorldView water) | >0 indicates water |

---

## III. Agent Selection Logic Rules

### Rule 1: Primary Classification by Application Domain

```
IF user requirement contains "vegetation" OR "greenness" OR "coverage" -> Enter Category A
IF user requirement contains "chlorophyll" OR "pigment" OR "anthocyanin" -> Enter Category B
IF user requirement contains "water" OR "drought" OR "stress" -> Enter Category C
IF user requirement contains "water body" OR "water area" OR "snow/ice" -> Enter Category D
IF user requirement contains "fire" OR "burned" OR "combustion" -> Enter Category E
IF user requirement contains "building" OR "urban" OR "impervious surface" -> Enter Category F
IF user requirement contains "mineral" OR "geology" OR "alteration" -> Enter Category G
IF user requirement contains "litter" OR "residue" OR "lignin" -> Enter Category H
IF user specifies "WorldView" sensor -> Enter Category I
```

### Rule 2: Filter by Data Conditions

```
IF only RGB three bands -> Recommend VARI, GLI
IF has nir + red -> Recommend NDVI, SAVI, EVI, etc.
IF has green band -> Recommend GNDVI, GCI, MNDWI, etc.
IF has red-edge band -> Recommend RENDVI, MRENDVI, VREI1, etc.
IF has shortwave infrared (SWIR) -> Recommend NBR, NDII, MNDWI, etc.
IF has thermal infrared -> Recommend NBRT1
IF has full hyperspectral bands -> Match from all indices based on target
IF sparse vegetation / obvious soil background -> Prioritize SAVI, OSAVI, MSAVI2
IF dense vegetation / high biomass -> Prioritize EVI, WDRVI, MSR
IF atmosphere resistance needed -> Prioritize ARVI, EVI, VARI
```

### Rule 3: Recommend by Specific Target

```
IF target = "most common vegetation index" -> NDVI
IF target = "atmosphere resistance" -> ARVI or EVI
IF target = "sparse vegetation" -> SAVI or OSAVI
IF target = "high biomass anti-saturation" -> EVI or WDRVI
IF target = "quantitative chlorophyll" -> MCARI or TCARI (with OSAVI)
IF target = "nitrogen management" -> NDNI or RENDVI
IF target = "early water stress detection" -> PRI or MSI
IF target = "water body extraction (urban areas)" -> MNDWI (suppresses building noise)
IF target = "fire severity assessment" -> NBR + dNBR
IF target = "snow/ice coverage" -> NDSI
IF target = "built-up area extraction" -> NDBI
IF target = "porphyry copper exploration" -> PHAI + PRAI
IF target = "carbonate rock identification" -> CALI + CARI + DOLI
```

---

## IV. Band Abbreviation Reference Table

| Abbreviation | Meaning | Typical Wavelength (nm) |
|---|---|---|
| blue | Blue band | ~450 |
| green | Green band | ~550 |
| red | Red band | ~660 |
| rededge | Red-edge band | ~710 |
| nir | Near-infrared band | ~800-850 |
| swir1 | Shortwave infrared 1 | ~1600 |
| swir | Shortwave infrared | ~2100 |
| thermal | Thermal infrared band | ~10400 |
| midir | Mid-infrared band | ~1640 |
| w430-w11300 | Specific wavelength (nm) | See individual index definitions |
| tm1-tm7 | Landsat TM bands | See Landsat band definitions |
| wv2* | WorldView-2 bands | See WorldView-2 band definitions |
