# 📁 Repository Organization Guidelines

**Repository**: cogpy/yggdraphitecho  
**Version**: 2.0  
**Last Updated**: November 9, 2025

This document defines the organizational standards and best practices for the yggdraphitecho repository.

---

## 🎯 Core Principles

1. **Clarity**: Every file and directory should have a clear, obvious purpose
2. **Consistency**: Follow established patterns and naming conventions
3. **Discoverability**: Organize content for easy navigation and search
4. **Maintainability**: Structure should support long-term maintenance
5. **Scalability**: Organization should accommodate future growth

---

## 📂 Directory Structure

### Root Level

```
yggdraphitecho/
├── README.md              # Project overview (keep in root)
├── CONTRIBUTING.md        # Contribution guidelines (keep in root)
├── CODE_OF_CONDUCT.md    # Community standards (keep in root)
├── ORGANIZATION.md        # This file (keep in root)
├── pyproject.toml        # Main project configuration
├── setup.py              # Setup script
├── docs/                 # All documentation
├── tests/                # All tests
├── scripts/              # Utility and validation scripts
├── echo/                 # Unified Echo subsystems
├── core/                 # Core components
├── aphrodite/            # Aphrodite engine
└── [other packages]/     # Additional packages
```

### Documentation Structure

```
docs/
├── INDEX.md              # Comprehensive navigation index
├── README.md             # Documentation overview
├── architecture/         # Architecture and design docs
├── guides/               # User guides and tutorials
├── api/                  # API reference documentation
├── reports/              # Test reports and fix summaries
├── summaries/            # Analysis and status summaries
└── subsystems/           # Subsystem-specific documentation
    ├── dash/
    ├── dream/
    ├── kern/
    └── [others]/
```

### Test Structure

```
tests/
├── README.md             # Test documentation
├── integration/          # Integration tests
├── unit/                 # Unit tests
├── performance/          # Performance and scalability tests
└── [component]/          # Component-specific tests
```

### Scripts Structure

```
scripts/
├── README.md             # Scripts documentation
├── validation/           # Validation scripts
└── utilities/            # Utility scripts
```

---

## 📝 Naming Conventions

### Python Packages and Modules

Follow **PEP 8** standards:

- **Packages/Modules**: lowercase with underscores
  - ✅ `echo_dash`, `deep_tree_echo`
  - ❌ `echo.dash`, `deep-tree-echo`

- **Classes**: CapWords (PascalCase)
  - ✅ `AgentManager`, `EchoPropagation`
  - ❌ `agent_manager`, `echo_propagation`

- **Functions/Variables**: lowercase with underscores
  - ✅ `process_data`, `user_input`
  - ❌ `processData`, `UserInput`

- **Constants**: uppercase with underscores
  - ✅ `MAX_ITERATIONS`, `DEFAULT_CONFIG`
  - ❌ `maxIterations`, `defaultConfig`

### Files and Directories

- Use lowercase with underscores
- Be descriptive but concise
- Avoid special characters except underscore and hyphen
- Use consistent prefixes for related files

**Examples**:
- ✅ `test_integration.py`, `validate_system.py`
- ❌ `TestIntegration.py`, `validate-system.py`

---

## 📚 Documentation Standards

### Markdown Files

1. **Location**: All documentation in `docs/` directory
2. **Naming**: UPPERCASE for major docs, lowercase for specific docs
3. **Format**: Use GitHub-flavored Markdown
4. **Structure**: Include clear headings and table of contents

### Documentation Types

| Type | Location | Example |
|------|----------|---------|
| Architecture | `docs/architecture/` | System design documents |
| User Guides | `docs/guides/` | How-to guides and tutorials |
| API Reference | `docs/api/` | API documentation |
| Reports | `docs/reports/` | Test and fix reports |
| Summaries | `docs/summaries/` | Status and analysis summaries |
| Subsystem Docs | `docs/subsystems/` | Subsystem-specific documentation |

### Documentation Requirements

- **Title**: Clear, descriptive title at the top
- **Date**: Include creation/update date
- **Purpose**: Brief description of document purpose
- **Navigation**: Links to related documents
- **Examples**: Include code examples where relevant
- **Cross-references**: Link to related documentation

---

## 🧪 Test Organization

### Test Categories

1. **Unit Tests** (`tests/unit/`): Test individual components
2. **Integration Tests** (`tests/integration/`): Test component interactions
3. **Performance Tests** (`tests/performance/`): Benchmark and scalability tests

### Test Naming

- Prefix with `test_`
- Descriptive of what is being tested
- Group related tests in subdirectories

**Examples**:
- `tests/unit/test_agent_manager.py`
- `tests/integration/test_aphrodite_integration.py`
- `tests/performance/test_scalability_framework.py`

---

## 🔧 Configuration Management

### Configuration Files

- **Main Config**: `pyproject.toml` (primary)
- **Environment Configs**: `configs/` directory
- **Subsystem Configs**: Within subsystem directories

### Configuration Organization

```
configs/
├── development/          # Development environment
├── production/           # Production environment
├── testing/              # Testing environment
└── subsystems/           # Subsystem-specific configs
```

---

## 📦 Dependency Management

### Primary Dependency File

Use `pyproject.toml` as the single source of truth for dependencies.

### Optional Dependencies

Define subsystem dependencies as optional:

```toml
[project.optional-dependencies]
dash = [...]
dream = [...]
kern = [...]
all = [...]              # All subsystems
dev = [...]              # Development tools
```

### Dependency Guidelines

1. Pin major versions, allow minor updates
2. Document why specific versions are required
3. Regularly audit and update dependencies
4. Avoid duplicate dependencies across subsystems

---

## 🚫 What NOT to Do

### ❌ Don't

- Place test files in root directory
- Use dot notation in directory names (`echo.dash`)
- Create duplicate directory structures
- Scatter documentation across multiple locations
- Use inconsistent naming conventions
- Create deep nesting (>4 levels) without good reason
- Leave orphaned or unused files
- Commit temporary or generated files

### ✅ Do

- Place all tests in `tests/` directory
- Use underscore notation (`echo_dash`)
- Consolidate related components
- Centralize documentation in `docs/`
- Follow PEP 8 naming conventions
- Keep directory structure flat and logical
- Regularly clean up unused files
- Use `.gitignore` for generated files

---

## 🔄 Maintenance Guidelines

### Regular Reviews

- **Weekly**: Check for misplaced files
- **Monthly**: Review and update documentation
- **Quarterly**: Audit dependencies and cleanup

### Pre-commit Checklist

- [ ] Files in correct directories
- [ ] Naming conventions followed
- [ ] Documentation updated
- [ ] Tests passing
- [ ] No temporary files committed

### Refactoring Guidelines

When refactoring:
1. Plan changes before implementing
2. Update documentation simultaneously
3. Maintain backward compatibility when possible
4. Update import paths systematically
5. Test thoroughly after changes
6. Commit in logical, reviewable batches

---

## 📈 Evolution and Updates

This document will evolve with the repository. When making organizational changes:

1. Update this document first
2. Implement changes incrementally
3. Document rationale for changes
4. Communicate changes to team
5. Update related documentation

---

## 🆘 Questions?

If you're unsure about where something should go:

1. Check this document
2. Look for similar existing files
3. Ask in repository discussions
4. When in doubt, follow PEP 8 and Python best practices

---

**Last Major Update**: November 9, 2025 - Repository reorganization and coherence optimization
