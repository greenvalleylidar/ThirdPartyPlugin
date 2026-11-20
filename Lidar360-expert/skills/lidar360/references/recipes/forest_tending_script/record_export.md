# Operation Record and Work-Design Table Export

## Source of Truth

Before writing export code, inspect the selected LiDAR360 installation in this order:

1. `<install-root>/python310/Lib/site-packages/forest_tending_sdk/__init__.pyi`
2. `<install-root>/python310/Lib/site-packages/forest_tending_sdk/operation_record.py`
3. `<install-root>/config/ForestAnalysis/tending_operation_record_exporter.py`
4. Runtime `dir()` output from the selected installation's Python

Use only APIs confirmed by the target installation. Do not infer APIs from another version, an old example, a similarly named Excel library, or general Python conventions.

The built-in exporter is a read-only baseline:

```text
config/ForestAnalysis/tending_operation_record_exporter.py
```

Never modify, overwrite, rename, delete, format, or normalize it.

## Preferred Approach: Configure `layout`

For ordinary work-design tables, do not create a Python exporter. Configure the new plan JSON under:

```text
RecordExportConfig.layout
```

The built-in `ForestTendingOperationRecordExporter` already renders these block types:

- `title`
- `text`
- `form`
- `table`
- `groupedTable`

Supported record sources are:

- `stands`
- `allTrees`
- `reserveTrees`
- `harvestTrees`

Example:

```json
{
  "RecordExportConfig": {
    "enabled": true,
    "exporterScriptPath": "",
    "exporterScriptPathType": "application",
    "appendToExisting": true,
    "layout": {
      "sheets": [
        {
          "name": "Work Design Table",
          "repeatFor": "",
          "blocks": [
            {
              "type": "groupedTable",
              "source": "stands",
              "title": "Design Table",
              "columns": 4,
              "mergeColumns": 8,
              "fields": [
                {
                  "fieldKey": "plan.harvestPercent",
                  "alias": "Harvest Intensity (Count)",
                  "group": "Harvest Design",
                  "subGroup": "",
                  "format": "0.00",
                  "visible": true,
                  "width": 14
                }
              ]
            }
          ]
        }
      ]
    }
  }
}
```

Prefer field keys already used by the installed default plan. Confirm any new field key against `operation_record.py` before adding it.

## Confirmed Field-Key Families

The current SDK resolver supports these families:

- `tree.treeId`, `tree.xy`, `tree.decision`
- `attributes.<existing tree attribute key>`
- `standBefore.area`, `standBefore.numTrees`, `standBefore.<existing stand attribute key>`
- `standAfter.area`, `standAfter.numTrees`, `standAfter.<existing stand attribute key>`
- `plan.beforeTreeCount`, `plan.reserveCount`, `plan.harvestCount`
- `plan.harvestPercent`, `plan.beforeBasalArea`, `plan.removedBasalArea`
- `plan.basalAreaRemovalPercent`, `plan.beforeCrownClosure`
- `plan.crownClosureAfter`, `plan.crownClosureChange`, `plan.maxCanopyGapArea`
- `plan.customValues.<custom metric key>`
- `custom.<metadata key>`

Do not invent paths such as `plan.target_count`, `stand_before.area`, or arbitrary nested properties. The JSON field-key syntax and Python property syntax are different.

## When Python Is Actually Required

Create a separate custom exporter only when the layout system cannot express the requirement, for example:

- A newly calculated value not present in metadata, tree attributes, stand attributes, or plan metrics.
- Custom row grouping or multi-row transformation that layout blocks cannot represent.
- A workbook operation proven to require a verified lower-level SDK API.

Default filename when the user does not provide one:

```text
config/ForestAnalysis/custom_tending_operation_record_exporter.py
```

If it exists, do not overwrite it without explicit user selection.

## Confirmed High-Level Python API

The current target SDK publicly declares:

```python
from forest_tending_sdk import (
    ForestTendingOperationRecordExporter,
    RecordContext,
    RecordExportInput,
    RecordStand,
    SheetData,
)
```

Confirmed exporter entry points and extension methods:

```text
main(argv=None) -> int
load_input(input_path) -> RecordExportInput
export(ctx) -> str
build_overview_sheet(ctx, sheet_config, index) -> SheetData
build_tree_sheets(ctx, sheet_config, start_index) -> list[SheetData]
resolve_value(ctx, record, field_key) -> Any
```

Confirmed input properties:

```text
RecordExportInput.output_path
RecordExportInput.append_to_existing
RecordExportInput.layout
RecordExportInput.stand

RecordStand.stand_before
RecordStand.stand_after
RecordStand.plan
RecordStand.metadata_values
RecordStand.all_trees
```

Confirmed `SheetData` fields:

```text
name
rows
merges
widths
```

Start from `exporter_template.py`. The template only uses the confirmed high-level API.

## Prohibited API Guessing

Do not generate any of the following unless the exact target installation proves they exist:

- `from forest_tending_sdk.xlsx import ...`
- `sheet = doc.addSheet(...)` followed by `sheet.setCellValue(...)`
- `sheet.setColumnWidth(...)`
- `tree.tags` unless present in the target type declarations/runtime
- `stand.plan.target_count`
- `SheetData` methods such as `add_row()`, `append_row()`, `merge()`, or `set_width()`
- Any method copied from `openpyxl`, `xlsxwriter`, Qt, or another Excel wrapper

Do not use `hasattr()` as evidence that an invented SDK method is valid. Confirm the member in `.pyi`, implementation source, or runtime reflection first.

## Lower-Level `ExcelDocumentPy`

Do not use `ExcelDocumentPy` by default. It is a separate native module, not `forest_tending_sdk.xlsx`.

If exact workbook operations require it:

1. Configure the target installation's DLL directories.
2. Import `ExcelDocumentPy` with the target installation's Python.
3. Inspect `dir(ExcelDocumentPy.ExcelDocument)` at runtime.
4. Use only methods present in that output.
5. Build and run a minimal temporary XLSX smoke test before writing the real exporter.

For the currently inspected installation, runtime reflection confirmed these names, among others:

```text
addSheet
deleteSheet
mergeCells
mergeSheetCells
renameSheet
save
saveAs
selectSheet
setCellValue
setSheetColumnWidth
setSheetRowHeight
sheetDimension
sheetNames
```

Method signatures and return types are not established by names alone. Never assume `addSheet()` returns a sheet object. Follow the installed `operation_record.py` implementation or a successful smoke test.

## Validation

Before accepting a custom exporter:

1. Run `scripts/validate_forest_tending_exporter.py` against the target installation and script.
2. Run the target Python with `-m py_compile`.
3. Import the custom module with the target Python; importing must not execute export work.
4. If sample `RecordExportInput` JSON is available, run the exporter end to end and open the produced XLSX.
5. Confirm the built-in exporter hash is unchanged.

Syntax compilation alone is insufficient because Python accepts calls to nonexistent methods until runtime.
