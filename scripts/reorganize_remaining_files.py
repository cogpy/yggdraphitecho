#!/usr/bin/env python3.11
"""
Second Pass: Reorganize Remaining Root Files
"""

import shutil
from pathlib import Path

def reorganize_remaining():
    """Reorganize remaining root-level files"""
    
    # Additional file mappings for files found in second pass
    file_mappings = {
        # More demo files
        'demo_error_monitoring.py': 'examples/monitoring/',
        'demo_hardware_abstraction.py': 'examples/backend/',
        'demo_integration.py': 'examples/backend/',
        'demo_meta_learning.py': 'examples/training/',
        'demo_monitoring_standalone.py': 'examples/monitoring/',
        'demo_multimodal_sensors.py': 'examples/embodiment/',
        'demo_optimization_showcase.py': 'examples/backend/',
        'demo_phase_3_3_3_self_monitoring.py': 'examples/monitoring/',
        'demo_phase_7_1_3_data_pipelines.py': 'examples/backend/',
        'demo_phase_8_2_3_production_data_pipeline.py': 'examples/backend/',
        'demo_production_alerting.py': 'integrations/alerting/',
        'demo_scalability_framework.py': 'examples/backend/',
        'demo_serialization_optimization.py': 'examples/backend/',
        'demo_server_monitoring.py': 'examples/monitoring/',
        'demo_server_side_continuous_learning.py': 'examples/training/',
        'demo_streaming_responses.py': 'examples/backend/',
        'demo_task_8_1_1_integration.py': 'integrations/',
        'demo_template_rendering.py': 'examples/backend/',
        'demo_virtual_body.py': 'examples/embodiment/',
        'demonstrate_async_implementation.py': 'examples/backend/',
        
        # Integration/middleware examples
        'example_dtesn_middleware_integration.py': 'examples/deep_tree_echo/',
        
        # Utility scripts
        'env.py': 'scripts/',
        'fix_script.py': 'scripts/',
        'forensic_analysis.py': 'scripts/analysis/',
        
        # Keep in root (core entry points):
        # - hypergraph_api.py
        # - hypergraph_service.py
        # - hypergraph_model_runner.py
        # - run_deep_tree_echo_server.py
        # - setup.py
        # - use_existing_torch.py
    }
    
    print("🔄 Moving remaining files...")
    moved = 0
    
    for source_file, dest_dir in file_mappings.items():
        source_path = Path(source_file)
        dest_path = Path(dest_dir) / source_file
        
        if source_path.exists():
            try:
                shutil.move(str(source_path), str(dest_path))
                print(f"  ✓ Moved: {source_file} → {dest_dir}")
                moved += 1
            except Exception as e:
                print(f"  ✗ Error moving {source_file}: {e}")
        else:
            print(f"  ⚠ Not found: {source_file}")
    
    print(f"\n✅ Moved {moved} additional files")
    
    # Show remaining root files
    remaining = list(Path('.').glob('*.py'))
    print(f"\n📊 Remaining root-level Python files: {len(remaining)}")
    
    # Categorize remaining files
    entry_points = ['hypergraph_api.py', 'hypergraph_service.py', 
                    'hypergraph_model_runner.py', 'run_deep_tree_echo_server.py']
    config_files = ['setup.py', 'use_existing_torch.py']
    
    print("\n📌 Core Entry Points (should remain in root):")
    for f in remaining:
        if f.name in entry_points:
            print(f"  ✓ {f.name}")
    
    print("\n⚙️  Configuration Files (should remain in root):")
    for f in remaining:
        if f.name in config_files:
            print(f"  ✓ {f.name}")
    
    print("\n📋 Other Files:")
    for f in remaining:
        if f.name not in entry_points and f.name not in config_files:
            print(f"  • {f.name}")

if __name__ == "__main__":
    reorganize_remaining()
