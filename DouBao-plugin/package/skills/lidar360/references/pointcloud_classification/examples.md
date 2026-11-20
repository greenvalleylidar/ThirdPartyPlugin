# Point Cloud Classification Examples

> Examples show structure only. Before execution, you must read the target tool schema and pass through the in-place modification or long-task confirmation gate.

## CSF Ground Classification

```json
{
  "tool": "classify_ground_by_csf",
  "params": {
    "input_data": ["D:/data/site.lidata"],
    "from_class": [0, 1],
    "to_class": 2,
    "scene_type": 2,
    "grid_size": 1.0,
    "classify_threshold": 0.5,
    "max_iterations": 500,
    "do_postprocessing": false
  }
}
```

This tool modifies source data in place. Before execution, list the input files and category changes, and obtain explicit L3 confirmation.

## Trained Model Inference

```text
1. Read the classify_by_trained_ml_model schema.
2. Verify the model field, input file list, and model compatibility.
3. If the schema indicates source data will be updated, obtain L3 confirmation.
4. After execution, inspect the output class distribution.
```

Model fields are not hardcoded in examples because their complete nested structure must be obtained from the current schema.

## Classification by Additional Attribute

Preconditions: the point cloud must already contain additional attributes and the `additional_attribute` field must exist and be non-empty; `min_value` and `max_value` are user-specified with `min_value <= max_value`; when `from_class` is omitted it applies to all classes.

```json
{
  "tool": "classify_by_additional_attribute",
  "params": {
    "input_data": ["D:/data/site.lidata"],
    "to_class": 6,
    "additional_attribute": "NDVI",
    "min_value": 0.3,
    "max_value": 1.0
  }
}
```

Output parameters are not hardcoded in the example; if the schema indicates source data will be updated, obtain explicit L3 confirmation before execution.

## Point Cloud Classification Model Training

```text
1. Read the train_point_cloud_classification_model schema.
2. Construct task_name, task_description, model, training, split_transform, and input_data according to the schema.
3. Validate training/validation data, labels, and class mappings.
4. Present resource parameters and output location, and obtain L3 confirmation.
5. After execution, verify model files and logs.
```

Do not promise checkpoint, cancellation, or resume capabilities unless the interface explicitly provides them.
