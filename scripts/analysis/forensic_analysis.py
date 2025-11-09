#!/usr/bin/env python3.11
"""
Super-Sleuth Intro-spect Mode: Forensic Analysis of yggdraphitecho Repository
Identifies fragmentation, architectural issues, and improvement opportunities
"""

import os
import ast
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import re

class ForensicAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.issues = defaultdict(list)
        self.metrics = defaultdict(int)
        self.file_analysis = {}
        
    def analyze_imports(self, file_path: Path) -> Dict:
        """Analyze import statements to detect fragmentation"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            return {
                'imports': imports,
                'import_count': len(imports),
                'unique_imports': len(set(imports))
            }
        except Exception as e:
            return {'error': str(e)}
    
    def detect_code_duplication(self, file_path: Path) -> Dict:
        """Detect potential code duplication patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find function definitions
            tree = ast.parse(content)
            functions = []
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
            
            return {
                'function_count': len(functions),
                'class_count': len(classes),
                'functions': functions,
                'classes': classes,
                'lines_of_code': len(content.split('\n'))
            }
        except Exception as e:
            return {'error': str(e)}
    
    def check_documentation(self, file_path: Path) -> Dict:
        """Check for documentation quality"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Check module docstring
            has_module_doc = ast.get_docstring(tree) is not None
            
            # Check function/class docstrings
            documented_items = 0
            total_items = 0
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    total_items += 1
                    if ast.get_docstring(node):
                        documented_items += 1
            
            doc_coverage = (documented_items / total_items * 100) if total_items > 0 else 0
            
            return {
                'has_module_doc': has_module_doc,
                'documented_items': documented_items,
                'total_items': total_items,
                'doc_coverage': doc_coverage
            }
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_complexity(self, file_path: Path) -> Dict:
        """Analyze code complexity"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Count nested structures
            max_nesting = 0
            current_nesting = 0
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.For, ast.While, ast.If, ast.With)):
                    current_nesting += 1
                    max_nesting = max(max_nesting, current_nesting)
            
            # Count TODO/FIXME comments
            todos = len(re.findall(r'#\s*(TODO|FIXME|XXX|HACK|BUG)', content, re.IGNORECASE))
            
            return {
                'max_nesting_depth': max_nesting,
                'todo_count': todos,
                'has_issues': todos > 0
            }
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_file(self, file_path: Path):
        """Comprehensive file analysis"""
        rel_path = file_path.relative_to(self.repo_path)
        
        analysis = {
            'path': str(rel_path),
            'size': file_path.stat().st_size,
        }
        
        # Run all analyses
        analysis['imports'] = self.analyze_imports(file_path)
        analysis['structure'] = self.detect_code_duplication(file_path)
        analysis['documentation'] = self.check_documentation(file_path)
        analysis['complexity'] = self.analyze_complexity(file_path)
        
        # Identify issues
        issues = []
        
        # Check for large files
        if analysis['size'] > 10000:
            issues.append('large_file')
            self.metrics['large_files'] += 1
        
        # Check for poor documentation
        if 'doc_coverage' in analysis['documentation']:
            if analysis['documentation']['doc_coverage'] < 50:
                issues.append('poor_documentation')
                self.metrics['poorly_documented_files'] += 1
        
        # Check for high complexity
        if 'todo_count' in analysis['complexity']:
            if analysis['complexity']['todo_count'] > 5:
                issues.append('many_todos')
                self.metrics['files_with_many_todos'] += 1
        
        # Check for import issues
        if 'import_count' in analysis['imports']:
            if analysis['imports']['import_count'] > 30:
                issues.append('too_many_imports')
                self.metrics['files_with_too_many_imports'] += 1
        
        analysis['issues'] = issues
        self.file_analysis[str(rel_path)] = analysis
        
        return analysis
    
    def scan_repository(self):
        """Scan entire repository for Python files"""
        print("🔍 Starting Super-Sleuth Intro-spect Mode...")
        print(f"📂 Repository: {self.repo_path}")
        
        python_files = list(self.repo_path.rglob("*.py"))
        print(f"📊 Found {len(python_files)} Python files")
        
        for i, py_file in enumerate(python_files):
            if i % 100 == 0:
                print(f"   Analyzing file {i+1}/{len(python_files)}...")
            
            try:
                self.analyze_file(py_file)
                self.metrics['total_files_analyzed'] += 1
            except Exception as e:
                self.issues['analysis_errors'].append({
                    'file': str(py_file.relative_to(self.repo_path)),
                    'error': str(e)
                })
        
        print(f"✅ Analysis complete: {self.metrics['total_files_analyzed']} files analyzed")
    
    def detect_architectural_fragmentation(self):
        """Detect architectural fragmentation patterns"""
        print("\n🏗️ Detecting Architectural Fragmentation...")
        
        # Group files by directory
        directory_structure = defaultdict(list)
        for file_path, analysis in self.file_analysis.items():
            directory = str(Path(file_path).parent)
            directory_structure[directory].append(analysis)
        
        # Analyze directory cohesion
        for directory, files in directory_structure.items():
            if len(files) > 20:
                self.issues['large_directories'].append({
                    'directory': directory,
                    'file_count': len(files)
                })
        
        # Check for orphaned files (files with no clear module structure)
        root_files = [f for f in self.file_analysis.keys() if '/' not in f]
        if len(root_files) > 10:
            self.issues['too_many_root_files'].append({
                'count': len(root_files),
                'files': root_files[:20]  # Show first 20
            })
        
        print(f"   Found {len(self.issues['large_directories'])} large directories")
        print(f"   Found {len(root_files)} root-level Python files")
    
    def detect_dependency_fragmentation(self):
        """Detect dependency fragmentation"""
        print("\n🔗 Detecting Dependency Fragmentation...")
        
        # Collect all imports
        all_imports = defaultdict(set)
        for file_path, analysis in self.file_analysis.items():
            if 'imports' in analysis and 'imports' in analysis['imports']:
                for imp in analysis['imports']['imports']:
                    all_imports[imp].add(file_path)
        
        # Find heavily used imports (potential coupling points)
        heavy_imports = {k: v for k, v in all_imports.items() if len(v) > 50}
        
        self.issues['heavy_coupling'] = [
            {'import': imp, 'used_in': len(files)} 
            for imp, files in heavy_imports.items()
        ]
        
        print(f"   Found {len(heavy_imports)} heavily coupled imports")
    
    def generate_report(self) -> Dict:
        """Generate comprehensive forensic report"""
        print("\n📋 Generating Forensic Report...")
        
        report = {
            'summary': {
                'total_files': self.metrics['total_files_analyzed'],
                'large_files': self.metrics['large_files'],
                'poorly_documented': self.metrics['poorly_documented_files'],
                'files_with_many_todos': self.metrics['files_with_many_todos'],
                'files_with_too_many_imports': self.metrics['files_with_too_many_imports']
            },
            'issues': dict(self.issues),
            'metrics': dict(self.metrics),
            'recommendations': self.generate_recommendations()
        }
        
        return report
    
    def generate_recommendations(self) -> List[Dict]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if self.metrics['poorly_documented_files'] > 0:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Documentation',
                'issue': f"{self.metrics['poorly_documented_files']} files have poor documentation",
                'action': 'Add comprehensive docstrings to functions and classes',
                'impact': 'Improves code maintainability and developer onboarding'
            })
        
        if self.metrics['files_with_many_todos'] > 0:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Technical Debt',
                'issue': f"{self.metrics['files_with_many_todos']} files have many TODO comments",
                'action': 'Create issues for TODOs and implement fixes',
                'impact': 'Reduces technical debt and improves code quality'
            })
        
        if len(self.issues['large_directories']) > 0:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Architecture',
                'issue': f"{len(self.issues['large_directories'])} directories have too many files",
                'action': 'Refactor large directories into smaller, cohesive modules',
                'impact': 'Improves code organization and reduces cognitive load'
            })
        
        if len(self.issues.get('too_many_root_files', [])) > 0:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Architecture',
                'issue': 'Too many root-level Python files',
                'action': 'Organize root files into appropriate subdirectories',
                'impact': 'Improves repository structure and navigation'
            })
        
        if self.metrics['files_with_too_many_imports'] > 0:
            recommendations.append({
                'priority': 'LOW',
                'category': 'Code Quality',
                'issue': f"{self.metrics['files_with_too_many_imports']} files have excessive imports",
                'action': 'Refactor to reduce dependencies and improve modularity',
                'impact': 'Reduces coupling and improves testability'
            })
        
        return recommendations

