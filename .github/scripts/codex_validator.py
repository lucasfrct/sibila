#!/usr/bin/env python3
"""
OpenAI Codex Validator Script
Validates code changes using OpenAI Codex before commits
"""

import os
import sys
import subprocess
import json
from typing import Dict, List, Any
from openai import OpenAI
import requests

class CodexValidator:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.github_token = os.environ.get('GITHUB_TOKEN')
        
    def get_git_diff(self) -> str:
        """Get git diff for current changes"""
        try:
            result = subprocess.run(
                ['git', 'diff', 'HEAD~1', 'HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            # If no previous commit, get diff from staging
            result = subprocess.run(
                ['git', 'diff', '--cached'],
                capture_output=True,
                text=True
            )
            return result.stdout
    
    def validate_with_codex(self, diff_content: str) -> Dict[str, Any]:
        """Validate code changes using OpenAI Codex"""
        prompt = f"""
        Analyze the following code changes and provide a comprehensive review:
        
        {diff_content}
        
        Please provide feedback on:
        1. Code quality and best practices
        2. Potential bugs or issues
        3. Security concerns
        4. Performance implications
        5. Maintainability
        
        Respond in JSON format with:
        {{
            "overall_score": <1-10>,
            "issues": [
                {{
                    "severity": "low|medium|high|critical",
                    "type": "bug|security|performance|style|logic",
                    "description": "Description of the issue",
                    "suggestion": "How to fix it",
                    "line_number": <number or null>
                }}
            ],
            "summary": "Overall assessment summary"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer with deep knowledge of Python, software engineering best practices, and security."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error calling Codex API: {e}")
            return {
                "overall_score": 5,
                "issues": [],
                "summary": f"Unable to validate with Codex: {str(e)}"
            }
    
    def create_validation_report(self, validation_result: Dict[str, Any]) -> str:
        """Create a markdown report from validation results"""
        score = validation_result.get('overall_score', 0)
        issues = validation_result.get('issues', [])
        summary = validation_result.get('summary', '')
        
        report = f"""# 🤖 Codex Code Validation Report

## Overall Score: {score}/10

## Summary
{summary}

## Issues Found ({len(issues)})
"""
        
        if not issues:
            report += "\n✅ No issues found!"
        else:
            for i, issue in enumerate(issues, 1):
                severity_icon = {
                    'low': '🟡',
                    'medium': '🟠', 
                    'high': '🔴',
                    'critical': '🚨'
                }.get(issue.get('severity', 'low'), '🟡')
                
                report += f"""
### {severity_icon} Issue {i}: {issue.get('type', '').title()}
**Severity:** {issue.get('severity', 'Unknown')}
**Description:** {issue.get('description', '')}
**Suggestion:** {issue.get('suggestion', '')}
"""
                if issue.get('line_number'):
                    report += f"**Line:** {issue['line_number']}\n"
        
        return report
    
    def run_validation(self):
        """Main validation workflow"""
        print("🔍 Running Codex validation...")
        
        # Get git diff
        diff_content = self.get_git_diff()
        if not diff_content.strip():
            print("✅ No changes to validate")
            return True
        
        print(f"📝 Analyzing {len(diff_content)} characters of changes...")
        
        # Validate with Codex
        validation_result = self.validate_with_codex(diff_content)
        
        # Create report
        report = self.create_validation_report(validation_result)
        print("\n" + report)
        
        # Save report to file
        os.makedirs('artifacts', exist_ok=True)
        with open('artifacts/codex-validation-report.md', 'w') as f:
            f.write(report)
        
        # Determine if validation passes
        score = validation_result.get('overall_score', 0)
        critical_issues = [i for i in validation_result.get('issues', []) 
                          if i.get('severity') == 'critical']
        
        if score < 6 or critical_issues:
            print(f"❌ Validation failed (Score: {score}/10, Critical issues: {len(critical_issues)})")
            return False
        
        print(f"✅ Validation passed (Score: {score}/10)")
        return True

if __name__ == "__main__":
    validator = CodexValidator()
    success = validator.run_validation()
    sys.exit(0 if success else 1)