# forestry Usage Examples

## Example 1: Query All Tree Species

**Scenario**: Retrieve all tree species information from the LiDAR360 tree species library

```json
{
  "keyword": ""
}
```

**Expected Result**: Returns detailed information for all tree species, including scientific names, common names, whether biomass models are supported, and whether tree species identification is supported.

## Example 2: Query Tree Species by Keyword

**Scenario**: Search for tree species containing "pine"

```json
{
  "keyword": "pine"
}
```

**Expected Result**: Returns information for all tree species whose names contain the keyword.

## Example 3: Get Available Tree Species Identification Models

**Scenario**: Retrieve all available point cloud and panorama image tree species identification models

```json
{}
```

**Expected Result**: Returns a list of available models, including point cloud model names and panorama image model names, which can be directly used with the identification tools in forestry_airborne and forestry_terrestrial.
