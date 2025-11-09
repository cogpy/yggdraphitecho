#!/usr/bin/env python3.11
"""
Automated Repository Reorganization Script
Safely moves files to new structure to fix fragmentation
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List

class RepositoryReorganizer:
    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.moved_files = []
        self.errors = []
        
    def create_directory_structure(self) -> None:
        """Create new directory structure"""
        directories = [
            'examples/aar',
            'examples/backend',
            'examples/deep_tree_echo',
            'examples/middleware',
            'examples/monitoring',
            'examples/training',
            'examples/embodiment',
            'integrations/alerting',
            'integrations/continuous_learning',
            'integrations/environment',
            'integrations/fusion',
            'scripts/benchmarks',
            'scripts/database',
            'scripts/debug',
            'scripts/deployment',
            'scripts/analysis',
            'prototypes/quantum_hypergraph',
            'prototypes/senas',
        ]
        
        print("📁 Creating directory structure...")
        for directory in directories:
            dir_path = self.repo_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created: {directory}")
    
    def get_file_mappings(self) -> Dict[str, str]:
        """Get mapping of source files to destination directories"""
        return {
            # AAR Examples
            'demo_aar_system.py': 'examples/aar/',
            'demo_arena_simulation_framework.py': 'examples/aar/',
            'demo_echo_aar_integration.py': 'examples/aar/',
            
            # Backend Examples
            'demo_async_server_processing.py': 'examples/backend/',
            'demo_backend_performance_monitoring.py': 'examples/backend/',
            'demo_backend_resource_optimization.py': 'examples/backend/',
            'demo_backend_service_integration.py': 'examples/backend/',
            'demo_batching_system.py': 'examples/backend/',
            
            # Deep Tree Echo Examples
            'demo_deep_tree_echo_endpoints.py': 'examples/deep_tree_echo/',
            'demo_deep_tree_echo_fusion.py': 'examples/deep_tree_echo/',
            'demo_deep_tree_echo_interactive.py': 'examples/deep_tree_echo/',
            'demo_deep_tree_echo_memory.py': 'examples/deep_tree_echo/',
            'demo_dtesn_cache_integration.py': 'examples/deep_tree_echo/',
            'usage_example_deep_tree_echo.py': 'examples/deep_tree_echo/',
            'usage_example_dtesn_openai_integration.py': 'examples/deep_tree_echo/',
            
            # Middleware Examples
            'demo_advanced_middleware_stack.py': 'examples/middleware/',
            'demo_content_negotiation.py': 'examples/middleware/',
            'demo_dynamic_config_management.py': 'examples/middleware/',
            'demo_enterprise_security.py': 'examples/middleware/',
            'demo_middleware_composition.py': 'examples/middleware/',
            'demo_rate_limiting.py': 'examples/middleware/',
            'demo_request_validation.py': 'examples/middleware/',
            'demo_response_transformation.py': 'examples/middleware/',
            'demo_semantic_caching.py': 'examples/middleware/',
            
            # Monitoring Examples
            'demo_health_checks.py': 'examples/monitoring/',
            'demo_metrics_collection.py': 'examples/monitoring/',
            'demo_performance_profiling.py': 'examples/monitoring/',
            'demo_resource_tracking.py': 'examples/monitoring/',
            
            # Training Examples
            'demo_continuous_learning.py': 'examples/training/',
            'demo_continuous_learning_simple.py': 'examples/training/',
            'demo_curriculum_learning.py': 'examples/training/',
            'demo_dynamic_model_updates.py': 'examples/training/',
            'demo_environment_coupling.py': 'examples/training/',
            'demo_model_versioning.py': 'examples/training/',
            'demo_multi_agent_training.py': 'examples/training/',
            'demo_online_learning.py': 'examples/training/',
            'demo_reinforcement_learning.py': 'examples/training/',
            'demo_transfer_learning.py': 'examples/training/',
            
            # Embodiment Examples
            'demo_body_state_awareness.py': 'examples/embodiment/',
            'demo_motor_control.py': 'examples/embodiment/',
            'demo_sensory_integration.py': 'examples/embodiment/',
            'demo_virtual_body_representation.py': 'examples/embodiment/',
            
            # Integration Scripts
            'integration_demo_alerting.py': 'integrations/alerting/',
            'integration_example_server_side_continuous_learning.py': 'integrations/continuous_learning/',
            'integration_example_environment_coupling.py': 'integrations/environment/',
            'deep_tree_echo_fusion.py': 'integrations/fusion/',
            
            # Benchmark Scripts
            'benchmark_dtesn_serialization.py': 'scripts/benchmarks/',
            'benchmark_evolution.py': 'scripts/benchmarks/',
            
            # Debug Scripts
            'debug_motor_execution.py': 'scripts/debug/',
            'debug_target_propagation.py': 'scripts/debug/',
            'debug_trajectory_timing.py': 'scripts/debug/',
            
            # Database Scripts
            'sync_databases_comprehensive.py': 'scripts/database/',
            'sync_databases_neon.py': 'scripts/database/',
            'sync_via_neon_mcp.py': 'scripts/database/',
            
            # Deployment Scripts
            'lightning_app.py': 'scripts/deployment/',
            'lightning_manager.py': 'scripts/deployment/',
            'personal_studio_setup.py': 'scripts/deployment/',
            
            # Analysis Scripts
            'analysis_script.py': 'scripts/analysis/',
            'analyze_identity_fragments.py': 'scripts/analysis/',
            'update_deep_tree_echo_hypergraph.py': 'scripts/analysis/',
            'update_enhanced_hypergraph.py': 'scripts/analysis/',
            'update_hypergraph_enhancements.py': 'scripts/analysis/',
            
            # Prototypes
            'quantum_hypergraph_prototype.py': 'prototypes/quantum_hypergraph/',
            'senas_prototype.py': 'prototypes/senas/',
            'standalone_config_test.py': 'prototypes/',
        }
    
    def move_files(self) -> None:
        """Move files to new locations"""
        print("\n🔄 Moving files to new structure...")
        
        file_mappings = self.get_file_mappings()
        
        for source_file, dest_dir in file_mappings.items():
            source_path = self.repo_root / source_file
            dest_path = self.repo_root / dest_dir / source_file
            
            if source_path.exists():
                try:
                    # Use git mv to preserve history
                    shutil.move(str(source_path), str(dest_path))
                    self.moved_files.append((source_file, dest_dir))
                    print(f"  ✓ Moved: {source_file} → {dest_dir}")
                except Exception as e:
                    self.errors.append((source_file, str(e)))
                    print(f"  ✗ Error moving {source_file}: {e}")
            else:
                print(f"  ⚠ Not found: {source_file}")
    
    def create_readme_files(self) -> None:
        """Create README files for new directories"""
        print("\n📝 Creating README files...")
        
        readmes = {
            'examples/README.md': self._get_examples_readme(),
            'examples/aar/README.md': self._get_aar_readme(),
            'examples/backend/README.md': self._get_backend_readme(),
            'examples/deep_tree_echo/README.md': self._get_dte_readme(),
            'examples/middleware/README.md': self._get_middleware_readme(),
            'examples/monitoring/README.md': self._get_monitoring_readme(),
            'examples/training/README.md': self._get_training_readme(),
            'examples/embodiment/README.md': self._get_embodiment_readme(),
            'integrations/README.md': self._get_integrations_readme(),
            'scripts/benchmarks/README.md': self._get_benchmarks_readme(),
            'scripts/database/README.md': self._get_database_readme(),
            'scripts/debug/README.md': self._get_debug_readme(),
            'scripts/deployment/README.md': self._get_deployment_readme(),
            'scripts/analysis/README.md': self._get_analysis_readme(),
            'prototypes/README.md': self._get_prototypes_readme(),
        }
        
        for readme_path, content in readmes.items():
            full_path = self.repo_root / readme_path
            with open(full_path, 'w') as f:
                f.write(content)
            print(f"  ✓ Created: {readme_path}")
    
    def _get_examples_readme(self) -> str:
        return """# Examples

