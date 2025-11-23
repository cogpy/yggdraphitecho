# Workflow Fix Instructions

## Critical Issue: PyTorch Installation Failure

The GitHub Actions build workflow is failing because pip cannot find `torch==2.6.0+cpu` in the standard PyPI repository. This is the **most critical issue** preventing the build from completing.

## The Problem

The workflow tries to install PyTorch with:
```bash
pip install -r requirements/cpu.txt --timeout 18000
```

While `requirements/cpu.txt` contains:
```
--extra-index-url https://download.pytorch.org/whl/cpu
torch==2.6.0+cpu
```

However, pip doesn't always respect the `--extra-index-url` directive in requirements files, especially in CI environments, causing the error:
```
ERROR: Could not find a version that satisfies the requirement torch==2.6.0+cpu
ERROR: No matching distribution found for torch==2.6.0+cpu
```

## The Solution

The workflow file `.github/workflows/build-engine.yml` needs to be updated to explicitly pass the `--extra-index-url` flag to pip when installing requirements.

## How to Apply the Fix

### Option 1: Apply the Patch File (Recommended)

```bash
cd /path/to/yggdraphitecho
git apply WORKFLOW_FIX.patch
git add .github/workflows/build-engine.yml
git commit -m "🔥 Fix PyTorch installation failure in build workflow"
git push origin main
```

### Option 2: Manual Edit

Edit `.github/workflows/build-engine.yml`:

**Line 243:** Change timeout from 24000 to 360 minutes:
```yaml
timeout-minutes: 360  # 6 hours - realistic for complex CUDA builds
```

**Lines 422-427:** Replace the dependency installation section with:
```yaml
          # Install target-specific requirements with explicit PyTorch index URL
          if [ -f "requirements/${{ matrix.target_device }}.txt" ]; then
            # For CPU and CUDA builds, ensure PyTorch index is used
            if [ "${{ matrix.target_device }}" == "cpu" ]; then
              pip install -r requirements/${{ matrix.target_device }}.txt \
                --extra-index-url https://download.pytorch.org/whl/cpu \
                --timeout 18000
            elif [ "${{ matrix.target_device }}" == "cuda" ]; then
              pip install -r requirements/${{ matrix.target_device }}.txt \
                --extra-index-url https://download.pytorch.org/whl/cu124 \
                --timeout 18000
            else
              pip install -r requirements/${{ matrix.target_device }}.txt --timeout 18000
            fi
          elif [ -f "requirements/common.txt" ]; then
            pip install -r requirements/common.txt --timeout 18000
          fi
```

### Option 3: Use GitHub Web Interface

1. Go to https://github.com/cogpy/yggdraphitecho/blob/main/.github/workflows/build-engine.yml
2. Click the "Edit" button (pencil icon)
3. Make the changes described in Option 2
4. Commit directly to main or create a new branch

## Why This Wasn't Pushed Automatically

The GitHub App authentication used by this system doesn't have the `workflows` permission required to modify workflow files. This is a security feature to prevent unauthorized workflow modifications.

## Testing the Fix

After applying the fix:

1. Trigger a manual workflow run:
   ```bash
   gh workflow run build-engine.yml --ref main
   ```

2. Monitor the build:
   ```bash
   gh run watch
   ```

3. The build should now successfully install PyTorch and proceed to compilation

## Expected Results

After this fix:
- ✅ PyTorch installation will succeed
- ✅ Build will proceed to compilation phase
- ✅ All deep_tree_echo packages will be functional (already fixed in PR #23)
- ✅ Full build and deployment will complete without errors

## Additional Changes in This Fix

- **Reduced timeout:** Changed from 24000 minutes (unrealistic) to 360 minutes (6 hours)
- **Explicit index URL:** Added `--extra-index-url` for both CPU and CUDA builds
- **Better error handling:** Conditional logic ensures correct index URL for each target device

## Related Pull Request

PR #23 fixes the deep_tree_echo import errors. Once that is merged and this workflow fix is applied, the entire build pipeline should work correctly.

## Questions?

See BUILD_ANALYSIS.md for comprehensive analysis of all issues and fixes.
