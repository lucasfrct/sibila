#!/usr/bin/env python3
"""
Sibila Application Test Suite
Test script to validate application functionality after dependency updates
"""

import sys
import os
import traceback
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing imports...")
    
    try:
        import flask
        print(f"✓ Flask {flask.__version__}")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False
        
    try:
        import requests
        print(f"✓ Requests {requests.__version__}")
    except ImportError as e:
        print(f"✗ Requests import failed: {e}")
        return False
        
    try:
        import openai
        print(f"✓ OpenAI {openai.__version__}")
    except ImportError as e:
        print(f"✗ OpenAI import failed: {e}")
        return False
        
    try:
        import ollama
        print(f"✓ Ollama {ollama.__version__}")
    except ImportError as e:
        print(f"✗ Ollama import failed: {e}")
        return False
        
    try:
        try:
            import docling
            print(f"✓ Docling {docling.__version__}")
        except ImportError:
            print("⚠ Docling not available - using PDF fallback")
            import pdfplumber
            print(f"✓ PDFPlumber {pdfplumber.__version__}")
    except ImportError as e:
        print(f"✗ Document processing libraries import failed: {e}")
        return False
        
    try:
        import chromadb
        print(f"✓ ChromaDB {chromadb.__version__}")
    except ImportError as e:
        print(f"✗ ChromaDB import failed: {e}")
        return False
        
    return True

def test_application_structure():
    """Test application module imports"""
    print("\n🏗️  Testing application structure...")
    
    try:
        from server import app
        print("✓ Flask application imported")
    except ImportError as e:
        print(f"✗ Application import failed: {e}")
        return False
        
    try:
        from routes.routes import app as routes
        print("✓ Routes imported")
    except ImportError as e:
        print(f"✗ Routes import failed: {e}")
        return False
        
    try:
        from routines import migrate
        print("✓ Migration routines imported")
    except ImportError as e:
        print(f"✗ Migration routines import failed: {e}")
        return False
        
    return True

def test_flask_app():
    """Test Flask application functionality"""
    print("\n🚀 Testing Flask application...")
    
    try:
        from server import app
        
        # Test app configuration
        with app.test_client() as client:
            print("✓ Test client created")
            
            # Test if app responds (basic health check)
            try:
                response = client.get('/')
                print(f"✓ Root endpoint responds with status: {response.status_code}")
            except Exception as e:
                print(f"⚠ Root endpoint test failed: {e}")
                
        return True
    except Exception as e:
        print(f"✗ Flask app test failed: {e}")
        return False

def test_openai_compatibility():
    """Test OpenAI library compatibility"""
    print("\n🤖 Testing OpenAI compatibility...")
    
    try:
        import openai
        
        # Test if we can create a client (without API key)
        try:
            client = openai.OpenAI(api_key="test-key")
            print("✓ OpenAI client can be instantiated")
        except Exception as e:
            print(f"⚠ OpenAI client instantiation warning: {e}")
            
        # Check for common methods that might have changed
        if hasattr(openai, 'ChatCompletion'):
            print("✓ ChatCompletion class available")
        else:
            print("⚠ ChatCompletion class not found - API may have changed")
            
        return True
    except Exception as e:
        print(f"✗ OpenAI compatibility test failed: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("\n⚙️  Testing environment...")
    
    # Check for .env file
    if os.path.exists('.env'):
        print("✓ .env file exists")
        
        # Try to load environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print("✓ Environment variables loaded")
            
            # Check for required variables
            openai_key = os.getenv('OPENAI_API_KEY')
            ollama_url = os.getenv('OLLAMA_PROXY_URL')
            
            if openai_key:
                print("✓ OPENAI_API_KEY configured")
            else:
                print("⚠ OPENAI_API_KEY not set")
                
            if ollama_url:
                print("✓ OLLAMA_PROXY_URL configured")
            else:
                print("⚠ OLLAMA_PROXY_URL not set")
                
        except Exception as e:
            print(f"⚠ Environment loading warning: {e}")
    else:
        print("⚠ .env file not found")
        
    return True

def run_all_tests():
    """Run all tests"""
    print("🧪 Sibila Application Test Suite")
    print("=" * 40)
    
    all_passed = True
    
    all_passed &= test_imports()
    all_passed &= test_application_structure()
    all_passed &= test_flask_app()
    all_passed &= test_openai_compatibility()
    all_passed &= test_environment()
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! Application is ready to use.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        
    print("\n📋 Next steps:")
    print("1. Configure your .env file with API keys")
    print("2. Install and start Ollama if using local LLMs")
    print("3. Run: python main.py")
    print("4. Access the application at http://localhost:5000")
    
    return all_passed

if __name__ == "__main__":
    # Change to the script directory
    os.chdir(Path(__file__).parent)
    
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n🚨 Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)