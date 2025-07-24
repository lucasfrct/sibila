# flake8: noqa: E501

"""
    EXAMINING BOARD: banca examinadora
    Este arquivo tem o papel de ser a banca examinadora que elabora as perguntas e gera o questionário.
    
    VERSÃO APRIMORADA: Integra com o módulo de análise jurídica enriquecida para
    questões mais elaboradas baseadas na análise de documentos e catálogo.
"""


import re
from typing import List, Dict, Optional

# Conditional imports with fallbacks
try:
    from src.models.ollama import ModelOllama
    MODEL_AVAILABLE = True
except ImportError:
    MODEL_AVAILABLE = False

try:
    from src.modules.analysis import federal_constitution_retrieval as FederalContitutionRetrieval
    FEDERAL_CONST_AVAILABLE = True
except ImportError:
    FEDERAL_CONST_AVAILABLE = False

# Import enhanced analysis functionality
try:
    from src.modules.analysis.enhanced_legal_analysis import (
        enhanced_legal_document_analysis,
        extract_legal_context,
        generate_subject_synthesis,
        check_service_integration
    )
    ENHANCED_ANALYSIS_AVAILABLE = True
except ImportError:
    ENHANCED_ANALYSIS_AVAILABLE = False


def _setup_standard_llm(max_tokens: int = 200, temperature: float = 0.3, out_focus: float = 8.0) -> 'ModelOllama':
    """
    Configura um modelo LLM com parâmetros padrão para análise de questionários.
    
    Args:
        max_tokens (int): Número máximo de tokens para resposta
        temperature (float): Temperatura para variação da resposta
        out_focus (float): Foco de saída
        
    Returns:
        ModelOllama: Instância configurada do modelo
    """
    if not MODEL_AVAILABLE:
        return None
    
    llm = ModelOllama()
    llm.max_tokens = max_tokens
    llm.temperature = temperature
    llm.out_focus = out_focus
    llm.out_reduction_rate = 100.0
    llm.penalty_rate = 5.0
    return llm


# questões para serem aplicas a um artigo
common_questions = [
    "Existe ambiguidade na sequinte lei?",
    "Qual é o principal objetivo deste artigo?",
    "Quais as conseqûencias prátcias da seguinte lei?",
    "Quais direitos ou garantias são assegurados por este artigo?",
    "Qual o ponto de insconsistência mais crítico na seguinte lei?",
]

# questão apra se prguntar para a IA treinada
constextual_questions = [
    "Quais são os direitos garantidos pela Constituição de 1988 em relação à liberdade de expressão?",
    "Qual é a importância do princípio da função social da propriedade na Constituição de 1988?",
    "Quais mudanças significativas a Constituição de 1988 trouxe para o sistema de saúde no Brasil?",
]


def ask_a_question(docs: str, article: str, ask: str ) -> str:
    """
	Faz uma pergunta a partir de um conjunto de documentos e um artigo específico.

	Args:
		docs (str): Texto contendo os documentos a serem analisados.
		ask (str): Pergunta a ser feita com base nos documentos.
		article (str): Artigo específico que deve ser considerado na resposta.

	Returns:
		str: Resposta gerada pelo modelo, sem texto de saudação, despedida ou descrição.
   	"""
    
    if not MODEL_AVAILABLE:
        return f"Resposta não disponível - modelo não encontrado. Pergunta: {ask}"
    
    try:
        llm = _setup_standard_llm(max_tokens=100)
        if not llm:
            return f"Resposta não disponível - modelo não encontrado. Pergunta: {ask}"
        
        llm.penalty_rate = 10.0
        prompt = f"""
            /clear
            Usando somente os textos abaixo, responda:
            # Documentos:
            {docs}
        """
        question = f"""
    		# Questão
            {ask} responda segundo a artigo: {article[0:512]}.
            Remova o texto de saudação ou despedida ou descrição.
        """
        response = llm.question(prompt=prompt, question=question).strip()
        return re.sub(r'[\n;.\'"]', '', response).strip()
    except Exception as e:
        return f"Erro na geração de resposta: {e}"

