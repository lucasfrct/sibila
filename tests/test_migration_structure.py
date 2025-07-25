#!/usr/bin/env python3
"""
Minimal test script for Docling migration structure
Tests only the structural changes without external dependencies
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_file_structure():
    """Test that all required files exist"""
    print("🧪 Testing file structure...")
    
    required_files = [
        "src/modules/document/docling_reader.py",
        "src/modules/document/service.py", 
        "src/modules/document/document_info.py",
        "requirements.txt"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False
    
    return all_exist

def test_requirements():
    """Test that requirements.txt has Docling dependencies"""
    print("🧪 Testing requirements...")
    
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
            
        required_packages = ["docling", "docling-core", "docling-ibm-models", "docling-parse"]
        found_packages = []
        
        for package in required_packages:
            if package in content:
                found_packages.append(package)
                print(f"✓ {package} found in requirements.txt")
            else:
                print(f"✗ {package} missing from requirements.txt")
        
        return len(found_packages) == len(required_packages)
        
    except Exception as e:
        print(f"✗ Error reading requirements.txt: {e}")
        return False

def test_import_structure():
    """Test basic import structure without external dependencies"""
    print("🧪 Testing import structure...")
    
    try:
        # Test that we can import the modules (they should handle missing dependencies gracefully)
        print("Testing docling_reader import...")
        from modules.document import docling_reader
        print("✓ docling_reader imports successfully")
        
        print("Testing service import...")
        from modules.document import service 
        print("✓ service imports successfully")
        
        print("Testing document_info import...")
        from modules.document import document_info
        print("✓ document_info imports successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_function_availability():
    """Test that expected functions are available"""
    print("🧪 Testing function availability...")
    
    try:
        from modules.document import service
        
        # Test new functions
        expected_functions = [
            'document_reader',
            'document_content', 
            'document_pages_with_details',
            'document_paragraphs_with_details',
            'document_phrases_with_details'
        ]
        
        # Test compatibility aliases
        compatibility_aliases = [
            'pdf_reader',
            'pdf_content',
            'pdf_pages_with_details', 
            'pdf_paragraphs_with_details',
            'pdf_phrases_with_details'
        ]
        
        all_functions_exist = True
        
        for func_name in expected_functions:
            if hasattr(service, func_name):
                print(f"✓ {func_name} available")
            else:
                print(f"✗ {func_name} missing")
                all_functions_exist = False
        
        for alias_name in compatibility_aliases:
            if hasattr(service, alias_name):
                print(f"✓ {alias_name} alias available")
            else:
                print(f"✗ {alias_name} alias missing")
                all_functions_exist = False
                
        return all_functions_exist
        
    except Exception as e:
        print(f"✗ Function availability test failed: {e}")
        return False

def run_all_tests():
    """Run all structural tests"""
    print("🧪 Docling Migration Structural Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    all_passed &= test_file_structure()
    print()
    all_passed &= test_requirements()
    print() 
    all_passed &= test_import_structure()
    print()
    all_passed &= test_function_availability()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All structural tests passed!")
        print("📋 Migration status:")
        print("  • ✅ File structure is correct")
        print("  • ✅ Requirements updated with Docling")  
        print("  • ✅ Modules import without errors")
        print("  • ✅ All expected functions are available")
        print("  • ✅ Backward compatibility maintained")
        print("\n🚀 Ready for integration testing with dependencies!")
    else:
        print("⚠️  Some structural tests failed.")
        print("Please check the output above for details.")
        
    return all_passed

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n🚨 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)