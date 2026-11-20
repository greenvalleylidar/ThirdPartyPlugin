# Interpolation Methods and Sampling Configuration

## DEM Interpolation Methods (interpolator)

| Value | Method | Characteristics | Use Cases |
|---|------|------|---------|
| 0 | IDW | Inverse Distance Weighting, fast | General accuracy, quick generation |
| 1 | Kriging | Kriging, high accuracy | Detailed terrain, good smoothing |
| 2 | TIN | Triangulated Irregular Network interpolation | Preserves terrain features, steep slope areas |

---

## IDW Parameters

| Parameter | Description | Default |
|-----|------|-------|
| `power` | Weight decay exponent | 2 |
| `radius_type` | Search radius type | 0-Fixed, 1-Variable |
| `distance` | Search distance (m) | 5 |
| `number_of_points` | Minimum number of points | 12 |

---

## Raster Sampling Methods (sampling_method)

| Value | Method | Characteristics |
|---|------|------|
| NEAREST | Nearest Neighbor | Fastest, preserves original values |
| BILINEAR | Bilinear | Smooth transitions |
| CUBIC | Cubic Convolution | High-quality smoothing |
| CUBICSPLINE | Cubic Spline | Smoothest |
| LANCZOS | Lanczos | High-quality resampling |
| AVERAGE | Average | Statistical properties |
| MODE | Mode | Categorical rasters |
| GAUSS | Gauss | Smoothing + noise reduction |
| RMS | Root Mean Square | Statistical properties |

---

## Radius Type (radius_type)

| Value | Type | Description |
|---|------|------|
| 0 | Fixed | Fixed search radius |
| 1 | Variable | Variable radius (adaptive) |

---

## Return Number (return_number)

| Value | Description | Use Case |
|---|------|------|
| 0 | All returns | All points |
| 1 | First return | DSM common choice |
| 2 | Second return | Vegetation penetration |
| 3+ | Subsequent returns | Vegetation analysis |

---

## DEM Precision Configuration (elevation_prec)

| Value | Decimal Places | Use Cases |
|---|---------|---------|
| 0 | Integer | Large-scale terrain |
| 1 | 0.1m | Regional planning |
| 2 | 0.01m | Engineering survey |
| 3 | 0.001m | Detailed survey |

---

## Recommended Configurations for Common Scenarios

### Quick DEM Generation
```
interpolator: 0 (IDW)
radius_type: 0 (Fixed)
power: 2
```

### High-Precision DEM
```
interpolator: 1 (Kriging)
radius_type: 1 (Variable)
number_of_points: 16
```

### Steep Slope Terrain
```
interpolator: 2 (TIN)
use_spike: true
```

### DSM Generation
```
return_number: [1]  # First return
```
