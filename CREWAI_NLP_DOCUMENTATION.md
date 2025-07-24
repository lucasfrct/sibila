# Documentação: Integração CrewAI no Módulo NLP

## Visão Geral

Esta documentação descreve a integração do CrewAI no módulo NLP do projeto Sibila, que permite o uso de agentes inteligentes para processamento de linguagem natural em documentos legais.

## Estrutura da Integração

### Módulos Principais

1. **`crewai_integration.py`** - Implementação principal dos agentes e workflows
2. **`crewai_config.py`** - Configurações e definições dos agentes
3. **`crewai_pipeline.py`** - Pipelines avançados para processamento complexo

### Ferramentas (Tools) Disponíveis

#### 1. Enhanced Sentiment Analysis Tool
```python
enhanced_sentiment_analysis_tool(text: str) -> str
```
- **Função**: Análise abrangente de sentimentos em textos legais
- **Entrada**: Texto para análise
- **Saída**: JSON com análise completa (sentimento, emoções, intensidade, confiança)

#### 2. Legal Document Classification Tool
```python
legal_document_classification_tool(text: str, classification_type: str) -> str
```
- **Função**: Classificação de documentos legais por tipo
- **Tipos suportados**: subject, article_type, legal_intention, legal_category, normative_type
- **Saída**: JSON com resultado da classificação

#### 3. Comprehensive Legal Analysis Tool
```python
comprehensive_legal_analysis_tool(text: str) -> str
```
- **Função**: Análise legal completa combinando múltiplas classificações
- **Saída**: JSON com todas as classificações disponíveis

#### 4. Text Preprocessing Tool
```python
text_preprocessing_tool(text: str, operations: str) -> str
```
- **Função**: Pré-processamento de texto
- **Operações**: clean, normalize, lowercase, remove_numbers
- **Saída**: JSON com texto processado

### Agentes CrewAI

#### 1. Analista de Sentimentos (Sentiment Agent)
- **Papel**: Especialista em análise de sentimentos para textos legais
- **Ferramentas**: enhanced_sentiment_analysis_tool, text_preprocessing_tool
- **Expertise**: Detecção de emoções, análise de subjetividade, sentimentos baseados em aspectos

#### 2. Classificador Legal (Legal Classifier Agent)
- **Papel**: Especialista em classificação de documentos jurídicos
- **Ferramentas**: legal_document_classification_tool, comprehensive_legal_analysis_tool
- **Expertise**: Classificação por área do direito, tipo normativo, hierarquia legal

#### 3. Analisador de Texto (Text Analyzer Agent)
- **Papel**: Especialista em análise estrutural e semântica
- **Ferramentas**: Todas as ferramentas + FileReadTool, FileWriterTool
- **Expertise**: Análise sintática, extração de entidades, análise de coesão

### Workflows Disponíveis

#### 1. Sentiment Analysis Workflow
```python
sentiment_analysis_workflow(text: str) -> Dict[str, Any]
```
- **Objetivo**: Análise completa de sentimentos usando agentes CrewAI
- **Agente**: Sentiment Agent
- **Duração**: ~30 segundos

#### 2. Legal Document Analysis Workflow
```python
legal_document_analysis_workflow(text: str) -> Dict[str, Any]
```
- **Objetivo**: Análise abrangente de documentos legais
- **Agentes**: Legal Classifier Agent + Text Analyzer Agent
- **Duração**: ~60 segundos

#### 3. Comprehensive NLP Workflow
```python
comprehensive_nlp_workflow(text: str) -> Dict[str, Any]
```
- **Objetivo**: Análise completa combinando múltiplas dimensões
- **Agentes**: Todos os agentes disponíveis
- **Duração**: ~120 segundos

### Pipelines Avançados

#### 1. Legal Document Comprehensive Pipeline
- **ID**: `legal_document_comprehensive`
- **Tarefas**: 6 (preprocessing → identification → classification → sentiment → structure → synthesis)
- **Complexidade**: Alta
- **Duração estimada**: 10 minutos

#### 2. Batch Processing Optimized Pipeline
- **ID**: `batch_processing_optimized`
- **Tarefas**: 4 (batch_preprocessing → parallel_classification → quality_assessment → summary)
- **Complexidade**: Média
- **Duração estimada**: 5 minutos por lote

## Como Usar

### Configuração Inicial

1. **Instalar dependências**:
```bash
pip install crewai crewai-tools textblob vaderSentiment nltk scikit-learn
```

2. **Configurar variáveis de ambiente** (opcional):
```bash
export OPENAI_API_KEY="sua_chave_aqui"
export CREWAI_MODEL="gpt-3.5-turbo"
export CREWAI_TEMPERATURE="0.1"
```

### Uso Básico das Ferramentas

```python
from src.modules.nlp import (
    enhanced_sentiment_analysis_tool,
    legal_document_classification_tool,
    comprehensive_legal_analysis_tool,
    text_preprocessing_tool
)

# Análise de sentimentos
texto = "Art. 1º É livre a manifestação do pensamento."
resultado = enhanced_sentiment_analysis_tool._run(texto)
print(resultado)

# Classificação legal
resultado = legal_document_classification_tool._run(texto, "subject")
print(resultado)

# Pré-processamento
resultado = text_preprocessing_tool._run(texto, "clean,normalize")
print(resultado)
```

### Uso dos Workflows

```python
from src.modules.nlp import analyze_text_with_crewai

# Análise de sentimentos com CrewAI
resultado = analyze_text_with_crewai(texto, "sentiment")

# Análise legal completa
resultado = analyze_text_with_crewai(texto, "legal")

# Análise abrangente
resultado = analyze_text_with_crewai(texto, "comprehensive")
```

### Uso dos Pipelines

