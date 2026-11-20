# Forest Tending Hook Workflow Reference

## Imports

Use SDK bindings:

```python
from forest_tending_sdk import (
    ForestTendingHook,
    HookInput,
    HookOutput,
    TreeFields,
    StandFields,
    radius_neighbor_map,
)
```

Import `Parameter`, `Field`, or control-rule classes only when the decision rules below show they are required. Do not include them by default.

## HookInput By Phase

All phases receive:

- `ctx.stand: StandInfo`
- `ctx.trees: list[Tree]`
- `ctx.parameters: ParameterValues`
- `ctx.hook_phase`

`select_targets` additionally receives:

- `ctx.target_candidates: list[TargetCandidate]`

`select_harvest` additionally receives:

- `ctx.target_tree_ids: list[int]`
- `ctx.harvest_candidates: list[HarvestCandidate]`

`validate` additionally receives:

- `ctx.target_tree_ids: list[int]`
- `ctx.plan: PlanDraft`
- `ctx.control_rules: list[ControlRule]`

## Phase Responsibilities

### `attribute(ctx)`

Use only when the script creates dynamic tree attributes. Return `HookOutput.attribute_result(...)`. Dynamic attribute keys must not contain `.`.

### `select_targets(ctx)`

Return final retained target trees. Treat `ctx.target_candidates` as C++ reserve-rule candidates. Use `mandatory=True` for candidates that must remain reserved and cannot be overridden by harvest selection.

Typical logic:

- Build `tree_by_id` from `ctx.trees`.
- Score candidate and non-candidate trees using built-in fields.
- Preserve mandatory candidates first.
- Apply density, spacing, distribution, or species composition limits inside Python if needed.
- Return `out.add_target(tree_id, mandatory=..., priority=..., score=..., reason=..., tags=[...])`.

### `select_harvest(ctx)`

Return ordered harvest candidates. C++ applies built-in controls during final acceptance. Python should normally decide priority, not duplicate the final acceptance limits.

Typical logic:

- `allowed_ids = {candidate.tree_id for candidate in ctx.harvest_candidates}`.
- Never emit target trees: skip IDs in `ctx.target_tree_ids`.
- Rank candidates from most preferred harvest to least preferred harvest.
- Use `affected_target_tree_ids` when a harvest candidate releases one or more target trees.
- Leave `metrics` empty unless a genuinely custom Python control rule needs a per-candidate value that C++ cannot compute.
- Return `out.add_harvest_candidate(...)`.

### Built-in Controls and Python `controlRules`

Do not recreate these C++ built-in controls in Python:

- `METRIC_HARVEST_PERCENT`: harvest count/intensity percentage.
- `METRIC_BASAL_AREA_REMOVAL_PERCENT`: basal-area removal percentage.
- `METRIC_CROWN_CLOSURE_AFTER`: minimum crown closure after tending.
- `METRIC_CROWN_CLOSURE_CHANGE`: maximum crown-closure change.
- `METRIC_MAX_CANOPY_GAP_AREA`: maximum canopy-gap area.

For these requirements, rank candidates in `select_harvest()` and let C++ accept or skip them. Do not create matching `Parameter` values, duplicate calculations, `add_control_rule(...)` calls, or candidate `metrics` unless the user explicitly requests an alternative custom behavior that the built-in control cannot express.

Use a Python control rule only for a new cumulative metric with no built-in equivalent. For example, a project-specific release-pressure budget may require a custom rule:

```python
out.add_control_rule(
    key="custom_release_pressure",
    alias="Release Pressure",
    op=ConstraintOperator.LessEqual,
    value=10.0,
    severity=ConstraintSeverity.Hard,
    reason="Limit total release pressure",
)
```

Each harvest candidate must then provide `metrics={"custom_release_pressure": value}`, unless C++ can compute the named metric. If a built-in metric can express the requirement, remove this custom rule.

### `validate(ctx)`

Use for final diagnostics. Do not try to choose more harvest trees here. Return issues or a plain successful validation result.

## Field Access

Use static field objects:

```python
dbh = tree.number(TreeFields.DBH, 0.0)
height = tree.number(TreeFields.TREE_HEIGHT, 0.0)
area = ctx.stand.number(StandFields.AREA, 0.0)
species = tree.string(TreeFields.TREESPECIES, "")
```

Useful tree fields include:

