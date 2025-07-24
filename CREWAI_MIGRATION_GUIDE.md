# Migração para CrewAI - Análise Jurídica

Este documento detalha a transformação do módulo de análise jurídica para usar agentes CrewAI especializados.

## Visão Geral da Transformação

### Antes: Abordagem Tradicional
- Chamadas diretas ao modelo Ollama local
- Funções isoladas sem coordenação
- Processamento sequencial simples
- Sem especialização por domínio jurídico

### Depois: Abordagem CrewAI
- Agentes especializados por área jurídica
- Coordenação inteligente entre agentes
- Ferramentas reutilizáveis e modulares
- Processamento colaborativo
- Integração com modelos OpenAI (GPT-3.5/4)

## Arquitetura dos Agentes

### 1. Legal Context Analyst
**Função**: Extração de contexto jurídico abrangente
- **Ferramentas**: LegalContextExtractionTool, ConstitutionalRetrievalTool
- **Especialização**: Identificação de entidades, ações jurídicas, pontos críticos

### 2. Legal Subject Matter Expert
**Função**: Análise e síntese do assunto jurídico principal
- **Ferramentas**: SubjectSynthesisTool, StructuredSummaryTool
- **Especialização**: Síntese de assuntos, resumos estruturados

### 3. Legal Document Structure Analyst
**Função**: Análise de estrutura e artigos individuais
- **Ferramentas**: DocumentArticleAnalysisTool
- **Especialização**: Decomposição estrutural de documentos

### 4. Legal Examiner and Question Generator
**Função**: Geração de perguntas e condução de exames jurídicos
- **Ferramentas**: QuestionGenerationTool, QuestionAnsweringTool
- **Especialização**: Criação de questionários e avaliações

### 5. Senior Legal Assessment Coordinator
**Função**: Coordenação e avaliação geral (Orquestrador Principal)
- **Ferramentas**: LegalAssessmentTool
- **Especialização**: Integração de análises e avaliação final

## Ferramentas Transformadas

### LegalContextExtractionTool
```python
# Entrada: Texto jurídico (string)
# Saída: JSON com contexto estruturado
{
    "success": true,
    "context": {
        "names": ["entidades", "pessoas", "órgãos"],
        "actions": ["ações jurídicas"],
        "deductions": ["deduções legais"],
        "events": ["eventos importantes"],
        "attention_points": ["pontos críticos"],
        "legal_terms": ["termos jurídicos"],
        "dates_deadlines": ["datas e prazos"],
        "penalties": ["penalidades"]
    }
}
```

### SubjectSynthesisTool
```python
# Entrada: Texto jurídico (string)
# Saída: JSON com síntese do assunto
{
    "success": true,
    "synthesis": "Síntese clara e objetiva do assunto principal"
}
```

### StructuredSummaryTool
```python
# Entrada: Texto jurídico (string), análise de artigos (JSON opcional)
# Saída: JSON com resumo estruturado
{
    "success": true,
    "summary": "Resumo hierárquico organizado por seções"
}
```

### DocumentArticleAnalysisTool
```python
# Entrada: Texto jurídico (string), caminho do documento (opcional)
# Saída: JSON com análise de artigos
{
    "success": true,
    "articles_count": 5,
    "articles": [
        {
            "article_number": 1,
            "title": "Título do artigo",
            "category": "Categoria jurídica",
            "summary": "Resumo do artigo",
            "normative_type": "Tipo normativo"
        }
    ]
}
```

## Como Usar

### Configuração
```bash
# Instalar dependências
pip install crewai==0.86.0 crewai-tools==0.17.0

# Configurar chave da OpenAI
export OPENAI_API_KEY="sua-chave-da-openai"
```

### Uso Básico
```python
from src.modules.analysis import crewai_enhanced_legal_document_analysis

# Análise completa com CrewAI
resultado = crewai_enhanced_legal_document_analysis(
    document_text="Texto do documento jurídico...",
    openai_api_key="sua-chave-api"  # Opcional se configurada no ambiente
)

print(resultado["comprehensive_analysis"])
```

### Uso Avançado
```python
from src.modules.analysis import LegalAnalysisCrewManager

# Criar gerenciador de agentes
manager = LegalAnalysisCrewManager(
    openai_api_key="sua-chave-api",
    model_name="gpt-4"  # ou "gpt-3.5-turbo"
)

# Análise completa
analise = manager.analyze_legal_document(
    document_text="Texto jurídico...",
    document_path="/caminho/para/documento.pdf"
)

# Geração de questionário
questionario = manager.generate_legal_questions(
    document_text="Texto jurídico...",
    mode="questionnaire"
)

# Resposta a pergunta específica
resposta = manager.answer_legal_question(
    question="Qual o objetivo principal desta lei?",
    documents="Documentos de suporte...",
    article="Artigo específico..."
)
```

## Compatibilidade com Sistema Existente

