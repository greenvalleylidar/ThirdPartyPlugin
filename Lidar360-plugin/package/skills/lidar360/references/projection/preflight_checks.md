# Projection Preflight Checks

## Check Flow Table

| Tool | Check Item | Check Method | Pass Condition |
|------|--------|----------|----------|
| define_projection | Input data exists | Check file path | File is accessible |
| define_projection | Input data format supported | Check file extension | Extension is in supported list |
| define_projection | Coordinate system parameters valid | Check EPSG code or WKT | Parameter format is correct |
| reproject | Input data exists | Check file path | File is accessible |
| reproject | Input data format supported | Check file extension | Extension is in supported list |
| reproject | Source coordinate system defined | Check data metadata | Data has coordinate system definition |
| reproject | Target coordinate system parameters valid | Check EPSG code or WKT | Parameter format is correct |
| reproject | Output path writable | Check directory permissions | Directory exists and is writable |

---

## Input Data Checks

### define_projection

| Check Item | Description | Failure Handling |
|--------|------|----------|
| File path | Input file must exist and be accessible | Prompt user to check path |
| File format | Must be a supported format | Prompt with supported format list |
| Data integrity | File must not be corrupted | Prompt that file may be corrupted |

### reproject

| Check Item | Description | Failure Handling |
|--------|------|----------|
| File path | Input file must exist and be accessible | Prompt user to check path |
| File format | Must be a supported format | Prompt with supported format list |
| Source coordinate system | Data must have a defined coordinate system | Prompt to use define_projection first |
| Output path | Output directory must exist and be writable | Prompt user to check output path |

---

## Coordinate System Parameter Checks

### EPSG Code Check

| Check Item | Description | Failure Handling |
|--------|------|----------|
| Format correct | Must follow EPSG:XXXX format | Prompt with correct format |
| Code valid | EPSG code must exist | Prompt that code is invalid |

### WKT Check

| Check Item | Description | Failure Handling |
|--------|------|----------|
| Syntax correct | WKT string must follow specification | Prompt with syntax error |
| Content complete | WKT must contain required elements | Prompt with missing elements |

### Seven-Parameter Check

| Check Item | Description | Failure Handling |
|--------|------|----------|
| Parameter count | Must provide 7 parameters | Prompt with incorrect parameter count |
| Parameter type | Must be numeric type | Prompt with type error |

---

## Output Path Check

### reproject

| Check Item | Description | Failure Handling |
|--------|------|----------|
| Directory exists | Output directory must exist | Prompt to create directory |
| Write permission | Must have write permission | Prompt with insufficient permissions |
| Disk space | Must have sufficient space | Prompt with insufficient space |

---

## Pre-Execution Check Template

Before executing the projection tool, please check in the following order:

1. **Input Data**
   - [ ] File path exists and is accessible
   - [ ] File format is in the supported list
   - [ ] Data is intact and not corrupted

2. **Coordinate System Parameters** (if used)
   - [ ] EPSG code format is correct and valid
   - [ ] Or WKT string syntax is correct and complete
   - [ ] Or seven-parameter count and type are correct

3. **Output Path** (reproject only)
   - [ ] Output directory exists
   - [ ] Has write permission
   - [ ] Has sufficient disk space

4. **Source Coordinate System** (reproject only)
   - [ ] Data has a defined coordinate system

---

Detailed parameters: {SKILL_DIR}/scripts/mcp-tool.exe get_tool_schema "projection-toolID"
