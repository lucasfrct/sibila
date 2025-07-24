# Módulo CrewAI para Análise Legislativa

Este módulo implementa agentes especializados para análise colaborativa de documentos legislativos usando o framework CrewAI, seguindo o padrão do projeto Sibila com documentação em português e estrutura de código em inglês.

## Características Principais

### ✅ Requisitos Atendidos
- **Documentação em Português**: Todas as instruções, comentários e explicações estão em português brasileiro
- **Estrutura em Inglês**: Funções, variáveis e design de código mantidos em inglês
- **Compatibilidade**: Integração com a arquitetura existente do projeto Sibila
- **Robustez**: Tratamento gracioso de dependências ausentes (ollama, textblob, etc.)

### 🤖 Agentes Implementados

#### 1. LegalAnalysisAgent (Agente de Análise Jurídica)
- **Especialização**: Identificação de categorias jurídicas, tipos normativos e entidades legais
- **Funcionalidades**:
  - Classificação de categoria jurídica (Constitucional, Civil, Penal, etc.)
  - Identificação do tipo normativo (Lei, Decreto, Portaria, etc.)
  - Extração de entidades jurídicas relevantes
  - Análise de implicações legais

#### 2. DocumentReviewAgent (Agente de Revisão de Documentos)
- **Especialização**: Verificação de consistência, completude e conformidade estrutural
- **Funcionalidades**:
  - Verificação da estrutura do documento
  - Análise de completude de informações
  - Verificação de consistência interna
  - Avaliação de qualidade geral

#### 3. ComplianceAgent (Agente de Conformidade Regulatória)
- **Especialização**: Verificação de conformidade com normas e regulamentos
- **Funcionalidades**:
  - Verificação de conformidade regulatória
  - Identificação de conflitos legais
  - Detecção de lacunas de conformidade
  - Geração de recomendações

### 🎯 Orquestrador CrewAI

O `CrewAIOrchestrator` coordena o trabalho colaborativo dos agentes, fornecendo:
- Análises coordenadas e abrangentes
- Consolidação de resultados de múltiplos agentes
- Geração de relatórios unificados
- Recomendações prioritárias baseadas em todas as análises

## Uso Básico

```python
from src.modules.analysis.crewai.agents import analyze_legal_document

# Análise completa de um documento
resultado = analyze_legal_document(texto_legislativo, 'completa')

# Análise específica por tipo
resultado_juridico = analyze_legal_document(texto, 'juridica')
resultado_revisao = analyze_legal_document(texto, 'revisao')
resultado_conformidade = analyze_legal_document(texto, 'conformidade')
```

## Uso Avançado

```python
from src.modules.analysis.crewai.agents import (
    LegalAnalysisAgent, 
    DocumentReviewAgent, 
    ComplianceAgent,
    CrewAIOrchestrator
)

# Uso individual dos agentes
agente_juridico = LegalAnalysisAgent()
resultado = agente_juridico.analyze(texto)

# Uso do orquestrador
orquestrador = CrewAIOrchestrator()
analise_completa = orquestrador.analyze_document(texto, 'completa')
```

## Sistema de Fallback

O módulo foi projetado para funcionar mesmo quando dependências externas não estão disponíveis:

### Quando Ollama/LLM não está disponível:
- Análise baseada em palavras-chave e padrões regex
- Classificação por mapeamento de termos jurídicos
- Extração de entidades usando expressões regulares
- Scores de confiança ajustados automaticamente

### Quando CrewAI não está disponível:
- Agentes funcionam independentemente
- Orquestrador usa lógica simples de coordenação
- Funcionalidades básicas mantidas

## Estrutura de Resposta

```python
{
    'agent_name': 'legal_analyst',
    'analysis_type': 'juridica',
    'legal_category': 'Direito Civil',
    'normative_type': 'Lei',
    'legal_entities': ['Ministério da Justiça', 'ANPD'],
    'confidence_score': 0.85,
    'status': 'Análise completa'
}
```

## Extensibilidade

O sistema foi projetado para ser facilmente extensível:
- Novos agentes podem herdar de `BaseAgent`
- Métodos de fallback podem ser personalizados
- Padrões de análise podem ser adicionados
- Integração com outros frameworks é suportada

## Dependências Opcionais

- `crewai`: Framework para agentes colaborativos (opcional)
- `ollama`: Modelos LLM locais (opcional)
- `textblob`: Análise de sentimento (opcional)

O módulo funciona sem essas dependências, com funcionalidade reduzida mas ainda útil.

## Contribuição

Para adicionar novos agentes ou funcionalidades:
1. Herde de `BaseAgent` para novos agentes
2. Implemente métodos de fallback para cenários sem LLM
3. Adicione documentação em português
4. Mantenha estrutura de código em inglês
5. Inclua testes abrangentes

## Licença

Este módulo segue a mesma licença do projeto Sibila principal.