### Funções Mantidas (Retrocompatibilidade)
```python
# Funções tradicionais ainda funcionam
from src.modules.analysis import (
    enhanced_legal_document_analysis,  # Versão original
    examining_board,                   # Módulo original
    legislation                        # Módulo original
)

# Novas funções CrewAI
from src.modules.analysis import (
    crewai_enhanced_legal_document_analysis,  # Nova versão CrewAI
    LegalAnalysisCrewManager                  # Gerenciador de agentes
)
```

### Verificação de Disponibilidade
```python
from src.modules.analysis import (
    ENHANCED_ANALYSIS_AVAILABLE,    # Análise tradicional disponível
    CREWAI_ANALYSIS_AVAILABLE,      # CrewAI disponível
    LEGACY_ANALYSIS_AVAILABLE       # Módulos legados disponíveis
)

if CREWAI_ANALYSIS_AVAILABLE:
    # Usar CrewAI
    resultado = crewai_enhanced_legal_document_analysis(texto)
elif ENHANCED_ANALYSIS_AVAILABLE:
    # Fallback para análise tradicional
    resultado = enhanced_legal_document_analysis(texto)
else:
    # Análise básica ou erro
    print("Nenhum sistema de análise disponível")
```

## Fluxo de Trabalho dos Agentes

### Processo Sequencial
1. **Context Analyst** → Extrai contexto jurídico estruturado
2. **Subject Expert** → Gera síntese e resumo estruturado
3. **Structure Analyst** → Analisa artigos e estrutura do documento
4. **Legal Examiner** → Cria perguntas e material de exame
5. **Assessment Coordinator** → Integra todas as análises em avaliação final

### Coordenação Inteligente
- Cada agente tem acesso aos resultados dos agentes anteriores
- O coordenador integra todas as análises especializadas
- Processamento paralelo quando possível
- Fallback automático em caso de falha de agentes específicos

## Vantagens da Nova Abordagem

### 1. Especialização por Domínio
- Cada agente é especialista em sua área
- Prompts otimizados para tarefas específicas
- Melhor qualidade de análise

### 2. Modularidade
- Ferramentas reutilizáveis
- Fácil manutenção e extensão
- Testes unitários por ferramenta

### 3. Escalabilidade
- Processamento distribuído
- Integração com diferentes modelos LLM
- Facilidade para adicionar novos agentes

### 4. Robustez
- Tratamento de erros por agente
- Fallback para análise tradicional
- Validação de resultados

## Customização

### Adicionando Novos Agentes
```python
# Exemplo: Agente especializado em contratos
contract_agent = Agent(
    role='Contract Legal Specialist',
    goal='Analyze contractual clauses and obligations',
    backstory="""You are a contract law expert...""",
    tools=[contract_analysis_tool],
    llm=llm
)
```

### Criando Novas Ferramentas
```python
from crewai_tools import BaseTool

class ContractAnalysisTool(BaseTool):
    name: str = "Contract Analysis"
    description: str = "Analyzes contractual clauses..."
    
    def _run(self, contract_text: str) -> str:
        # Implementação da análise
        return json.dumps({"analysis": "..."})
```

## Testes e Validação

### Testes Automatizados
```bash
# Executar testes do CrewAI
python test_crewai_simple.py

# Executar demonstração
python demo_crewai_legal_analysis.py
```

### Validação Manual
```python
# Comparar resultados tradicional vs CrewAI
texto_teste = "Art. 1º Esta lei..."

resultado_tradicional = enhanced_legal_document_analysis(texto_teste)
resultado_crewai = crewai_enhanced_legal_document_analysis(texto_teste)

# Comparar qualidade e completude
```

## Considerações de Performance

### Custos da API
- Uso de tokens OpenAI (GPT-3.5/4)
- Otimização de prompts para reduzir custos
- Cache de resultados quando apropriado

### Tempo de Execução
- Processamento sequencial por padrão
- Possibilidade de paralelização futura
- Timeout configurável por agente

### Monitoramento
- Logs detalhados por agente
- Métricas de uso e performance
- Alertas para falhas de agentes

## Migração Gradual

### Fase 1: Instalação e Configuração ✅
- Instalar CrewAI e dependências
- Configurar ferramentas e agentes
- Testes básicos de funcionamento

### Fase 2: Integração Paralela ✅
- Sistema CrewAI funcionando em paralelo
- Manter sistema tradicional como fallback
- Testes comparativos

### Fase 3: Migração Progressiva (Próxima)
- Migrar casos de uso específicos
- Coletar feedback e ajustar
- Otimizar performance

### Fase 4: Deprecação do Sistema Antigo (Futura)
- Remover dependências do Ollama local
- CrewAI como sistema principal
- Documentação final

## Conclusão

A transformação para CrewAI representa uma evolução significativa na análise jurídica:

- **Maior especialização**: Agentes focados em tarefas específicas
- **Melhor coordenação**: Trabalho colaborativo entre especialistas
- **Maior flexibilidade**: Fácil adição de novas capacidades
- **Melhor manutenibilidade**: Código modular e testável
- **Escalabilidade**: Pronto para crescimento e novas demandas

O sistema mantém compatibilidade com a abordagem anterior enquanto oferece capacidades avançadas através dos agentes especializados CrewAI.