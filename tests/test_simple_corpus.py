#!/usr/bin/env python3
"""
Simple unit test for legislation article extraction improvements
Tests only the core regex and extraction logic without external dependencies
"""

import re
from typing import List

def split_into_articles_improved(text: str) -> List[str]:
    """
    Improved version of article splitting with enhanced regex patterns.
    This is a standalone version for testing without dependencies.
    """
    
    # Enhanced regex for capturing Brazilian legal articles
    regex = re.compile(r'^\s*(?:Art\.?|Artigo)\s*\d+(?:[ºº°]|o)?\b', re.IGNORECASE | re.MULTILINE)

    articles_raw: List[str] = []
    content_current: List[str] = []

    for line in text.splitlines():
        line_stripped = line.strip()
        
        # Check if line is a new article using regex
        match = regex.match(line)
        if match:
            # If we have accumulated content, add to articles list
            if content_current:
                content_art = '\n'.join(content_current).strip()
                if content_art:  # Only add if not empty
                    articles_raw.append(content_art)
            
            # Start new article
            content_current = [line]
        else:
            # Add line to current article
            content_current.append(line)

    # Add last article if exists
    if content_current:
        content_art = '\n'.join(content_current).strip()
        if content_art:
            articles_raw.append(content_art)

    # Filter only valid articles that start with "Art" or "Artigo"
    articles: List[str] = []
    for article in articles_raw:
        article_clean = article.strip()
        if article_clean and regex.match(article_clean):
            articles.append(article)

    return articles

def test_article_extraction():
    """Test the improved article extraction"""
    print("🧪 Testing improved article extraction...")
    
    # Sample legal text with various formats
    sample_text = """
    Preâmbulo do documento que não é artigo.
    
    Art. 1º Este artigo trata de direitos fundamentais.
    Parágrafo único. Este parágrafo detalha o artigo.
    
    Art. 2º Este é o segundo artigo.
    § 1º Este é o primeiro parágrafo do segundo artigo.
    § 2º Este é o segundo parágrafo com:
    I - primeiro inciso;
    II - segundo inciso;
    III - terceiro inciso com:
    a) primeira alínea;
    b) segunda alínea.
    
    Artigo 3º Este é o terceiro artigo em formato alternativo.
    I - Este artigo também tem incisos;
    II - E mais incisos para testar.
    
    Art. 4o Artigo com ordinal em formato alternativo.
    
    Texto que não é artigo e deve ser ignorado.
    
    Art. 5 Artigo sem ordinal.
    """
    
    articles = split_into_articles_improved(sample_text)
    
    print(f"✓ Extracted {len(articles)} articles")
    
    # Verify we got the expected articles
    expected_count = 5  # Art. 1º, Art. 2º, Artigo 3º, Art. 4o, Art. 5
    if len(articles) == expected_count:
        print(f"✓ Correct number of articles extracted ({expected_count})")
    else:
        print(f"⚠️  Expected {expected_count} articles, got {len(articles)}")
    
    # Check that each article contains its content
    for i, article in enumerate(articles, 1):
        lines = article.split('\n')
        if len(lines) > 1:  # Article should have more than just the header
            print(f"✓ Article {i} contains content ({len(lines)} lines)")
        else:
            print(f"⚠️  Article {i} seems incomplete")
    
    # Test specific patterns
    article_1 = articles[0] if articles else ""
    if "Parágrafo único" in article_1:
        print("✓ Paragraph extraction works")
    
    article_2 = articles[1] if len(articles) > 1 else ""
    if "§ 1º" in article_2 and "§ 2º" in article_2:
        print("✓ Multiple paragraph extraction works")
    
    if "I -" in article_2 and "II -" in article_2:
        print("✓ Item extraction works")
    
    if "a)" in article_2 and "b)" in article_2:
        print("✓ Subitem extraction works")
    
    return len(articles) == expected_count

