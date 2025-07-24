# flake8: noqa: E501

"""
ENHANCED LEGAL ANALYSIS MODULE

Este módulo implementa análise jurídica enriquecida que integra com os módulos de
documentos e catálogo para fornecer:
- Síntese do assunto jurídico
- Resumo estruturado das ideias principais
- Memória de contexto para nomes, ações, deduções, relatos de acontecimentos
- Análise abrangente de documentos jurídicos longos

A análise utiliza as capacidades aprimoradas de processamento de documentos e
catalogação para extrair informações estruturadas e metadados relevantes.
"""

import re
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

# Conditional imports with fallbacks
try:
    from src.models.ollama import ModelOllama
    MODEL_AVAILABLE = True
except ImportError:
    MODEL_AVAILABLE = False
    logging.warning("ModelOllama não disponível. Algumas funcionalidades serão limitadas.")

try:
    from src.modules.document import service as DocService
    DOCUMENT_SERVICE_AVAILABLE = True
except ImportError:
    DOCUMENT_SERVICE_AVAILABLE = False
    logging.warning("Document service não disponível.")

try:
    from src.modules.catalog.catalog import Catalog
    CATALOG_AVAILABLE = True
except ImportError:
    CATALOG_AVAILABLE = False
    logging.warning("Catalog service não disponível.")

# Import existing analysis functions
try:
    from src.modules.analysis import legislation as LegislationAnalysis
    LEGISLATION_ANALYSIS_AVAILABLE = True
except ImportError:
    LEGISLATION_ANALYSIS_AVAILABLE = False
    logging.warning("Legislation analysis não disponível.")

@dataclass
class LegalContext:
    """Estrutura para armazenar contexto jurídico extraído"""
    names: List[str]                    # Nomes de pessoas, entidades, órgãos
    actions: List[str]                  # Ações, verbos jurídicos importantes  
    deductions: List[str]               # Deduções e conclusões jurídicas
    events: List[str]                   # Relatos de acontecimentos
    attention_points: List[str]         # Pontos de atenção, alertas
    legal_terms: List[str]              # Termos jurídicos específicos
    dates_deadlines: List[str]          # Datas e prazos relevantes
    penalties: List[str]                # Penalidades mencionadas

@dataclass 
class LegalSynthesis:
    """Estrutura para síntese jurídica completa"""
    subject_synthesis: str              # Síntese do assunto
    structured_summary: str             # Resumo estruturado das ideias principais
    context: LegalContext              # Contexto jurídico extraído
    categories: List[str]               # Categorias jurídicas identificadas
    normative_type: str                 # Tipo normativo identificado
    articles_analysis: List[Dict]       # Análise de artigos individuais
    overall_assessment: str             # Avaliação geral do documento


def check_service_integration() -> Dict[str, bool]:
    """
    Verifica se os serviços de documento e catálogo estão disponíveis para integração.
    
    Returns:
        Dict[str, bool]: Status da disponibilidade de cada serviço
    """
    return {
        'document_service': DOCUMENT_SERVICE_AVAILABLE,
        'catalog_service': CATALOG_AVAILABLE,
        'model_service': MODEL_AVAILABLE,
        'legislation_analysis': LEGISLATION_ANALYSIS_AVAILABLE
    }


