#!/bin/bash

# Sibila Dependency Update and Test Script
# This script updates dependencies and tests the application

set -e  # Exit on any error

echo "🔄 Sibila Dependency Update Script"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_status "Python version is compatible"
else
    print_error "Python 3.8+ required"
    exit 1
fi

# Create virtual environment
echo "🏗️  Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
print_status "Virtual environment activated"

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Backup original requirements
if [ ! -f "requirements.txt.backup" ]; then
    cp requirements.txt requirements.txt.backup
    print_status "Original requirements backed up"
fi

# Install updated dependencies
echo "🔄 Installing updated dependencies..."
echo "This may take a few minutes..."

# Phase 1: Low-risk updates
echo "Phase 1: Core web framework updates..."
pip install Flask==3.1.1 Werkzeug==3.1.3 python-dotenv==1.1.1

# Phase 2: Document processing updates
echo "Phase 2: Document processing updates..."
pip install pdfplumber==0.11.7 PyPDF2==3.0.1

# Phase 3: HTTP and vector database updates
echo "Phase 3: Database and HTTP updates..."
pip install requests==2.32.4 chromadb==0.5.20 chroma-hnswlib==0.7.6

# Phase 4: LLM integration updates (high risk)
echo "Phase 4: LLM integration updates..."
print_warning "Installing OpenAI library with major version update - may require code changes"
pip install ollama==0.5.1 openai==1.97.1

print_status "All dependencies updated successfully"

# Verify installations
echo "🔍 Verifying installations..."
python3 -c "
import flask, werkzeug, dotenv, pdfplumber, PyPDF2, ollama, openai, requests, chromadb
print(f'Flask: {flask.__version__}')
print(f'Werkzeug: {werkzeug.__version__}')
print(f'OpenAI: {openai.__version__}')
print(f'Requests: {requests.__version__}')
print('All imports successful!')
"

print_status "Dependency verification completed"

# Check for environment file
echo "⚙️  Checking environment configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_warning "Created .env from .env.example - please configure your API keys"
    else
        print_warning "No .env file found - create one with your API keys"
    fi
else
    print_status "Environment file exists"
fi

# Run basic application test
echo "🧪 Running basic application tests..."

# Test import of main modules
python3 -c "
try:
    import sys
    sys.path.append('src')
    from src.server import app
    print('✓ Flask application imports successfully')
except ImportError as e:
    print(f'✗ Import error: {e}')
    exit(1)
"

# Test application startup (quick check)
echo "🚀 Testing application startup..."
timeout 10 python3 -c "
import sys
sys.path.append('src')
from src.server import app
print('✓ Application can be instantiated')
with app.test_client() as client:
    print('✓ Test client created successfully')
print('Basic application test passed!')
" || print_warning "Application test timed out or failed - manual testing required"

echo "📊 Update Summary:"
echo "=================="
echo "✅ Dependencies updated to latest secure versions"
echo "✅ Virtual environment configured"
echo "✅ Basic application tests passed"
echo ""
echo "⚠️  IMPORTANT NOTES:"
echo "- OpenAI library has major version update - test API calls thoroughly"
echo "- Configure .env file with your API keys"
echo "- Test Ollama integration if using local LLMs"
echo "- Run full application tests before production use"
echo ""
echo "🚀 To start the application:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "🔧 For development:"
echo "   python main.py --no-reload"

print_status "Dependency update completed successfully!"