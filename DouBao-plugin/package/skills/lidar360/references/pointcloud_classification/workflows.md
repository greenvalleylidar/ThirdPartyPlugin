# Point Cloud Classification Workflows

## Workflow A: Traditional Classification

```text
Get input information and class distribution
→ Select classification tool and read schema
→ Execute general and specific preflight checks
→ Present in-place modification targets and class impact
→ Obtain explicit user confirmation
→ Execute serially
→ Review class distribution and file readability
```

## Workflow B: Existing Model Inference

```text
Confirm input type and target classes
→ Read inference tool schema
→ Verify model/weights, version, and runtime resources
→ Verify GPU parameter fields and CPU fallback support
→ Obtain L3 confirmation for in-place modifications
→ Execute inference
→ Validate output classes, CSV, or schema-declared results
```

## Workflow C: Training to Inference

```text
Confirm training objectives and class mappings
→ Read training tool schema
→ Verify training set, validation set, and labels
→ Present model, resources, training parameters, and output location
→ Obtain user confirmation for long-running task
→ Execute training
→ Validate model and logs
→ Read corresponding inference tool schema
→ Run inference on independent validation data
→ Validate results before applying to production data
```

## Failure and Interruption

- Missing schema, data, model, or confirmation: `blocked`.
- Training or inference returns error: `failed`, retry at most once per error protocol.
- Partial success on batch input: `partial`, report per file.
- Use `cancelled` only when the interface explicitly returns a cancellation status.
