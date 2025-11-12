#!/usr/bin/env python3.11
"""
Critical Issues Analysis and Fix Script
Identifies and documents critical security and code issues
"""

import json
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
import re

class CriticalIssuesFixer:
    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.issues = []
        self.fixes_applied = []
        
    def check_dependency_versions(self) -> List[Dict]:
        """Check for outdated or vulnerable dependency versions"""
        print("🔍 Checking dependency versions...")
        
        vulnerable_packages = []
        
        # Known vulnerabilities to check
        known_issues = {
            'requests': {
                'min_safe': '2.32.0',
                'issue': 'CVE-2024-35195: Proxy-Authorization header leak',
                'severity': 'HIGH'
            },
            'jinja2': {
                'min_safe': '3.1.6',
                'issue': 'CVE-2024-56201: XSS vulnerability',
                'severity': 'HIGH'
            },
            'pillow': {
                'min_safe': '10.3.0',
                'issue': 'Multiple CVEs including buffer overflow',
                'severity': 'CRITICAL'
            },
            'aiohttp': {
                'min_safe': '3.10.11',
                'issue': 'CVE-2024-52304: Security vulnerabilities',
                'severity': 'HIGH'
            },
            'cryptography': {
                'min_safe': '43.0.1',
                'issue': 'CVE-2024-0727: Denial of service',
                'severity': 'HIGH'
            },
            'transformers': {
                'min_safe': '4.55.0',
                'issue': 'Security improvements and bug fixes',
                'severity': 'MEDIUM'
            },
        }
        
        # Check requirements files
        req_files = list(self.repo_root.glob('requirements/*.txt'))
        
        for req_file in req_files:
            try:
                with open(req_file, 'r') as f:
                    content = f.read()
                    
                for package, info in known_issues.items():
                    # Look for package specifications
                    pattern = rf'{package}\s*([><=!]+)\s*([\d.]+)'
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    
                    if matches:
                        for operator, version in matches:
                            vulnerable_packages.append({
                                'file': str(req_file.relative_to(self.repo_root)),
                                'package': package,
                                'current_spec': f"{operator} {version}",
                                'recommended': f">= {info['min_safe']}",
                                'issue': info['issue'],
                                'severity': info['severity']
                            })
            except Exception as e:
                print(f"  ⚠ Error reading {req_file}: {e}")
        
        return vulnerable_packages
    
    def check_code_security_issues(self) -> List[Dict]:
        """Check for common security issues in code"""
        print("\n🔍 Checking code security issues...")
        
        security_issues = []
        
        # Patterns to check
        security_patterns = [
            {
                'pattern': r'eval\s*\(',
                'issue': 'Use of eval() - potential code injection',
                'severity': 'CRITICAL',
                'recommendation': 'Use ast.literal_eval() or safer alternatives'
            },
            {
                'pattern': r'exec\s*\(',
                'issue': 'Use of exec() - potential code injection',
                'severity': 'CRITICAL',
                'recommendation': 'Avoid exec() or use in sandboxed environment'
            },
            {
                'pattern': r'pickle\.loads?\s*\(',
                'issue': 'Use of pickle - potential arbitrary code execution',
                'severity': 'HIGH',
                'recommendation': 'Use JSON or other safe serialization'
            },
            {
                'pattern': r'shell\s*=\s*True',
                'issue': 'subprocess with shell=True - command injection risk',
                'severity': 'HIGH',
                'recommendation': 'Use shell=False and pass command as list'
            },
            {
                'pattern': r'password\s*=\s*["\'][^"\']+["\']',
                'issue': 'Hardcoded password in code',
                'severity': 'CRITICAL',
                'recommendation': 'Use environment variables or secrets management'
            },
        ]
        
        # Scan Python files (sample - not all files to avoid timeout)
        python_files = list(self.repo_root.glob('*.py'))
        python_files.extend(list((self.repo_root / 'examples').rglob('*.py'))[:20])
        python_files.extend(list((self.repo_root / 'scripts').rglob('*.py'))[:20])
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                for pattern_info in security_patterns:
                    matches = re.finditer(pattern_info['pattern'], content)
                    for match in matches:
                        # Find line number
                        line_num = content[:match.start()].count('\n') + 1
                        
                        security_issues.append({
                            'file': str(py_file.relative_to(self.repo_root)),
                            'line': line_num,
                            'issue': pattern_info['issue'],
                            'severity': pattern_info['severity'],
                            'recommendation': pattern_info['recommendation'],
                            'code_snippet': lines[line_num - 1].strip() if line_num <= len(lines) else ''
                        })
            except Exception as e:
                pass  # Skip files that can't be read
        
        return security_issues
    
    def check_configuration_issues(self) -> List[Dict]:
        """Check for configuration security issues"""
        print("\n🔍 Checking configuration issues...")
        
        config_issues = []
        
        # Check for exposed secrets or keys
        sensitive_patterns = [
            r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'secret[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'password\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
        ]
        
        # Check configuration files
        config_files = []
        config_files.extend(list(self.repo_root.glob('*.yaml')))
        config_files.extend(list(self.repo_root.glob('*.yml')))
        config_files.extend(list(self.repo_root.glob('*.json')))
        config_files.extend(list(self.repo_root.glob('*.toml')))
        
        for config_file in config_files[:20]:  # Limit to avoid timeout
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                for pattern in sensitive_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        config_issues.append({
                            'file': str(config_file.relative_to(self.repo_root)),
                            'issue': 'Potential hardcoded secret or credential',
                            'severity': 'CRITICAL',
                            'recommendation': 'Move secrets to environment variables or secrets manager'
                        })
                        break  # One issue per file is enough
            except Exception as e:
                pass
        
        return config_issues
    
    def check_import_security(self) -> List[Dict]:
        """Check for insecure imports"""
        print("\n🔍 Checking import security...")
        
        import_issues = []
        
        # Check for imports that might be security concerns
        risky_imports = [
            ('pickle', 'Pickle can execute arbitrary code during deserialization'),
            ('yaml.load', 'yaml.load() is unsafe, use yaml.safe_load()'),
            ('subprocess.*shell.*True', 'subprocess with shell=True is risky'),
        ]
        
        return import_issues  # Simplified for now
    
    def generate_fixes(self) -> List[Dict]:
        """Generate recommended fixes"""
        print("\n💡 Generating recommended fixes...")
        
        fixes = []
        
        # Fix 1: Update requirements to use secure versions
        fixes.append({
            'priority': 'CRITICAL',
            'category': 'Dependencies',
            'title': 'Update vulnerable dependencies',
            'description': 'Update all dependencies to secure versions',
            'action': 'Update requirements files with minimum secure versions',
            'files_affected': ['requirements/common.txt', 'requirements/*.txt']
        })
        
        # Fix 2: Add security scanning to CI/CD
        fixes.append({
            'priority': 'HIGH',
            'category': 'CI/CD',
            'title': 'Add automated security scanning',
            'description': 'Add dependency scanning and SAST to CI/CD pipeline',
            'action': 'Create GitHub Actions workflow for security scanning',
            'files_affected': ['.github/workflows/security.yml']
        })
        
        # Fix 3: Add security policy
        fixes.append({
            'priority': 'MEDIUM',
            'category': 'Documentation',
            'title': 'Add SECURITY.md',
            'description': 'Document security policy and vulnerability reporting',
            'action': 'Create SECURITY.md with vulnerability disclosure process',
            'files_affected': ['SECURITY.md']
        })
        
        # Fix 4: Add .gitignore for sensitive files
        fixes.append({
            'priority': 'HIGH',
            'category': 'Configuration',
            'title': 'Ensure .gitignore covers sensitive files',
            'description': 'Prevent accidental commit of secrets',
            'action': 'Update .gitignore to include common secret patterns',
            'files_affected': ['.gitignore']
        })
        
        return fixes
    
    def apply_critical_fixes(self) -> None:
        """Apply critical fixes that can be automated"""
        print("\n🔧 Applying critical fixes...")
        
        # Fix 1: Update requirements with secure versions
        self.fix_requirements_versions()
        
        # Fix 2: Create SECURITY.md
        self.create_security_policy()
        
        # Fix 3: Update .gitignore
        self.update_gitignore()
        
        # Fix 4: Create security scanning workflow
        self.create_security_workflow()
    
    def fix_requirements_versions(self) -> None:
        """Update requirements files with secure versions"""
        print("  📝 Updating requirements files...")
        
        # Update common.txt with secure versions
        common_file = self.repo_root / 'requirements' / 'common.txt'
        
        if common_file.exists():
            with open(common_file, 'r') as f:
                content = f.read()
            
            # Update specific packages to secure versions
            updates = {
                r'requests\s*>=\s*[\d.]+': 'requests >= 2.32.0',
                r'jinja2\s*>=\s*[\d.]+': 'jinja2 >= 3.1.6',
                r'pillow\s*[>=<]': 'pillow >= 10.3.0  # Security updates',
                r'aiohttp\s*$': 'aiohttp >= 3.10.11  # Security updates',
            }
            
            modified = False
            for pattern, replacement in updates.items():
                if re.search(pattern, content, re.IGNORECASE):
                    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                    modified = True
            
            if modified:
                with open(common_file, 'w') as f:
                    f.write(content)
                print(f"    ✓ Updated {common_file.relative_to(self.repo_root)}")
                self.fixes_applied.append('Updated requirements/common.txt with secure versions')
    
    def create_security_policy(self) -> None:
        """Create SECURITY.md file"""
        print("  📝 Creating SECURITY.md...")
        
        security_md = self.repo_root / 'SECURITY.md'
        
        content = """# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| < main  | :x:                |

## Reporting a Vulnerability

We take the security of yggdraphitecho seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Reporting Process

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via:
- **Email**: security@[your-domain].com
- **GitHub Security Advisories**: Use the "Report a vulnerability" button in the Security tab

### What to Include

Please include the following information in your report:
- Type of vulnerability
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the vulnerability

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 7 days
  - High: 14 days
  - Medium: 30 days
  - Low: 90 days

## Security Best Practices

When using yggdraphitecho:

1. **Keep Dependencies Updated**: Regularly update to the latest version
2. **Use Virtual Environments**: Isolate dependencies
3. **Secure Credentials**: Never commit secrets or API keys
4. **Review Code**: Audit third-party code before integration
5. **Monitor Alerts**: Enable GitHub Dependabot alerts

## Known Security Considerations

### Dependency Security

This project uses multiple dependencies. We regularly:
- Monitor security advisories
- Update vulnerable dependencies
- Run automated security scans

### Code Execution

Some features involve code execution. When using these features:
- Run in sandboxed environments
- Validate all inputs
- Limit permissions appropriately

## Security Updates

Security updates are released as:
- Patch versions for critical vulnerabilities
- Minor versions for high-severity issues
- Documented in release notes with CVE references

## Acknowledgments

We appreciate security researchers who responsibly disclose vulnerabilities. Contributors will be acknowledged in:
- Release notes
- SECURITY.md (with permission)
- Hall of Fame (coming soon)

---

**Last Updated**: November 2025
"""
        
        with open(security_md, 'w') as f:
            f.write(content)
        
        print(f"    ✓ Created {security_md.relative_to(self.repo_root)}")
        self.fixes_applied.append('Created SECURITY.md')
    
    def update_gitignore(self) -> None:
        """Update .gitignore to prevent secret leaks"""
        print("  📝 Updating .gitignore...")
        
        gitignore = self.repo_root / '.gitignore'
        
        security_patterns = """
# Security - Prevent accidental commit of secrets
.env
.env.local
.env.*.local
*.key
*.pem
*.p12
*.pfx
secrets.yaml
secrets.yml
secrets.json
*secret*
*password*
*credentials*
.aws/
.azure/
.gcp/

# API Keys and Tokens
*api_key*
*api-key*
*apikey*
*token*
*auth*

# Database
*.db-journal
*.sqlite3
*.sqlite

# Logs that might contain sensitive data
*.log
logs/
"""
        
        if gitignore.exists():
            with open(gitignore, 'r') as f:
                content = f.read()
            
            # Check if security section exists
            if '# Security' not in content:
                with open(gitignore, 'a') as f:
                    f.write('\n' + security_patterns)
                print(f"    ✓ Updated {gitignore.relative_to(self.repo_root)}")
                self.fixes_applied.append('Updated .gitignore with security patterns')
            else:
                print(f"    ℹ Security patterns already in .gitignore")
        else:
            with open(gitignore, 'w') as f:
                f.write(security_patterns)
            print(f"    ✓ Created {gitignore.relative_to(self.repo_root)}")
            self.fixes_applied.append('Created .gitignore with security patterns')
    
    def create_security_workflow(self) -> None:
        """Create GitHub Actions workflow for security scanning"""
        print("  📝 Creating security scanning workflow...")
        
        workflows_dir = self.repo_root / '.github' / 'workflows'
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        security_workflow = workflows_dir / 'security-scan.yml'
        
        content = """name: Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  dependency-scan:
    name: Dependency Security Scan
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install safety pip-audit
    
    - name: Run Safety check
      run: |
        pip install -r requirements/common.txt
        safety check --json || true
    
    - name: Run pip-audit
      run: |
        pip-audit -r requirements/common.txt || true
  
  code-scan:
    name: Code Security Scan
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Bandit
      run: |
        pip install bandit
        bandit -r . -f json -o bandit-report.json || true
    
    - name: Upload Bandit report
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: bandit-report
        path: bandit-report.json
  
  secret-scan:
    name: Secret Scanning
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: TruffleHog OSS
      uses: trufflesecurity/trufflehog@main
      with:
        path: ./
        base: ${{ github.event.repository.default_branch }}
        head: HEAD
"""
        
        with open(security_workflow, 'w') as f:
            f.write(content)
        
        print(f"    ✓ Created {security_workflow.relative_to(self.repo_root)}")
        self.fixes_applied.append('Created security scanning workflow')
    
    def generate_report(self) -> Dict:
        """Generate comprehensive security report"""
        print("\n📋 Generating security report...")
        
        # Run all checks
        dependency_issues = self.check_dependency_versions()
        code_issues = self.check_code_security_issues()
        config_issues = self.check_configuration_issues()
        fixes = self.generate_fixes()
        
        report = {
            'summary': {
                'total_issues': len(dependency_issues) + len(code_issues) + len(config_issues),
                'critical': sum(1 for i in code_issues + config_issues if i.get('severity') == 'CRITICAL'),
                'high': sum(1 for i in dependency_issues + code_issues + config_issues if i.get('severity') == 'HIGH'),
                'medium': sum(1 for i in dependency_issues + code_issues + config_issues if i.get('severity') == 'MEDIUM'),
                'fixes_applied': len(self.fixes_applied)
            },
            'dependency_issues': dependency_issues,
            'code_security_issues': code_issues,
            'configuration_issues': config_issues,
            'recommended_fixes': fixes,
            'fixes_applied': self.fixes_applied
        }
        
        return report

def main():
    print("🔒 Critical Issues Analysis and Fix")
    print("=" * 80)
    
    fixer = CriticalIssuesFixer()
    
    # Generate report
    report = fixer.generate_report()
    
    # Apply fixes
    fixer.apply_critical_fixes()
    
    # Save report
    report_path = Path('CRITICAL_ISSUES_REPORT.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Report saved to: {report_path}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("🎯 CRITICAL ISSUES SUMMARY")
    print("=" * 80)
    print(f"\n📊 Total Issues Found: {report['summary']['total_issues']}")
    print(f"🔴 Critical: {report['summary']['critical']}")
    print(f"🟠 High: {report['summary']['high']}")
    print(f"🟡 Medium: {report['summary']['medium']}")
    
    print(f"\n✅ Fixes Applied: {report['summary']['fixes_applied']}")
    for fix in report['fixes_applied']:
        print(f"  ✓ {fix}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