def extract_legal_context(text: str) -> LegalContext:
    """
    Extrai contexto jurídico detalhado de um texto, incluindo nomes, ações,
    deduções, eventos e pontos de atenção.
    
    Args:
        text (str): Texto jurídico para análise
        
    Returns:
        LegalContext: Contexto jurídico estruturado extraído
    """
    context = LegalContext(
        names=[], actions=[], deductions=[], events=[],
        attention_points=[], legal_terms=[], dates_deadlines=[], penalties=[]
    )
    
    if not MODEL_AVAILABLE:
        logging.warning("Modelo não disponível para extração de contexto")
        return context
    
    try:
        llm = ModelOllama()
        llm.max_tokens = 300
        llm.temperature = 0.3
        llm.out_focus = 8.0
        
        # Extrair nomes e entidades
        names_prompt = """
        /clear
        Extraia do texto jurídico os nomes de pessoas, empresas, órgãos públicos,
        instituições e outras entidades relevantes.
        """
        names_question = f"""
        Identifique e liste os nomes e entidades presentes no texto: '{text[:2000]}'.
        Retorne apenas os nomes separados por vírgula.
        Se não houver nomes, retorne: '-'
        """
        names_response = llm.question(prompt=names_prompt, question=names_question)
        if names_response and names_response.strip() != '-':
            context.names = [name.strip() for name in names_response.split(',') if name.strip()]
        
        # Extrair ações jurídicas
        actions_prompt = """
        /clear
        Identifique ações, verbos e procedimentos jurídicos mencionados no texto.
        Foque em ações processuais, administrativas e legais.
        """
        actions_question = f"""
        Liste as principais ações jurídicas mencionadas no texto: '{text[:2000]}'.
        Retorne apenas as ações separadas por vírgula.
        Se não houver ações, retorne: '-'
        """
        actions_response = llm.question(prompt=actions_prompt, question=actions_question)
        if actions_response and actions_response.strip() != '-':
            context.actions = [action.strip() for action in actions_response.split(',') if action.strip()]
        
        # Extrair pontos de atenção
        attention_prompt = """
        /clear
        Identifique pontos críticos, alertas, exceções, condições especiais
        e aspectos que requerem atenção especial no texto jurídico.
        """
        attention_question = f"""
        Identifique os principais pontos de atenção no texto: '{text[:2000]}'.
        Retorne apenas os pontos separados por vírgula.
        Se não houver pontos de atenção, retorne: '-'
        """
        attention_response = llm.question(prompt=attention_prompt, question=attention_question)
        if attention_response and attention_response.strip() != '-':
            context.attention_points = [point.strip() for point in attention_response.split(',') if point.strip()]
        
        # Usar funções existentes se disponíveis
        if LEGISLATION_ANALYSIS_AVAILABLE:
            context.legal_terms = _extract_legal_terms_enhanced(text)
            context.dates_deadlines = _extract_dates_enhanced(text)
            context.penalties = _extract_penalties_enhanced(text)
        
    except Exception as e:
        logging.error(f"Erro na extração de contexto jurídico: {e}")
    
    return context


def _extract_legal_terms_enhanced(text: str) -> List[str]:
    """Extrai termos jurídicos usando a função existente com melhorias"""
    try:
        terms_response = LegislationAnalysis.define_the_legal_terms(text)
        if terms_response and terms_response.strip() != '-':
            # Parse the numbered list format
            terms = re.findall(r'\d+\.\s*([^:]+):', terms_response)
            return [term.strip() for term in terms if term.strip()]
    except Exception:
        pass
    return []


def _extract_dates_enhanced(text: str) -> List[str]:
    """Extrai datas e prazos usando a função existente"""
    try:
        dates_response = LegislationAnalysis.extract_legal_dates_and_deadlines(text)
        if dates_response and dates_response.strip() != '-':
            return [date.strip() for date in dates_response.split(',') if date.strip()]
    except Exception:
        pass
    return []


def _extract_penalties_enhanced(text: str) -> List[str]:
    """Extrai penalidades usando a função existente"""
    try:
        penalties_response = LegislationAnalysis.extract_the_penalties(text)
        if penalties_response and penalties_response.strip() != '-':
            return [penalty.strip() for penalty in penalties_response.split(',') if penalty.strip()]
    except Exception:
        pass
    return []


def generate_subject_synthesis(text: str) -> str:
    """
    Gera uma síntese do assunto jurídico principal do texto.
    
    Args:
        text (str): Texto jurídico para síntese
        
    Returns:
        str: Síntese do assunto principal
    """
    if not MODEL_AVAILABLE:
        return "Síntese não disponível - modelo não encontrado"
    
    try:
        llm = ModelOllama()
        llm.max_tokens = 200
        llm.temperature = 0.2
        llm.out_focus = 10.0
        
        prompt = """
        /clear
        Analise o texto jurídico e forneça uma síntese clara e objetiva do
        assunto principal tratado. A síntese deve capturar a essência do
        tema jurídico de forma concisa e precisa.
        """
        
        question = f"""
        Forneça uma síntese objetiva do assunto principal deste texto jurídico: '{text[:1500]}'.
        A síntese deve ter no máximo 3 frases e capturar o tema central.
        Remova textos de saudação ou despedida.
        """
        
        response = llm.question(prompt=prompt, question=question)
        return response.strip() if response else "Síntese não disponível"
        
    except Exception as e:
        logging.error(f"Erro na geração de síntese: {e}")
        return "Erro na geração de síntese"