def question_maker(article: str)-> str:
    """
    Gera uma pergunta para um artigo específico.
    Args:
        article (str): O artigo que será utilizado para gerar a pergunta.
    Returns:
        str: A pergunta gerada.
    """
    
    if not MODEL_AVAILABLE:
        return f"Pergunta não disponível - modelo não encontrado para artigo: {article[:100]}..."
    
    try:
        llm = _setup_standard_llm(max_tokens=100)
        if not llm:
            return f"Pergunta não disponível - modelo não encontrado para artigo: {article[:100]}..."
        
        llm.penalty_rate = 10.0
        prompt = f"""
            /clear
            Usando somente os textos abaixo, responda:
            # Documentos:
            {article}
        """
        question = f"""
            # Questão
            Faça uma pergunta objetiva de teor jurídico sobre o seguinte artigo: {article[0:1024]}.
            Remova o texto de saudação ou despedida ou descrição.
        """
        response = llm.question(prompt=prompt, question=question).strip()
        return re.sub(r'[\n;.\'"]', '', response).strip()
    except Exception as e:
        return f"Erro na geração de pergunta: {e}"


def questionnaire(article: str)-> List[dict]:
    """
    Gera respostas para um conjunto de perguntas comuns com base em um artigo fornecido.
    Args:
        article (str): O artigo que será utilizado para gerar as respostas.
    Returns:
        list: Uma lista contendo as perguntas e suas respectivas respostas.
    """
    
    common_questions.append(question_maker(article))
    
    resp = []
    for question in common_questions:
        
        if FEDERAL_CONST_AVAILABLE:
            docs = FederalContitutionRetrieval.query_in_dimencions(question)
            docs.extend(FederalContitutionRetrieval.query_in_dimencions(article))
            documents = "\n".join(docs)
        else:
            documents = article
        
        response = ask_a_question(documents, article, question)
        resp.append({ "prompt": question, "completion": response })
    return resp


# FUNÇÕES APRIMORADAS COM INTEGRAÇÃO DE ANÁLISE ENRIQUECIDA

def enhanced_questionnaire(document_text: str, document_path: str = None) -> Dict:
    """
    Gera questionário aprimorado utilizando análise jurídica enriquecida.
    
    Integra com os módulos de documento e catálogo para produzir análise
    mais detalhada e questões mais elaboradas baseadas no contexto jurídico
    extraído do documento.
    
    Args:
        document_text (str): Texto completo do documento jurídico
        document_path (str, optional): Caminho do documento para análise estruturada
        
    Returns:
        Dict: Questionário aprimorado com análise contextual
    """
    
    result = {
        'service_integration': {},
        'legal_analysis': {},
        'enhanced_questions': [],
        'context_questions': [],
        'synthesis_questions': [],
        'traditional_questions': []
    }
    
    # Verificar integração com serviços
    if ENHANCED_ANALYSIS_AVAILABLE:
        result['service_integration'] = check_service_integration()
        
        # Realizar análise jurídica abrangente
        try:
            legal_synthesis = enhanced_legal_document_analysis(document_text, document_path)
            
            result['legal_analysis'] = {
                'subject_synthesis': legal_synthesis.subject_synthesis,
                'normative_type': legal_synthesis.normative_type,
                'categories': legal_synthesis.categories,
                'articles_count': len(legal_synthesis.articles_analysis),
                'context_entities': len(legal_synthesis.context.names),
                'attention_points': len(legal_synthesis.context.attention_points)
            }
            
            # Gerar questões baseadas na análise enriquecida
            result['enhanced_questions'] = _generate_enhanced_questions(legal_synthesis)
            result['context_questions'] = _generate_context_questions(legal_synthesis.context)
            result['synthesis_questions'] = _generate_synthesis_questions(legal_synthesis)
            
        except Exception as e:
            result['legal_analysis']['error'] = f"Erro na análise enriquecida: {e}"
    
    # Gerar questões tradicionais como fallback
    try:
        # Dividir em artigos para análise tradicional
        articles = _extract_basic_articles(document_text)
        for article in articles[:3]:  # Limitar para os primeiros 3 artigos
            traditional_q = questionnaire(article)
            result['traditional_questions'].extend(traditional_q)
    except Exception as e:
        result['traditional_questions'] = [{"error": f"Erro nas questões tradicionais: {e}"}]
    
    return result


