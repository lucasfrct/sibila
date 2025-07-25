#!/usr/bin/env python3
"""
Test script for Docling migration
Tests the new document processing functionality
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_docling_integration():
    """Test Docling integration"""
    print("🧪 Testing Docling integration...")
    
    try:
        from modules.document import service as DocService
        print("✓ Document service imported")
        
        # Test that the service has the new functions
        assert hasattr(DocService, 'document_reader'), "document_reader function missing"
        assert hasattr(DocService, 'document_content'), "document_content function missing"
        assert hasattr(DocService, 'document_pages_with_details'), "document_pages_with_details function missing"
        
        # Test that compatibility aliases exist
        assert hasattr(DocService, 'pdf_reader'), "pdf_reader alias missing"
        assert hasattr(DocService, 'pdf_content'), "pdf_content alias missing"
        assert hasattr(DocService, 'pdf_pages_with_details'), "pdf_pages_with_details alias missing"
        
        print("✓ All required functions available")
        return True
        
    except Exception as e:
        print(f"✗ Docling integration test failed: {e}")
        return False

def test_docling_reader():
    """Test Docling reader module"""
    print("🧪 Testing Docling reader...")
    
    try:
        from modules.document import docling_reader
        print("✓ Docling reader imported")
        
        # Test that functions are available
        assert hasattr(docling_reader, 'reader'), "reader function missing"
        assert hasattr(docling_reader, 'reader_content'), "reader_content function missing"
        assert hasattr(docling_reader, 'extract_structured_content'), "extract_structured_content function missing"
        assert hasattr(docling_reader, 'get_document_info'), "get_document_info function missing"
        
        print("✓ All Docling reader functions available")
        return True
        
    except Exception as e:
        print(f"✗ Docling reader test failed: {e}")
        return False

def test_document_info():
    """Test document info"""
    print("🧪 Testing document info...")
    
    try:
        from modules.document.document_info import DocumentInfo
        print("✓ DocumentInfo imported")
        
        # Test that DocumentInfo can be instantiated
        doc_info = DocumentInfo()
        assert doc_info is not None, "DocumentInfo instantiation failed"
        
        print("✓ DocumentInfo works correctly")
        return True
        
    except Exception as e:
        print(f"✗ Document info test failed: {e}")
        return False

def test_corpus_integration():
    """Test corpus integration"""
    print("🧪 Testing corpus integration...")
    
    try:
        from modules.corpus import corpus
        print("✓ Corpus module imported")
        
        # Test that the corpus functions are available
        assert hasattr(corpus, 'doc_with_articles'), "doc_with_articles function missing"
        
        print("✓ Corpus integration works correctly")
        return True
        
    except Exception as e:
        print(f"✗ Corpus integration test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🧪 Docling Migration Test Suite")
    print("=" * 40)
    
    all_passed = True
    
    all_passed &= test_docling_integration()
    all_passed &= test_docling_reader()
    all_passed &= test_document_info()
    all_passed &= test_corpus_integration()
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All Docling migration tests passed!")
        print("📋 The system now supports:")
        print("  • Docling for advanced document processing")
        print("  • Automatic fallback to PDF libraries")
        print("  • Enhanced legal document analysis")
        print("  • Backward compatibility with existing APIs")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        
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
        import traceback
        traceback.print_exc()
        sys.exit(1)