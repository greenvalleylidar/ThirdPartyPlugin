---
name: lidar360-forestry
description: General forestry tools. Provides tree species query and tree species identification model retrieval capabilities.
---

Before executing any tool, you must follow the runtime schema retrieval, confirmation gate, and result contract defined in references/profiles/tool_call_conventions.md.

# forestry General Forestry Module

## Module Overview

The General Forestry module provides tree species database query and tree species identification model retrieval capabilities for LiDAR360, used by the tree species identification tools in the forestry_airborne and forestry_terrestrial modules.

## When to Invoke

- User needs to query tree species information (scientific name, common name, biomass model support, etc.)
- User needs to get the available tree species identification model list
- User mentions "tree species query", "tree species database", "identification model list"

## Invocation Convention

Read `references/forestry/tools.md` to get the tool registry.
Read `references/forestry/preflight_checks.md` and execute preflight checks before running.
Refer to `references/forestry/examples.md` for usage examples.

Pass documents under `references/forestry/` as context when invoking:
- `read_file('references/forestry/tools.md')`
- `read_file('references/forestry/preflight_checks.md')`
- `read_file('references/forestry/examples.md')`

## Tool List

### Tree Species Query
| Tool ID | Function | Input Format | Key Parameters |
|-------|------|---------|---------|
| `query_tree_species` | Query tree species information from LiDAR360 tree species database; empty keyword returns all | - | keyword |
| `get_tree_species_identification_models` | Get all available tree species identification model names (point cloud models and panoramic image models) | - | - |

## Usage Flow

1. **Query tree species**: Use `query_tree_species` to search by keyword or get the full tree species list
2. **Get models**: Use `get_tree_species_identification_models` to get available identification model names
3. **Use models**: Pass the retrieved model names to identification tools in forestry_airborne or forestry_terrestrial