def generate_structured_summary(text: str, articles_analysis: List[Dict] = None) -> str:
    """
    Gera um resumo estruturado das ideias principais organizadas por seções.
    
    Args:
        text (str): Texto jurídico para resumo
        articles_analysis (List[Dict], optional): Análise de artigos individuais
        
    Returns:
        str: Resumo estruturado das ideias principais
    """
    if not MODEL_AVAILABLE:
        return "Resumo estruturado não disponível - modelo não encontrado"
    
    try:
        llm = ModelOllama()
        llm.max_tokens = 400
        llm.temperature = 0.3
        llm.diversification_rate = 0.1
        
        prompt = """
        /clear
        Crie um resumo estruturado do texto jurídico organizando as ideias
        principais em seções lógicas. O resumo deve ser hierárquico e
        destacar os pontos mais relevantes de cada parte do documento.
        """
        
        # Include articles analysis context if available
        context_info = ""
        if articles_analysis:
            context_info = f"\nInformações dos artigos analisados: {len(articles_analysis)} artigos identificados."
        
        question = f"""
        Crie um resumo estruturado das ideias principais deste texto jurídico: '{text[:1800]}'.
        {context_info}
        Organize em seções com títulos claros.
        Use formato estruturado com tópicos e subtópicos.
        Remova textos de saudação ou despedida.
        """
        
        response = llm.question(prompt=prompt, question=question)
        return response.strip() if response else "Resumo estruturado não disponível"
        
    except Exception as e:
        logging.error(f"Erro na geração de resumo estruturado: {e}")
        return "Erro na geração de resumo estruturado"


def analyze_document_articles(text: str, document_path: str = None) -> List[Dict]:
    """
    Analisa artigos individuais do documento usando as capacidades
    aprimoradas de extração de artigos.
    
    Args:
        text (str): Texto completo do documento
        document_path (str, optional): Caminho do documento para análise estruturada
        
    Returns:
        List[Dict]: Lista de análises de artigos individuais
    """
    articles_analysis = []
    
    if not LEGISLATION_ANALYSIS_AVAILABLE:
        return articles_analysis
    
    try:
        # Use enhanced article splitting if available
        if hasattr(LegislationAnalysis, 'split_into_articles_enhanced'):
            articles = LegislationAnalysis.split_into_articles_enhanced(text, document_path)
        else:
            articles = LegislationAnalysis.split_into_articles(text)
        
        for i, article_text in enumerate(articles):
            if not article_text.strip():
                continue
                
            article_analysis = {
                'article_number': i + 1,
                'text': article_text,
                'title': '',
                'category': '',
                'normative_type': '',
                'summary': '',
                'components': {}
            }
            
            try:
                # Extract article components
                if hasattr(LegislationAnalysis, 'extract_article_components'):
                    article_analysis['components'] = LegislationAnalysis.extract_article_components(article_text)
                
                # Generate title, category, summary using existing functions
                article_analysis['title'] = LegislationAnalysis.set_a_title(article_text)
                article_analysis['category'] = LegislationAnalysis.define_categories(article_text)
                article_analysis['normative_type'] = LegislationAnalysis.define_the_normative_type(article_text)
                article_analysis['summary'] = LegislationAnalysis.summarize(article_text)
                
            except Exception as e:
                logging.warning(f"Erro na análise do artigo {i+1}: {e}")
            
            articles_analysis.append(article_analysis)
    
    except Exception as e:
        logging.error(f"Erro na análise de artigos: {e}")
    
    return articles_analysis


