# LiDAR360 Error Handling Reference

> **Processing Logic**:
> 1. All API responses return `{"code": 0, "data": {...}, "msg": "..."}`. `code == 0` means success; use the `data` content.
> 2. If `code != 0`, **prioritize parsing the `msg` field** for keyword matching; `code` serves only as a classification clue.
> 3. After matching a keyword, execute the corresponding action, then **retry the API call once**.
> 4. If no match is found or retry still fails, collect logs and guide the user to submit a support request.


## I. Special Rules: Error Codes 1-10 (JSON Parameters Fail Schema Validation)

**Trigger**: The JSON parameters passed to the API fail server-side schema validation; business logic has not yet executed.

| Code Range | Typical `msg` Keywords | Root Cause | Recommended Action |
| :------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **1-10** | `"Parameter validation failed"`, `"missing required property"`, `"type should be"`, `"additionalProperties not allowed"`, `"expected type"` | JSON missing required fields, wrong field types, undefined extra keys, invalid enum values | 1. Check the complete JSON parameters passed.<br>2. Compare against the API schema: fill in missing required fields; convert field types to correct types (String/Number/Boolean/Array); remove extra keys; correct enum values to allowed ones.<br>3. Retry with the corrected JSON. |


## II. 4xx Errors: Input/Parameter/File Issues (Self-Service Fix)

| Error Code | Typical `msg` Keywords | Root Cause | Recommended Action |
| :---------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **400** | `"Input data is empty"`, `"No data loaded"` | Algorithm executed without loading data | 1. Check if data is loaded; 2. Load `.las`/`.tif` files; 3. Check if the target layer is selected in the algorithm dialog |
| **401** | `"Input data is invalid"`, `"Invalid data"`, `"corrupted"` | Data content mismatch (e.g., point cloud passed as imagery) or file corruption | 1. Verify file readability with third-party software; 2. Confirm the data type required by the algorithm and reselect correct data |
| **402** | `"Data object is empty"`, `"intermediate result is null"` | Upstream prerequisite step did not execute successfully | 1. Go back and re-execute all prerequisite steps until successful; 2. If invalid, restart the software to clear memory state |
| **410** | `"File does not exist"`, `"File not found"`, `"No such file"` | File moved/renamed/network disconnected | 1. Check if the path in `msg` is valid; 2. Re-locate the file; 3. Copy to a local drive (e.g., `D:/Data/`) before operating |
| **411** | `"Attribute field does not exist"`, `"Missing attribute"`, `"field [X] not found"` | Data lacks attribute fields required by the algorithm (e.g., `Intensity`, `Classification`) | 1. Check current data field list; 2. Use "Add/Compute Attributes" to generate virtual fields; 3. If not possible, re-acquire data with complete attributes |
| **412** | `"File format is invalid"`, `"Unrecognized format"` | Corrupted file header or extension mismatch with actual format | 1. Confirm the actual format; 2. For ASCII text, use "Import ASCII" instead of opening directly; 3. Re-export original data |
| **413** | `"Reference file does not exist"`, `"Referenced [file] not found"` | External reference file path in algorithm config is invalid | 1. Check reference paths; 2. Clear invalid paths or re-specify valid files; 3. If not needed, disable "Enable Reference" |
| **420** | `"Insufficient data"`, `"Too few points"`, `"Minimum required: [N]"` | Points in the selected area are below the algorithm minimum threshold | 1. Expand the clipping range or merge adjacent tiles; 2. Check if filters are enabled causing drastic point reduction; temporarily disable them |
| **421** | `"Data quality insufficient"`, `"Poor quality"`, `"overlap too low"` | Point density too low or registration overlap insufficient | 1. Lower the "Minimum Matching Features" threshold; 2. Before registration, ensure an initial transformation matrix (coarse registration) is provided |
| **422** | `"No valid output"`, `"No valid output generated"` | Algorithm completed but output is null | 1. Relax algorithm thresholds (e.g., angle threshold from 80 to 89); 2. Confirm data contains target features; 3. Disable tiling and recompute the entire area |
| **423** | `"Data too sparse"`, `"Sparse point cloud"` | Points distributed very unevenly with large gaps | 1. If supported, enable "Sparse Compensation" or "Interpolation"; 2. Narrow the scope to dense areas; 3. Avoid algorithms that rely on neighborhood analysis |
| **424** | `"Range too small"`, `"Bounding box too small"` | Selected spatial extent is smaller than the algorithm minimum resolution | 1. Re-select a larger ROI; 2. Check for zero or negative coordinate values in parameters |
| **430** | `"Invalid parameter"`, `"Invalid parameter"`, `"[param] is null"` | Required parameter left empty | 1. Fill in reasonable values for all required fields; 2. Click "Restore Default Parameters" to reset |
| **431** | `"Parameter out of range"`, `"Out of range"`, `"must be between [A] and [B]"` | Numeric value exceeds physical/logical bounds | 1. Read the valid range from `msg`; 2. Clamp the parameter to the valid range; 3. Ensure integer types do not contain decimals |
| **432** | `"Parameter mismatch"`, `"Conflict"`, `"[A] cannot be greater than [B]"` | Conflicting related parameters | 1. Check mutually exclusive parameters (e.g., min height > max height); 2. Auto-swap values or re-enter |
| **433/434** | `"Type error"`, `"Type mismatch"`, `"Invalid format"` | Field type mismatch or format error | 1. Auto-convert types (e.g., `"1"` to `1`); 2. If conversion fails, refer to the example format (e.g., `0.01` instead of `1cm`) |
| **440/441** | `"Unsupported data format"`, `"Unsupported extension: [.xxx]"` | Current function does not support this format | 1. Check the supported format whitelist; 2. Use the "Format Conversion" tool to convert to a supported format, then retry |


