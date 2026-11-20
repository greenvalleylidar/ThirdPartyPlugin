---
name: lidar360-forest-tending-script
description: Create or modify LiDAR360 forest tending Python secondary development scripts, and synchronously generate standalone tending plan JSON files pointing to custom scripts. Used for writing attribute calculation, target tree selection, harvest tree ranking, and validation phases of the forest_tending_sdk ForestTendingHook. Prefer reusing TreeFields, StandFields, and C++ built-in control metrics; avoid redefining built-in attributes or general control metrics as Parameter, Field, or Python control rules. Protect the default crop-tree-selection.json, crope-tree-selection-script.py, and tending_operation_record_exporter.py from being overwritten, and support custom operation record export scripts.
---

# LiDAR360 Forest Tending Script Secondary Development

Create or modify forest tending Python scripts for a user-specified LiDAR360 installation instance. Do not treat the skill repository directory as the script runtime directory.

## Core Rules

- Prefer using `forest_tending_sdk` classes; do not parse the C++ input JSON yourself.
- Tending workflow scripts inherit from `ForestTendingHook`.
- Operation record XLSX export scripts inherit from `ForestTendingOperationRecordExporter`.
- Operation design tables should be configured through the plan JSON's `RecordExportConfig.layout` first; do not generate a Python exporter by default. Only create a new export script when the layout system cannot express the requirements.
- Before writing an exporter, you must read the target installation instance's `forest_tending_sdk/__init__.pyi`, `operation_record.py`, and the default exporter; only interfaces explicitly present in these files or discoverable via runtime reflection are allowed. Never fabricate SDK functions based on outdated examples.
- Use `TreeFields.FIELD_NAME` and `StandFields.FIELD_NAME` directly for built-in attributes. Do not redeclare data fields such as DBH, tree height, crown width, or stand area as `Parameter` or `Field`.
- Default to `fields = []`. Only declare `Field(...)` when the script computes a new attribute not present in the SDK and the result needs to be displayed to the user or used by subsequent rules.
- Default to `parameters = []`. Only declare `Parameter(...)` when a value genuinely needs user adjustment in the script interface and it is not an input data attribute, stand attribute, or an existing C++ control metric.
- General business scripts should not declare Python control rules. Stem count harvesting intensity, basal area harvesting intensity, post-harvest canopy closure, canopy closure change, and maximum gap area should be delegated to C++ built-in control metrics.
- Do not infer the script save location solely from the current working directory. Confirm in this order: user-explicitly-specified file > user-explicitly-specified LiDAR360 installation directory > directory of existing similar scripts in the current installation instance > ask the user.
- When modifying an existing script, save back to the script's original path. When creating a new script, confirm the target directory exists in the actual installation instance before writing; the standard directory for the current version is `<installation root>/config/ForestAnalysis`. Do not insert an extra `bin` level, and do not automatically create a guessed `PythonScript` directory.
- The built-in operation design table / operation record export script `config/ForestAnalysis/tending_operation_record_exporter.py` is a read-only baseline and must not be modified, overwritten, renamed, or deleted under any circumstances. When customizing operation design tables, prefer modifying only the new plan JSON's `RecordExportConfig.layout` and leave `exporterScriptPath` empty; do not create a new export script by default.
- When creating a custom exporter, prefer using the user-specified filename; if unspecified, use `custom_tending_operation_record_exporter.py`. If that file already exists and the user has not explicitly requested modification, generate a non-conflicting name or ask the user to confirm. Never fall back to overwriting the built-in default script.
- Other existing runtime scripts may only be edited in place when the user explicitly requests modification of that file; otherwise, use a new filename specified by the user.
- The built-in default plan `config/ForestAnalysis/crop-tree-selection.json` and its default script `crope-tree-selection-script.py` are read-only baselines and must not be modified, overwritten, renamed, or deleted under any circumstances.
- When creating or customizing a tending Hook, always synchronously generate a plan JSON with a different filename, and set `PythonHookConfig.scriptPath` to point to the new Hook. When the plan filename is unspecified, use the same base name as the Hook with a `.json` extension.
- The `outputFields`, `parameterDefinitions`, and `parameters` in the new plan must come from the new Hook's schema. Do not retain old parameters from the default plan that do not match the new script.
- Preserve the C++ command protocol. Use `raise SystemExit(MyHook().main())` or `raise SystemExit(MyExporter().main())` at the end of the script.
- Use the `platform-lidar360_software_information` tool to obtain the Python root directory and locate python.exe for local checks. Do not use the system Python as a substitute for the SDK runtime environment.

## Tending Execution Flow

The current C++ and Python collaboration sequence:

1. C++ raw retention rules generate `TargetCandidate`.
2. Python `select_targets(ctx)` receives `ctx.target_candidates` and returns the final target trees.
3. C++ applies harvest rules only to non-target trees, generating `HarvestCandidate`.
4. Python `select_harvest(ctx)` receives `ctx.target_tree_ids` and `ctx.harvest_candidates`, sorts or filters candidates, and may return `controlRules`.
5. As C++ accepts harvest candidates one by one, it applies both built-in control rules and Python-declared control rules.
6. Python `validate(ctx)` receives the final `ctx.plan` and `ctx.control_rules`, performs diagnostics only, and does not alter selection results.

Before implementing or reviewing a tending hook, read `references/recipes/forest_tending_script/hook_workflow.md`.