def generate_overall_assessment(text: str, context: LegalContext, articles_analysis: List[Dict]) -> str:
    """
    Gera uma avaliação geral do documento considerando todos os elementos analisados.
    
    Args:
        text (str): Texto completo
        context (LegalContext): Contexto jurídico extraído
        articles_analysis (List[Dict]): Análise dos artigos
        
    Returns:
        str: Avaliação geral do documento
    """
    if not MODEL_AVAILABLE:
        return "Avaliação geral não disponível - modelo não encontrado"
    
    try:
        llm = ModelOllama()
        llm.max_tokens = 300
        llm.temperature = 0.4
        
        # Prepare context summary
        context_summary = f"""
        Entidades identificadas: {len(context.names)} 
        Ações jurídicas: {len(context.actions)}
        Pontos de atenção: {len(context.attention_points)}
        Artigos analisados: {len(articles_analysis)}
        """
        
        prompt = """
        /clear
        Forneça uma avaliação geral abrangente do documento jurídico,
        considerando sua estrutura, conteúdo, complexidade e relevância.
        A avaliação deve ser profissional e destacar aspectos importantes.
        """
        
        question = f"""
        Com base na análise completa, forneça uma avaliação geral deste documento jurídico.
        Contexto da análise: {context_summary}
        Texto (início): {text[:1000]}
        
        A avaliação deve abordar:
        - Complexidade e estrutura do documento
        - Relevância jurídica
        - Pontos críticos identificados
        - Recomendações para aplicação prática
        
        Remova textos de saudação ou despedida.
        """
        
        response = llm.question(prompt=prompt, question=question)
        return response.strip() if response else "Avaliação geral não disponível"
        
    except Exception as e:
        logging.error(f"Erro na geração de avaliação geral: {e}")
        return "Erro na geração de avaliação geral"


def enhanced_legal_document_analysis(text: str, document_path: str = None) -> LegalSynthesis:
    """
    Realiza análise jurídica abrangente de um documento longo, integrando
    com os serviços de documento e catálogo quando disponíveis.
    
    Este é o método principal que pode receber um texto longo e extrair
    análise jurídica completa conforme especificado nos requisitos.
    
    Args:
        text (str): Texto jurídico completo para análise
        document_path (str, optional): Caminho do documento para análise estruturada
        
    Returns:
        LegalSynthesis: Análise jurídica completa e estruturada
    """
    
    # Verificar integração com serviços
    services_status = check_service_integration()
    logging.info(f"Status dos serviços: {services_status}")
    
    # Se o serviço de documentos estiver disponível, tentar usar para processamento aprimorado
    enhanced_text = text
    if DOCUMENT_SERVICE_AVAILABLE and document_path:
        try:
            # Usar serviço de documentos para extração aprimorada
            enhanced_content = DocService.document_content(document_path)
            if enhanced_content:
                enhanced_text = enhanced_content
                logging.info("Usando conteúdo extraído pelo serviço de documentos")
        except Exception as e:
            logging.warning(f"Falha ao usar serviço de documentos: {e}")
    
    # Extrair contexto jurídico
    logging.info("Extraindo contexto jurídico...")
    legal_context = extract_legal_context(enhanced_text)
    
    # Gerar síntese do assunto
    logging.info("Gerando síntese do assunto...")
    subject_synthesis = generate_subject_synthesis(enhanced_text)
    
    # Analisar artigos individuais
    logging.info("Analisando artigos individuais...")
    articles_analysis = analyze_document_articles(enhanced_text, document_path)
    
    # Gerar resumo estruturado
    logging.info("Gerando resumo estruturado...")
    structured_summary = generate_structured_summary(enhanced_text, articles_analysis)
    
    # Extrair categorias e tipo normativo usando funções existentes
    categories = []
    normative_type = ""
    if LEGISLATION_ANALYSIS_AVAILABLE:
        try:
            categories_response = LegislationAnalysis.define_categories(enhanced_text)
            if categories_response and categories_response.strip() != '-':
                categories = [cat.strip() for cat in categories_response.split(',') if cat.strip()]
            
            normative_type = LegislationAnalysis.define_the_normative_type(enhanced_text)
        except Exception as e:
            logging.warning(f"Erro na extração de categorias/tipo normativo: {e}")
    
    # Gerar avaliação geral
    logging.info("Gerando avaliação geral...")
    overall_assessment = generate_overall_assessment(enhanced_text, legal_context, articles_analysis)
    
    # Compilar síntese completa
    synthesis = LegalSynthesis(
        subject_synthesis=subject_synthesis,
        structured_summary=structured_summary,
        context=legal_context,
        categories=categories,
        normative_type=normative_type,
        articles_analysis=articles_analysis,
        overall_assessment=overall_assessment
    )
    
    logging.info("Análise jurídica abrangente concluída")
    return synthesis


