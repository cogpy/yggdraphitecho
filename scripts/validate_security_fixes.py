#!/usr/bin/env python3.11
"""
Validate Security Fixes
Ensures all security fixes are properly applied
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple

class SecurityFixValidator:
    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.passed = []
        self.failed = []
        self.warnings = []
        
    def check_dependency_versions(self) -> bool:
        """Verify dependencies are updated to secure versions"""
        print("🔍 Validating dependency versions...")
        
        required_versions = {
            'requests': ('2.32.0', '>='),
            'jinja2': ('3.1.6', '>='),
            'pillow': ('10.3.0', '>='),
            'aiohttp': ('3.10.11', '>='),
        }
        
        common_file = self.repo_root / 'requirements' / 'common.txt'
        
        if not common_file.exists():
            self.failed.append("requirements/common.txt not found")
            return False
        
        with open(common_file, 'r') as f:
            content = f.read()
        
        all_valid = True
        for package, (min_version, operator) in required_versions.items():
            pattern = rf'{package}\s*([><=]+)\s*([\d.]+)'
            match = re.search(pattern, content, re.IGNORECASE)
            
            if match:
                found_op, found_ver = match.groups()
                
                # Check if version meets minimum
                found_parts = [int(x) for x in found_ver.split('.')]
                min_parts = [int(x) for x in min_version.split('.')]
                
                version_ok = found_parts >= min_parts
                operator_ok = '>=' in found_op or '==' in found_op
                
                if version_ok and operator_ok:
                    self.passed.append(f"✓ {package} {found_op} {found_ver} (secure)")
                    print(f"  ✓ {package} {found_op} {found_ver}")
                else:
                    self.failed.append(f"✗ {package} {found_op} {found_ver} (needs >= {min_version})")
                    print(f"  ✗ {package} {found_op} {found_ver} - INSECURE")
                    all_valid = False
            else:
                self.failed.append(f"✗ {package} not found or no version specified")
                print(f"  ✗ {package} - NOT FOUND")
                all_valid = False
        
        return all_valid
    
    def check_security_policy(self) -> bool:
        """Verify SECURITY.md exists and is complete"""
        print("\n🔍 Validating security policy...")
        
        security_md = self.repo_root / 'SECURITY.md'
        
        if not security_md.exists():
            self.failed.append("SECURITY.md not found")
            print("  ✗ SECURITY.md not found")
            return False
        
        with open(security_md, 'r') as f:
            content = f.read()
        
        required_sections = [
            'Supported Versions',
            'Reporting a Vulnerability',
            'Security Best Practices',
        ]
        
        all_sections = True
        for section in required_sections:
            if section in content:
                self.passed.append(f"✓ SECURITY.md contains '{section}'")
                print(f"  ✓ Contains '{section}'")
            else:
                self.failed.append(f"✗ SECURITY.md missing '{section}'")
                print(f"  ✗ Missing '{section}'")
                all_sections = False
        
        return all_sections
    
    def check_gitignore(self) -> bool:
        """Verify .gitignore has security patterns"""
        print("\n🔍 Validating .gitignore...")
        
        gitignore = self.repo_root / '.gitignore'
        
        if not gitignore.exists():
            self.warnings.append(".gitignore not found")
            print("  ⚠ .gitignore not found")
            return False
        
        with open(gitignore, 'r') as f:
            content = f.read()
        
        security_patterns = [
            '.env',
            '*.key',
            '*secret*',
            '*password*',
        ]
        
        all_patterns = True
        for pattern in security_patterns:
            if pattern in content:
                self.passed.append(f"✓ .gitignore contains '{pattern}'")
                print(f"  ✓ Contains '{pattern}'")
            else:
                self.warnings.append(f"⚠ .gitignore missing '{pattern}'")
                print(f"  ⚠ Missing '{pattern}'")
                all_patterns = False
        
        return all_patterns
    
    def check_security_workflow(self) -> bool:
        """Verify security scanning workflow exists"""
        print("\n🔍 Validating security workflow...")
        
        workflow = self.repo_root / '.github' / 'workflows' / 'security-scan.yml'
        
        if not workflow.exists():
            self.failed.append("security-scan.yml not found")
            print("  ✗ security-scan.yml not found")
            return False
        
        with open(workflow, 'r') as f:
            content = f.read()
        
        required_jobs = [
            'dependency-scan',
            'code-scan',
            'secret-scan',
        ]
        
        all_jobs = True
        for job in required_jobs:
            if job in content:
                self.passed.append(f"✓ Workflow contains '{job}'")
                print(f"  ✓ Contains '{job}'")
            else:
                self.failed.append(f"✗ Workflow missing '{job}'")
                print(f"  ✗ Missing '{job}'")
                all_jobs = False
        
        return all_jobs
    
    def check_files_modified(self) -> bool:
        """Check that expected files were modified"""
        print("\n🔍 Validating file modifications...")
        
        expected_files = [
            'requirements/common.txt',
            'SECURITY.md',
            '.gitignore',
            '.github/workflows/security-scan.yml',
            'CRITICAL_SECURITY_ANALYSIS.md',
            'CRITICAL_ISSUES_REPORT.json',
        ]
        
        all_exist = True
        for file_path in expected_files:
            full_path = self.repo_root / file_path
            if full_path.exists():
                self.passed.append(f"✓ {file_path} exists")
                print(f"  ✓ {file_path}")
            else:
                self.failed.append(f"✗ {file_path} not found")
                print(f"  ✗ {file_path} - NOT FOUND")
                all_exist = False
        
        return all_exist
    
    def generate_report(self) -> Tuple[bool, str]:
        """Generate validation report"""
        success = len(self.failed) == 0
        
        report = []
        report.append("\n" + "="*80)
        report.append("SECURITY FIXES VALIDATION REPORT")
        report.append("="*80)
        
        if success:
            report.append("\n✅ ALL VALIDATIONS PASSED")
            report.append("\nAll critical security fixes have been successfully applied!")
        else:
            report.append("\n❌ VALIDATION FAILED")
            report.append(f"\nFound {len(self.failed)} critical issues:")
            for issue in self.failed:
                report.append(f"  {issue}")
        
        if self.warnings:
            report.append(f"\n⚠️  Found {len(self.warnings)} warnings:")
            for warning in self.warnings[:5]:
                report.append(f"  {warning}")
        
        report.append(f"\n✅ Passed Checks: {len(self.passed)}")
        report.append(f"❌ Failed Checks: {len(self.failed)}")
        report.append(f"⚠️  Warnings: {len(self.warnings)}")
        
        report.append("\n" + "="*80)
        
        return success, "\n".join(report)
    
    def run(self) -> bool:
        """Run all validation checks"""
        print("🔒 Validating Security Fixes...")
        print("="*80)
        
        checks = [
            self.check_dependency_versions(),
            self.check_security_policy(),
            self.check_gitignore(),
            self.check_security_workflow(),
            self.check_files_modified(),
        ]
        
        success, report = self.generate_report()
        print(report)
        
        return success

def main():
    validator = SecurityFixValidator()
    success = validator.run()
    
    if success:
        print("\n✅ All security fixes validated successfully!")
        print("\nReady to commit and push changes.")
        return 0
    else:
        print("\n⚠️  Validation completed with errors.")
        print("\nPlease review and fix issues before committing.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
