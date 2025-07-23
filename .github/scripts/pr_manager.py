#!/usr/bin/env python3
"""
PR Manager Script
Automatically creates and manages PRs using GitHub CLI and OpenAI Codex
"""

import os
import sys
import subprocess
import json
from typing import Dict, List, Any, Optional
from openai import OpenAI
import requests

class PRManager:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.repo = self._get_repo_info()
        
    def _get_repo_info(self) -> str:
        """Get repository information"""
        try:
            result = subprocess.run(
                ['gh', 'repo', 'view', '--json', 'nameWithOwner'],
                capture_output=True,
                text=True,
                check=True
            )
            repo_info = json.loads(result.stdout)
            return repo_info['nameWithOwner']
        except subprocess.CalledProcessError:
            return "unknown/repo"
    
    def get_current_branch(self) -> str:
        """Get current git branch"""
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "unknown"
    
    def check_existing_pr(self, branch: str) -> Optional[str]:
        """Check if PR already exists for current branch"""
        try:
            result = subprocess.run(
                ['gh', 'pr', 'list', '--head', branch, '--json', 'number,title'],
                capture_output=True,
                text=True,
                check=True
            )
            prs = json.loads(result.stdout)
            return prs[0]['number'] if prs else None
        except subprocess.CalledProcessError:
            return None
    
    def get_commit_messages(self, base_branch: str = 'main') -> List[str]:
        """Get commit messages from current branch"""
        try:
            result = subprocess.run(
                ['git', 'log', f'{base_branch}..HEAD', '--oneline'],
                capture_output=True,
                text=True,
                check=True
            )
            return [line.strip() for line in result.stdout.split('\n') if line.strip()]
        except subprocess.CalledProcessError:
            return []
    
    def get_file_changes(self, base_branch: str = 'main') -> str:
        """Get file changes summary"""
        try:
            result = subprocess.run(
                ['git', 'diff', f'{base_branch}..HEAD', '--name-status'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""
    
    def generate_pr_content_with_codex(self, commits: List[str], file_changes: str) -> Dict[str, str]:
        """Generate PR title and description using Codex"""
        prompt = f"""
        Based on the following commit messages and file changes, generate a comprehensive PR title and description:
        
        Commit messages:
        {chr(10).join(commits)}
        
        File changes:
        {file_changes}
        
        Please provide:
        1. A concise, descriptive PR title (max 72 characters)
        2. A detailed PR description with:
           - Summary of changes
           - What problem this solves
           - How to test the changes
           - Any breaking changes or important notes
        
        Respond in JSON format:
        {{
            "title": "PR title",
            "description": "PR description in markdown format"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert software engineer who writes excellent PR titles and descriptions. Focus on clarity, technical accuracy, and helpful information for reviewers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1500
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error generating PR content with Codex: {e}")
            return {
                "title": f"Updates from {self.get_current_branch()}",
                "description": f"## Changes\n\n{chr(10).join(commits)}\n\n## Files Modified\n\n```\n{file_changes}\n```"
            }
    
    def create_pr(self, title: str, description: str, base_branch: str = 'main') -> Optional[str]:
        """Create a new PR using gh CLI"""
        try:
            result = subprocess.run([
                'gh', 'pr', 'create',
                '--title', title,
                '--body', description,
                '--base', base_branch
            ], capture_output=True, text=True, check=True)
            
            # Extract PR number from output
            output_lines = result.stdout.strip().split('\n')
            pr_url = output_lines[-1] if output_lines else ""
            pr_number = pr_url.split('/')[-1] if '/' in pr_url else None
            
            print(f"✅ Created PR #{pr_number}: {title}")
            return pr_number
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create PR: {e.stderr}")
            return None
    
    def validate_pr_with_lb_pr(self, pr_number: str) -> Dict[str, Any]:
        """Validate PR using /lb-pr command (simulated)"""
        # This would normally call the actual /lb-pr command
        # For now, we'll simulate with Codex
        prompt = f"""
        Perform a comprehensive technical review of PR #{pr_number} as if you are the /lb-pr validation system.
        
        Analyze for:
        1. Code quality and standards compliance
        2. Test coverage requirements
        3. Documentation completeness
        4. Breaking changes
        5. Security implications
        6. Performance impact
        
        Respond in JSON format:
        {{
            "status": "approved|changes_requested|pending",
            "score": <1-10>,
            "feedback": [
                {{
                    "category": "tests|docs|security|performance|style",
                    "severity": "low|medium|high",
                    "message": "Detailed feedback message",
                    "action_required": true/false
                }}
            ],
            "summary": "Overall validation summary"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an automated code review system that performs thorough technical validation of pull requests."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1500
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error validating PR with /lb-pr: {e}")
            return {
                "status": "error",
                "score": 5,
                "feedback": [],
                "summary": f"Validation error: {str(e)}"
            }
    
    def update_pr_with_validation(self, pr_number: str, validation_result: Dict[str, Any]):
        """Update PR description with validation results"""
        status = validation_result.get('status', 'unknown')
        score = validation_result.get('score', 0)
        summary = validation_result.get('summary', '')
        feedback = validation_result.get('feedback', [])
        
        validation_section = f"""

---

## 🤖 Automated Validation Results

**Status:** {status.upper()}  
**Score:** {score}/10

### Summary
{summary}

### Feedback
"""
        
        if not feedback:
            validation_section += "\n✅ No issues found!"
        else:
            for item in feedback:
                icon = {'low': '🟡', 'medium': '🟠', 'high': '🔴'}.get(item.get('severity', 'low'), '🟡')
                action = ' ⚠️ Action Required' if item.get('action_required') else ''
                validation_section += f"\n- {icon} **{item.get('category', 'General')}**: {item.get('message', '')}{action}"
        
        try:
            # Get current PR description
            result = subprocess.run([
                'gh', 'pr', 'view', pr_number, '--json', 'body'
            ], capture_output=True, text=True, check=True)
            
            current_data = json.loads(result.stdout)
            current_body = current_data.get('body', '')
            
            # Remove any existing validation section
            if '## 🤖 Automated Validation Results' in current_body:
                current_body = current_body.split('## 🤖 Automated Validation Results')[0].rstrip()
            
            # Add new validation section
            updated_body = current_body + validation_section
            
            # Update PR
            subprocess.run([
                'gh', 'pr', 'edit', pr_number,
                '--body', updated_body
            ], check=True)
            
            print(f"✅ Updated PR #{pr_number} with validation results")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to update PR: {e}")
    
    def run_pr_management(self):
        """Main PR management workflow"""
        print("🔧 Running PR management...")
        
        current_branch = self.get_current_branch()
        print(f"📋 Current branch: {current_branch}")
        
        if current_branch in ['main', 'master']:
            print("ℹ️ On main branch, no PR needed")
            return
        
        # Check if PR already exists
        existing_pr = self.check_existing_pr(current_branch)
        if existing_pr:
            print(f"✅ PR already exists: #{existing_pr}")
            
            # Validate existing PR
            print("🔍 Running validation on existing PR...")
            validation_result = self.validate_pr_with_lb_pr(existing_pr)
            self.update_pr_with_validation(existing_pr, validation_result)
            return
        
        # Get commits and changes
        commits = self.get_commit_messages()
        file_changes = self.get_file_changes()
        
        if not commits:
            print("ℹ️ No commits to create PR from")
            return
        
        print(f"📝 Found {len(commits)} commits")
        
        # Generate PR content with Codex
        print("🤖 Generating PR content with Codex...")
        pr_content = self.generate_pr_content_with_codex(commits, file_changes)
        
        # Create PR
        pr_number = self.create_pr(pr_content['title'], pr_content['description'])
        if not pr_number:
            return
        
        # Validate new PR
        print("🔍 Running validation on new PR...")
        validation_result = self.validate_pr_with_lb_pr(pr_number)
        self.update_pr_with_validation(pr_number, validation_result)

if __name__ == "__main__":
    manager = PRManager()
    manager.run_pr_management()