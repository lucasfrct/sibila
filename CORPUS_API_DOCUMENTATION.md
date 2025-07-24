# Corpus API Enhancement Documentation

## Enhanced Article Extraction API

The corpus module has been enhanced with improved article extraction capabilities specifically designed for Brazilian legal documents.

### New API Parameters

#### `/api/v1/corpus/generate` (POST)

Enhanced parameters for better precision:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | string | required | Path to the document file |
| `page_start` | integer | 1 | Starting page for extraction |
| `page_end` | integer | -1 | Ending page (-1 = last page) |
| `use_filters` | boolean | true | Enable enhanced filtering for precision |
| `min_length` | integer | 50 | Minimum article length in characters |
| `extract_components` | boolean | false | Extract structural components (paragraphs, items, etc.) |

### Example API Calls

#### Basic enhanced extraction:
```bash
POST /api/v1/corpus/generate?path=/path/to/document.pdf&use_filters=true
```

#### With component extraction:
```bash
POST /api/v1/corpus/generate?path=/path/to/document.pdf&extract_components=true&min_length=100
```

#### Custom page range with filters:
```bash
POST /api/v1/corpus/generate?path=/path/to/document.pdf&page_start=10&page_end=50&use_filters=true&min_length=200
```

### Enhanced Response Format

```json
{
  "status": 201,
  "data": {
    "document_info": {
      "path": "/path/to/document.pdf",
      "name": "document.pdf",
      "pages": 100,
      "total_articles": 45
    },
    "processing_info": {
      "filters_used": true,
      "components_extracted": true,
      "min_length_filter": 50,
      "filtered": true,
      "original_count": 52
    },
    "annotations": [
      {
        "text": "Art. 1º Complete article text...",
        "subject": "Article Title",
        "components": {
          "caput": "Art. 1º Main article content",
          "paragraphs": [
            "§ 1º First paragraph content",
            "§ 2º Second paragraph content"
          ],
          "items": [
            "I - First item",
            "II - Second item"
          ],
          "subitems": [
            "a) First subitem",
            "b) Second subitem"
          ],
          "full_text": "Complete article text..."
        }
      }
    ]
  }
}
```

## Code Usage Examples

### Basic Enhanced Extraction

```python
from src.modules.corpus import corpus

# Enhanced extraction with default settings
doc = corpus.doc_with_articles(path, use_enhanced=True)
```

### Filtered Extraction

```python
# With filtering for better precision
doc = corpus.doc_with_articles_filtered(
    path="document.pdf",
    min_article_length=100,
    filter_empty=True
)
```

### Component Extraction

```python
from src.modules.analysis import legislation

# Extract article components
article_text = "Art. 1º Sample article..."
components = legislation.extract_article_components(article_text)

print(f"Caput: {components['caput']}")
print(f"Paragraphs: {len(components['paragraphs'])}")
print(f"Items: {len(components['items'])}")
```

### Enhanced Article Splitting

```python
# Use Docling-enhanced extraction when available
articles = legislation.split_into_articles_enhanced(
    text=document_content,
    document_path="path/to/source.pdf"
)
```

## Legal Document Structure Support

The enhanced extraction now properly handles Brazilian legal document formatting:

### Article Formats
- `Art. 1º` - Standard format with ordinal
- `Art. 2°` - Alternative ordinal symbol
- `Art. 3o` - Simple ordinal
- `Artigo 4º` - Full word format

### Structural Components
- **Caput**: Main article content
- **Paragraphs**: `§ 1º`, `§ 2º`, `Parágrafo único`
- **Items**: `I -`, `II -`, `III -`, etc.
- **Subitems**: `a)`, `b)`, `c)`, etc.

### Extraction Quality Improvements

1. **Complete Article Capture**: Extracts entire article content including all subsections
2. **Precise Boundaries**: Correctly identifies where one article ends and another begins
3. **Hierarchical Structure**: Maintains the relationship between paragraphs, items, and subitems
4. **Filtering Options**: Removes incomplete or malformed extractions
5. **Docling Integration**: Uses advanced document analysis when available

## Backward Compatibility

All existing API calls continue to work without modification. New parameters are optional and default to maintaining current behavior.

## Migration Guide

### From Basic to Enhanced Extraction

```python
# Before
articles = legislation.split_into_articles(text)

# After (with fallback)
if hasattr(legislation, 'split_into_articles_enhanced'):
    articles = legislation.split_into_articles_enhanced(text, document_path)
else:
    articles = legislation.split_into_articles(text)
```

### API Parameter Migration

```bash
# Before
POST /api/v1/corpus/generate?path=/doc.pdf

# After (enhanced)
POST /api/v1/corpus/generate?path=/doc.pdf&use_filters=true&extract_components=true
```