def format_synthesis_report(synthesis: LegalSynthesis) -> str:
    """
    Formata a síntese jurídica em um relatório estruturado legível.
    
    Args:
        synthesis (LegalSynthesis): Síntese jurídica completa
        
    Returns:
        str: Relatório formatado
    """
    report = []
    
    report.append("=" * 80)
    report.append("RELATÓRIO DE ANÁLISE JURÍDICA ABRANGENTE")
    report.append("=" * 80)
    
    # Síntese do assunto
    report.append("\n1. SÍNTESE DO ASSUNTO")
    report.append("-" * 40)
    report.append(synthesis.subject_synthesis)
    
    # Informações gerais
    report.append(f"\n2. CLASSIFICAÇÃO")
    report.append("-" * 40)
    report.append(f"Tipo Normativo: {synthesis.normative_type}")
    report.append(f"Categorias: {', '.join(synthesis.categories) if synthesis.categories else 'Não identificadas'}")
    
    # Resumo estruturado
    report.append(f"\n3. RESUMO ESTRUTURADO")
    report.append("-" * 40)
    report.append(synthesis.structured_summary)
    
    # Contexto jurídico
    report.append(f"\n4. CONTEXTO JURÍDICO EXTRAÍDO")
    report.append("-" * 40)
    context = synthesis.context
    
    if context.names:
        report.append(f"Entidades Identificadas ({len(context.names)}): {', '.join(context.names[:5])}")
        if len(context.names) > 5:
            report.append(f"... e mais {len(context.names) - 5} entidades")
    
    if context.actions:
        report.append(f"Ações Jurídicas ({len(context.actions)}): {', '.join(context.actions[:3])}")
    
    if context.attention_points:
        report.append(f"Pontos de Atenção ({len(context.attention_points)}): {', '.join(context.attention_points[:3])}")
    
    if context.legal_terms:
        report.append(f"Termos Jurídicos ({len(context.legal_terms)}): {', '.join(context.legal_terms[:3])}")
    
    if context.dates_deadlines:
        report.append(f"Datas/Prazos ({len(context.dates_deadlines)}): {', '.join(context.dates_deadlines[:3])}")
    
    if context.penalties:
        report.append(f"Penalidades ({len(context.penalties)}): {', '.join(context.penalties[:3])}")
    
    # Análise de artigos
    if synthesis.articles_analysis:
        report.append(f"\n5. ANÁLISE DE ARTIGOS ({len(synthesis.articles_analysis)} artigos)")
        report.append("-" * 40)
        for i, article in enumerate(synthesis.articles_analysis[:3]):  # Show first 3 articles
            report.append(f"Artigo {i+1}:")
            report.append(f"  Título: {article.get('title', 'N/A')}")
            report.append(f"  Categoria: {article.get('category', 'N/A')}")
            report.append(f"  Resumo: {article.get('summary', 'N/A')[:100]}...")
        
        if len(synthesis.articles_analysis) > 3:
            report.append(f"... e mais {len(synthesis.articles_analysis) - 3} artigos analisados")
    
    # Avaliação geral
    report.append(f"\n6. AVALIAÇÃO GERAL")
    report.append("-" * 40)
    report.append(synthesis.overall_assessment)
    
    report.append("\n" + "=" * 80)
    
    return "\n".join(report)


# Alias para compatibilidade
analyze_long_legal_text = enhanced_legal_document_analysis