def _generate_enhanced_questions(legal_synthesis) -> List[Dict]:
    """
    Gera questões aprimoradas baseadas na síntese jurídica completa.
    
    Args:
        legal_synthesis: Resultado da análise jurídica abrangente
        
    Returns:
        List[Dict]: Lista de questões aprimoradas
    """
    questions = []
    
    if not MODEL_AVAILABLE:
        return [{"question": "Questões aprimoradas não disponíveis - modelo não encontrado", "type": "error"}]
    
    try:
        # Questões sobre a síntese do assunto
        if legal_synthesis.subject_synthesis:
            questions.append({
                "question": f"Com base na síntese '{legal_synthesis.subject_synthesis[:100]}...', quais são as implicações práticas desta norma?",
                "type": "synthesis_analysis",
                "context": "subject_synthesis"
            })
        
        # Questões sobre tipo normativo e categorias
        if legal_synthesis.normative_type:
            questions.append({
                "question": f"Considerando que este é um {legal_synthesis.normative_type}, qual é sua hierarquia no ordenamento jurídico brasileiro?",
                "type": "normative_hierarchy",
                "context": "normative_type"
            })
        
        # Questões sobre artigos analisados
        if legal_synthesis.articles_analysis:
            questions.append({
                "question": f"Analisando os {len(legal_synthesis.articles_analysis)} artigos identificados, qual apresenta maior complexidade jurídica?",
                "type": "comparative_analysis",
                "context": "articles_structure"
            })
        
        # Questões sobre avaliação geral
        if legal_synthesis.overall_assessment:
            questions.append({
                "question": f"Com base na avaliação geral, quais são os principais desafios de implementação desta norma?",
                "type": "implementation_challenges",
                "context": "overall_assessment"
            })
    
    except Exception as e:
        questions.append({"question": f"Erro na geração de questões aprimoradas: {e}", "type": "error"})
    
    return questions


def _generate_context_questions(legal_context) -> List[Dict]:
    """
    Gera questões baseadas no contexto jurídico extraído.
    
    Args:
        legal_context: Contexto jurídico com entidades, ações, etc.
        
    Returns:
        List[Dict]: Lista de questões contextuais
    """
    questions = []
    
    try:
        # Questões sobre entidades identificadas
        if legal_context.names:
            entities_text = ', '.join(legal_context.names[:3])
            questions.append({
                "question": f"Qual é o papel das entidades '{entities_text}' no contexto desta norma?",
                "type": "entity_role",
                "context": "legal_entities"
            })
        
        # Questões sobre ações jurídicas
        if legal_context.actions:
            actions_text = ', '.join(legal_context.actions[:3])
            questions.append({
                "question": f"Como as ações '{actions_text}' impactam a aplicabilidade da norma?",
                "type": "action_impact",
                "context": "legal_actions"
            })
        
        # Questões sobre pontos de atenção
        if legal_context.attention_points:
            questions.append({
                "question": f"Quais cuidados especiais devem ser observados considerando os {len(legal_context.attention_points)} pontos de atenção identificados?",
                "type": "attention_points",
                "context": "critical_points"
            })
        
        # Questões sobre prazos e datas
        if legal_context.dates_deadlines:
            questions.append({
                "question": f"Como os prazos identificados ({len(legal_context.dates_deadlines)}) afetam o cumprimento da norma?",
                "type": "temporal_compliance",
                "context": "deadlines"
            })
        
        # Questões sobre penalidades
        if legal_context.penalties:
            questions.append({
                "question": f"Qual é o regime sancionatório previsto e suas consequências jurídicas?",
                "type": "penalty_regime",
                "context": "sanctions"
            })
    
    except Exception as e:
        questions.append({"question": f"Erro na geração de questões contextuais: {e}", "type": "error"})
    
    return questions


def _generate_synthesis_questions(legal_synthesis) -> List[Dict]:
    """
    Gera questões baseadas na síntese estruturada do documento.
    
    Args:
        legal_synthesis: Síntese jurídica completa
        
    Returns:
        List[Dict]: Lista de questões sobre síntese
    """
    questions = []
    
    try:
        # Questão sobre resumo estruturado
        if legal_synthesis.structured_summary:
            questions.append({
                "question": "Com base no resumo estruturado, qual é a lógica organizacional deste documento normativo?",
                "type": "structural_logic",
                "context": "structured_summary"
            })
        
        # Questão sobre categorização
        if legal_synthesis.categories:
            categories_text = ', '.join(legal_synthesis.categories)
            questions.append({
                "question": f"Considerando as categorias jurídicas '{categories_text}', como esta norma se relaciona com outras do mesmo ramo?",
                "type": "categorical_relationship",
                "context": "legal_categories"
            })
        
        # Questão sintética geral
        questions.append({
            "question": "Realizando uma síntese crítica, quais são os aspectos mais inovadores ou controversos desta norma?",
            "type": "critical_synthesis",
            "context": "overall_innovation"
        })
    
    except Exception as e:
        questions.append({"question": f"Erro na geração de questões de síntese: {e}", "type": "error"})
    
    return questions


