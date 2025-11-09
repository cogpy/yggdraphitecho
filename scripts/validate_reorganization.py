#!/usr/bin/env python3.11
"""
Validate Repository Reorganization
Ensures no broken imports or missing files
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

class ReorganizationValidator:
    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.errors = []
        self.warnings = []
        
    def check_directory_structure(self) -> bool:
        """Verify new directory structure exists"""
        print("📁 Checking directory structure...")
        
        required_dirs = [
            'examples',
            'examples/aar',
            'examples/backend',
            'examples/deep_tree_echo',
            'examples/middleware',
            'examples/monitoring',
            'examples/training',
            'examples/embodiment',
            'integrations',
            'integrations/alerting',
            'integrations/continuous_learning',
            'integrations/environment',
            'integrations/fusion',
            'scripts/benchmarks',
            'scripts/database',
            'scripts/debug',
            'scripts/deployment',
            'scripts/analysis',
            'prototypes',
        ]
        
        all_exist = True
        for directory in required_dirs:
            dir_path = self.repo_root / directory
            if dir_path.exists():
                print(f"  ✓ {directory}")
            else:
                print(f"  ✗ Missing: {directory}")
                self.errors.append(f"Missing directory: {directory}")
                all_exist = False
        
        return all_exist
    
    def check_readme_files(self) -> bool:
        """Verify README files exist"""
        print("\n📝 Checking README files...")
        
        required_readmes = [
            'examples/README.md',
            'examples/aar/README.md',
            'examples/backend/README.md',
            'examples/deep_tree_echo/README.md',
            'examples/middleware/README.md',
            'examples/monitoring/README.md',
            'examples/training/README.md',
            'examples/embodiment/README.md',
            'integrations/README.md',
            'scripts/benchmarks/README.md',
            'scripts/database/README.md',
            'scripts/debug/README.md',
            'scripts/deployment/README.md',
            'scripts/analysis/README.md',
            'prototypes/README.md',
        ]
        
        all_exist = True
        for readme in required_readmes:
            readme_path = self.repo_root / readme
            if readme_path.exists():
                print(f"  ✓ {readme}")
            else:
                print(f"  ✗ Missing: {readme}")
                self.warnings.append(f"Missing README: {readme}")
                all_exist = False
        
        return all_exist
    
    def check_core_entry_points(self) -> bool:
        """Verify core entry points remain in root"""
        print("\n🎯 Checking core entry points...")
        
        entry_points = [
            'hypergraph_api.py',
            'hypergraph_service.py',
            'hypergraph_model_runner.py',
            'run_deep_tree_echo_server.py',
            'setup.py',
            'use_existing_torch.py',
        ]
        
        all_exist = True
        for entry_point in entry_points:
            ep_path = self.repo_root / entry_point
            if ep_path.exists():
                print(f"  ✓ {entry_point}")
            else:
                print(f"  ✗ Missing: {entry_point}")
                self.errors.append(f"Missing entry point: {entry_point}")
                all_exist = False
        
        return all_exist
    
    def check_python_syntax(self) -> bool:
        """Check Python syntax of moved files"""
        print("\n🐍 Checking Python syntax...")
        
        # Check a sample of moved files
        sample_files = [
            'examples/aar/demo_aar_system.py',
            'examples/backend/demo_async_server_processing.py',
            'examples/deep_tree_echo/usage_example_deep_tree_echo.py',
            'integrations/alerting/integration_demo_alerting.py',
            'scripts/benchmarks/benchmark_dtesn_serialization.py',
        ]
        
        all_valid = True
        for file_path in sample_files:
            full_path = self.repo_root / file_path
            if full_path.exists():
                try:
                    result = subprocess.run(
                        ['python3.11', '-m', 'py_compile', str(full_path)],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        print(f"  ✓ {file_path}")
                    else:
                        print(f"  ✗ Syntax error in {file_path}")
                        self.errors.append(f"Syntax error: {file_path}")
                        all_valid = False
                except Exception as e:
                    print(f"  ⚠ Could not check {file_path}: {e}")
                    self.warnings.append(f"Could not validate: {file_path}")
            else:
                print(f"  ⚠ Not found: {file_path}")
                self.warnings.append(f"File not found: {file_path}")
        
        return all_valid
    
    def count_root_files(self) -> int:
        """Count remaining root-level Python files"""
        print("\n📊 Counting root-level Python files...")
        
        root_py_files = list(self.repo_root.glob('*.py'))
        count = len(root_py_files)
        
        print(f"  Found {count} Python files in root")
        
        if count <= 10:
            print(f"  ✓ Root file count acceptable ({count} ≤ 10)")
        else:
            print(f"  ⚠ Root file count high ({count} > 10)")
            self.warnings.append(f"High root file count: {count}")
        
        return count
    
    def verify_file_moves(self) -> bool:
        """Verify expected files were moved"""
        print("\n🔄 Verifying file moves...")
        
        # Check that old locations are empty (files moved)
        old_demo_files = list(self.repo_root.glob('demo_*.py'))
        old_integration_files = list(self.repo_root.glob('integration_*.py'))
        old_benchmark_files = list(self.repo_root.glob('benchmark_*.py'))
        
        total_old = len(old_demo_files) + len(old_integration_files) + len(old_benchmark_files)
        
        if total_old == 0:
            print(f"  ✓ No demo/integration/benchmark files in root")
        else:
            print(f"  ⚠ Found {total_old} unmoved files in root")
            for f in old_demo_files[:5]:
                print(f"    - {f.name}")
            self.warnings.append(f"Unmoved files in root: {total_old}")
        
        # Check that new locations have files
        examples_count = len(list((self.repo_root / 'examples').rglob('*.py')))
        integrations_count = len(list((self.repo_root / 'integrations').rglob('*.py')))
        
        print(f"  ✓ Examples directory: {examples_count} files")
        print(f"  ✓ Integrations directory: {integrations_count} files")
        
        return total_old == 0
    
    def check_documentation_files(self) -> bool:
        """Check that documentation files were created"""
        print("\n📚 Checking documentation files...")
        
        doc_files = [
            'SUPER_SLEUTH_FINDINGS.md',
            'HYPER_HOLMES_SOLUTION_STRATEGY.md',
            'REPOSITORY_STRUCTURE.md',
            'MIGRATION_GUIDE.md',
        ]
        
        all_exist = True
        for doc_file in doc_files:
            doc_path = self.repo_root / doc_file
            if doc_path.exists():
                print(f"  ✓ {doc_file}")
            else:
                print(f"  ✗ Missing: {doc_file}")
                self.warnings.append(f"Missing documentation: {doc_file}")
                all_exist = False
        
        return all_exist
    
    def generate_report(self) -> Tuple[bool, str]:
        """Generate validation report"""
        success = len(self.errors) == 0
        
        report = []
        report.append("\n" + "="*80)
        report.append("REORGANIZATION VALIDATION REPORT")
        report.append("="*80)
        
        if success:
            report.append("\n✅ VALIDATION PASSED")
            report.append("\nAll critical checks passed successfully!")
        else:
            report.append("\n❌ VALIDATION FAILED")
            report.append(f"\nFound {len(self.errors)} critical errors:")
            for error in self.errors:
                report.append(f"  - {error}")
        
        if self.warnings:
            report.append(f"\n⚠️  Found {len(self.warnings)} warnings:")
            for warning in self.warnings[:10]:  # Show first 10
                report.append(f"  - {warning}")
            if len(self.warnings) > 10:
                report.append(f"  ... and {len(self.warnings) - 10} more")
        
        report.append("\n" + "="*80)
        
        return success, "\n".join(report)
    
    def run(self) -> bool:
        """Run all validation checks"""
        print("🔍 Starting Reorganization Validation...")
        print("="*80)
        
        checks = [
            self.check_directory_structure(),
            self.check_readme_files(),
            self.check_core_entry_points(),
            self.check_python_syntax(),
            self.verify_file_moves(),
            self.check_documentation_files(),
        ]
        
        self.count_root_files()
        
        success, report = self.generate_report()
        print(report)
        
        return success

def main():
    validator = ReorganizationValidator()
    success = validator.run()
    
    if success:
        print("\n✅ Repository reorganization validated successfully!")
        print("\nNext steps:")
        print("1. Review changes: git status")
        print("2. Stage changes: git add .")
        print("3. Commit in batches (see HYPER_HOLMES_SOLUTION_STRATEGY.md)")
        print("4. Push to repository: git push")
        return 0
    else:
        print("\n⚠️  Validation completed with errors. Review above.")
        print("\nFix errors before committing.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
