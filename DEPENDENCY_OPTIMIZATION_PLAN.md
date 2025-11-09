# 📦 Dependency Optimization Plan

**Repository**: cogpy/yggdraphitecho  
**Analysis Date**: November 9, 2025  
**Phase**: Coherence Optimization - Dependency Management

---

## 📊 Current Dependency State

### Main Project Dependencies

**Primary Files**:
- `pyproject.toml` - Main project configuration
- `setup.py` - Setup script

### Echo Subsystem Dependencies

**Identified Dependency Files**:

| Subsystem | Files | Status |
|-----------|-------|--------|
| **echo/dash** | `requirements.txt`, `requirements-ci.txt`, `setup.cfg` | 🟡 Multiple files |
| **echo/dream** | `pyproject.toml` | 🟢 Modern format |
| **echo/self** | `pyproject.toml`, `requirements.txt`, `setup.py`, `netlify.toml`, `supabase/config.toml` | 🟡 Multiple files |

---

## 🎯 Optimization Strategy

### Approach: Monorepo-Style Dependency Management

Rather than consolidating all dependencies into a single file (which could break subsystem independence), we'll implement a **hybrid approach**:

1. **Main `pyproject.toml`**: Core dependencies and optional subsystem groups
2. **Subsystem configs**: Keep subsystem-specific configs for modularity
3. **Clear documentation**: Document dependency relationships

### Benefits

✅ **Modularity**: Subsystems remain independently installable  
✅ **Flexibility**: Install only needed subsystems  
✅ **Clarity**: Clear dependency boundaries  
✅ **Maintainability**: Easier to update and audit  

---

## 📋 Recommended Structure

### Main pyproject.toml Enhancement

```toml
[project]
name = "aphrodite-engine"
# ... existing config ...

[project.optional-dependencies]
# Echo subsystem groups
echo-dash = [
    # Dependencies from echo/dash/requirements.txt
]

echo-dream = [
    # Dependencies from echo/dream/pyproject.toml
]

echo-self = [
    # Dependencies from echo/self/
]

echo-kern = [
    # DTESN kernel dependencies
]

echo-rkwv = [
    # RWKV integration dependencies
]

# Convenience groups
echo-all = [
    "aphrodite-engine[echo-dash]",
    "aphrodite-engine[echo-dream]",
    "aphrodite-engine[echo-self]",
    "aphrodite-engine[echo-kern]",
    "aphrodite-engine[echo-rkwv]",
]

# Development dependencies
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio",
    "pytest-cov",
    "ruff",
    "mypy",
    # ... other dev tools
]

# Documentation dependencies
docs = [
    "sphinx",
    "sphinx-rtd-theme",
    "myst-parser",
]
```

### Installation Examples

```bash
# Install base aphrodite engine
pip install aphrodite-engine

# Install with specific echo subsystem
pip install aphrodite-engine[echo-dash]

# Install with multiple subsystems
pip install aphrodite-engine[echo-dash,echo-dream]

# Install everything
pip install aphrodite-engine[echo-all]

# Install for development
pip install aphrodite-engine[echo-all,dev,docs]
```

---

## 🔍 Dependency Audit Recommendations

### Phase 1: Inventory (Completed)
✅ Identified all dependency files across repository

### Phase 2: Analysis (Recommended)

Create a dependency analysis script to:

1. **Extract all dependencies** from each file
2. **Identify duplicates** across subsystems
3. **Check for version conflicts**
4. **Find unused dependencies**
5. **Generate consolidated report**

### Phase 3: Consolidation (Future)

1. **Document dependencies** in main `pyproject.toml` optional groups
2. **Update installation docs** with new installation patterns
3. **Create migration guide** for existing users
4. **Test installation** in clean environments

---

## 📝 Documentation Requirements

### Update Required Documentation

1. **README.md**: Add installation options section
2. **docs/guides/INSTALLATION.md**: Create comprehensive installation guide
3. **CONTRIBUTING.md**: Update development setup instructions
4. **echo/*/README.md**: Document subsystem-specific dependencies

### New Documentation to Create

1. **DEPENDENCIES.md**: Comprehensive dependency documentation
2. **docs/guides/DEPENDENCY_MANAGEMENT.md**: Dependency management guide

---

## 🚀 Implementation Plan

### Immediate Actions (Low Risk)

1. ✅ **Document current state** (this file)
2. ⏳ **Create dependency inventory script**
3. ⏳ **Generate dependency report**
4. ⏳ **Document installation patterns**

### Future Actions (Medium Risk)

1. ⏳ **Add optional-dependencies to pyproject.toml**
2. ⏳ **Test installation patterns**
3. ⏳ **Update documentation**
4. ⏳ **Create migration guide**

### Long-term Actions (Ongoing)

1. ⏳ **Regular dependency audits**
2. ⏳ **Automated dependency updates**
3. ⏳ **Security vulnerability scanning**
4. ⏳ **Dependency version pinning strategy**

---

## 🎯 Success Criteria

### Installation Simplicity
✅ Single command to install base system  
✅ Clear options for subsystem installation  
✅ Documented installation patterns  

### Dependency Clarity
✅ Clear dependency boundaries  
✅ No hidden dependencies  
✅ Version conflicts resolved  

### Maintainability
✅ Easy to add new dependencies  
✅ Easy to update existing dependencies  
✅ Automated dependency checks  

---

## 📊 Current Status

| Task | Status | Priority |
|------|--------|----------|
| Dependency inventory | ✅ Complete | HIGH |
| Dependency analysis script | ⏳ Recommended | MEDIUM |
| Consolidation in pyproject.toml | ⏳ Future | MEDIUM |
| Documentation updates | ⏳ Future | MEDIUM |
| Installation testing | ⏳ Future | HIGH |

---

## 💡 Key Insights

### Why Not Full Consolidation?

**Reasons to maintain subsystem configs**:

1. **Independence**: Subsystems may be used standalone
2. **Development**: Subsystem-specific development workflows
3. **Deployment**: Different deployment scenarios
4. **Flexibility**: Different version requirements

### Hybrid Approach Benefits

The hybrid approach provides:
- **Central documentation** in main `pyproject.toml`
- **Subsystem autonomy** with local configs
- **Installation flexibility** via optional groups
- **Clear boundaries** between components

---

## 🔗 Related Documentation

- [ORGANIZATION.md](ORGANIZATION.md) - Repository organization guidelines
- [COHERENCE_ANALYSIS.md](COHERENCE_ANALYSIS.md) - Coherence analysis
- [pyproject.toml](pyproject.toml) - Main project configuration

---

## 📅 Next Steps

1. **Review this plan** with maintainers
2. **Create dependency analysis script** (if approved)
3. **Generate dependency report**
4. **Implement optional-dependencies** (if approved)
5. **Update documentation**
6. **Test installation patterns**

---

**Status**: Analysis Complete - Recommendations Documented  
**Risk Level**: Low (documentation only at this stage)  
**Impact**: High (improved developer experience and maintainability)