- `TreeFields.DBH`
- `TreeFields.TREE_HEIGHT`
- `TreeFields.CROWN_AREA`
- `TreeFields.CROWN_DIAMETER`
- `TreeFields.CROWN_HEIGHT_RATIO`
- `TreeFields.CROWN_ASYMMETRY`
- `TreeFields.HEIGHT_DIAMETER_RATIO`
- `TreeFields.STRAIGHTNESS`
- `TreeFields.IS_FORKED`
- `TreeFields.TREESPECIES`

Use `TreeFields.names()` and `StandFields.names()` to inspect all available fields.

## Definition Decision Table

| Requirement source | Correct representation | Do not use |
|---|---|---|
| Existing tree data such as DBH, height, crown area, species, straightness | `TreeFields.*` | `Parameter`, duplicate `Field` |
| Existing stand data such as area, tree count, dominant height, basal area | `StandFields.*` | `Parameter`, duplicate `Field` |
| Built-in final harvest limits such as harvest percentage, basal-area removal, crown closure, canopy gap | C++ built-in control configuration | Python `Parameter`, duplicate `ControlRule` |
| Fixed implementation detail that users do not need to tune | Python constant or local value | `Parameter` |
| New script setting that users must tune and that has no existing SDK/C++ setting | `Parameter.*` | Hard-coded hidden value |
| New calculated tree attribute needed by the rule editor or output | `Field(...)` | Reusing an unrelated built-in field |
| New cumulative acceptance metric unsupported by C++ | Python control rule plus candidate `metrics` | Duplicating a built-in metric |

## Parameters

Default to no custom parameters:

```python
class MyHook(ForestTendingHook):
    fields = []
    parameters = []
```

Never declare DBH, height, crown dimensions, species, straightness, stand area, tree count, dominant height, basal area, or another existing input attribute as a `Parameter`. Read the built-in field instead:

```python
dbh = tree.number(TreeFields.DBH, 0.0)
```

Do not create parameters for built-in final controls. For example, harvest intensity and minimum post-harvest crown closure belong to the C++ control configuration, not the hook's `parameters` list.

Declare a parameter only when the user needs to tune script-specific behavior and no existing setting represents it. A custom neighborhood radius is a valid example when it controls only Python ranking logic:

```python
from forest_tending_sdk import Parameter

COMPETITION_RADIUS = Parameter.number(
    "competition_radius",
    "Competition Radius",
    default=8.0,
    minimum=1.0,
    maximum=50.0,
    step=0.5,
    unit="m",
    group="Harvest Ranking",
    description="Neighborhood radius used only by the custom Python ranking logic.",
)

class MyHook(ForestTendingHook):
    fields = []
    parameters = [COMPETITION_RADIUS]
```

Read values with:

```python
radius = ctx.parameters.number(COMPETITION_RADIUS)
```

## Validation Checklist

- Use only SDK classes for hook input/output.
- Ensure every emitted tree ID is positive and exists in `ctx.trees`.
- Do not emit duplicate target or harvest IDs.
- Do not emit harvest IDs that are final target trees.
- Ensure scores and metric values are finite.
- Keep dynamic attribute keys free of dots.
- Verify that no built-in tree or stand attribute was declared as a `Parameter` or duplicate `Field`.
- Verify that harvest percentage, basal-area removal, crown closure, crown-closure change, and canopy-gap limits were not reimplemented as Python parameters or control rules.
- Justify every custom `Parameter`: it must be user-tunable and have no existing SDK/C++ representation.
- Resolve the target script path from the user's explicit path or the selected LiDAR360 installation. Never save relative to the skill repository merely because it is the current working directory.
- Use the Python executable at `<LiDAR360 root>/python310/python.exe`. The current installation root directly contains `LiDAR360.exe`, `config`, and `python310`; do not insert an extra `bin` directory.
- Always run `python.exe -m py_compile <script.py>` with the selected installation's Python. Run `python.exe <script.py> --lidar360-schema` only when that installation exposes `forest_tending_sdk` to standalone Python. Some installations inject the SDK from the LiDAR360 process; for those, validate schema by loading or refreshing the script in LiDAR360. A standalone `ModuleNotFoundError` is then an environment limitation, not a syntax failure.
- For a newly generated hook, also create a separate plan JSON following `plan_config.md`. Do not modify the built-in `crop-tree-selection.json` or `crope-tree-selection-script.py`.
