#!/usr/bin/env python3
"""
Setup script for Codex Pipeline
Installs git hooks and configures the development environment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def setup_git_hooks():
    """Setup git hooks for local validation"""
    print("🔧 Setting up git hooks...")
    
    # Ensure .git/hooks directory exists
    hooks_dir = Path('.git/hooks')
    hooks_dir.mkdir(parents=True, exist_ok=True)
    
    # Create pre-push hook
    pre_push_hook = hooks_dir / 'pre-push'
    
    hook_content = '''#!/bin/bash
# Pre-push hook for Codex validation
python .github/scripts/pre_push_hook.py
exit $?
'''
    
    with open(pre_push_hook, 'w') as f:
        f.write(hook_content)
    
    # Make hook executable
    pre_push_hook.chmod(0o755)
    
    print(f"✅ Created pre-push hook: {pre_push_hook}")

def check_dependencies():
    """Check required dependencies"""
    print("🔍 Checking dependencies...")
    
    required_commands = ['git', 'python3', 'gh']
    missing = []
    
    for cmd in required_commands:
        if not shutil.which(cmd):
            missing.append(cmd)
    
    if missing:
        print(f"❌ Missing required commands: {', '.join(missing)}")
        print("Please install the missing dependencies:")
        print("- git: https://git-scm.com/downloads")
        print("- python3: https://www.python.org/downloads/")
        print("- gh (GitHub CLI): https://cli.github.com/")
        return False
    
    # Check Python packages
    try:
        import openai
        print("✅ OpenAI package is available")
    except ImportError:
        print("⚠️  OpenAI package not found. Install with: pip install openai")
        return False
    
    print("✅ All dependencies are available")
    return True

def check_environment():
    """Check environment configuration"""
    print("🔍 Checking environment configuration...")
    
    # Check for OpenAI API key
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        # Check .env file
        env_file = Path('.env')
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith('OPENAI_API_KEY='):
                        api_key = line.split('=', 1)[1].strip().strip('"\'')
                        break
    
    if api_key:
        print("✅ OpenAI API key is configured")
    else:
        print("⚠️  OpenAI API key not found")
        print("Add OPENAI_API_KEY to your environment or .env file")
        print("Get your API key from: https://platform.openai.com/api-keys")
    
    # Check GitHub CLI authentication
    try:
        result = subprocess.run(['gh', 'auth', 'status'], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ GitHub CLI is authenticated")
        else:
            print("⚠️  GitHub CLI not authenticated")
            print("Run: gh auth login")
    except subprocess.CalledProcessError:
        print("⚠️  Could not check GitHub CLI authentication")

def create_gitignore_entries():
    """Add necessary entries to .gitignore"""
    print("📝 Updating .gitignore...")
    
    gitignore_entries = [
        "# Codex Pipeline artifacts",
        "artifacts/",
        ".codex_cache/",
        "*.codex.log",
        ""
    ]
    
    gitignore_path = Path('.gitignore')
    
    # Read existing .gitignore
    existing_content = ""
    if gitignore_path.exists():
        with open(gitignore_path) as f:
            existing_content = f.read()
    
    # Check if our entries are already present
    if "# Codex Pipeline artifacts" not in existing_content:
        with open(gitignore_path, 'a') as f:
            f.write('\n'.join(gitignore_entries) + '\n')
        print("✅ Updated .gitignore with Codex Pipeline entries")
    else:
        print("✅ .gitignore already contains Codex Pipeline entries")

def create_example_env():
    """Create example .env file if it doesn't exist"""
    env_example_path = Path('.env.example')
    
    if not env_example_path.exists():
        env_content = """# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Custom model settings
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.1

# GitHub Configuration (usually set by GitHub Actions)
GITHUB_TOKEN=your_github_token_here
"""
        
        with open(env_example_path, 'w') as f:
            f.write(env_content)
        
        print("✅ Created .env.example file")
    
    # Add OpenAI entries to existing .env.example if needed
    with open(env_example_path) as f:
        content = f.read()
    
    if 'OPENAI_API_KEY' not in content:
        with open(env_example_path, 'a') as f:
            f.write('\n# OpenAI API Configuration\n')
            f.write('OPENAI_API_KEY=your_openai_api_key_here\n')
        print("✅ Added OpenAI configuration to .env.example")

def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "="*60)
    print("🎉 CODEX PIPELINE SETUP COMPLETE!")
    print("="*60)
    
    print("""
📋 WHAT'S BEEN CONFIGURED:

1. ✅ GitHub Actions workflows (.github/workflows/codex-pipeline.yml)
   - Runs on every push and PR
   - Automatically validates code with Codex
   - Creates and manages PRs
   - Posts automated reviews

2. ✅ Pre-push git hook (.git/hooks/pre-push)
   - Validates code locally before pushing
   - Checks for secrets and large files
   - Uses OpenAI Codex for analysis

3. ✅ Python scripts (.github/scripts/)
   - codex_validator.py: Code validation
   - pr_manager.py: Automated PR management  
   - pr_reviewer.py: Automated code reviews
   - pre_push_hook.py: Local validation

📋 NEXT STEPS:

1. 🔑 Set up your OpenAI API key:
   - Get key from: https://platform.openai.com/api-keys
   - Add to .env file: OPENAI_API_KEY=your_key_here
   - Or set environment variable: export OPENAI_API_KEY=your_key

2. 🔑 Configure GitHub secrets (for repository owner):
   - Go to: Settings → Secrets and variables → Actions
   - Add: OPENAI_API_KEY (your OpenAI API key)
   - GITHUB_TOKEN is automatically provided

3. 🚀 Test the pipeline:
   - Make some code changes
   - Try: git add . && git commit -m "test codex pipeline"
   - Push: git push (pre-push hook will run)
   - Create a PR to see automated reviews

📋 COMMANDS AVAILABLE:

Local validation:
  python .github/scripts/pre_push_hook.py

Manual PR review:
  PR_NUMBER=123 python .github/scripts/pr_reviewer.py

Manual PR management:
  python .github/scripts/pr_manager.py

💡 TIPS:

- The pre-push hook will validate your code before pushing
- PR reviews use the simulated /lb-pr and /pr commands
- All validations are logged and can be reviewed
- You can bypass hooks with: git push --no-verify
""")

def main():
    """Main setup function"""
    print("🚀 Setting up OpenAI Codex Pipeline...")
    print("="*60)
    
    # Check if we're in a git repository
    if not Path('.git').exists():
        print("❌ Not in a git repository! Please run this from the root of your git repo.")
        return 1
    
    # Run setup steps
    steps = [
        ("Checking dependencies", check_dependencies),
        ("Setting up git hooks", setup_git_hooks),
        ("Checking environment", check_environment),
        ("Creating .gitignore entries", create_gitignore_entries),
        ("Creating example environment file", create_example_env),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        try:
            result = step_func()
            if result is False:
                print(f"⚠️  {step_name} completed with warnings")
        except Exception as e:
            print(f"❌ Error in {step_name}: {e}")
            return 1
    
    print_usage_instructions()
    return 0

if __name__ == "__main__":
    sys.exit(main())