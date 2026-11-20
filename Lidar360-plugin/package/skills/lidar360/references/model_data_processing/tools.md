# Model Data Processing Tools Registration
---

## Model Merging
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| merge_libim_files | Merge multiple LiBIM files into one LiBIM file | LiBIM | - |
| merge_3dtiles | Merge multi 3d tiles root tileset into one | TILESET.JSON | - |

---

## Model Processing
| Tool ID | Function | Input | Required Parameters |
|-----|------|---------|---------|
| smooth_meshes | Smooth the triangulation model | LiTin/OBJ | smooth_iterations |

---

## Common Parameter Explanation

### Merge Methods
| Method | Description |
|---|------|
| Union | Union of all models |
| Intersection | Intersection of models |
| Append | Append models together |
| Layer | Layer-based merging |

### Smoothing Algorithms
| Algorithm | Description |
|---|------|
| Laplacian | Laplacian smoothing |
| HC | HC Laplacian smoothing |
| Taubin | Taubin smoothing |
| Bilateral | Bilateral filtering |

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "model_data_processing-toolID"
