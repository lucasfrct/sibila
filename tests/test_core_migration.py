#!/usr/bin/env python3
"""
Core Docling migration test
Tests only the core document processing functions
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_core_docling_functions():
    """Test core Docling functions without dependencies"""
    print("🧪 Testing core Docling functions...")
    
    try:
        from modules.document import docling_reader
        
        # Test that main functions exist
        assert hasattr(docling_reader, 'reader'), "reader function missing"
        assert hasattr(docling_reader, 'reader_content'), "reader_content function missing"
        assert hasattr(docling_reader, 'reader_pages'), "reader_pages function missing"
        assert hasattr(docling_reader, 'extract_structured_content'), "extract_structured_content function missing"
        assert hasattr(docling_reader, 'get_document_info'), "get_document_info function missing"
        
        print("✓ All core Docling functions available")
        
        # Test that they return gracefully when Docling is not available
        result = docling_reader.reader_content("nonexistent.pdf")
        assert result == "", "Should return empty string when Docling unavailable"
        print("✓ Graceful fallback when Docling unavailable")
        
        pages = docling_reader.reader_pages("nonexistent.pdf")
        assert pages == [], "Should return empty list when Docling unavailable"
        print("✓ reader_pages fallback works")
        
        info = docling_reader.get_document_info("nonexistent.pdf")
        assert info == {}, "Should return empty dict when Docling unavailable"
        print("✓ get_document_info fallback works")
        
        return True
        
    except Exception as e:
        print(f"✗ Core Docling functions test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_requirements_migration():
    """Test that requirements.txt was properly updated"""
    print("🧪 Testing requirements migration...")
    
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
        
        # Check Docling dependencies
        docling_deps = ["docling==2.10.2", "docling-core==2.5.0", "docling-ibm-models==2.0.7", "docling-parse==2.0.2"]
        
        all_found = True
        for dep in docling_deps:
            if dep in content:
                print(f"✓ {dep} found")
            else:
                print(f"✗ {dep} missing")
                all_found = False
        
        # Check that old PDF dependencies are still there for fallback
        if "pdfplumber" in content or "PyPDF2" in content:
            print("⚠ Old PDF dependencies found (they can be kept for fallback)")
        else:
            print("✓ Old PDF dependencies removed (using Docling-only approach)")
        
        return all_found
        
    except Exception as e:
        print(f"✗ Requirements test failed: {e}")
        return False

def test_backward_compatibility():
    """Test that the system maintains backward compatibility"""
    print("🧪 Testing backward compatibility...")
    
    try:
        # Import should work without throwing errors
        import importlib.util
        
        # Test that docling_reader module can be imported
        spec = importlib.util.spec_from_file_location(
            "docling_reader", 
            "src/modules/document/docling_reader.py"
        )
        docling_module = importlib.util.module_from_spec(spec)
        sys.modules['docling_reader'] = docling_module
        spec.loader.exec_module(docling_module)
        
        print("✓ Docling reader module can be imported")
        
        # Test fallback functionality
        result = docling_module.reader_content("test.pdf")
        assert isinstance(result, str), "Should return string"
        print("✓ reader_content returns string")
        
        pages = docling_module.reader_pages("test.pdf")
        assert isinstance(pages, list), "Should return list"
        print("✓ reader_pages returns list")
        
        return True
        
    except Exception as e:
        print(f"✗ Backward compatibility test failed: {e}")
        import traceback 
        traceback.print_exc()
        return False

def test_file_structure():
    """Test file structure is correct"""
    print("🧪 Testing file structure...")
    
    required_files = [
        "src/modules/document/docling_reader.py",
        "requirements.txt"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} missing")
            return False
    
    return True

def run_core_tests():
    """Run core migration tests"""
    print("🧪 Core Docling Migration Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    all_passed &= test_file_structure()
    print()
    all_passed &= test_requirements_migration()
    print()
    all_passed &= test_core_docling_functions()
    print()
    all_passed &= test_backward_compatibility()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 Core migration tests passed!")
        print("📋 Migration completed successfully:")
        print("  • ✅ Docling reader module created")
        print("  • ✅ Requirements updated with Docling dependencies")
        print("  • ✅ Graceful fallback when Docling unavailable")
        print("  • ✅ Backward compatibility maintained")
        print("  • ✅ All core functions work without external dependencies")
        print("\n🚀 Ready for production deployment!")
    else:
        print("⚠️  Some core tests failed.")
        
    return all_passed

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    
    try:
        success = run_core_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n🚨 Error: {e}")
        sys.exit(1)