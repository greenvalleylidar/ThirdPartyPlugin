# Point Cloud Class Codes (ASPRS Standard)

## Standard Classes (0-38)

| Code | Name | English | Common Use Cases |
|---|------|------|---------|
| 0 | Never Classified | Never Classified | - |
| 1 | Unclassified | Unclassified | Raw point default |
| **2** | **Ground** | **Ground** | **Required for DEM generation** |
| 3 | Low Vegetation | Low Vegetation | <0.5m |
| 4 | Medium Vegetation | Medium Vegetation | 0.5-2m |
| 5 | High Vegetation | High Vegetation | >2m |
| **6** | **Building** | **Building** | DSM/Modeling |
| 7 | Low Point (Noise) | Low Point | Noise processing |
| 8 | Model Key Point | Model Key Point | - |
| 9 | Water | Water | - |
| 10 | Car | Car | - |
| 11 | Street Light | Street Light | - |
| 12 | Overlap | Overlap | - |
| **13** | **Roof** | **Roof** | Building modeling |
| 14 | Wall | Wall | Building modeling |
| 15 | Pole | Pole | Power line inspection |
| 16 | Powerline | Powerline | Power line inspection |
| 17 | Tower | Tower | Power line inspection |
| 18-28 | Electrical Equipment | Scissors/Shield/Insulator etc. | Power line inspection |
| **29** | **Bridge** | **Bridge** | Transportation facilities |
| 30 | Tunnel | Tunnel | Transportation facilities |
| 31-36 | Other Facilities | Ventilation pipe/Cable/Debris etc. | - |
| **37** | **Noise Points** | **Noise Points** | Denoising |
| **38** | **Road** | **Road** | Transportation/Road surface |

---

## User-Defined Classes (39-255)

| Range | Description |
|-----|------|
| 39-63 | Reserved for extension |
| 64-255 | User-defined |

---

## Common Combinations

### DEM Generation
```python
from_class = [2]  # Ground points only
```

### DSM Generation
```python
from_class = [1, 2, 3, 4, 5, 6]  # All surface points
```

### Building Modeling
```python
building_class = [6, 13, 14]  # Building + Roof + Wall
```

### Vegetation Analysis
```python
from_class = [3, 4, 5, 23, 24]  # Vegetation-related
```

### Power Line Inspection
```python
from_class = [15, 16, 17, 27, 28]  # Power facilities
```

### Noise Removal
```python
from_class = [7, 37]  # Noise points
```

---

## Related Parameter Names

| Parameter | Purpose | Example Tool |
|-----|------|---------|
| `from_class` | Input class filter | generate_general_dem_from_pointcloud |
| `to_class` | Output target class | classify_ground_by_csf |
| `ground_class` | Ground point class reference | classify_top_surface |
| `building_class` | Building class | auto_create_buildings |
