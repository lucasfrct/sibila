#!/usr/bin/env python3
"""
PR Reviewer Script
Performs automated code review using OpenAI Codex and posts comments on PRs
"""

import os
import sys
import subprocess
import json
from typing import Dict, List, Any, Optional
from openai import OpenAI
import requests

class PRReviewer:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.pr_number = os.environ.get('PR_NUMBER')
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
    
    def get_pr_diff(self, pr_number: str) -> str:
        """Get PR diff content"""
        try:
            result = subprocess.run([
                'gh', 'pr', 'diff', pr_number
            ], capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error getting PR diff: {e}")
            return ""
    
    def get_pr_info(self, pr_number: str) -> Dict[str, Any]:
        """Get PR information"""
        try:
            result = subprocess.run([
                'gh', 'pr', 'view', pr_number, '--json', 
                'title,body,author,files,additions,deletions'
            ], capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error getting PR info: {e}")
            return {}
    
    def analyze_pr_with_codex(self, pr_info: Dict[str, Any], diff_content: str) -> Dict[str, Any]:
        """Analyze PR using OpenAI Codex /pr command simulation"""
        title = pr_info.get('title', '')
        body = pr_info.get('body', '')
        files = [f['path'] for f in pr_info.get('files', [])]
        additions = pr_info.get('additions', 0)
        deletions = pr_info.get('deletions', 0)
        
        prompt = f"""
        You are performing a comprehensive code review as the /pr command system. 
        
        PR Information:
        - Title: {title}
        - Description: {body}
        - Files changed: {len(files)}
        - Lines added: {additions}
        - Lines deleted: {deletions}
        - Modified files: {', '.join(files[:10])}
        
        Code diff:
        {diff_content[:8000]}  # Truncate for token limits
        
        Provide a thorough code review covering:
        1. Architecture and design decisions
        2. Code quality and maintainability
        3. Security vulnerabilities
        4. Performance implications
        5. Test coverage adequacy
        6. Documentation completeness
        7. Best practices adherence
        8. Potential edge cases or bugs
        
        Respond in JSON format:
        {{
            "overall_assessment": {{
                "score": <1-10>,
                "recommendation": "approve|request_changes|comment",
                "summary": "Overall assessment summary"
            }},
            "detailed_review": {{
                "architecture": {{
                    "score": <1-10>,
                    "comments": ["comment1", "comment2"],
                    "suggestions": ["suggestion1", "suggestion2"]
                }},
                "code_quality": {{
                    "score": <1-10>,
                    "comments": ["comment1", "comment2"],
                    "suggestions": ["suggestion1", "suggestion2"]
                }},
                "security": {{
                    "score": <1-10>,
                    "vulnerabilities": ["vuln1", "vuln2"],
                    "recommendations": ["rec1", "rec2"]
                }},
                "performance": {{
                    "score": <1-10>,
                    "concerns": ["concern1", "concern2"],
                    "optimizations": ["opt1", "opt2"]
                }},
                "testing": {{
                    "score": <1-10>,
                    "coverage_assessment": "description",
                    "missing_tests": ["test1", "test2"]
                }},
                "documentation": {{
                    "score": <1-10>,
                    "gaps": ["gap1", "gap2"],
                    "improvements": ["imp1", "imp2"]
                }}
            }},
            "action_items": [
                {{
                    "priority": "high|medium|low",
                    "category": "security|performance|testing|docs|refactoring",
                    "description": "Detailed action item",
                    "blocking": true/false
                }}
            ]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior software engineer and security expert conducting a thorough code review. Be constructive, specific, and focus on actionable feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=3000
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error analyzing PR with Codex: {e}")
            return {
                "overall_assessment": {
                    "score": 5,
                    "recommendation": "comment",
                    "summary": f"Review failed due to error: {str(e)}"
                },
                "detailed_review": {},
                "action_items": []
            }
    
    def format_review_comment(self, review_result: Dict[str, Any]) -> str:
        """Format the review result into a comprehensive comment"""
        overall = review_result.get('overall_assessment', {})
        detailed = review_result.get('detailed_review', {})
        action_items = review_result.get('action_items', [])
        
        score = overall.get('score', 0)
        recommendation = overall.get('recommendation', 'comment')
        summary = overall.get('summary', '')
        
        # Header with recommendation
        rec_emoji = {
            'approve': '✅',
            'request_changes': '❌',
            'comment': '💬'
        }.get(recommendation, '💬')
        
        comment = f"""## {rec_emoji} Automated Code Review - /pr Results

**Overall Score:** {score}/10  
**Recommendation:** {recommendation.replace('_', ' ').title()}

### Summary
{summary}

---

"""
        
        # Detailed review sections
        sections = [
            ('architecture', '🏗️ Architecture & Design'),
            ('code_quality', '🔧 Code Quality'),
            ('security', '🔒 Security Analysis'),
            ('performance', '⚡ Performance'),
            ('testing', '🧪 Testing'),
            ('documentation', '📚 Documentation')
        ]
        
        for section_key, section_title in sections:
            section_data = detailed.get(section_key, {})
            if not section_data:
                continue
                
            section_score = section_data.get('score', 0)
            comment += f"\n### {section_title} ({section_score}/10)\n"
            
            # Comments
            comments = section_data.get('comments', [])
            if comments:
                comment += "\n**Observations:**\n"
                for c in comments:
                    comment += f"- {c}\n"
            
            # Suggestions/Recommendations/etc
            for key in ['suggestions', 'recommendations', 'optimizations', 'improvements']:
                items = section_data.get(key, [])
                if items:
                    comment += f"\n**{key.title()}:**\n"
                    for item in items:
                        comment += f"- {item}\n"
            
            # Special handling for specific sections
            if section_key == 'security':
                vulns = section_data.get('vulnerabilities', [])
                if vulns:
                    comment += "\n**🚨 Security Vulnerabilities:**\n"
                    for vuln in vulns:
                        comment += f"- {vuln}\n"
            
            elif section_key == 'performance':
                concerns = section_data.get('concerns', [])
                if concerns:
                    comment += "\n**⚠️ Performance Concerns:**\n"
                    for concern in concerns:
                        comment += f"- {concern}\n"
            
            elif section_key == 'testing':
                coverage = section_data.get('coverage_assessment', '')
                missing = section_data.get('missing_tests', [])
                if coverage:
                    comment += f"\n**Coverage Assessment:** {coverage}\n"
                if missing:
                    comment += "\n**Missing Tests:**\n"
                    for test in missing:
                        comment += f"- {test}\n"
            
            elif section_key == 'documentation':
                gaps = section_data.get('gaps', [])
                if gaps:
                    comment += "\n**Documentation Gaps:**\n"
                    for gap in gaps:
                        comment += f"- {gap}\n"
        
        # Action Items
        if action_items:
            comment += "\n---\n\n## 📋 Action Items\n"
            
            # Group by priority
            for priority in ['high', 'medium', 'low']:
                priority_items = [item for item in action_items if item.get('priority') == priority]
                if not priority_items:
                    continue
                
                priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(priority, '🔵')
                comment += f"\n### {priority_emoji} {priority.title()} Priority\n"
                
                for item in priority_items:
                    blocking = " 🚫 **BLOCKING**" if item.get('blocking') else ""
                    category = item.get('category', 'general').title()
                    description = item.get('description', '')
                    comment += f"- **{category}**: {description}{blocking}\n"
        
        comment += "\n---\n*This review was generated automatically by OpenAI Codex. Please review and validate the suggestions.*"
        
        return comment
    
    def post_review_comment(self, pr_number: str, comment: str):
        """Post review comment to PR"""
        try:
            # Create a temporary file for the comment
            with open('/tmp/review_comment.md', 'w') as f:
                f.write(comment)
            
            # Post comment using gh CLI
            subprocess.run([
                'gh', 'pr', 'comment', pr_number,
                '--body-file', '/tmp/review_comment.md'
            ], check=True)
            
            print(f"✅ Posted review comment to PR #{pr_number}")
            
            # Clean up
            os.remove('/tmp/review_comment.md')
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to post comment: {e}")
    
    def run_pr_review(self):
        """Main PR review workflow"""
        if not self.pr_number:
            print("❌ No PR number provided")
            return
        
        print(f"🔍 Reviewing PR #{self.pr_number}...")
        
        # Get PR information
        pr_info = self.get_pr_info(self.pr_number)
        if not pr_info:
            print("❌ Could not retrieve PR information")
            return
        
        print(f"📋 PR: {pr_info.get('title', 'Unknown')}")
        print(f"👤 Author: {pr_info.get('author', {}).get('login', 'Unknown')}")
        
        # Get PR diff
        diff_content = self.get_pr_diff(self.pr_number)
        if not diff_content:
            print("❌ Could not retrieve PR diff")
            return
        
        print(f"📝 Analyzing {len(diff_content)} characters of changes...")
        
        # Analyze with Codex
        review_result = self.analyze_pr_with_codex(pr_info, diff_content)
        
        # Format and post comment
        comment = self.format_review_comment(review_result)
        print(f"💬 Generated {len(comment)} character review")
        
        self.post_review_comment(self.pr_number, comment)
        
        # Print summary
        overall = review_result.get('overall_assessment', {})
        score = overall.get('score', 0)
        recommendation = overall.get('recommendation', 'comment')
        
        print(f"📊 Review completed: {score}/10 - {recommendation}")

if __name__ == "__main__":
    reviewer = PRReviewer()
    reviewer.run_pr_review()