# attribute_table Usage Examples

## Example 1: Update an Existing Field

**Scenario**: Multiply the "height" field values in a SHP file by 2

```json
{
  "input_file": "C:/data/buildings.shp",
  "operation": "update_field",
  "target_field": "height",
  "expression": "\"height\" * 2"
}
```

## Example 2: Create a New Field

**Scenario**: Create a new double-type field "area_m2" in a GPKG file to calculate area

```json
{
  "input_file": "C:/data/parcels.gpkg",
  "operation": "create_field",
  "target_field": "area_m2",
  "expression": "$area",
  "field_type": "double",
  "field_precision": 2
}
```

## Example 3: Calculate on Selected Rows

**Scenario**: Calculate the average DBH only for specified rows in a TreeDB file

```json
{
  "input_file": "C:/data/forest.treedb",
  "operation": "update_field",
  "target_field": "avg_dbh",
  "expression": "(\"dbh_1\" + \"dbh_2\") / 2",
  "selected_fids": [1, 2, 3, 5, 8]
}
```
