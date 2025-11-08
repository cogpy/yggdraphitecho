#!/usr/bin/env python3.11
"""
Comprehensive Fix Script for Repository Issues
Fixes syntax errors, adds missing __init__.py files, and improves code quality
"""

import os
import json
from pathlib import Path

class RepositoryFixer:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.fixes_applied = []
        
    def fix_syntax_errors(self):
        """Fix all identified syntax errors"""
        print("🔧 Fixing syntax errors...")
        
        # Fix 1: validate_deep_tree_echo_implementation.py line 177
        # The issue is using split() inside an f-string with backslash
        file1 = self.repo_path / "validate_deep_tree_echo_implementation.py"
        if file1.exists():
            with open(file1, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix the f-string issue by extracting the split operation
            old_line = 'f"Routes: {", ".join([r.split(\'"\')[1] for r in present_routes])}"'
            new_line = 'f"Routes: {", ".join([r.split(chr(34))[1] for r in present_routes])}"'
            
            if old_line in content:
                content = content.replace(old_line, new_line)
                with open(file1, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixes_applied.append(f"Fixed f-string in {file1.name}")
                print(f"  ✅ Fixed f-string syntax error in {file1.name}")
        
        # Fix 2: aphrodite/endpoints/deep_tree_echo/dtesn_processor.py line 564
        # The issue is "10x" being interpreted as invalid literal
        file2 = self.repo_path / "aphrodite/endpoints/deep_tree_echo/dtesn_processor.py"
        if file2.exists():
            with open(file2, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Fix line 564 by changing "10x" to "10-fold" or "ten times"
            if len(lines) > 563:
                if "10x" in lines[563]:
                    lines[563] = lines[563].replace("10x", "10-fold")
                    with open(file2, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                    self.fixes_applied.append(f"Fixed invalid literal in {file2.name}")
                    print(f"  ✅ Fixed invalid literal in {file2.name}")
        
        # Fix 3: aphrodite/endpoints/deep_tree_echo/routes.py line 25
        # Missing closing parenthesis
        file3 = self.repo_path / "aphrodite/endpoints/deep_tree_echo/routes.py"
        if file3.exists():
            with open(file3, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Add closing parenthesis after line 27
            if len(lines) > 27:
                if "MultiFormatResponse" in lines[26] and not lines[26].rstrip().endswith(")"):
                    lines[26] = lines[26].rstrip() + "\n"
                    lines.insert(27, ")\n")
                    with open(file3, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                    self.fixes_applied.append(f"Fixed missing parenthesis in {file3.name}")
                    print(f"  ✅ Fixed missing parenthesis in {file3.name}")
        
        # Fix 4: aphrodite/endpoints/openai/api_server.py line 110
        # Unexpected indent - missing try block
        file4 = self.repo_path / "aphrodite/endpoints/openai/api_server.py"
        if file4.exists():
            with open(file4, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Add try block before line 110
            if len(lines) > 109:
                if "logger.info" in lines[109] and "try:" not in lines[108]:
                    # Find the import statement that should be in the try block
                    for i in range(max(0, 109-10), 109):
                        if "from aphrodite.endpoints.middleware.ab_testing_middleware" in lines[i]:
                            lines.insert(i, "try:\n")
                            break
                    with open(file4, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                    self.fixes_applied.append(f"Fixed indentation in {file4.name}")
                    print(f"  ✅ Fixed indentation in {file4.name}")
        
        # Fix 5: echo.kern/performance_integration.py line 18
        # Missing except/finally block
        file5 = self.repo_path / "echo.kern/performance_integration.py"
        if file5.exists():
            with open(file5, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # The issue is nested try blocks without proper except
            # Line 14 has first try, line 18 has second try
            # We need to add except for the second try before the third except
            if len(lines) > 24:
                # Check if line 18 has try and line 25 has except
                if "try:" in lines[17] and "except ImportError:" in lines[24]:
                    # Add except block after line 24
                    lines.insert(24, "except ImportError:\n")
                    lines.insert(25, "    DTESN_CACHE_AVAILABLE = False\n")
                    with open(file5, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                    self.fixes_applied.append(f"Fixed try-except in {file5.name}")
                    print(f"  ✅ Fixed try-except structure in {file5.name}")
        
        # Fix 6: echo.self/NanoCog/introspection/echo_client.py line 196
        # Unterminated string literal in f-string
        file6 = self.repo_path / "echo.self/NanoCog/introspection/echo_client.py"
        if file6.exists():
            with open(file6, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # The issue is multi-line f-string with list inside
            # Need to extract the random.choice outside the f-string
            old_pattern = '''f"Level {i} insight: {random.choice([
                            'Enhanced attention allocation detected',
                            'Persona dimension coherence improved',
                            'Recursive reasoning depth optimized',
                            'Hypergraph pattern encoding refined',
                            'Cognitive synergy level increased'
                        ])}"'''
            
            new_pattern = '''f"Level {i} insight: " + random.choice([
                            'Enhanced attention allocation detected',
                            'Persona dimension coherence improved',
                            'Recursive reasoning depth optimized',
                            'Hypergraph pattern encoding refined',
                            'Cognitive synergy level increased'
                        ])'''
            
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                with open(file6, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixes_applied.append(f"Fixed f-string in {file6.name}")
                print(f"  ✅ Fixed f-string syntax in {file6.name}")
    
    def add_missing_init_files(self):
        """Add missing __init__.py files to Python packages"""
        print("\n🔧 Adding missing __init__.py files...")
        
        # Load the analysis report to get missing init files
        report_file = self.repo_path / "analysis_report.json"
        if not report_file.exists():
            print("  ⚠️  Analysis report not found, skipping...")
            return
        
        with open(report_file, 'r') as f:
            report = json.load(f)
        
        missing_init_dirs = report.get('issues', {}).get('missing_init_files', [])
        
        for dir_path in missing_init_dirs[:20]:  # Fix first 20 to avoid too many changes
            full_path = self.repo_path / dir_path / "__init__.py"
            
            # Skip if already exists or if it's a special directory
            if full_path.exists():
                continue
            
            # Create a basic __init__.py file
            init_content = f'''"""
{dir_path.split('/')[-1]} package.

This package is part of the Aphrodite Engine / Deep Tree Echo integration.
"""

__version__ = "0.1.0"
'''
            
            try:
                full_path.parent.mkdir(parents=True, exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(init_content)
                self.fixes_applied.append(f"Added __init__.py to {dir_path}")
                print(f"  ✅ Added __init__.py to {dir_path}")
            except Exception as e:
                print(f"  ⚠️  Could not add __init__.py to {dir_path}: {e}")
    
    def fix_wildcard_imports(self):
        """Fix wildcard imports by making them explicit"""
        print("\n🔧 Documenting wildcard imports...")
        
        # We'll add comments to wildcard imports rather than changing them
        # as changing them requires knowing all exported symbols
        wildcard_files = [
            "aphrodite/distributed/__init__.py",
            "aphrodite/distributed/eplb/__init__.py"
        ]
        
        for file_path in wildcard_files:
            full_path = self.repo_path / file_path
            if not full_path.exists():
                continue
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add a comment about wildcard imports
            if "# Wildcard imports for backward compatibility" not in content:
                header = '''"""
Package initialization with wildcard imports for backward compatibility.

Note: Wildcard imports are used here for API compatibility.
Consider using explicit imports in new code.
"""

'''
                content = header + content
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixes_applied.append(f"Documented wildcard imports in {file_path}")
                print(f"  ✅ Documented wildcard imports in {file_path}")
    
    def generate_summary(self):
        """Generate summary of fixes applied"""
        print("\n" + "="*80)
        print("📊 FIX SUMMARY")
        print("="*80)
        print(f"\nTotal fixes applied: {len(self.fixes_applied)}")
        print("\nDetailed fixes:")
        for i, fix in enumerate(self.fixes_applied, 1):
            print(f"  {i}. {fix}")
        print("="*80)
    
    def run_all_fixes(self):
        """Run all fix operations"""
        print("🚀 Starting comprehensive repository fixes...")
        print(f"📁 Repository: {self.repo_path}\n")
        
        self.fix_syntax_errors()
        self.add_missing_init_files()
        self.fix_wildcard_imports()
        self.generate_summary()

if __name__ == "__main__":
    fixer = RepositoryFixer("/home/ubuntu/yggdraphitecho")
    fixer.run_all_fixes()
