# Migration Guide: Repository Reorganization

## Overview

On November 9, 2025, the yggdraphitecho repository underwent a comprehensive reorganization to fix fragmentation issues. This guide helps you adapt to the new structure.

## What Changed

### Summary
- **72 files** moved from root to organized subdirectories
- **Root files reduced** from 78 to 6 (92% reduction)
- **New directories created**: `examples/`, `integrations/`, `scripts/` subdirectories, `prototypes/`
- **Core entry points** remain in root (no breaking changes for main APIs)

### Files That Stayed in Root

These files remain in the root directory and **require no changes**:

```
✅ hypergraph_api.py              # Main API - unchanged
✅ hypergraph_service.py          # Service - unchanged  
✅ hypergraph_model_runner.py     # Model runner - unchanged
✅ run_deep_tree_echo_server.py   # Server - unchanged
✅ setup.py                       # Setup - unchanged
✅ use_existing_torch.py          # Build config - unchanged
```

**If you only use these entry points, no changes are needed!**

## Quick Reference: File Relocations

### Demo Files → `examples/`

All `demo_*.py` files moved to categorized subdirectories:

| Old Location | New Location | Category |
|-------------|--------------|----------|
| `demo_aar_system.py` | `examples/aar/` | AAR |
| `demo_async_server_processing.py` | `examples/backend/` | Backend |
| `demo_deep_tree_echo_*.py` | `examples/deep_tree_echo/` | Deep Tree Echo |
| `demo_advanced_middleware_stack.py` | `examples/middleware/` | Middleware |
| `demo_*_monitoring.py` | `examples/monitoring/` | Monitoring |
| `demo_continuous_learning.py` | `examples/training/` | Training |
| `demo_body_state_awareness.py` | `examples/embodiment/` | Embodiment |

### Integration Files → `integrations/`

| Old Location | New Location |
|-------------|--------------|
| `integration_demo_alerting.py` | `integrations/alerting/` |
| `integration_example_server_side_continuous_learning.py` | `integrations/continuous_learning/` |
| `integration_example_environment_coupling.py` | `integrations/environment/` |
| `deep_tree_echo_fusion.py` | `integrations/fusion/` |

### Utility Scripts → `scripts/`

| Old Location | New Location |
|-------------|--------------|
| `benchmark_*.py` | `scripts/benchmarks/` |
| `debug_*.py` | `scripts/debug/` |
| `sync_*.py` | `scripts/database/` |
| `lightning_*.py` | `scripts/deployment/` |
| `analysis_*.py` | `scripts/analysis/` |
| `update_*.py` | `scripts/analysis/` |

### Prototypes → `prototypes/`

| Old Location | New Location |
|-------------|--------------|
| `quantum_hypergraph_prototype.py` | `prototypes/quantum_hypergraph/` |
| `senas_prototype.py` | `prototypes/senas/` |
| `standalone_config_test.py` | `prototypes/` |

## Migration Steps

### For Script Users

If you run scripts directly:

**Before:**
```bash
python3.11 demo_aar_system.py
```

**After:**
```bash
python3.11 examples/aar/demo_aar_system.py
```

**Or navigate first:**
```bash
cd examples/aar
python3.11 demo_aar_system.py
```

### For Python Imports

If you import from moved files:

**Before:**
```python
from demo_aar_system import AARSystem
from integration_demo_alerting import setup_alerting
from benchmark_evolution import run_benchmark
```

**After:**
```python
from examples.aar.demo_aar_system import AARSystem
from integrations.alerting.integration_demo_alerting import setup_alerting
from scripts.benchmarks.benchmark_evolution import run_benchmark
```

### For Shell Scripts

If you have shell scripts that reference files:

**Before:**
```bash
#!/bin/bash
python3.11 demo_continuous_learning.py
python3.11 sync_databases_neon.py
```

**After:**
```bash
#!/bin/bash
python3.11 examples/training/demo_continuous_learning.py
python3.11 scripts/database/sync_databases_neon.py
```

### For Documentation/README Links

Update any documentation links:

**Before:**
```markdown
See [demo_aar_system.py](demo_aar_system.py) for examples.
```

**After:**
```markdown
See [demo_aar_system.py](examples/aar/demo_aar_system.py) for examples.
```

## Common Scenarios

### Scenario 1: Running Examples

**Task**: Run an example script

**Solution**:
1. Check `examples/README.md` for category
2. Navigate to appropriate subdirectory
3. Run script

```bash
# Find the example
ls examples/*/demo_*.py

# Run it
python3.11 examples/aar/demo_aar_system.py
```

### Scenario 2: Finding Integration Scripts

**Task**: Find integration scripts

**Solution**:
1. Check `integrations/README.md`
2. Look in category subdirectories

```bash
# List all integrations
ls integrations/*/

# Run integration
python3.11 integrations/alerting/integration_demo_alerting.py
```

### Scenario 3: Running Benchmarks

**Task**: Run performance benchmarks

**Solution**:
```bash
# All benchmarks now in scripts/benchmarks/
python3.11 scripts/benchmarks/benchmark_dtesn_serialization.py
```

### Scenario 4: Database Utilities

**Task**: Sync databases

**Solution**:
```bash
# All database scripts in scripts/database/
python3.11 scripts/database/sync_databases_neon.py
```

### Scenario 5: Debugging

**Task**: Use debug utilities