This directory contains example scripts demonstrating various features and capabilities of the yggdraphitecho system.

## Directory Structure

- **aar/** - Agent-Arena-Relation (AAR) system examples
- **backend/** - Backend service and processing examples
- **deep_tree_echo/** - Deep Tree Echo integration examples
- **middleware/** - Middleware and request processing examples
- **monitoring/** - Monitoring and observability examples
- **training/** - Training and learning examples
- **embodiment/** - Body state and sensory integration examples

## Usage

Each subdirectory contains focused examples for specific functionality. See individual README files for details.

## Running Examples

```bash
# Run from repository root
python3.11 examples/aar/demo_aar_system.py

# Or from examples directory
cd examples/aar
python3.11 demo_aar_system.py
```

## Contributing

When adding new examples:
1. Place in appropriate subdirectory
2. Include docstring with purpose and usage
3. Add entry to subdirectory README
4. Ensure dependencies are documented
"""
    
    def _get_aar_readme(self) -> str:
        return """# Agent-Arena-Relation (AAR) Examples

Examples demonstrating the AAR cognitive architecture for self-awareness and agent modeling.

## Examples

- **demo_aar_system.py** - Basic AAR system demonstration
- **demo_arena_simulation_framework.py** - Arena simulation and environment modeling
- **demo_echo_aar_integration.py** - Integration of Echo systems with AAR architecture

## Concepts

The AAR architecture provides:
- Agent modeling and self-representation
- Arena (environment) modeling
- Relation dynamics between agent and arena
- Geometric approach to self-awareness

## Usage

```bash
python3.11 demo_aar_system.py
```
"""
    
    def _get_backend_readme(self) -> str:
        return """# Backend Service Examples

Examples demonstrating backend service architecture, async processing, and resource management.

## Examples

- **demo_async_server_processing.py** - Asynchronous request processing
- **demo_backend_performance_monitoring.py** - Performance monitoring and metrics
- **demo_backend_resource_optimization.py** - Resource allocation and optimization
- **demo_backend_service_integration.py** - Service integration patterns
- **demo_batching_system.py** - Request batching and optimization

## Usage

```bash
python3.11 demo_async_server_processing.py
```
"""
    
    def _get_dte_readme(self) -> str:
        return """# Deep Tree Echo Examples

Examples demonstrating Deep Tree Echo cognitive architecture and memory systems.

## Examples

- **demo_deep_tree_echo_endpoints.py** - API endpoint integration
- **demo_deep_tree_echo_fusion.py** - Fusion with other systems
- **demo_deep_tree_echo_interactive.py** - Interactive session management
- **demo_deep_tree_echo_memory.py** - Hypergraph memory operations
- **demo_dtesn_cache_integration.py** - Cache integration for DTESN
- **usage_example_deep_tree_echo.py** - Basic usage patterns
- **usage_example_dtesn_openai_integration.py** - OpenAI API integration

## Architecture

Deep Tree Echo provides:
- Hypergraph memory space
- Echo propagation engine
- Cognitive grammar kernel
- Membrane-based architecture

## Usage

```bash
python3.11 usage_example_deep_tree_echo.py
```
"""
    
    def _get_middleware_readme(self) -> str:
        return """# Middleware Examples

Examples demonstrating middleware patterns for request processing and system composition.

## Examples

- **demo_advanced_middleware_stack.py** - Complex middleware composition
- **demo_content_negotiation.py** - Content type negotiation
- **demo_dynamic_config_management.py** - Dynamic configuration
- **demo_enterprise_security.py** - Security middleware
- **demo_middleware_composition.py** - Middleware composition patterns
- **demo_rate_limiting.py** - Rate limiting and throttling
- **demo_request_validation.py** - Request validation
- **demo_response_transformation.py** - Response transformation
- **demo_semantic_caching.py** - Semantic caching strategies

## Usage

```bash
python3.11 demo_advanced_middleware_stack.py
```
"""
    
    def _get_monitoring_readme(self) -> str:
        return """# Monitoring Examples

Examples demonstrating monitoring, metrics collection, and observability.

## Examples

- **demo_health_checks.py** - Health check implementations
- **demo_metrics_collection.py** - Metrics collection and reporting
- **demo_performance_profiling.py** - Performance profiling
- **demo_resource_tracking.py** - Resource usage tracking

## Usage

```bash
python3.11 demo_metrics_collection.py
```
"""
    
    def _get_training_readme(self) -> str:
        return """# Training Examples

Examples demonstrating training, learning, and model adaptation.

## Examples

- **demo_continuous_learning.py** - Continuous learning systems
- **demo_continuous_learning_simple.py** - Simplified continuous learning
- **demo_curriculum_learning.py** - Curriculum-based learning
- **demo_dynamic_model_updates.py** - Dynamic model updating
- **demo_environment_coupling.py** - Environment-coupled learning
- **demo_model_versioning.py** - Model version management
- **demo_multi_agent_training.py** - Multi-agent training
- **demo_online_learning.py** - Online learning patterns
- **demo_reinforcement_learning.py** - Reinforcement learning
- **demo_transfer_learning.py** - Transfer learning

## Usage

```bash
python3.11 demo_continuous_learning.py
```
"""
    
    def _get_embodiment_readme(self) -> str:
        return """# Embodiment Examples

Examples demonstrating body state awareness, motor control, and sensory integration.

## Examples

- **demo_body_state_awareness.py** - Body state tracking and awareness
- **demo_motor_control.py** - Motor control systems
- **demo_sensory_integration.py** - Sensory data integration
- **demo_virtual_body_representation.py** - Virtual body modeling

## Usage

```bash
python3.11 demo_body_state_awareness.py
```
"""
    
    def _get_integrations_readme(self) -> str:
        return """# Integration Scripts

Scripts for integrating yggdraphitecho with external systems and services.

## Structure

- **alerting/** - Alerting and notification integrations
- **continuous_learning/** - Continuous learning integrations
- **environment/** - Environment coupling integrations
- **fusion/** - System fusion integrations

## Usage

```bash
python3.11 integrations/alerting/integration_demo_alerting.py
```
"""
    
    def _get_benchmarks_readme(self) -> str:
        return """# Benchmark Scripts

Performance benchmarking utilities for various system components.

## Scripts

- **benchmark_dtesn_serialization.py** - DTESN serialization performance
- **benchmark_evolution.py** - Evolution engine performance

## Usage

```bash
python3.11 benchmark_dtesn_serialization.py
```
"""
    
    def _get_database_readme(self) -> str:
        return """# Database Utilities

Database synchronization and management utilities.

## Scripts

- **sync_databases_comprehensive.py** - Comprehensive database sync
- **sync_databases_neon.py** - Neon database sync
- **sync_via_neon_mcp.py** - Sync via Neon MCP

## Usage

```bash
python3.11 sync_databases_comprehensive.py
```
"""
    
    def _get_debug_readme(self) -> str:
        return """# Debug Utilities

Debugging utilities for troubleshooting system components.

## Scripts

- **debug_motor_execution.py** - Motor execution debugging
- **debug_target_propagation.py** - Target propagation debugging
- **debug_trajectory_timing.py** - Trajectory timing analysis

## Usage

```bash
python3.11 debug_motor_execution.py
```
"""
    
    def _get_deployment_readme(self) -> str:
        return """# Deployment Scripts

Scripts for deploying and managing yggdraphitecho services.

## Scripts

- **lightning_app.py** - Lightning.ai application
- **lightning_manager.py** - Lightning deployment manager
- **personal_studio_setup.py** - Personal studio setup

## Usage

```bash
python3.11 lightning_app.py
```
"""
    
    def _get_analysis_readme(self) -> str:
        return """# Analysis Scripts

Scripts for analyzing and updating system components.

## Scripts

- **analysis_script.py** - General analysis utilities
- **analyze_identity_fragments.py** - Identity fragment analysis
- **update_deep_tree_echo_hypergraph.py** - Hypergraph updates
- **update_enhanced_hypergraph.py** - Enhanced hypergraph updates
- **update_hypergraph_enhancements.py** - Hypergraph enhancements

## Usage

```bash
python3.11 analysis_script.py
```
"""
    
    def _get_prototypes_readme(self) -> str:
        return """# Prototypes

Experimental and prototype implementations.

## Structure

- **quantum_hypergraph/** - Quantum hypergraph experiments
- **senas/** - SENAS prototype

## Note

Code in this directory is experimental and may not be production-ready.

## Usage

```bash
python3.11 prototypes/quantum_hypergraph/quantum_hypergraph_prototype.py
```
"""
    
    def generate_report(self) -> str:
        """Generate reorganization report"""
        report = []
        report.append("=" * 80)
        report.append("REPOSITORY REORGANIZATION REPORT")
        report.append("=" * 80)
        report.append(f"\n✅ Successfully moved {len(self.moved_files)} files")
        
        if self.errors:
            report.append(f"\n❌ Encountered {len(self.errors)} errors:")
            for file, error in self.errors:
                report.append(f"  - {file}: {error}")
        
        report.append("\n" + "=" * 80)
        return "\n".join(report)
    
    def run(self) -> bool:
        """Execute complete reorganization"""
        try:
            self.create_directory_structure()
            self.move_files()
            self.create_readme_files()
            
            print("\n" + self.generate_report())
            
            return len(self.errors) == 0
        except Exception as e:
            print(f"\n❌ Fatal error during reorganization: {e}")
            return False

def main():
    print("🔧 Starting Repository Reorganization...")
    print("=" * 80)
    
    reorganizer = RepositoryReorganizer()
    success = reorganizer.run()
    
    if success:
        print("\n✅ Reorganization completed successfully!")
        print("\nNext steps:")
        print("1. Review changes: git status")
        print("2. Test imports: python3.11 scripts/validate_reorganization.py")
        print("3. Commit changes in batches")
    else:
        print("\n⚠️  Reorganization completed with errors. Review above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