```python
from src.modules.nlp import (
    execute_legal_document_pipeline,
    execute_batch_processing_pipeline,
    get_available_pipelines
)

# Ver pipelines disponíveis
pipelines = get_available_pipelines()
print(pipelines.keys())

# Executar pipeline de documento legal
documento = "LEI Nº 12.965, DE 23 DE ABRIL DE 2014..."
resultado = execute_legal_document_pipeline(documento)

# Executar pipeline em lote
documentos = [{"text": doc1}, {"text": doc2}]
resultado = execute_batch_processing_pipeline(documentos)
```

## Compatibilidade

### Backwards Compatibility
A integração CrewAI mantém total compatibilidade com as funcionalidades existentes:

```python
# Funcionalidades antigas continuam funcionando
from src.modules.nlp import (
    classifier,
    sentiment_analysis_enhanced,
    get_classifier,
    SimpleLegalClassifier
)

# Novas funcionalidades CrewAI
from src.modules.nlp import (
    create_nlp_crew,
    analyze_text_with_crewai,
    CrewAIPipelineManager
)
```

### Verificação de Disponibilidade
```python
from src.modules.nlp import CREWAI_AVAILABLE

if CREWAI_AVAILABLE:
    # Usar funcionalidades CrewAI
    from src.modules.nlp import crewai_sentiment_analysis
    resultado = crewai_sentiment_analysis(texto)
else:
    # Usar funcionalidades tradicionais
    from src.modules.nlp import sentiment_analysis_enhanced
    resultado = sentiment_analysis_enhanced(texto)
```

## Configuração Avançada

### Personalização de Agentes

```python
from src.modules.nlp.crewai_integration import CrewAINLPConfiguration

# Configuração personalizada
config = CrewAINLPConfiguration()
config.llm_config["model"] = "gpt-4"
config.llm_config["temperature"] = 0.2

# Customizar papel do agente
config.sentiment_agent_config["backstory"] = "Seu backstory personalizado..."
```

### Monitoramento e Logging

```python
from src.modules.nlp import create_pipeline_manager

manager = create_pipeline_manager()

# Executar pipeline
resultado = manager.execute_pipeline(config, input_data)

# Ver histórico
historico = manager.get_pipeline_history()

# Ver estatísticas
stats = manager.get_pipeline_statistics()
print(f"Taxa de sucesso: {stats['success_rate']}%")
```

## Limitações e Considerações

### Limitações Atuais
1. **Modelos de classificação**: Usam dados sintéticos para treinamento inicial
2. **Dependência de LLM**: Workflows completos requerem API key (OpenAI/outros)
3. **Performance**: Pipelines complexos podem ser lentos sem configuração otimizada

### Considerações de Produção
1. **Rate Limiting**: Configure limites adequados para APIs de LLM
2. **Caching**: Habilite cache para melhorar performance
3. **Monitoring**: Implemente monitoramento para pipelines longos
4. **Error Handling**: Pipelines incluem tratamento de erro e fallbacks

## Exemplos Completos

### Exemplo 1: Análise Simples
```python
import json
from src.modules.nlp import enhanced_sentiment_analysis_tool

texto = "A violação desta norma resultará em multa severa."
resultado = enhanced_sentiment_analysis_tool._run(texto)
data = json.loads(resultado)

print(f"Sentimento: {data['basic_sentiment']['classification']}")
print(f"Polaridade: {data['basic_sentiment']['polarity']}")
print(f"Emoção: {data['emotions']['dominant_emotion']}")
```

### Exemplo 2: Pipeline Completo
```python
from src.modules.nlp import execute_legal_document_pipeline

documento = """
LEI Nº 13.709, DE 14 DE AGOSTO DE 2018.
Lei Geral de Proteção de Dados Pessoais (LGPD)

Art. 1º Esta Lei dispõe sobre o tratamento de dados pessoais...
"""

resultado = execute_legal_document_pipeline(documento)
print(f"Status: {resultado.status}")
print(f"Tempo de execução: {resultado.execution_time:.2f}s")
print(f"Resultado: {resultado.output_data}")
```

### Exemplo 3: Workflow Personalizado
```python
from src.modules.nlp.crewai_integration import CrewAINLPWorkflows

workflows = CrewAINLPWorkflows()
resultado = workflows.comprehensive_nlp_workflow(texto)

print(f"Workflow: {resultado['workflow']}")
print(f"Status: {resultado['status']}")
```

## Troubleshooting

### Problemas Comuns

1. **ImportError: No module named 'crewai'**
   - Solução: `pip install crewai crewai-tools`

2. **"Tool object is not callable"**
   - Solução: Use `tool._run(args)` em vez de `tool(args)`

3. **Erro de treinamento do classificador**
   - Esperado: Classificadores usam dados sintéticos iniciais
   - Solução: Configure dados de treinamento reais para produção

4. **Timeout em workflows**
   - Solução: Aumente timeout ou configure OpenAI API key

### Logs e Debugging

```python
import logging
logging.basicConfig(level=logging.INFO)

# Logs detalhados dos agentes
workflows = CrewAINLPWorkflows()
workflows.config.sentiment_agent_config["verbose"] = True
```

## Conclusão

A integração CrewAI no módulo NLP fornece capacidades avançadas de processamento de linguagem natural usando agentes inteligentes, mantendo compatibilidade total com funcionalidades existentes. Esta implementação permite:

- **Análise mais sofisticada** usando múltiplos agentes especializados
- **Workflows complexos** para processamento de documentos legais
- **Pipelines escaláveis** para processamento em lote
- **Extensibilidade** para customizações específicas do domínio

Para uso em produção, recomenda-se configurar adequadamente as APIs de LLM e personalizar os agentes conforme o domínio específico da aplicação.