def _extract_basic_articles(text: str) -> List[str]:
    """
    Extrai artigos do texto usando a função unificada do módulo de legislação.
    
    Args:
        text (str): Texto completo do documento
        
    Returns:
        List[str]: Lista de artigos extraídos
    """
    try:
        # Usar função unificada do módulo de legislação
        from src.modules.analysis.legislation import split_into_articles
        return split_into_articles(text)
    except Exception:
        # Fallback para implementação básica se necessário
        article_pattern = r'Art\.?\s*\d+[ºº°]?.*?(?=Art\.?\s*\d+[ºº°]?|\Z)'
        articles = re.findall(article_pattern, text, re.DOTALL | re.IGNORECASE)
        return [article.strip() for article in articles if article.strip()]


def analyze_document_with_enhanced_board(document_text: str, document_path: str = None) -> Dict:
    """
    Realiza análise completa de documento utilizando a banca examinadora aprimorada.
    
    Este método integra a análise jurídica enriquecida com a geração de questionários,
    cumprindo o objetivo de analisar documentos conforme indicado no doc block de
    cada método e produzindo análise enriquecida com as novas informações extraídas
    dos módulos de documentos e catálogo.
    
    Args:
        document_text (str): Texto completo do documento jurídico
        document_path (str, optional): Caminho do documento para análise estruturada
        
    Returns:
        Dict: Análise completa com questionário aprimorado
    """
    
    analysis_result = {
        'timestamp': None,
        'document_info': {
            'length': len(document_text),
            'has_path': bool(document_path)
        },
        'enhanced_questionnaire': {},
        'analysis_summary': {},
        'recommendations': []
    }
    
    try:
        import datetime
        analysis_result['timestamp'] = datetime.datetime.now().isoformat()
        
        # Executar questionário aprimorado
        analysis_result['enhanced_questionnaire'] = enhanced_questionnaire(document_text, document_path)
        
        # Gerar resumo da análise
        questionnaire_data = analysis_result['enhanced_questionnaire']
        
        analysis_result['analysis_summary'] = {
            'services_available': sum(questionnaire_data.get('service_integration', {}).values()),
            'total_enhanced_questions': len(questionnaire_data.get('enhanced_questions', [])),
            'total_context_questions': len(questionnaire_data.get('context_questions', [])),
            'total_synthesis_questions': len(questionnaire_data.get('synthesis_questions', [])),
            'total_traditional_questions': len(questionnaire_data.get('traditional_questions', [])),
            'has_legal_analysis': bool(questionnaire_data.get('legal_analysis', {}))
        }
        
        # Gerar recomendações
        analysis_result['recommendations'] = _generate_analysis_recommendations(questionnaire_data)
        
    except Exception as e:
        analysis_result['error'] = f"Erro na análise com banca aprimorada: {e}"
    
    return analysis_result


def _generate_analysis_recommendations(questionnaire_data: Dict) -> List[str]:
    """
    Gera recomendações baseadas na análise realizada.
    
    Args:
        questionnaire_data (Dict): Dados do questionário aprimorado
        
    Returns:
        List[str]: Lista de recomendações
    """
    recommendations = []
    
    try:
        # Recomendações baseadas na integração de serviços
        services = questionnaire_data.get('service_integration', {})
        if not any(services.values()):
            recommendations.append("Considere instalar dependências para análise mais robusta (ollama, docling, scikit-learn)")
        
        # Recomendações baseadas na análise jurídica
        legal_analysis = questionnaire_data.get('legal_analysis', {})
        if legal_analysis.get('articles_count', 0) > 10:
            recommendations.append("Documento extenso: considere análise por seções para melhor compreensão")
        
        if legal_analysis.get('attention_points', 0) > 5:
            recommendations.append("Múltiplos pontos de atenção identificados: revisar cuidadosamente antes da implementação")
        
        # Recomendações baseadas no tipo de questões geradas
        if len(questionnaire_data.get('enhanced_questions', [])) < 3:
            recommendations.append("Análise limitada: considere fornecer mais contexto ou usar versão completa do sistema")
        
        if not recommendations:
            recommendations.append("Análise concluída com sucesso. Revisar questões geradas para melhor compreensão do documento")
    
    except Exception:
        recommendations.append("Erro na geração de recomendações")
    
    return recommendations