## Definition Selection Order

For each requirement, evaluate in the following order and stop once matched. Do not continue creating duplicate definitions:

1. If the value comes from individual tree or stand input data, use `TreeFields.*` or `StandFields.*`.
2. If the value is a harvest control metric already supported by C++, reserve it for built-in control configuration; Python only sorts candidate trees.
3. If the value is a fixed algorithm constant internal to the script, use a plain Python constant or local variable.
4. Only use `Parameter(...)` when the value needs user adjustment and SDK/C++ has no corresponding configuration.
5. Only use `Field(...)` when the value is newly computed by the script and needs to be exposed to the rule configurator.
6. Only use Python custom control rules and candidate tree `metrics` when built-in control metrics cannot express per-tree cumulative constraints.

Do not automatically define a value as `Parameter` just because it appears in an algorithm formula or filter condition. If the user has not requested "configurable, adjustable, interface parameter," prefer keeping `parameters = []`.

## Development Entry Points

- When creating a new `ForestTendingHook` script, start from `references/recipes/forest_tending_script/hook_template.py`.
- When synchronously generating a plan JSON, read `references/recipes/forest_tending_script/plan_config.md` and use `scripts/create_forest_tending_plan.py`.
- When customizing operation record XLSX export, read `references/recipes/forest_tending_script/record_export.md`.
- When a Python exporter is truly needed, start from `references/recipes/forest_tending_script/exporter_template.py` and run `scripts/validate_forest_tending_exporter.py`.
- This module is a Python secondary development specification. It is not invoked through `mcp-tool.exe` and has no `module-toolID`.

## Save Path Confirmation

The following steps must be completed before performing any file write:

1. If the user provided a full `.py` file path, use that path as the candidate target. If it is the built-in `tending_operation_record_exporter.py`, do not write to it; instead, create a custom exporter in the same directory. Treat other existing files as modification tasks only.
2. If the user only provided the LiDAR360 installation root directory, check whether it directly contains `LiDAR360.exe`, `config`, and `python310/python.exe`.
3. Search for similar scripts in the installation instance: for tending hooks, search for the user's currently selected hook; for operation record exporters, search for `tending_operation_record_exporter.py`, but that file is only used to confirm the directory and read the baseline implementation.
4. After finding a similar script, use its parent directory as the runtime script directory for that installation version. Do not override the actual layout with directories from another version's documentation. Custom exporters must be created in that directory with a different filename.
5. If there are multiple LiDAR360 installation instances, multiple scripts with the same name, or the new script has no explicit filename, list the candidate absolute paths and let the user confirm. Do not select the latest version on your own.
6. Report the final absolute path before writing. When overwriting an existing non-built-in file, explicitly state that this is an in-place modification. When creating a file, explicitly state that it is new and confirm the target is not `tending_operation_record_exporter.py`.
7. When creating a new Hook, also report the absolute path of the new plan JSON, confirm the target is not `crop-tree-selection.json`, and verify that the application-relative `scriptPath` in the JSON points to the new Hook.

A confirmed installation instance on the current machine:

```text
Installation root: E:\Lidar360\GreenValley Suite\LiDAR360\10.0.0.0
Tending script directory: E:\Lidar360\GreenValley Suite\LiDAR360\10.0.0.0\config\ForestAnalysis
Python: E:\Lidar360\GreenValley Suite\LiDAR360\10.0.0.0\python310\python.exe
```

These paths are only confirmed candidates for the current machine and must not be hardcoded as defaults for all users or all LiDAR360 versions.

## Pre-Completion Checks

- Confirm that output tree IDs are positive and exist in `ctx.trees`.
- Do not output duplicate target tree or harvest tree IDs.
- Do not output final target trees as harvest candidates.
- Confirm that score and metrics values are finite and do not contain NaN or Infinity.
- Dynamic attribute keys do not contain `.`.
- Check whether `TreeFields.*` or `StandFields.*` data has been incorrectly wrapped as `Parameter`.
- Check whether C++ already handles harvest intensity, basal area, canopy closure, or gap control metrics and avoid re-implementing them.
- Check whether each `Parameter` truly needs user adjustment; otherwise, convert it to a plain constant or remove it.
- Confirm that the final absolute save path belongs to a user-specified or confirmed LiDAR360 installation instance.
- If the task involves operation design tables or XLSX operation record export, confirm that the built-in `tending_operation_record_exporter.py` remains unchanged before and after modification, and that actual changes are only in newly created or user-explicitly-specified non-built-in scripts.
- Check whether the operation design table can be fully implemented by `RecordExportConfig.layout`; if so, do not generate an additional Python exporter.
- For custom exporters, perform API validation to confirm that all SDK imports, `TreeFields`/`StandFields` members, parent class method calls, and `ExcelDocumentPy` methods exist in the target installation version.
- If the task involves Hooks or tending plans, confirm that the built-in `crop-tree-selection.json` and `crope-tree-selection-script.py` remain unchanged before and after modification, and verify that the new plan's schema configuration matches the new Hook.
- Use the target instance's `python310/python.exe -m py_compile <script.py>` to check syntax. If the installation instance allows direct command-line import of `forest_tending_sdk`, then run `<script.py> --lidar360-schema`; if the SDK is only injected at runtime by the LiDAR360 process, load the script in the LiDAR360 interface and refresh the schema. Do not misinterpret a command-line `ModuleNotFoundError` as a script syntax error.
