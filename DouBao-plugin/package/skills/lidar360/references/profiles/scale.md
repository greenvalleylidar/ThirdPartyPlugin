profiles:
  contour_scale_1_500:
    scale: "1:500"
    minor_spacing_m: 0.25
    basic_spacing_m: 0.5
    major_spacing_m: 2
    description: Large-scale topographic map, suitable for detailed terrain survey and urban planning

  contour_scale_1_1000:
    scale: "1:1000"
    minor_spacing_m: 0.5
    basic_spacing_m: 1
    major_spacing_m: 5
    description: Commonly used for detailed urban planning, engineering design, and building surveys

  contour_scale_1_2000:
    scale: "1:2000"
    minor_spacing_m: 1
    basic_spacing_m: 2
    major_spacing_m: 10
    description: Standard topographic map scale, widely used for engineering survey and terrain mapping

  contour_scale_1_5000:
    scale: "1:5000"
    minor_spacing_m: 2.5
    basic_spacing_m: 5
    major_spacing_m: 25
    description: Medium scale, suitable for urban planning, land use, and water resource engineering

  contour_scale_1_10000:
    scale: "1:10000"
    minor_spacing_m: 2.5
    basic_spacing_m: 5
    major_spacing_m: 25
    description: Small scale, suitable for regional planning, hydrological analysis, and forestry survey

  contour_scale_1_25000:
    scale: "1:25000"
    minor_spacing_m: 5
    basic_spacing_m: 10
    major_spacing_m: 50
    description: Common topographic map scale, suitable for large-area terrain survey and planning

  contour_scale_1_50000:
    scale: "1:50000"
    minor_spacing_m: 10
    basic_spacing_m: 20
    major_spacing_m: 100
    description: Small-to-medium scale, suitable for regional geological survey and natural resource management

  contour_scale_1_100000:
    scale: "1:100000"
    minor_spacing_m: 20
    basic_spacing_m: 40
    major_spacing_m: 200
    description: Small scale, suitable for provincial or national-level regional planning

notes:
  - The manual lists 11 supported contour line scales; the default for point cloud contour generation is 1:10000
  - These configuration profiles are recommended standard defaults parsed by MCP; if internal standards differ, calibration with the product owner is advised
  - For high-precision surveys (e.g., buildings, road engineering), 1:500 or 1:1000 is recommended
  - For standard topographic mapping, 1:2000 is the most commonly used scale
  - For large-area planning, 1:10000 and smaller scales are more appropriate

dem_resolution_profiles:
  dem_high_precision:
    cell_size_m: 0.5
    description: High-precision DEM, suitable for detailed terrain analysis and building design
    typical_use_cases:
    - Building design
    - Detailed terrain analysis
    - Airport runway design

  dem_standard:
    cell_size_m: 1.0
    description: Standard DEM resolution, widely used for engineering survey and terrain mapping
    typical_use_cases:
    - Engineering survey
    - Terrain mapping
    - Hydrological analysis
    - Urban planning

  dem_regional:
    cell_size_m: 2.0
    description: Regional-level DEM resolution, suitable for large-area terrain analysis
    typical_use_cases:
    - Regional planning
    - Forestry survey
    - Watershed analysis

  dem_large_scale:
    cell_size_m: 5.0
    description: Large-scale DEM resolution, suitable for provincial or national-level regional analysis
    typical_use_cases:
    - Provincial planning
    - Natural resource management
    - Geological survey
