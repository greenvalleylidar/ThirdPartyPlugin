# attribute_table Preflight Checks

## General Checks

| Check Item | Description | Failure Handling |
|------------|-------------|------------------|
| File path | Input file must exist | Prompt user to verify the path |
| File format | Must be a supported format (gpkg/dxf/shp/kml/csv/treedb/libim) | Prompt user with the list of supported formats |

### attribute_table_field_calculator

| Check Item | Description | Failure Handling |
|------------|-------------|------------------|
| input_file | Input file must exist and be readable | Prompt user to verify the file path |
| operation | Must be update_field or create_field | Prompt user with valid enum values |
| target_field | Target field name must not be empty | Prompt user to specify a field name |
| expression | Calculation expression must not be empty | Prompt user to enter an expression |
| Field type | When creating a new field, field_type must be integer/double/text/datetime | Prompt user with valid enum values |