def main():
    repo_path = "/home/ubuntu/yggdraphitecho"
    
    analyzer = ForensicAnalyzer(repo_path)
    
    # Run comprehensive analysis
    analyzer.scan_repository()
    analyzer.detect_architectural_fragmentation()
    analyzer.detect_dependency_fragmentation()
    
    # Generate report
    report = analyzer.generate_report()
    
    # Save report
    report_path = Path(repo_path) / "forensic_analysis_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Forensic report saved to: {report_path}")
    
    # Print summary
    print("\n" + "="*80)
    print("🎯 FORENSIC ANALYSIS SUMMARY")
    print("="*80)
    print(f"\n📊 Files Analyzed: {report['summary']['total_files']}")
    print(f"📏 Large Files: {report['summary']['large_files']}")
    print(f"📝 Poorly Documented: {report['summary']['poorly_documented']}")
    print(f"⚠️  Files with Many TODOs: {report['summary']['files_with_many_todos']}")
    print(f"🔗 Files with Too Many Imports: {report['summary']['files_with_too_many_imports']}")
    
    print("\n🎯 TOP RECOMMENDATIONS:")
    for i, rec in enumerate(report['recommendations'][:5], 1):
        print(f"\n{i}. [{rec['priority']}] {rec['category']}")
        print(f"   Issue: {rec['issue']}")
        print(f"   Action: {rec['action']}")
        print(f"   Impact: {rec['impact']}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
