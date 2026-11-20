# General Workflow Index

> This directory records cross-module workflows that do not belong to a single module. Module-internal workflows are still governed by each module's `references/{module}/workflows.md`.

---

## Workflow List

| Workflow File | Applicable Scenario | Brief Description |
|---------|---------|---------|
| [`uav.md`](uav.md) | UAV / Airborne LiDAR data processing | Complete cross-module workflow from DJI raw data reconstruction, strip adjustment, trajectory cutting, redundancy removal, point cloud preprocessing to ground point and deep learning classification. |

---

## Usage Conventions

- When handling cross-module tasks, refer to this index first to select the appropriate workflow file.
- When handling single-module tasks, refer to the `workflows.md` indexed in the corresponding module skill first.
- When adding new non-module workflows in the future, append the workflow file, applicable scenario, and brief description to this file.
