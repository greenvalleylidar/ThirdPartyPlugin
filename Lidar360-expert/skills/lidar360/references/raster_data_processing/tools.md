# Raster Data Processing Tools Registration
---

## Raster Clipping
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| clip_raster_by_polygon | Extracts the cells of a raster based on a polygon file or by specifying the polygon's vertices | Input data | - |
| clip_raster_by_draw_polygon | Extracts the cells of a raster based on a polygon file or by specifying the polygon's vertices | TIF/TIFF/IMG/DAT/HDR | polygons |
| clip_raster_by_circle | Extracts the cells of a raster based on a circle by specifying the circle's center and radius | TIF/TIFF/IMG/DAT/HDR | center_x, center_y, radius |
| clip_raster_by_rectangle | Extracts the cells of a raster based on a rectangle by specifying the rectangle's extent | TIF/TIFF/IMG/DAT/HDR | x_min, x_max, y_min, y_max |

---

## Mosaic Rasters
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| raster_mosaic | Mosaic multiple raster files into a single raster file | TIF/TIFF/IMG/DAT/HDR | sample_type |

---

## Band Processing
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| composite_raster_bands | Creates a single raster dataset from multiple bands | TIF/TIFF/IMG/DAT/HDR | - |
| create_color_composite | Create a three-band raster dataset from a multiband raster dataset | TIF/TIFF/IMG/DAT/HDR | red_expression, green_expression, blue_expression |

---

## Raster Extraction
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| extract_by_attributes | Extracts the cells of a raster based on a logical query | TIF/TIFF/IMG/DAT/HDR | sql |
| extract_raster_by_mask | Extracts the cells of a raster that correspond to the areas defined by a mask | Input data | - |

---

## Raster Algebra
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| raster_calculator | You can enter raster data algebraic expressions and use operators and functions to perform mathematical calculations. Supports common mathematical operators (+, -, *, /, ^, <, >, <=, >=, ==, !=, &, \|) and functions (abs, acos, acosh, cos, sin, asin, asinh, tan, atan, atanh, atan2, ceil, cot, floor, pow, log, round, sqrt, log10, log2, logn, sinc) | TIF/TIFF/DAT/IMG/HDR | expression, xmin, ymin, xmax, ymax, col, row |

---

## Raster Data Management
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| define_raster_nodata_value | Define raster NoData value of TIFF image | TIF/TIFF/IMG/DAT/HDR | - |
| raster_subdivision | Divide an image into multiple frames according to different scales | TIF/TIFF/IMG/DAT/HDR | scale |

---

## Common Parameter Explanation

### sample_type (mosaic method)
| Value | Method | Application scenario |
|---|------|---------|
| first | First value | Fast mosaicking |
| last | Last value | Overwrite update |
| mean | Mean value | Smooth transition |
| max | Maximum value | Use higher value |
| min | Minimum value | Use lower value |

### supported formats
| Type | Format |
|-----|------|
| Input raster | TIF, TIFF, IMG, DAT, HDR |
| Vector boundary | SHP, GPKG, DXF |
| Output raster | TIF, TIFF |

### raster calculator operators
| Type | Values |
|---|------|
| Operators | +, -, *, /, ^, <, >, <=, >=, ==, !=, &, \| |
| Functions | abs, acos, acosh, cos, sin, asin, asinh, tan, atan, atanh, atan2, ceil, cot, floor, pow, log, round, sqrt, log10, log2, logn, sinc |

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "raster_data_processing-toolID"
