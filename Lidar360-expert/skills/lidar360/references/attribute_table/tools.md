# attribute_table Tool Registry

## Field Calculation
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| attribute_table_field_calculator | Calculate attribute table fields using field expressions, writing results to an existing field or a newly created field. Supports vector data such as GPKG, DXF, SHP, KML; table data such as CSV, TreeDB; and building data such as LiBIM | gpkg/dxf/shp/kml/csv/treedb/libim | input_file, operation, target_field, expression |
