# Repository Structure

This document describes the reorganized structure of the yggdraphitecho repository after the November 2025 reorganization to fix fragmentation issues.

## 📁 Directory Organization

### Root Level

The root directory now contains only **core entry points** and **essential configuration files**:

```
yggdraphitecho/
├── hypergraph_api.py              # Main hypergraph API entry point
├── hypergraph_service.py          # Hypergraph service entry point
├── hypergraph_model_runner.py     # Model runner entry point
├── run_deep_tree_echo_server.py   # Deep Tree Echo server entry point
├── setup.py                       # Package setup configuration
├── use_existing_torch.py          # PyTorch build configuration
├── pyproject.toml                 # Project configuration
├── README.md                      # Main documentation
└── requirements/                  # Dependency specifications
```

### Core Systems

```
├── aphrodite/                     # Aphrodite inference engine (core)
│   ├── attention/                 # Attention mechanisms
│   ├── compilation/               # Model compilation
│   ├── endpoints/                 # API endpoints
│   ├── modeling/                  # Model implementations
│   ├── quantization/              # Quantization utilities
│   └── ...                        # Other core components
│
├── echo/                          # Echo cognitive systems
│   ├── dash/                      # Echo.Dash dashboard
│   ├── dream/                     # Echo.Dream (AAR architecture)
│   ├── files/                     # Echo.Files
│   ├── kern/                      # Echo.Kern
│   ├── rkwv/                      # Echo.RKWV
│   └── self/                      # Echo.Self evolution engine
│
└── yggdrasil_integration/         # Yggdrasil integration layer
    ├── bridge/                    # Aphrodite bridge
    ├── core/                      # Core integration
    ├── dtesn/                     # Deep Tree Echo Network
    ├── fusion/                    # System fusion
    ├── membranes/                 # Membrane architecture
    ├── plingua/                   # P-Lingua integration
    ├── rros/                      # RROS integration
    ├── transformer/               # Transformer schema
    └── triadic/                   # Triadic architecture
```

### Examples (NEW)

Organized demonstration scripts showing system capabilities:

```
examples/
├── README.md                      # Examples overview
├── aar/                           # Agent-Arena-Relation examples
│   ├── demo_aar_system.py
│   ├── demo_arena_simulation_framework.py
│   └── demo_echo_aar_integration.py
│
├── backend/                       # Backend service examples
│   ├── demo_async_server_processing.py
│   ├── demo_backend_performance_monitoring.py
│   ├── demo_batching_system.py
│   ├── demo_hardware_abstraction.py
│   ├── demo_optimization_showcase.py
│   ├── demo_scalability_framework.py
│   └── ... (15 total)
│
├── deep_tree_echo/                # Deep Tree Echo examples
│   ├── demo_deep_tree_echo_endpoints.py
│   ├── demo_deep_tree_echo_fusion.py
│   ├── demo_deep_tree_echo_interactive.py
│   ├── demo_deep_tree_echo_memory.py
│   ├── usage_example_deep_tree_echo.py
│   └── ... (8 total)
│
├── middleware/                    # Middleware examples
│   ├── demo_advanced_middleware_stack.py
│   ├── demo_content_negotiation.py
│   ├── demo_enterprise_security.py
│   └── ... (4 total)
│
├── monitoring/                    # Monitoring examples
│   ├── demo_error_monitoring.py
│   ├── demo_monitoring_standalone.py
│   ├── demo_server_monitoring.py
│   └── ... (6 total)
│
├── training/                      # Training & learning examples
│   ├── demo_continuous_learning.py
│   ├── demo_curriculum_learning.py
│   ├── demo_meta_learning.py
│   ├── demo_multi_agent_training.py
│   └── ... (8 total)
│
└── embodiment/                    # Embodiment examples
    ├── demo_body_state_awareness.py
    ├── demo_multimodal_sensors.py
    └── demo_virtual_body.py
```

### Integrations (NEW)

Integration scripts for external systems:

```
integrations/
├── README.md
├── alerting/                      # Alerting integrations
│   ├── integration_demo_alerting.py
│   └── demo_production_alerting.py
│
├── continuous_learning/           # Continuous learning integrations
│   └── integration_example_server_side_continuous_learning.py
│
├── environment/                   # Environment coupling
│   └── integration_example_environment_coupling.py
│
└── fusion/                        # System fusion
    └── deep_tree_echo_fusion.py
```

### Scripts (ENHANCED)

Utility scripts organized by purpose:

```
scripts/
├── README.md
├── analysis/                      # Analysis utilities (NEW)
│   ├── analysis_script.py
│   ├── analyze_identity_fragments.py
│   ├── forensic_analysis.py
│   └── update_*.py
│
├── benchmarks/                    # Performance benchmarks (NEW)
│   ├── benchmark_dtesn_serialization.py
│   └── benchmark_evolution.py
│
├── database/                      # Database utilities (NEW)
│   ├── sync_databases_comprehensive.py
│   ├── sync_databases_neon.py
│   └── sync_via_neon_mcp.py
│
├── debug/                         # Debug utilities (NEW)
│   ├── debug_motor_execution.py
│   ├── debug_target_propagation.py
│   └── debug_trajectory_timing.py
│
├── deployment/                    # Deployment scripts (NEW)
│   ├── lightning_app.py
│   ├── lightning_manager.py
│   └── personal_studio_setup.py
│
├── validation/                    # Validation scripts (existing)
│   └── ... (25 validation scripts)
│
├── env.py                         # Environment utilities
├── fix_script.py                  # Fix utilities
├── reorganize_repository.py       # Repository reorganization
└── reorganize_remaining_files.py  # Second pass reorganization
```