## III. 5xx Errors: Algorithm/Environment Exceptions (Retry Once, Then Report)

| Error Code | Typical `msg` Keywords | Root Cause | Recommended Action |
| :---------- | :----------------------------------------------------------- | :-------------------------------- | :----------------------------------------------------------- |
| **500** | `"Algorithm execution failed"`, `"Core exception"`, `"at tile [X]"` | Algorithm core computation triggered an uncaught exception | 1. Retry once immediately; 2. If tile number is provided, process that tile individually; 3. If still failing, collect logs and report |
| **501** | `"Algorithm step failed"`, `"Step [StepName] failed"` | An intermediate step in a multi-stage algorithm failed | 1. Parse `StepName`; 2. If supported, invoke that step individually with adjusted parameters; 3. Otherwise retry the entire process with relaxed tolerances |
| **502** | `"Algorithm did not converge"`, `"Did not converge"`, `"Max iterations exceeded"` | Iterative algorithm reached max iterations without meeting accuracy | 1. Double the max iterations; 2. Relax convergence tolerance by 1-2 orders of magnitude; 3. Check if initial pose was provided |
| **503** | `"Invalid algorithm result"`, `"Result validation failed"`, `"NaN detected"` | Output contains NaN/Inf or singular matrix | 1. Perform outlier removal (SOR filter); 2. Remove duplicate coordinate points; 3. Try a different parameter combination or alternative algorithm |
| **504** | `"Index build failed"`, `"KD-Tree error"`, `"Octree creation failed"` | Spatial index construction failed (often co-occurs with 530) | 1. Refer to 530 handling first; 2. Split point cloud into 2-4 blocks and build indices separately |
| **510** | `"File write failed"`, `"Permission denied"`, `"No space left"` | Output directory has no write permission or disk space is insufficient | 1. Check remaining space; clean up or change drive if insufficient; 2. Change output path to user directory; 3. Retry with administrator privileges |
| **511** | `"File read failed"`, `"Access denied"`, `"File in use"` | File is exclusively locked by another process | 1. Close other programs using the file; 2. If on NAS/USB drive, copy to local drive first; 3. Temporarily disable antivirus software |
| **520** | `"External program not found"`, `"[ExeName] not found"`, `"PATH error"` | Third-party dependency not installed or environment variable not configured | 1. Check if the program exists under `bin/`; 2. Run the "Repair Dependencies" tool; 3. Manually add the program directory to `PATH` |
| **521/522** | `"External program startup failed"`, `"External process crashed"`, `"exit code [X]"` | Version incompatibility or runtime crash | 1. Confirm version match; 2. Run manually from command line to observe errors; 3. Check if path contains non-ASCII characters or spaces |
| **523** | `"External program timeout"`, `"Timeout after [N]s"` | Single processing timeout | 1. Split data for parallel processing; 2. If supported, increase the `Timeout` value; 3. Upgrade hardware |
| **524** | `"Model training failed"`, `"Training loss is NaN"`, `"Insufficient samples for class [X]"` | Sample imbalance or label coordinate system inconsistency | 1. Ensure each class has at least >50 samples; 2. Check that labels and point cloud coordinate systems are consistent; 3. Reduce `Batch Size` or learning rate |
| **530** | `"Out of Memory"`, `"Out of Memory"`, `"Failed to allocate [N] MB"` | Physical RAM or GPU VRAM exhausted | 1. **Primary**: Reduce "Block Size" by half (e.g., 100m to 50m); 2. Close other memory-intensive applications; 3. Increase virtual memory to 1.5x physical memory; 4. For over 500 million points, use a 64GB+ workstation |
| **540** | `"Cancelled by user"`, `"Cancelled by user"` | User manually interrupted the operation | Normal termination; no action needed |


## IV. Fallback Strategy (When Unable to Handle)

When `msg` keywords do not match any entry in the above tables, or when **retrying once** still fails, guide the user with the following message:

> "The API call returned an error (Code: [code]) and automatic recovery was unsuccessful. Please provide:
> 1. The latest `.log` file from today in the `%TEMP%/LiDAR360 V10.0 Alpha/Log/` folder.
> 2. The complete red error log text from the log output window.
> 3. The software version number (Help > About).
> Submit the above information to the GreenValley technical support team."

---

## Quick Reference

| Scenario | Key Action |
| :------------------ | :------------------------------- |
| `code == 0` | Use `data` directly; workflow complete |
| `code in [1, 10]` | Check and correct request JSON structure |
| `code in [400, 441]` | Check input data, file paths, and parameter configuration |
| `code in [500, 530]` | Reduce data volume or relax precision; retry once |
| `code == 530` | Prioritize reducing block size |
| `code == 540` | User cancelled; normal termination |
| Retry still fails | Collect logs and escalate to technical support |
