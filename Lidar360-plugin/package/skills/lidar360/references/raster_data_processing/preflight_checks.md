# Preflight Check Flow

## Mandatory Checks

The following checks apply to all raster processing tools and must be completed before any operation:

1. Confirm the selected layer type is correct (raster type)
2. Check whether the input file exists
3. Validate coordinate system consistency (mosaicing, raster band compositing) -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS
4. Check resolution consistency (mosaicing, band compositing) -> `get_data_information` x N, compare `resolution_x`/`resolution_y`, all identical -> PASS
5. Validate extent overlap (clipping, mask extraction) -> `get_data_information` x N, compare `bounds`, intersection area > 0 -> PASS
6. Execute the tool
7. Check whether the output raster file exists; if so, call get_data_information to obtain file information and verify that data type, spatial extent, resolution, band count, or NoData value meets expectations

---

## Tool Execution

### Clipping Tools

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `clip_raster_by_polygon` | Raster exists + polygon vector exists + overlapping extents -> `get_data_information` x N, compare `bounds`, intersection area > 0 -> PASS | "Please select the raster first" / "Polygon file does not exist" / "Clip extent has no overlap" |
| `clip_raster_by_draw_polygon` | Raster exists + coordinates valid + extent within raster | "Please select the raster first" / "Coordinates are invalid" / "Clip extent exceeds raster" |
| `clip_raster_by_circle` | Raster exists + center valid + radius > 0 | "Please select the raster first" / "Center coordinates are invalid" / "Radius must be greater than 0" |
| `clip_raster_by_rectangle` | Raster exists + coordinates valid + xmin < xmax + ymin < ymax | "Please select the raster first" / "Rectangle coordinates are invalid" / "Coordinate range error" |

### Mosaicing Tools

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `raster_mosaic` | >=2 rasters + same coordinate system -> `get_data_information` x N, compare `coordinate_system`, all identical -> PASS + same resolution -> `get_data_information` x N, compare `resolution_x`/`resolution_y`, all identical -> PASS + overlapping extents -> `get_data_information` x N, compare `bounds`, intersection area > 0 -> PASS | "Insufficient raster count" / "Coordinate system mismatch" / "Resolution mismatch" / "No extent overlap among rasters" |

### Band Processing

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `composite_raster_bands` | >=2 bands + same extent -> `get_data_information` x N, compare `bounds`, all identical -> PASS + same resolution -> `get_data_information` x N, compare `resolution_x`/`resolution_y` + same coordinate system -> `get_data_information` x N, compare `coordinate_system` | "Insufficient band count" / "Extent mismatch" / "Resolution mismatch" |
| `create_color_composite` | Multi-band raster + band numbers valid | "Please select a multi-band raster" / "Band number out of range" |

### Extraction Tools

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `extract_by_attributes` | Raster exists + expression syntax correct | "Please select the raster first" / "Expression syntax error" |
| `extract_raster_by_mask` | Raster exists + mask exists + overlapping extents -> `get_data_information` x N, compare `bounds`, intersection area > 0 -> PASS | "Please select the raster first" / "Mask file does not exist" / "No extent overlap" |

### Algebraic Operations

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `raster_calculator` | Expression valid + referenced rasters exist + same extent -> `get_data_information` x N, compare `bounds`, all identical -> PASS | "Expression is empty" / "Referenced raster does not exist" / "Raster extent mismatch" |

### Data Management

| Tool | Check Item | Failure Message |
|-----|--------|---------| 
| `define_raster_nodata_value` | Raster exists + value within data range | "Please select the raster first" / "NoData value is invalid" |
| `raster_subdivision` | Raster exists + `scale` within 0..3 | "Please select the raster first" / "Scale out of range" |

---

## Other

### Common Error Troubleshooting

| Error Type | Possible Cause | Solution |
|---------|---------|---------|
| Coordinate system mismatch | Different sources, different projections | Use projection transformation to unify coordinate systems |
| Resolution mismatch | Data source differences | Use resampling to unify resolution |
| No extent overlap | Incorrect data extents | Check data spatial extents |
| Band number exceeded | Band index error | Check raster band count |
| Expression error | Syntax or function name error | Check expression syntax |

---

**Tip**: Use `{SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "raster_data_processing-toolID"` to get detailed parameter descriptions
