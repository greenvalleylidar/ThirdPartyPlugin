# Forest Tending Plan Configuration

Generate a configured plan JSON together with each custom forest-tending hook. Treat the installed default plan as a read-only baseline:

```text
config/ForestAnalysis/crop-tree-selection.json
```

Never modify, overwrite, rename, delete, format, or normalize this file. Also protect its paired built-in hook when present:

```text
config/ForestAnalysis/crope-tree-selection-script.py
```

## Pair Generation

For a custom hook, produce two separate files in the confirmed `config/ForestAnalysis` directory:

```text
<custom-name>.py
<custom-name>.json
```

The JSON plan must point to the custom hook through:

```json
{
  "PythonHookConfig": {
    "enabled": true,
    "scriptPath": "config/ForestAnalysis/<custom-name>.py",
    "scriptPathType": "application"
  }
}
```

Use forward slashes in application-relative paths. Do not store a machine-specific absolute script path in the plan.

## Schema Synchronization

Keep these fields synchronized with the generated hook schema:

- `PythonHookConfig.outputFields`
- `PythonHookConfig.parameterDefinitions`
- `PythonHookConfig.parameters`

When the hook uses `fields = []` and `parameters = []`, write empty arrays and an empty object. Do not copy stale parameter definitions from the default plan.

For each parameter definition, copy its `default` value into `PythonHookConfig.parameters[key]`. Preserve types, aliases, ranges, steps, units, groups, descriptions, and enum values from the schema.

Do not move built-in final controls into Python parameters. Keep these settings in `ControlIndicators`:

- `targetIntensity` and `useIntensity`
- `basalAreaRemoval` and `useBasalArea`
- `minCanopyDensityAfterThinning` and `useMinCanopyDensity`
- `maxChangeOfCanopyDensity` and `useMaxCanopyDensityChange`

## Exporter Synchronization

For ordinary work-design-table customization, configure `RecordExportConfig.layout` and keep:

```json
{
  "RecordExportConfig": {
    "enabled": true,
    "exporterScriptPath": "",
    "exporterScriptPathType": "application"
  }
}
```

This uses the installed built-in exporter and avoids unsupported custom SDK calls. Read `record_export.md` for supported layout blocks, sources, and field-key families.

Only when the layout system cannot express the requirement and a custom exporter has passed API validation, set:

```json
{
  "RecordExportConfig": {
    "enabled": true,
    "exporterScriptPath": "config/ForestAnalysis/<custom-exporter>.py",
    "exporterScriptPathType": "application"
  }
}
```

Never point a customized plan at a modified built-in exporter. The built-in `tending_operation_record_exporter.py` remains read-only.

## Generation Tool

Use `scripts/create_forest_tending_plan.py` to create a new plan with exclusive-create semantics:

```powershell
python scripts/create_forest_tending_plan.py `
  --install-root "<INSTALL_ROOT>" `
  --base-plan "<INSTALL_ROOT>\config\ForestAnalysis\crop-tree-selection.json" `
  --output-plan "<INSTALL_ROOT>\config\ForestAnalysis\custom-target-selection.json" `
  --hook-script "<INSTALL_ROOT>\config\ForestAnalysis\custom-target-selection.py" `
  --schema-file "<WORK_DIR>\custom-target-selection.schema.json"
```

If standalone schema export works in the selected installation, replace `--schema-file` with:

```text
--python-exe <install-root>/python310/python.exe
```

The tool must reject:

- A base plan other than the installed `config/ForestAnalysis/crop-tree-selection.json`.
- Output equal to the base plan.
- Any output named `crop-tree-selection.json`.
- Any output outside the selected installation's `config/ForestAnalysis` directory.
- Any output path that already exists.
- Hook or exporter paths outside the selected LiDAR360 installation.
- A custom exporter path named `tending_operation_record_exporter.py`.

## Completion Check

- Hash the default plan before and after generation and verify it is unchanged.
- Verify the new plan is valid JSON.
- Verify `scriptPath` points to the custom hook.
- Verify schema fields and parameters match the custom hook rather than the default plan.
- Verify built-in controls remain in `ControlIndicators`.
- Verify custom export configuration never modifies the default exporter.