**Solution**:
```bash
# All debug scripts in scripts/debug/
python3.11 scripts/debug/debug_motor_execution.py
```

## Breaking Changes

### None for Core APIs

**Good news**: The main entry points remain unchanged:
- `hypergraph_api.py`
- `hypergraph_service.py`
- `hypergraph_model_runner.py`
- `run_deep_tree_echo_server.py`

**If you only use these, no changes needed!**

### For Direct File Access

If you directly accessed demo/integration/utility files, update paths as shown above.

### For Git Workflows

Git history is preserved. Use `git log --follow` to track moved files:

```bash
# Track a moved file
git log --follow examples/aar/demo_aar_system.py
```

## Finding Files

### Method 1: Use README Files

Each directory has a README.md listing all files:

```bash
cat examples/README.md
cat examples/aar/README.md
cat integrations/README.md
```

### Method 2: Use Find Command

```bash
# Find all demo files
find examples -name "demo_*.py"

# Find all integration files
find integrations -name "*.py"

# Find specific file
find . -name "demo_aar_system.py"
```

### Method 3: Use Grep

```bash
# Search for functionality
grep -r "AAR" examples/*/README.md
```

### Method 4: Check REPOSITORY_STRUCTURE.md

See `REPOSITORY_STRUCTURE.md` for complete directory layout and file listings.

## Updating Your Projects

### Step 1: Update Script Paths

Find all references to moved files:

```bash
# In your project
grep -r "demo_" your_project/
grep -r "integration_" your_project/
grep -r "benchmark_" your_project/
```

### Step 2: Update Imports

Replace old imports with new paths:

```python
# Old imports
from demo_aar_system import *
from integration_demo_alerting import *

# New imports
from examples.aar.demo_aar_system import *
from integrations.alerting.integration_demo_alerting import *
```

### Step 3: Update Documentation

Update any documentation referencing old paths.

### Step 4: Test

Run your tests to ensure everything works:

```bash
pytest your_project/tests/
```

## Automated Migration

### Search and Replace

Use this script to update imports in your code:

```python
#!/usr/bin/env python3.11
"""
Update imports to new structure
"""

import re
from pathlib import Path

# Mapping of old imports to new imports
IMPORT_MAPPINGS = {
    r'from demo_aar_system': 'from examples.aar.demo_aar_system',
    r'from demo_async_server': 'from examples.backend.demo_async_server',
    r'from demo_deep_tree_echo': 'from examples.deep_tree_echo.demo_deep_tree_echo',
    r'from integration_demo_alerting': 'from integrations.alerting.integration_demo_alerting',
    r'from benchmark_': 'from scripts.benchmarks.benchmark_',
    r'from debug_': 'from scripts.debug.debug_',
    r'from sync_': 'from scripts.database.sync_',
    # Add more as needed
}

def update_imports(file_path: Path):
    """Update imports in a Python file"""
    content = file_path.read_text()
    
    for old, new in IMPORT_MAPPINGS.items():
        content = re.sub(old, new, content)
    
    file_path.write_text(content)

# Run on your project
for py_file in Path('your_project').rglob('*.py'):
    update_imports(py_file)
```

## FAQ

### Q: Will this break my existing code?

**A**: Only if you directly import from moved files. Core entry points are unchanged.

### Q: How do I find where a file moved?

**A**: Check this migration guide, `REPOSITORY_STRUCTURE.md`, or use `find`:
```bash
find . -name "your_file.py"
```

### Q: Can I still use old paths?

**A**: No, files have been physically moved. Update your references.

### Q: What if I can't find a file?

**A**: Check the "Quick Reference" section above or search:
```bash
find . -name "*keyword*.py"
```

### Q: Are there any performance impacts?

**A**: No, this is purely organizational. Performance is unchanged.

### Q: Will future updates follow this structure?

**A**: Yes, this is the new standard structure going forward.

## Support

If you encounter issues:

1. Check `REPOSITORY_STRUCTURE.md` for complete layout
2. Check README files in each directory
3. Use `find` to locate files
4. Review this migration guide
5. Check git history: `git log --follow <file>`

## Rollback (If Needed)

If you need to temporarily revert:

```bash
# This reorganization was committed in a series of commits
# To rollback, use git revert or reset to before the reorganization

# Find the commit before reorganization
git log --oneline | grep -B 1 "reorganization"

# Checkout that commit (temporary)
git checkout <commit-hash>

# Or revert (permanent)
git revert <reorganization-commits>
```

**Note**: Rollback is not recommended. Updating your code is the better path forward.

## Benefits of New Structure

1. ✅ **Easier Navigation**: Find files by category
2. ✅ **Better Organization**: Related files grouped together
3. ✅ **Clearer Purpose**: Directory names indicate content
4. ✅ **Improved Maintainability**: Easier to maintain organized code
5. ✅ **Faster Onboarding**: New developers understand structure quickly
6. ✅ **Scalability**: Structure supports growth

## Timeline

- **November 9, 2025**: Reorganization completed
- **Effective Immediately**: All new code should use new structure
- **Grace Period**: Update existing code at your convenience
- **Future**: New structure is permanent

---

**Questions?** Check `REPOSITORY_STRUCTURE.md` or repository README files.

**Reorganization Date**: November 9, 2025  
**Files Moved**: 72  
**Root Files Reduced**: 78 → 6 (92% reduction)  
**Status**: ✅ Complete
