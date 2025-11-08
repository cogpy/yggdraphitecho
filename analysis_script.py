#!/usr/bin/env python3.11
"""
Comprehensive Repository Analysis Script
Identifies code quality issues, syntax errors, and improvement opportunities
"""

import os
import re
import json
import ast
from pathlib import Path
from collections import defaultdict
import subprocess

class RepositoryAnalyzer:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.issues = defaultdict(list)
        self.stats = defaultdict(int)
        
    def analyze_syntax_errors(self):
        """Find Python syntax errors"""
        print("🔍 Analyzing syntax errors...")
        python_files = list(self.repo_path.rglob("*.py"))
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    ast.parse(content)
            except SyntaxError as e:
                self.issues['syntax_errors'].append({
                    'file': str(py_file.relative_to(self.repo_path)),
                    'line': e.lineno,
                    'error': str(e.msg),
                    'text': e.text.strip() if e.text else ''
                })
                self.stats['syntax_errors'] += 1
            except Exception as e:
                self.issues['parse_errors'].append({
                    'file': str(py_file.relative_to(self.repo_path)),
                    'error': str(e)
                })
                
    def analyze_code_quality(self):
        """Analyze code quality issues"""
        print("🔍 Analyzing code quality...")
        python_files = list(self.repo_path.rglob("*.py"))
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    # Check for long lines
                    for i, line in enumerate(lines, 1):
                        if len(line) > 120:
                            self.stats['long_lines'] += 1
                            
                    # Check for TODO/FIXME comments
                    for i, line in enumerate(lines, 1):
                        if re.search(r'#\s*(TODO|FIXME|XXX|HACK)', line, re.IGNORECASE):
                            self.issues['todos'].append({
                                'file': str(py_file.relative_to(self.repo_path)),
                                'line': i,
                                'text': line.strip()
                            })
                            self.stats['todos'] += 1
                            
                    # Check for print statements (should use logging)
                    for i, line in enumerate(lines, 1):
                        if re.search(r'\bprint\s*\(', line) and not py_file.name.startswith('test_'):
                            self.stats['print_statements'] += 1
                            
            except Exception as e:
                pass
                
    def analyze_documentation(self):
        """Analyze documentation completeness"""
        print("🔍 Analyzing documentation...")
        python_files = list(self.repo_path.rglob("*.py"))
        
        for py_file in python_files:
            if py_file.name.startswith('test_'):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    tree = ast.parse(content)
                    
                    # Check for module docstring
                    if not ast.get_docstring(tree):
                        self.issues['missing_module_docstrings'].append(
                            str(py_file.relative_to(self.repo_path))
                        )
                        self.stats['missing_module_docstrings'] += 1
                        
                    # Check for function/class docstrings
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                            if not ast.get_docstring(node):
                                self.stats['missing_docstrings'] += 1
                                
            except Exception as e:
                pass
                
    def analyze_imports(self):
        """Analyze import statements"""
        print("🔍 Analyzing imports...")
        python_files = list(self.repo_path.rglob("*.py"))
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    # Check for wildcard imports
                    for i, line in enumerate(lines, 1):
                        if re.search(r'from\s+\S+\s+import\s+\*', line):
                            self.issues['wildcard_imports'].append({
                                'file': str(py_file.relative_to(self.repo_path)),
                                'line': i,
                                'text': line.strip()
                            })
                            self.stats['wildcard_imports'] += 1
                            
            except Exception as e:
                pass
                
    def analyze_file_structure(self):
        """Analyze file and directory structure"""
        print("🔍 Analyzing file structure...")
        
        # Check for __init__.py files
        for dirpath in self.repo_path.rglob("*"):
            if dirpath.is_dir() and not any(part.startswith('.') for part in dirpath.parts):
                py_files = list(dirpath.glob("*.py"))
                if py_files and not (dirpath / "__init__.py").exists():
                    if dirpath.name not in ['tests', 'scripts', 'tools', 'examples']:
                        self.issues['missing_init_files'].append(
                            str(dirpath.relative_to(self.repo_path))
                        )
                        self.stats['missing_init_files'] += 1
                        
    def analyze_requirements(self):
        """Analyze requirements and dependencies"""
        print("🔍 Analyzing requirements...")
        
        req_files = list(self.repo_path.rglob("requirements*.txt"))
        setup_py = self.repo_path / "setup.py"
        pyproject_toml = self.repo_path / "pyproject.toml"
        
        self.stats['requirement_files'] = len(req_files)
        self.stats['has_setup_py'] = setup_py.exists()
        self.stats['has_pyproject_toml'] = pyproject_toml.exists()
        
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "="*80)
        print("📊 REPOSITORY ANALYSIS REPORT")
        print("="*80)
        
        print("\n🔢 STATISTICS:")
        print("-" * 80)
        for key, value in sorted(self.stats.items()):
            print(f"  {key}: {value}")
            
        print("\n🚨 CRITICAL ISSUES:")
        print("-" * 80)
        
        if self.issues['syntax_errors']:
            print(f"\n❌ Syntax Errors ({len(self.issues['syntax_errors'])}):")
            for issue in self.issues['syntax_errors'][:10]:
                print(f"  📄 {issue['file']}:{issue['line']}")
                print(f"     Error: {issue['error']}")
                print(f"     Code: {issue['text']}")
                
        if self.issues['wildcard_imports']:
            print(f"\n⚠️  Wildcard Imports ({len(self.issues['wildcard_imports'])}):")
            for issue in self.issues['wildcard_imports'][:5]:
                print(f"  📄 {issue['file']}:{issue['line']}")
                print(f"     {issue['text']}")
                
        if self.issues['missing_init_files']:
            print(f"\n📦 Missing __init__.py ({len(self.issues['missing_init_files'])}):")
            for issue in self.issues['missing_init_files'][:10]:
                print(f"  📁 {issue}")
                
        if self.issues['todos']:
            print(f"\n📝 TODO/FIXME Comments ({len(self.issues['todos'])}):")
            for issue in self.issues['todos'][:10]:
                print(f"  📄 {issue['file']}:{issue['line']}")
                print(f"     {issue['text']}")
                
        # Save detailed report to JSON
        report_path = self.repo_path / "analysis_report.json"
        with open(report_path, 'w') as f:
            json.dump({
                'stats': dict(self.stats),
                'issues': dict(self.issues)
            }, f, indent=2)
            
        print(f"\n💾 Detailed report saved to: {report_path}")
        print("="*80)
        
    def run_full_analysis(self):
        """Run all analysis steps"""
        print("🚀 Starting comprehensive repository analysis...")
        print(f"📁 Repository: {self.repo_path}")
        print()
        
        self.analyze_syntax_errors()
        self.analyze_code_quality()
        self.analyze_documentation()
        self.analyze_imports()
        self.analyze_file_structure()
        self.analyze_requirements()
        self.generate_report()

if __name__ == "__main__":
    analyzer = RepositoryAnalyzer("/home/ubuntu/yggdraphitecho")
    analyzer.run_full_analysis()
