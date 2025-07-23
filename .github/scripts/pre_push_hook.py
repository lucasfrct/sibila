#!/usr/bin/env python3
"""
Pre-push Git Hook Script
Runs OpenAI Codex validation locally before pushing to remote
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any
from openai import OpenAI

class PrePushValidator:
    def __init__(self):
        # Check if OpenAI API key is available
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            # Try to load from .env file
            env_file = Path('.env')
            if env_file.exists():
                with open(env_file) as f:
                    for line in f:
                        if line.startswith('OPENAI_API_KEY='):
                            api_key = line.split('=', 1)[1].strip().strip('"\'')
                            break
        
        if api_key:
            self.client = OpenAI(api_key=api_key)
            self.codex_available = True
        else:
            self.client = None
            self.codex_available = False
    
    def get_staged_changes(self) -> str:
        """Get staged changes (what would be committed)"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""
    
    def get_commit_diff(self) -> str:
        """Get diff of commits being pushed"""
        try:
            # Get the range of commits being pushed
            result = subprocess.run(
                ['git', 'log', '--oneline', '@{u}..HEAD'],
                capture_output=True,
                text=True
            )
            
            if not result.stdout.strip():
                # No new commits to push
                return ""
            
            # Get diff for the commits being pushed
            result = subprocess.run(
                ['git', 'diff', '@{u}..HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            # Fallback to staged changes
            return self.get_staged_changes()
    
    def validate_with_codex(self, diff_content: str) -> Dict[str, Any]:
        """Validate changes using OpenAI Codex"""
        if not self.codex_available:
            return {
                "overall_score": 7,
                "issues": [],
                "summary": "Codex validation skipped - no API key available"
            }
        
        prompt = f"""
        You are a pre-commit code validation system. Analyze the following code changes and identify any critical issues that should prevent pushing to remote:
        
        {diff_content}
        
        Focus on:
        1. Syntax errors and obvious bugs
        2. Security vulnerabilities
        3. Breaking changes without proper migration
        4. Hardcoded secrets or credentials
        5. Large files or binary content that shouldn't be committed
        6. Code that violates basic Python conventions
        
        Be conservative - only flag real issues that would break the build or cause security problems.
        
        Respond in JSON format:
        {{
            "overall_score": <1-10>,
            "issues": [
                {{
                    "severity": "low|medium|high|critical",
                    "type": "syntax|security|breaking|credentials|size|style",
                    "description": "Clear description of the issue",
                    "file": "filename if applicable",
                    "line": <number or null>,
                    "blocking": true/false
                }}
            ],
            "summary": "Brief assessment summary"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a strict code validation system that prevents problematic code from being pushed to production. Focus on critical issues only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=1500
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Warning: Codex validation failed: {e}")
            return {
                "overall_score": 7,
                "issues": [],
                "summary": f"Validation error (allowing push): {str(e)}"
            }
    
    def check_file_sizes(self) -> List[Dict[str, Any]]:
        """Check for large files that shouldn't be committed"""
        issues = []
        try:
            # Get list of files being added/modified
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only'],
                capture_output=True,
                text=True,
                check=True
            )
            
            for file_path in result.stdout.strip().split('\n'):
                if not file_path:
                    continue
                
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    
                    # Flag files larger than 10MB
                    if file_size > 10 * 1024 * 1024:
                        issues.append({
                            "severity": "high",
                            "type": "size",
                            "description": f"Large file detected: {file_size / (1024*1024):.1f}MB",
                            "file": file_path,
                            "line": None,
                            "blocking": True
                        })
                    
                    # Flag specific file types that are typically problematic
                    problematic_extensions = ['.exe', '.dll', '.so', '.dylib', '.jar', '.war']
                    if any(file_path.endswith(ext) for ext in problematic_extensions):
                        issues.append({
                            "severity": "medium",
                            "type": "binary",
                            "description": f"Binary file detected: {os.path.basename(file_path)}",
                            "file": file_path,
                            "line": None,
                            "blocking": False
                        })
        
        except subprocess.CalledProcessError:
            pass
        
        return issues
    
    def check_secrets(self, diff_content: str) -> List[Dict[str, Any]]:
        """Basic check for potential secrets in diff"""
        issues = []
        
        # Simple patterns for common secrets
        secret_patterns = [
            (r'api[_-]?key["\']?\s*[:=]\s*["\'][^"\']{20,}', 'API key'),
            (r'secret[_-]?key["\']?\s*[:=]\s*["\'][^"\']{20,}', 'Secret key'),
            (r'password["\']?\s*[:=]\s*["\'][^"\']{8,}', 'Password'),
            (r'token["\']?\s*[:=]\s*["\'][^"\']{20,}', 'Token'),
            (r'BEGIN [A-Z ]+PRIVATE KEY', 'Private key'),
        ]
        
        import re
        lines = diff_content.split('\n')
        
        for i, line in enumerate(lines):
            if line.startswith('+'):  # Only check added lines
                line_content = line[1:].strip()
                
                for pattern, secret_type in secret_patterns:
                    if re.search(pattern, line_content, re.IGNORECASE):
                        issues.append({
                            "severity": "critical",
                            "type": "credentials",
                            "description": f"Potential {secret_type.lower()} detected",
                            "file": None,
                            "line": i + 1,
                            "blocking": True
                        })
        
        return issues
    
    def display_validation_results(self, validation_result: Dict[str, Any], file_issues: List[Dict[str, Any]], secret_issues: List[Dict[str, Any]]) -> bool:
        """Display validation results and return whether to allow push"""
        
        all_issues = validation_result.get('issues', []) + file_issues + secret_issues
        score = validation_result.get('overall_score', 0)
        summary = validation_result.get('summary', '')
        
        print("\n" + "="*60)
        print("🤖 PRE-PUSH CODEX VALIDATION")
        print("="*60)
        
        if self.codex_available:
            print(f"📊 Overall Score: {score}/10")
        else:
            print("⚠️  Codex API not available - running basic checks only")
        
        print(f"📝 Summary: {summary}")
        
        if not all_issues:
            print("\n✅ No blocking issues found - push allowed!")
            return True
        
        # Separate blocking and non-blocking issues
        blocking_issues = [i for i in all_issues if i.get('blocking', False)]
        non_blocking_issues = [i for i in all_issues if not i.get('blocking', False)]
        
        if blocking_issues:
            print(f"\n❌ {len(blocking_issues)} BLOCKING ISSUE(S) FOUND:")
            for i, issue in enumerate(blocking_issues, 1):
                severity_icon = {'low': '🟡', 'medium': '🟠', 'high': '🔴', 'critical': '🚨'}.get(issue.get('severity'), '🔴')
                print(f"\n{i}. {severity_icon} {issue.get('type', '').upper()}")
                print(f"   {issue.get('description', '')}")
                if issue.get('file'):
                    print(f"   File: {issue['file']}")
                if issue.get('line'):
                    print(f"   Line: {issue['line']}")
        
        if non_blocking_issues:
            print(f"\n⚠️  {len(non_blocking_issues)} WARNING(S):")
            for i, issue in enumerate(non_blocking_issues, 1):
                severity_icon = {'low': '🟡', 'medium': '🟠', 'high': '🔴', 'critical': '🚨'}.get(issue.get('severity'), '🟡')
                print(f"   {severity_icon} {issue.get('description', '')}")
        
        if blocking_issues:
            print("\n🚫 PUSH BLOCKED - Please fix the above issues before pushing")
            print("💡 Tip: You can bypass this check with 'git push --no-verify' if needed")
            return False
        
        print("\n✅ No blocking issues - push allowed!")
        return True
    
    def run_validation(self) -> bool:
        """Run pre-push validation"""
        print("🔍 Running pre-push validation...")
        
        # Get changes being pushed
        diff_content = self.get_commit_diff()
        
        if not diff_content.strip():
            print("ℹ️  No changes to validate")
            return True
        
        print(f"📝 Analyzing {len(diff_content)} characters of changes...")
        
        # Run validations
        validation_result = self.validate_with_codex(diff_content)
        file_issues = self.check_file_sizes()
        secret_issues = self.check_secrets(diff_content)
        
        # Display results and determine if push should be allowed
        return self.display_validation_results(validation_result, file_issues, secret_issues)

def main():
    """Main entry point for pre-push hook"""
    validator = PrePushValidator()
    
    # Skip validation in CI environments
    if os.environ.get('CI') or os.environ.get('GITHUB_ACTIONS'):
        print("🤖 Skipping pre-push validation in CI environment")
        return 0
    
    try:
        allowed = validator.run_validation()
        return 0 if allowed else 1
    except KeyboardInterrupt:
        print("\n❌ Validation cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Validation error: {e}")
        print("⚠️  Allowing push due to validation error")
        return 0

if __name__ == "__main__":
    sys.exit(main())