def extract_article_components_test(article_text: str) -> dict:
    """
    Test version of component extraction.
    """
    
    components = {
        'caput': '',
        'paragraphs': [],  # Paragraphs (§)
        'items': [],       # Items (I, II, III)
        'subitems': [],    # Subitems (a, b, c)
        'full_text': article_text
    }
    
    lines = article_text.split('\n')
    current_section = 'caput'
    current_content = []
    
    # Regex to identify different components
    paragraph_regex = re.compile(r'^\s*§\s*\d+[ºº°]?', re.IGNORECASE)
    paragraph_unique_regex = re.compile(r'^\s*Parágrafo\s+único', re.IGNORECASE)
    item_regex = re.compile(r'^\s*[IVX]+\s*[-–]', re.IGNORECASE)
    subitem_regex = re.compile(r'^\s*[a-z]\)\s*', re.IGNORECASE)
    
    for line in lines:
        line_stripped = line.strip()
        
        if paragraph_regex.match(line_stripped) or paragraph_unique_regex.match(line_stripped):
            # Save previous section
            if current_content:
                content = '\n'.join(current_content).strip()
                if current_section == 'caput':
                    components['caput'] = content
                elif current_section == 'paragraph':
                    components['paragraphs'].append(content)
                elif current_section == 'item':
                    components['items'].append(content)
                elif current_section == 'subitem':
                    components['subitems'].append(content)
            
            # Start new paragraph
            current_section = 'paragraph'
            current_content = [line]
            
        elif item_regex.match(line_stripped):
            # Save previous section
            if current_content:
                content = '\n'.join(current_content).strip()
                if current_section == 'caput':
                    components['caput'] = content
                elif current_section == 'paragraph':
                    components['paragraphs'].append(content)
                elif current_section == 'item':
                    components['items'].append(content)
                elif current_section == 'subitem':
                    components['subitems'].append(content)
            
            # Start new item
            current_section = 'item'
            current_content = [line]
            
        elif subitem_regex.match(line_stripped):
            # Save previous section
            if current_content:
                content = '\n'.join(current_content).strip()
                if current_section == 'caput':
                    components['caput'] = content
                elif current_section == 'paragraph':
                    components['paragraphs'].append(content)
                elif current_section == 'item':
                    components['items'].append(content)
                elif current_section == 'subitem':
                    components['subitems'].append(content)
            
            # Start new subitem
            current_section = 'subitem'
            current_content = [line]
            
        else:
            # Continue current section
            current_content.append(line)
    
    # Save last section
    if current_content:
        content = '\n'.join(current_content).strip()
        if current_section == 'caput':
            components['caput'] = content
        elif current_section == 'paragraph':
            components['paragraphs'].append(content)
        elif current_section == 'item':
            components['items'].append(content)
        elif current_section == 'subitem':
            components['subitems'].append(content)
    
    return components

def test_component_extraction():
    """Test article component extraction"""
    print("🧪 Testing component extraction...")
    
    sample_article = """Art. 2º Este é o segundo artigo.
§ 1º Este é o primeiro parágrafo do segundo artigo.
§ 2º Este é o segundo parágrafo com:
I - primeiro inciso;
II - segundo inciso;
III - terceiro inciso com:
a) primeira alínea;
b) segunda alínea."""
    
    components = extract_article_components_test(sample_article)
    
    # Check components
    if components['caput']:
        print("✓ Caput extracted")
    else:
        print("⚠️  Caput not found")
    
    if len(components['paragraphs']) == 2:
        print(f"✓ Correct number of paragraphs extracted ({len(components['paragraphs'])})")
    else:
        print(f"⚠️  Expected 2 paragraphs, got {len(components['paragraphs'])}")
    
    if len(components['items']) == 3:
        print(f"✓ Correct number of items extracted ({len(components['items'])})")
    else:
        print(f"⚠️  Expected 3 items, got {len(components['items'])}")
    
    if len(components['subitems']) == 2:
        print(f"✓ Correct number of subitems extracted ({len(components['subitems'])})")
    else:
        print(f"⚠️  Expected 2 subitems, got {len(components['subitems'])}")
    
    return (len(components['paragraphs']) == 2 and 
            len(components['items']) == 3 and 
            len(components['subitems']) == 2)

def run_simple_tests():
    """Run simple tests without external dependencies"""
    print("🧪 Simple Corpus Improvements Test")
    print("=" * 40)
    
    test1_passed = test_article_extraction()
    test2_passed = test_component_extraction()
    
    print("\n" + "=" * 40)
    if test1_passed and test2_passed:
        print("🎉 All simple tests passed!")
        print("📋 Core improvements verified:")
        print("  • Enhanced regex patterns work correctly")
        print("  • Complete article extraction with content")
        print("  • Component extraction (paragraphs, items, subitems)")
        print("  • Proper handling of Brazilian legal formatting")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        
    return test1_passed and test2_passed

if __name__ == "__main__":
    try:
        success = run_simple_tests()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n🚨 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)