### Prototypes (NEW)

Experimental and prototype implementations:

```
prototypes/
├── README.md
├── quantum_hypergraph/            # Quantum hypergraph experiments
│   └── quantum_hypergraph_prototype.py
│
├── senas/                         # SENAS prototype
│   └── senas_prototype.py
│
└── standalone_config_test.py      # Configuration testing
```

### Tests

Comprehensive test suite:

```
tests/
├── README.md
├── aar/                           # AAR tests
├── aphrodite_test_utils/          # Test utilities
├── basic_correctness/             # Correctness tests
├── benchmarks/                    # Benchmark tests
├── integration/                   # Integration tests
├── kernels/                       # Kernel tests
├── models/                        # Model tests
├── unit/                          # Unit tests
└── ... (many more test categories)
```

### Documentation

```
docs/                              # Documentation
wiki/                              # Wiki content
├── docs/
├── features/
└── source/
```

## 🎯 Key Improvements

### Before Reorganization
- ❌ 78 Python files in root directory
- ❌ No clear organization
- ❌ Difficult to navigate
- ❌ Mixed concerns (demos, utilities, prototypes)

### After Reorganization
- ✅ Only 6 essential files in root (92% reduction!)
- ✅ Clear categorical organization
- ✅ Easy navigation with README files
- ✅ Separated concerns (examples, integrations, scripts, prototypes)

## 📖 Usage Guide

### Running Examples

```bash
# From repository root
python3.11 examples/aar/demo_aar_system.py

# Or navigate to directory
cd examples/deep_tree_echo
python3.11 usage_example_deep_tree_echo.py
```

### Running Integrations

```bash
python3.11 integrations/alerting/integration_demo_alerting.py
```

### Running Scripts

```bash
# Benchmarks
python3.11 scripts/benchmarks/benchmark_dtesn_serialization.py

# Database utilities
python3.11 scripts/database/sync_databases_comprehensive.py

# Debug utilities
python3.11 scripts/debug/debug_motor_execution.py
```

### Running Prototypes

```bash
python3.11 prototypes/quantum_hypergraph/quantum_hypergraph_prototype.py
```

## 🔍 Finding Specific Functionality

### By Category

| What you need | Where to look |
|---------------|---------------|
| AAR system examples | `examples/aar/` |
| Backend/server examples | `examples/backend/` |
| Deep Tree Echo usage | `examples/deep_tree_echo/` |
| Middleware patterns | `examples/middleware/` |
| Monitoring examples | `examples/monitoring/` |
| Training/learning | `examples/training/` |
| Embodiment/sensors | `examples/embodiment/` |
| External integrations | `integrations/` |
| Performance benchmarks | `scripts/benchmarks/` |
| Database tools | `scripts/database/` |
| Debug utilities | `scripts/debug/` |
| Deployment scripts | `scripts/deployment/` |
| Analysis tools | `scripts/analysis/` |
| Experimental code | `prototypes/` |

### By Functionality

**API Servers & Entry Points** (root level):
- `hypergraph_api.py` - Hypergraph API
- `hypergraph_service.py` - Hypergraph service
- `run_deep_tree_echo_server.py` - Deep Tree Echo server

**Core Systems**:
- `aphrodite/` - Inference engine
- `echo/` - Cognitive systems
- `yggdrasil_integration/` - Integration layer

**Learning Examples**:
- `examples/training/` - All training examples

**Monitoring & Observability**:
- `examples/monitoring/` - Monitoring examples
- Backend monitoring in `examples/backend/`

**System Integration**:
- `integrations/` - External system integrations
- `yggdrasil_integration/` - Core integration layer

## 📚 Documentation

Each major directory contains a README.md file with:
- Purpose and overview
- List of files and their functions
- Usage examples
- Related documentation links

Start with:
1. Main `README.md` - Project overview
2. `examples/README.md` - Examples overview
3. Category-specific READMEs - Detailed information

## 🔄 Migration Guide

If you have existing code or scripts that reference old paths:

### Path Changes

| Old Path | New Path |
|----------|----------|
| `./demo_*.py` | `examples/*/demo_*.py` |
| `./integration_*.py` | `integrations/*/integration_*.py` |
| `./benchmark_*.py` | `scripts/benchmarks/benchmark_*.py` |
| `./debug_*.py` | `scripts/debug/debug_*.py` |
| `./sync_*.py` | `scripts/database/sync_*.py` |
| `.*_prototype.py` | `prototypes/*/` |

### Import Updates

If you import from moved files, update import paths:

```python
# Old
from demo_aar_system import AARSystem

# New
from examples.aar.demo_aar_system import AARSystem
```

### Script Execution

Update script execution paths:

```bash
# Old
python3.11 demo_aar_system.py

# New
python3.11 examples/aar/demo_aar_system.py
```

## 🎉 Benefits

1. **Improved Navigation**: Clear structure makes finding code easy
2. **Better Organization**: Related files grouped together
3. **Reduced Cognitive Load**: Fewer root files to scan
4. **Easier Onboarding**: New developers can understand structure quickly
5. **Maintainability**: Clear separation of concerns
6. **Scalability**: Structure supports future growth

## 📊 Statistics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Root Python Files | 78 | 6 | 92% reduction |
| Organization Score | Poor | Excellent | Dramatic |
| Navigation Ease | Difficult | Easy | Significant |
| Maintainability | Low | High | Major |

---

**Reorganization Date**: November 9, 2025  
**Reorganization Tool**: Super-Sleuth Intro-spect + Hyper-Holmes Turbo-Solve  
**Files Reorganized**: 72 files moved to logical locations  
**Status**: ✅ Complete
