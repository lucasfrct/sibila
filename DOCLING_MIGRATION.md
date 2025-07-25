# Migração para Docling

Este documento descreve a migração do sistema de processamento de documentos do Sibila de bibliotecas PDF tradicionais (pdfplumber, PyPDF2) para o Docling da IBM.

## Visão Geral

O [Docling](https://github.com/DS4SD/docling) é uma biblioteca avançada de processamento de documentos da IBM que oferece:

- Suporte a múltiplos formatos (PDF, Word, PowerPoint, etc.)
- Extração estruturada de conteúdo (textos, tabelas, figuras)
- Análise otimizada para documentos jurídicos
- Detecção avançada de layout e estrutura
- OCR integrado para documentos escaneados
- Melhor precisão na extração de texto

## Mudanças Implementadas

### 1. Novo Módulo Docling Reader (`src/modules/document/docling_reader.py`)

Módulo completamente novo que implementa:

- `reader(path)`: Leitura de documentos usando Docling
- `reader_content(path, init, final)`: Extração de texto completo
- `reader_pages(path, init, final)`: Extração por páginas
- `extract_structured_content(path)`: Extração de conteúdo estruturado específica do Docling
- `get_document_info(path)`: Informações básicas do documento

**Características especiais:**

- Configuração otimizada para documentos jurídicos
- OCR automático para documentos escaneados
- Detecção de estrutura de tabelas
- Fallback gracioso quando Docling não está disponível

### 2. Atualização do Serviço de Documentos (`src/modules/document/service.py`)

O serviço foi atualizado para:

- **Priorizar Docling**: Usa Docling quando disponível
- **Fallback para PDF**: Mantém compatibilidade com bibliotecas PDF
- **Novas funções principais**:
  - `document_reader()` - substitui `pdf_reader()`
  - `document_content()` - substitui `pdf_content()`
  - `document_pages_with_details()` - substitui `pdf_pages_with_details()`
  - `document_paragraphs_with_details()` - substitui `pdf_paragraphs_with_details()`
  - `document_phrases_with_details()` - substitui `pdf_phrases_with_details()`

- **Aliases de compatibilidade**: Todas as funções antigas continuam disponíveis como aliases

### 3. Atualização de Metadados (`src/modules/document/document_info.py`)

- Integração com `get_document_info()` do Docling
- Detecção automática de tipo de documento
- Suporte a formatos além de PDF
- Fallback para método tradicional quando necessário

### 4. Dependências (`requirements.txt`)

Adicionadas as dependências do Docling:

```
docling==2.10.2
docling-core==2.5.0
docling-ibm-models==2.0.7
docling-parse==2.0.2
```

### 5. Atualizações no Corpus (`src/modules/corpus/corpus.py`)

- Função `doc_with_articles()` atualizada para usar as novas funções de documento
- Melhor análise de documentos jurídicos com estruturação Docling

### 6. Rotas Atualizadas (`src/routes/document/document.py`)

- Endpoints atualizados para usar as novas funções
- Mantém a mesma API externa

## Compatibilidade

### Backward Compatibility

- **100% compatível**: Todas as funções existentes continuam funcionando
- **Aliases mantidos**: `pdf_reader`, `pdf_content`, etc. são aliases das novas funções
- **APIs inalteradas**: Interfaces públicas não mudaram

### Fallback Strategy

1. **Docling disponível**: Usa Docling para processamento avançado
2. **Docling indisponível**: Fallback automático para bibliotecas PDF
3. **Sem bibliotecas**: Retorna dados vazios com logs de erro

## Benefícios da Migração

### Para Documentos Jurídicos

- **Melhor extração de estrutura**: Detecta seções, artigos, e hierarquias
- **Tabelas preservadas**: Extração precisa de dados tabulares
- **OCR integrado**: Processa documentos escaneados automaticamente
- **Metadados enriquecidos**: Mais informações sobre o documento

### Para o Sistema

- **Múltiplos formatos**: Suporte nativo a Word, PowerPoint, etc.
- **Performance melhorada**: Processamento mais eficiente
- **Qualidade superior**: Melhor precisão na extração de texto
- **Manutenibilidade**: Menos dependências para gerenciar

## Instalação e Uso

### 1. Instalação

```bash
pip install -r requirements.txt
```

### 2. Uso Básico

```python
from src.modules.document import service as DocService

# Usando as novas funções (recomendado)
content = DocService.document_content("documento.pdf")
pages = DocService.document_pages_with_details("documento.pdf")

# Usando aliases de compatibilidade (ainda funciona)
content = DocService.pdf_content("documento.pdf")
pages = DocService.pdf_pages_with_details("documento.pdf")
```

### 3. Análise Avançada (específica do Docling)

```python
from src.modules.document import docling_reader

# Extração estruturada completa
structured = docling_reader.extract_structured_content("documento.pdf")
print(structured['texts'])   # Textos estruturados
print(structured['tables'])  # Tabelas detectadas
print(structured['titles'])  # Títulos e cabeçalhos
```

## Testes

Execute os testes de migração:

```bash
# Teste estrutural básico
python tests/test_core_migration.py

# Teste completo (requer dependências)
python tests/test_docling_migration.py
```

## Próximos Passos

1. **Teste em produção**: Validar com documentos reais
2. **Otimização**: Ajustar configurações específicas do domínio
3. **Monitoramento**: Acompanhar performance vs. bibliotecas antigas
4. **Treinamento**: Documentar casos de uso avançados

## Troubleshooting

### Docling não instala

```bash
# Verificar versão do Python (requer 3.8+)
python --version

# Instalar dependências do sistema (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install build-essential

# Instalar Docling individualmente
pip install docling
```

### Fallback para PDF

Se Docling não estiver disponível, o sistema automaticamente usa:
- pdfplumber para extração de texto
- PyPDF2 para metadados básicos

### Performance

Para melhor performance com Docling:
- Use documentos de qualidade (não escaneados quando possível)
- Configure OCR apenas quando necessário
- Processe documentos em lotes quando possível

## Conclusão

A migração para Docling representa um upgrade significativo nas capacidades de processamento de documentos do Sibila, especialmente para documentos jurídicos, mantendo total compatibilidade com o código existente.