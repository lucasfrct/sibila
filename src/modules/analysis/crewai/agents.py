# flake8: noqa: E501

"""
Agentes especializados para análise legislativa usando CrewAI.

Este módulo define agentes inteligentes que trabalham em colaboração
para analisar documentos legislativos de forma abrangente e precisa.
Cada agente possui especialização específica e contribui para o
resultado final da análise.
"""

from typing import Dict, List, Optional, Any
import json
from abc import ABC, abstractmethod

# Importação condicional do CrewAI
try:
    from crewai import Agent, Task, Crew
    from crewai.tools import BaseTool
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    Agent = None
    Task = None
    Crew = None
    BaseTool = None

# Importações condicionais para lidar com dependências opcionais
try:
    from src.models.ollama import ModelOllama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    ModelOllama = None

try:
    from src.modules.analysis.legislation import LegislationAnalyzer
    LEGISLATION_ANALYZER_AVAILABLE = True
except ImportError:
    LEGISLATION_ANALYZER_AVAILABLE = False
    LegislationAnalyzer = None


class BaseAgent(ABC):
    """
    Classe base abstrata para todos os agentes de análise legislativa.
    
    Define a interface comum que todos os agentes devem implementar
    e fornece funcionalidades básicas compartilhadas.
    """
    
    def __init__(self, name: str, role: str, goal: str, backstory: str):
        """
        Inicializa o agente base com informações fundamentais.
        
        Args:
            name (str): Nome identificador do agente
            role (str): Papel/função do agente no sistema
            goal (str): Objetivo principal do agente
            backstory (str): Contexto e experiência do agente
        """
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        
        # Inicializar dependências quando disponíveis
        if OLLAMA_AVAILABLE:
            self.llm = ModelOllama()
            self._setup_llm()
        else:
            self.llm = None
            
        if LEGISLATION_ANALYZER_AVAILABLE:
            self.legislation_analyzer = LegislationAnalyzer()
        else:
            self.legislation_analyzer = None
    
    def _setup_llm(self):
        """Configura parâmetros específicos do LLM para este agente."""
        if self.llm is not None:
            self.llm.max_tokens = 300
            self.llm.temperature = 0.3
            self.llm.out_focus = 8.0
            self.llm.penalty_rate = 2.0
    
    @abstractmethod
    def analyze(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Método abstrato para análise de texto.
        
        Args:
            text (str): Texto a ser analisado
            context (Optional[Dict]): Contexto adicional para análise
            
        Returns:
            Dict[str, Any]: Resultado da análise do agente
        """
        pass
    
    def get_agent_info(self) -> Dict[str, str]:
        """
        Retorna informações básicas do agente.
        
        Returns:
            Dict[str, str]: Dicionário com informações do agente
        """
        return {
            'name': self.name,
            'role': self.role,
            'goal': self.goal,
            'backstory': self.backstory
        }


class LegalAnalysisAgent(BaseAgent):
    """
    Agente especializado em análise jurídica de textos legislativos.
    
    Este agente foca na identificação de elementos jurídicos fundamentais
    como categorias legais, tipos normativos, entidades envolvidas e 
    implicações legais dos textos analisados.
    """
    
    def __init__(self):
        """Inicializa o agente de análise jurídica com configurações específicas."""
        super().__init__(
            name="legal_analyst",
            role="Analista Jurídico Especializado",
            goal="Analisar textos legislativos identificando categorias, tipos normativos e elementos jurídicos relevantes",
            backstory="""Você é um analista jurídico experiente com vasta experiência em 
            legislação brasileira. Sua especialidade é identificar rapidamente os aspectos 
            jurídicos mais importantes de qualquer texto legal, classificando adequadamente 
            cada documento segundo as categorias do direito brasileiro."""
        )
        self._setup_specialized_llm()
    
    def _setup_specialized_llm(self):
        """Configura parâmetros específicos para análise jurídica."""
        self.llm.max_tokens = 400
        self.llm.temperature = 0.2  # Maior precisão para análise jurídica
        self.llm.out_focus = 10.0
        self.llm.penalty_rate = 3.0
    
    def analyze(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Realiza análise jurídica completa do texto fornecido.
        
        Args:
            text (str): Texto legislativo a ser analisado
            context (Optional[Dict]): Contexto adicional da análise
            
        Returns:
            Dict[str, Any]: Resultado detalhado da análise jurídica
        """
        # Verificar disponibilidade de dependências
        if not OLLAMA_AVAILABLE or not LEGISLATION_ANALYZER_AVAILABLE:
            return self._fallback_analysis(text)
        
        # Análise estrutural usando o analisador de legislação
        structural_analysis = self.legislation_analyzer.analyze_text_structure(text)
        
        # Classificação jurídica
        legal_category = self._classify_legal_category(text)
        normative_type = self._identify_normative_type(text)
        legal_entities = self._extract_legal_entities(text)
        legal_implications = self._analyze_legal_implications(text)
        
        return {
            'agent_name': self.name,
            'analysis_type': 'juridica',
            'structural_analysis': structural_analysis,
            'legal_category': legal_category,
            'normative_type': normative_type,
            'legal_entities': legal_entities,
            'legal_implications': legal_implications,
            'confidence_score': self._calculate_confidence(structural_analysis)
        }
    
    def _fallback_analysis(self, text: str) -> Dict[str, Any]:
        """
        Análise simplificada quando dependências não estão disponíveis.
        
        Args:
            text (str): Texto a ser analisado
            
        Returns:
            Dict[str, Any]: Análise básica do texto
        """
        return {
            'agent_name': self.name,
            'analysis_type': 'juridica_basica',
            'text_length': len(text),
            'word_count': len(text.split()),
            'has_articles': 'art.' in text.lower() or 'artigo' in text.lower(),
            'status': 'Análise limitada - dependências não disponíveis',
            'confidence_score': 0.3
        }
    
    def _classify_legal_category(self, text: str) -> str:
        """
        Classifica a categoria jurídica do texto.
        
        Args:
            text (str): Texto a ser classificado
            
        Returns:
            str: Categoria jurídica identificada
        """
        if not self.llm:
            return self._classify_category_fallback(text)
            
        prompt = """
        /clear
        Você é um especialista em direito brasileiro. Analise o texto fornecido e 
        identifique a categoria jurídica mais apropriada baseando-se nas seguintes opções:
        
        - Direito Constitucional: Organização do Estado e direitos fundamentais
        - Direito Civil: Relações privadas, contratos, família, propriedade
        - Direito Penal: Crimes, punições e processo penal
        - Direito Administrativo: Administração pública e seus agentes
        - Direito Trabalhista: Relações de trabalho e direitos trabalhistas
        - Direito Tributário: Impostos, taxas e arrecadação
        - Direito Ambiental: Proteção do meio ambiente
        - Direito Comercial: Atividades empresariais e comerciais
        - Direito Internacional: Relações entre países
        - Direito Processual: Procedimentos judiciais
        
        Responda apenas com a categoria mais apropriada.
        """
        
        question = f"Classifique juridicamente este texto: {text[:500]}"
        
        response = self.llm.question(prompt=prompt, question=question)
        return response.strip()
    
    def _classify_category_fallback(self, text: str) -> str:
        """Classificação básica por palavras-chave quando LLM não disponível."""
        text_lower = text.lower()
        
        # Mapeamento básico por palavras-chave
        if any(word in text_lower for word in ['constituição', 'fundamental', 'estado']):
            return 'Direito Constitucional'
        elif any(word in text_lower for word in ['crime', 'pena', 'prisão', 'delito']):
            return 'Direito Penal'
        elif any(word in text_lower for word in ['trabalho', 'empregado', 'salário']):
            return 'Direito Trabalhista'
        elif any(word in text_lower for word in ['tributo', 'imposto', 'taxa']):
            return 'Direito Tributário'
        elif any(word in text_lower for word in ['ambiente', 'poluição', 'ecológico']):
            return 'Direito Ambiental'
        elif any(word in text_lower for word in ['administração', 'público', 'servidor']):
            return 'Direito Administrativo'
        elif any(word in text_lower for word in ['contrato', 'família', 'propriedade']):
            return 'Direito Civil'
        else:
            return 'Categoria não identificada'
    
    def _identify_normative_type(self, text: str) -> str:
        """
        Identifica o tipo normativo do documento.
        
        Args:
            text (str): Texto a ser analisado
            
        Returns:
            str: Tipo normativo identificado
        """
        prompt = """
        /clear
        Identifique o tipo normativo do texto analisando sua estrutura e conteúdo.
        Tipos possíveis: Lei, Decreto, Portaria, Resolução, Instrução Normativa, 
        Medida Provisória, Emenda Constitucional, Regulamento, Circular, Despacho.
        
        Responda apenas com o tipo normativo identificado.
        """
        
        question = f"Qual o tipo normativo deste texto: {text[:300]}"
        
        response = self.llm.question(prompt=prompt, question=question)
        return response.strip()
    
    def _extract_legal_entities(self, text: str) -> List[str]:
        """
        Extrai entidades jurídicas relevantes do texto.
        
        Args:
            text (str): Texto para extração de entidades
            
        Returns:
            List[str]: Lista de entidades jurídicas identificadas
        """
        prompt = """
        /clear
        Extraia as principais entidades jurídicas do texto, incluindo:
        - Órgãos públicos e instituições
        - Pessoas jurídicas mencionadas
        - Autoridades e cargos relevantes
        - Entidades reguladoras
        
        Retorne as entidades separadas por vírgula, máximo 5 entidades.
        Se não houver entidades relevantes, retorne '-'.
        """
        
        question = f"Extraia as entidades jurídicas deste texto: {text[:400]}"
        
        response = self.llm.question(prompt=prompt, question=question)
        entities = [entity.strip() for entity in response.split(',') if entity.strip()]
        return entities if entities and entities[0] != '-' else []
    
    def _analyze_legal_implications(self, text: str) -> Dict[str, Any]:
        """
        Analisa as implicações jurídicas do texto.
        
        Args:
            text (str): Texto a ser analisado
            
        Returns:
            Dict[str, Any]: Análise das implicações jurídicas
        """
        prompt = """
        /clear
        Analise as principais implicações jurídicas do texto fornecido.
        Identifique:
        1. Direitos conferidos ou alterados
        2. Obrigações impostas
        3. Penalidades ou sanções
        4. Prazos e datas importantes
        5. Impacto em legislação existente
        
        Seja objetivo e conciso em cada ponto.
        """
        
        question = f"Quais as implicações jurídicas deste texto: {text[:500]}"
        
        response = self.llm.question(prompt=prompt, question=question)
        
        # Estruturar resposta em categorias
        return {
            'general_implications': response.strip(),
            'affected_rights': self._extract_affected_rights(text),
            'obligations': self._extract_obligations(text),
            'penalties': self._extract_penalties(text)
        }
    
    def _extract_affected_rights(self, text: str) -> str:
        """Extrai direitos afetados pelo texto."""
        prompt = "Identifique brevemente quais direitos são afetados por este texto legal:"
        question = text[:300]
        return self.llm.question(prompt=prompt, question=question).strip()
    
    def _extract_obligations(self, text: str) -> str:
        """Extrai obrigações impostas pelo texto."""
        prompt = "Identifique as principais obrigações impostas por este texto legal:"
        question = text[:300]
        return self.llm.question(prompt=prompt, question=question).strip()
    
    def _extract_penalties(self, text: str) -> str:
        """Extrai penalidades mencionadas no texto."""
        prompt = "Identifique as penalidades ou sanções mencionadas neste texto:"
        question = text[:300]
        return self.llm.question(prompt=prompt, question=question).strip()
    
    def _calculate_confidence(self, structural_analysis: Dict) -> float:
        """
        Calcula nível de confiança da análise jurídica.
        
        Args:
            structural_analysis (Dict): Análise estrutural do texto
            
        Returns:
            float: Nível de confiança entre 0 e 1
        """
        confidence = structural_analysis.get('confidence_score', 0.5)
        
        # Ajustar confiança baseado na qualidade da análise jurídica
        if 'legislative_patterns' in structural_analysis:
            patterns = structural_analysis['legislative_patterns']
            pattern_score = sum(patterns.values()) / max(len(patterns), 1)
            confidence = min(confidence + (pattern_score * 0.1), 1.0)
        
        return confidence


class DocumentReviewAgent(BaseAgent):
    """
    Agente especializado em revisão e validação de documentos legislativos.
    
    Este agente foca na verificação da consistência, completude e 
    conformidade dos documentos analisados, identificando possíveis
    inconsistências ou elementos que necessitam atenção especial.
    """
    
    def __init__(self):
        """Inicializa o agente de revisão de documentos."""
        super().__init__(
            name="document_reviewer",
            role="Revisor de Documentos Legislativos",
            goal="Revisar e validar a consistência e completude de documentos legislativos",
            backstory="""Você é um revisor experiente especializado em documentos legais. 
            Sua expertise está em identificar inconsistências, verificar a completude de 
            informações e garantir que os documentos estejam em conformidade com os padrões 
            legislativos brasileiros."""
        )
    
    def analyze(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Realiza revisão completa do documento legislativo.
        
        Args:
            text (str): Texto do documento a ser revisado
            context (Optional[Dict]): Contexto da revisão
            
        Returns:
            Dict[str, Any]: Resultado da revisão do documento
        """
        # Verificações de estrutura e formatação
        structure_check = self._check_document_structure(text)
        completeness_check = self._check_document_completeness(text)
        consistency_check = self._check_internal_consistency(text)
        compliance_check = self._check_legal_compliance(text)
        
        # Avaliação geral da qualidade
        quality_score = self._calculate_quality_score(
            structure_check, completeness_check, consistency_check, compliance_check
        )
        
        return {
            'agent_name': self.name,
            'analysis_type': 'revisao',
            'structure_check': structure_check,
            'completeness_check': completeness_check,
            'consistency_check': consistency_check,
            'compliance_check': compliance_check,
            'quality_score': quality_score,
            'recommendations': self._generate_recommendations(text, quality_score)
        }
    
    def _check_document_structure(self, text: str) -> Dict[str, Any]:
        """
        Verifica a estrutura do documento legislativo.
        
        Args:
            text (str): Texto a ser verificado
            
        Returns:
            Dict[str, Any]: Resultado da verificação estrutural
        """
        structure_elements = {
            'has_articles': 'art.' in text.lower() or 'artigo' in text.lower(),
            'has_paragraphs': '§' in text,
            'has_items': any(roman in text for roman in ['I ', 'II ', 'III ', 'IV ', 'V ']),
            'has_dates': bool(self.legislation_analyzer._identify_legislative_patterns(text)['dates']),
            'proper_formatting': self._check_formatting(text)
        }
        
        structure_score = sum(structure_elements.values()) / len(structure_elements)
        
        return {
            'elements': structure_elements,
            'score': structure_score,
            'issues': self._identify_structure_issues(text, structure_elements)
        }
    
    def _check_formatting(self, text: str) -> bool:
        """Verifica formatação básica do documento."""
        # Verificar se há numeração adequada de artigos
        import re
        article_pattern = re.compile(r'Art\.?\s*\d+', re.IGNORECASE)
        articles = article_pattern.findall(text)
        
        # Verificar consistência na numeração
        if len(articles) > 1:
            numbers = []
            for article in articles:
                number_match = re.search(r'\d+', article)
                if number_match:
                    numbers.append(int(number_match.group()))
            
            # Verificar se numeração é sequencial
            if numbers:
                return all(numbers[i] <= numbers[i+1] for i in range(len(numbers)-1))
        
        return True
    
    def _identify_structure_issues(self, text: str, elements: Dict) -> List[str]:
        """Identifica problemas estruturais específicos."""
        issues = []
        
        if not elements['has_articles']:
            issues.append("Documento não possui artigos claramente identificados")
        
        if not elements['proper_formatting']:
            issues.append("Numeração de artigos pode estar inconsistente")
        
        if len(text.strip()) < 100:
            issues.append("Documento muito curto para análise completa")
        
        return issues
    
    def _check_document_completeness(self, text: str) -> Dict[str, Any]:
        """
        Verifica a completude do documento.
        
        Args:
            text (str): Texto a ser verificado
            
        Returns:
            Dict[str, Any]: Resultado da verificação de completude
        """
        completeness_criteria = {
            'has_title_info': self._has_title_information(text),
            'has_content': len(text.strip()) > 50,
            'has_legal_references': self._has_legal_references(text),
            'has_clear_objectives': self._has_clear_objectives(text)
        }
        
        completeness_score = sum(completeness_criteria.values()) / len(completeness_criteria)
        
        return {
            'criteria': completeness_criteria,
            'score': completeness_score,
            'missing_elements': [k for k, v in completeness_criteria.items() if not v]
        }
    
    def _has_title_information(self, text: str) -> bool:
        """Verifica se há informações de título/identificação."""
        title_indicators = ['lei', 'decreto', 'portaria', 'resolução', 'n°', 'nº']
        return any(indicator in text.lower()[:200] for indicator in title_indicators)
    
    def _has_legal_references(self, text: str) -> bool:
        """Verifica se há referências legais apropriadas."""
        import re
        legal_ref_patterns = [
            r'lei\s+n[°º]\s*\d+',
            r'decreto\s+n[°º]\s*\d+',
            r'art\.?\s*\d+',
            r'constituição'
        ]
        
        return any(re.search(pattern, text.lower()) for pattern in legal_ref_patterns)
    
    def _has_clear_objectives(self, text: str) -> bool:
        """Verifica se há objetivos claros definidos."""
        objective_indicators = ['estabelece', 'dispõe', 'regulamenta', 'determina', 'institui']
        return any(indicator in text.lower() for indicator in objective_indicators)
    
    def _check_internal_consistency(self, text: str) -> Dict[str, Any]:
        """
        Verifica consistência interna do documento.
        
        Args:
            text (str): Texto a ser verificado
            
        Returns:
            Dict[str, Any]: Resultado da verificação de consistência
        """
        # Verificar referências internas
        internal_references = self._check_internal_references(text)
        terminology_consistency = self._check_terminology_consistency(text)
        
        consistency_score = (internal_references + terminology_consistency) / 2
        
        return {
            'internal_references': internal_references,
            'terminology_consistency': terminology_consistency,
            'score': consistency_score
        }
    
    def _check_internal_references(self, text: str) -> float:
        """Verifica consistência de referências internas."""
        # Implementação simplificada - verificar se artigos referenciados existem
        import re
        
        # Encontrar referências a artigos
        ref_pattern = re.compile(r'art\.?\s*(\d+)', re.IGNORECASE)
        references = [int(match.group(1)) for match in ref_pattern.finditer(text)]
        
        # Encontrar artigos existentes
        article_pattern = re.compile(r'Art\.?\s*(\d+)', re.IGNORECASE)
        articles = [int(match.group(1)) for match in article_pattern.finditer(text)]
        
        if not references:
            return 1.0  # Sem referências, sem problemas
        
        # Verificar se todas as referências existem
        valid_references = sum(1 for ref in references if ref in articles)
        return valid_references / len(references) if references else 1.0
    
    def _check_terminology_consistency(self, text: str) -> float:
        """Verifica consistência terminológica."""
        # Implementação básica - verificar uso consistente de termos legais
        return 0.8  # Placeholder para implementação mais sofisticada
    
    def _check_legal_compliance(self, text: str) -> Dict[str, Any]:
        """
        Verifica conformidade com padrões legais.
        
        Args:
            text (str): Texto a ser verificado
            
        Returns:
            Dict[str, Any]: Resultado da verificação de conformidade
        """
        compliance_checks = {
            'proper_legal_language': self._uses_proper_legal_language(text),
            'constitutional_compliance': self._check_constitutional_compliance(text),
            'formal_requirements': self._check_formal_requirements(text)
        }
        
        compliance_score = sum(compliance_checks.values()) / len(compliance_checks)
        
        return {
            'checks': compliance_checks,
            'score': compliance_score
        }
    
    def _uses_proper_legal_language(self, text: str) -> bool:
        """Verifica uso de linguagem jurídica apropriada."""
        legal_terms = ['estabelece', 'determina', 'regulamenta', 'dispõe', 'institui', 'revoga']
        return any(term in text.lower() for term in legal_terms)
    
    def _check_constitutional_compliance(self, text: str) -> bool:
        """Verifica conformidade constitucional básica."""
        # Implementação simplificada
        return True  # Requer análise mais complexa
    
    def _check_formal_requirements(self, text: str) -> bool:
        """Verifica requisitos formais básicos."""
        return len(text.strip()) > 50 and any(char.isalpha() for char in text)
    
    def _calculate_quality_score(self, structure_check: Dict, completeness_check: Dict, 
                                consistency_check: Dict, compliance_check: Dict) -> float:
        """
        Calcula pontuação geral de qualidade do documento.
        
        Args:
            structure_check (Dict): Resultado da verificação estrutural
            completeness_check (Dict): Resultado da verificação de completude
            consistency_check (Dict): Resultado da verificação de consistência
            compliance_check (Dict): Resultado da verificação de conformidade
            
        Returns:
            float: Pontuação de qualidade entre 0 e 1
        """
        scores = [
            structure_check['score'],
            completeness_check['score'],
            consistency_check['score'],
            compliance_check['score']
        ]
        
        return sum(scores) / len(scores)
    
    def _generate_recommendations(self, text: str, quality_score: float) -> List[str]:
        """
        Gera recomendações para melhoria do documento.
        
        Args:
            text (str): Texto analisado
            quality_score (float): Pontuação de qualidade
            
        Returns:
            List[str]: Lista de recomendações
        """
        recommendations = []
        
        if quality_score < 0.7:
            recommendations.append("Revisar estrutura geral do documento")
        
        if quality_score < 0.5:
            recommendations.append("Verificar completude das informações obrigatórias")
            
        if len(text.strip()) < 200:
            recommendations.append("Considerar expandir o conteúdo para maior clareza")
        
        return recommendations


class ComplianceAgent(BaseAgent):
    """
    Agente especializado em verificação de conformidade regulatória.
    
    Este agente foca na verificação de conformidade com normas,
    regulamentos e padrões estabelecidos, identificando possíveis
    conflitos ou questões de conformidade regulatória.
    """
    
    def __init__(self):
        """Inicializa o agente de conformidade regulatória."""
        super().__init__(
            name="compliance_checker",
            role="Especialista em Conformidade Regulatória",
            goal="Verificar conformidade de documentos com normas e regulamentos aplicáveis",
            backstory="""Você é um especialista em conformidade regulatória com profundo 
            conhecimento das normas brasileiras. Sua função é identificar possíveis 
            conflitos regulatórios e garantir que os documentos estejam em conformidade 
            com a legislação vigente."""
        )
    
    def analyze(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Realiza análise de conformidade regulatória.
        
        Args:
            text (str): Texto a ser analisado
            context (Optional[Dict]): Contexto da análise
            
        Returns:
            Dict[str, Any]: Resultado da análise de conformidade
        """
        # Verificações de conformidade
        regulatory_compliance = self._check_regulatory_compliance(text)
        legal_conflicts = self._identify_legal_conflicts(text)
        compliance_gaps = self._identify_compliance_gaps(text)
        
        # Avaliação geral de conformidade
        overall_compliance = self._calculate_overall_compliance(
            regulatory_compliance, legal_conflicts, compliance_gaps
        )
        
        return {
            'agent_name': self.name,
            'analysis_type': 'conformidade',
            'regulatory_compliance': regulatory_compliance,
            'legal_conflicts': legal_conflicts,
            'compliance_gaps': compliance_gaps,
            'overall_compliance': overall_compliance,
            'compliance_recommendations': self._generate_compliance_recommendations(text)
        }
    
    def _check_regulatory_compliance(self, text: str) -> Dict[str, Any]:
        """
        Verifica conformidade com regulamentos aplicáveis.
        
        Args:
            text (str): Texto a ser verificado
            
        Returns:
            Dict[str, Any]: Resultado da verificação regulatória
        """
        prompt = """
        /clear
        Analise o texto fornecido e identifique possíveis questões de conformidade 
        regulatória, considerando:
        1. Conformidade com a Constituição Federal
        2. Adequação à legislação federal vigente
        3. Respeito às normas administrativas
        4. Compatibilidade com tratados internacionais
        
        Responda de forma objetiva sobre a conformidade geral.
        """
        
        question = f"Analise a conformidade regulatória deste texto: {text[:500]}"
        
        compliance_analysis = self.llm.question(prompt=prompt, question=question)
        
        return {
            'analysis': compliance_analysis.strip(),
            'score': self._calculate_compliance_score(text),
            'critical_issues': self._identify_critical_issues(text)
        }
    
    def _calculate_compliance_score(self, text: str) -> float:
        """Calcula pontuação de conformidade baseada em indicadores."""
        # Indicadores básicos de conformidade
        indicators = {
            'has_legal_basis': self._has_legal_basis_reference(text),
            'proper_authority': self._has_proper_authority_reference(text),
            'procedural_compliance': self._check_procedural_compliance(text),
            'constitutional_alignment': self._check_constitutional_alignment(text)
        }
        
        return sum(indicators.values()) / len(indicators)
    
    def _has_legal_basis_reference(self, text: str) -> bool:
        """Verifica se há referência à base legal."""
        basis_indicators = ['fundamentado', 'baseado', 'nos termos', 'de acordo com']
        return any(indicator in text.lower() for indicator in basis_indicators)
    
    def _has_proper_authority_reference(self, text: str) -> bool:
        """Verifica se há referência à autoridade competente."""
        authority_indicators = ['competência', 'autoridade', 'órgão', 'ministério']
        return any(indicator in text.lower() for indicator in authority_indicators)
    
    def _check_procedural_compliance(self, text: str) -> bool:
        """Verifica conformidade procedimental básica."""
        procedural_indicators = ['processo', 'procedimento', 'tramitação', 'publicação']
        return any(indicator in text.lower() for indicator in procedural_indicators)
    
    def _check_constitutional_alignment(self, text: str) -> bool:
        """Verifica alinhamento constitucional."""
        # Implementação simplificada
        return not any(term in text.lower() for term in ['inconstitucional', 'violação'])
    
    def _identify_critical_issues(self, text: str) -> List[str]:
        """Identifica questões críticas de conformidade."""
        critical_issues = []
        
        # Verificar possíveis violações
        if 'violação' in text.lower():
            critical_issues.append("Possível violação identificada no texto")
        
        if 'inconstitucional' in text.lower():
            critical_issues.append("Questão de constitucionalidade identificada")
        
        return critical_issues
    
    def _identify_legal_conflicts(self, text: str) -> Dict[str, Any]:
        """
        Identifica possíveis conflitos legais.
        
        Args:
            text (str): Texto a ser analisado
            
        Returns:
            Dict[str, Any]: Resultado da identificação de conflitos
        """
        prompt = """
        /clear
        Identifique possíveis conflitos legais ou inconsistências no texto fornecido.
        Considere:
        1. Conflitos com legislação existente
        2. Inconsistências internas
        3. Contradições com normas superiores
        4. Problemas de hierarquia normativa
        
        Se não houver conflitos aparentes, responda 'Nenhum conflito identificado'.
        """
        
        question = f"Identifique conflitos legais neste texto: {text[:400]}"
        
        conflicts_analysis = self.llm.question(prompt=prompt, question=question)
        
        return {
            'analysis': conflicts_analysis.strip(),
            'has_conflicts': 'nenhum conflito' not in conflicts_analysis.lower(),
            'severity': self._assess_conflict_severity(conflicts_analysis)
        }
    
    def _assess_conflict_severity(self, conflicts_text: str) -> str:
        """Avalia severidade dos conflitos identificados."""
        if 'nenhum conflito' in conflicts_text.lower():
            return 'baixa'
        elif any(term in conflicts_text.lower() for term in ['grave', 'crítico', 'inconstitucional']):
            return 'alta'
        else:
            return 'média'
    
    def _identify_compliance_gaps(self, text: str) -> Dict[str, Any]:
        """
        Identifica lacunas de conformidade.
        
        Args:
            text (str): Texto a ser analisado
            
        Returns:
            Dict[str, Any]: Resultado da identificação de lacunas
        """
        gaps = {
            'missing_definitions': self._check_missing_definitions(text),
            'unclear_procedures': self._check_unclear_procedures(text),
            'incomplete_regulations': self._check_incomplete_regulations(text),
            'missing_enforcement': self._check_missing_enforcement(text)
        }
        
        gap_count = sum(1 for gap in gaps.values() if gap)
        
        return {
            'identified_gaps': gaps,
            'gap_count': gap_count,
            'severity': 'alta' if gap_count > 2 else 'média' if gap_count > 0 else 'baixa'
        }
    
    def _check_missing_definitions(self, text: str) -> bool:
        """Verifica se há definições importantes ausentes."""
        # Procurar por termos que geralmente precisam de definição
        undefined_terms = ['sistema', 'processo', 'órgão', 'entidade']
        text_lower = text.lower()
        
        has_undefined = any(term in text_lower for term in undefined_terms)
        has_definitions = 'define' in text_lower or 'conceito' in text_lower
        
        return has_undefined and not has_definitions
    
    def _check_unclear_procedures(self, text: str) -> bool:
        """Verifica se há procedimentos mal definidos."""
        procedure_indicators = ['procedimento', 'processo', 'tramitação']
        detail_indicators = ['prazo', 'etapa', 'responsável', 'como']
        
        has_procedures = any(indicator in text.lower() for indicator in procedure_indicators)
        has_details = any(indicator in text.lower() for indicator in detail_indicators)
        
        return has_procedures and not has_details
    
    def _check_incomplete_regulations(self, text: str) -> bool:
        """Verifica se há regulamentações incompletas."""
        return 'regulamentação posterior' in text.lower() or 'será definido' in text.lower()
    
    def _check_missing_enforcement(self, text: str) -> bool:
        """Verifica se há mecanismos de execução ausentes."""
        enforcement_indicators = ['fiscalização', 'sanção', 'penalidade', 'multa']
        has_rules = len(text) > 200  # Assume que textos longos precisam de enforcement
        has_enforcement = any(indicator in text.lower() for indicator in enforcement_indicators)
        
        return has_rules and not has_enforcement
    
    def _calculate_overall_compliance(self, regulatory_compliance: Dict, 
                                    legal_conflicts: Dict, compliance_gaps: Dict) -> Dict[str, Any]:
        """
        Calcula conformidade geral.
        
        Args:
            regulatory_compliance (Dict): Resultado da conformidade regulatória
            legal_conflicts (Dict): Resultado dos conflitos legais
            compliance_gaps (Dict): Resultado das lacunas
            
        Returns:
            Dict[str, Any]: Avaliação geral de conformidade
        """
        # Calcular pontuação geral
        base_score = regulatory_compliance['score']
        
        # Penalizar por conflitos
        if legal_conflicts['has_conflicts']:
            severity_penalty = {'alta': 0.3, 'média': 0.2, 'baixa': 0.1}
            base_score -= severity_penalty.get(legal_conflicts['severity'], 0.1)
        
        # Penalizar por lacunas
        gap_penalty = compliance_gaps['gap_count'] * 0.1
        base_score -= gap_penalty
        
        final_score = max(base_score, 0.0)
        
        return {
            'score': final_score,
            'level': self._get_compliance_level(final_score),
            'critical_actions_needed': final_score < 0.5
        }
    
    def _get_compliance_level(self, score: float) -> str:
        """Determina nível de conformidade baseado na pontuação."""
        if score >= 0.8:
            return 'Excelente'
        elif score >= 0.6:
            return 'Boa'
        elif score >= 0.4:
            return 'Adequada'
        else:
            return 'Insuficiente'
    
    def _generate_compliance_recommendations(self, text: str) -> List[str]:
        """
        Gera recomendações para melhoria da conformidade.
        
        Args:
            text (str): Texto analisado
            
        Returns:
            List[str]: Lista de recomendações
        """
        recommendations = []
        
        if self._has_legal_basis_reference(text) is False:
            recommendations.append("Incluir referência clara à base legal da norma")
        
        if self._has_proper_authority_reference(text) is False:
            recommendations.append("Especificar a autoridade competente para a norma")
        
        if self._check_missing_definitions(text):
            recommendations.append("Adicionar seção de definições para termos técnicos")
        
        if self._check_unclear_procedures(text):
            recommendations.append("Detalhar procedimentos e prazos aplicáveis")
        
        return recommendations


class CrewAIOrchestrator:
    """
    Orquestrador para coordenar múltiplos agentes de análise legislativa.
    
    Esta classe coordena o trabalho colaborativo entre diferentes agentes
    especializados, combinando suas análises para produzir um resultado
    abrangente e detalhado.
    """
    
    def __init__(self):
        """Inicializa o orquestrador com todos os agentes especializados."""
        self.legal_analyst = LegalAnalysisAgent()
        self.document_reviewer = DocumentReviewAgent()
        self.compliance_checker = ComplianceAgent()
        
        # Configurar CrewAI se disponível
        self.crew = None
        if CREWAI_AVAILABLE:
            self._setup_crew()
    
    def _setup_crew(self):
        """Configura o crew do CrewAI com os agentes especializados."""
        try:
            # Criar agentes CrewAI baseados nos nossos agentes especializados
            legal_agent = Agent(
                role=self.legal_analyst.role,
                goal=self.legal_analyst.goal,
                backstory=self.legal_analyst.backstory,
                verbose=True
            )
            
            review_agent = Agent(
                role=self.document_reviewer.role,
                goal=self.document_reviewer.goal,
                backstory=self.document_reviewer.backstory,
                verbose=True
            )
            
            compliance_agent = Agent(
                role=self.compliance_checker.role,
                goal=self.compliance_checker.goal,
                backstory=self.compliance_checker.backstory,
                verbose=True
            )
            
            # Criar crew com os agentes
            self.crew = Crew(
                agents=[legal_agent, review_agent, compliance_agent],
                verbose=2
            )
            
        except Exception as e:
            print(f"Aviso: Não foi possível configurar CrewAI: {e}")
            self.crew = None
    
    def analyze_document(self, text: str, analysis_type: str = 'completa') -> Dict[str, Any]:
        """
        Realiza análise coordenada do documento usando múltiplos agentes.
        
        Args:
            text (str): Texto do documento a ser analisado
            analysis_type (str): Tipo de análise ('completa', 'juridica', 'revisao', 'conformidade')
            
        Returns:
            Dict[str, Any]: Resultado consolidado da análise
        """
        results = {
            'document_summary': self._generate_document_summary(text),
            'analysis_timestamp': self._get_timestamp(),
            'analysis_type': analysis_type
        }
        
        # Executar análises baseadas no tipo solicitado
        if analysis_type in ['completa', 'juridica']:
            results['legal_analysis'] = self.legal_analyst.analyze(text)
        
        if analysis_type in ['completa', 'revisao']:
            results['document_review'] = self.document_reviewer.analyze(text)
        
        if analysis_type in ['completa', 'conformidade']:
            results['compliance_check'] = self.compliance_checker.analyze(text)
        
        # Gerar conclusões consolidadas
        if analysis_type == 'completa':
            results['consolidated_analysis'] = self._consolidate_analyses(results)
        
        return results
    
    def _generate_document_summary(self, text: str) -> Dict[str, Any]:
        """
        Gera resumo básico do documento.
        
        Args:
            text (str): Texto do documento
            
        Returns:
            Dict[str, Any]: Resumo do documento
        """
        return {
            'length': len(text),
            'word_count': len(text.split()),
            'has_articles': 'art.' in text.lower() or 'artigo' in text.lower(),
            'document_type': self._identify_document_type(text)
        }
    
    def _identify_document_type(self, text: str) -> str:
        """Identifica tipo básico do documento."""
        text_lower = text.lower()
        
        if 'lei' in text_lower:
            return 'Lei'
        elif 'decreto' in text_lower:
            return 'Decreto'
        elif 'portaria' in text_lower:
            return 'Portaria'
        elif 'resolução' in text_lower:
            return 'Resolução'
        else:
            return 'Documento Legal'
    
    def _get_timestamp(self) -> str:
        """Retorna timestamp da análise."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _consolidate_analyses(self, results: Dict) -> Dict[str, Any]:
        """
        Consolida resultados de múltiplas análises.
        
        Args:
            results (Dict): Resultados das análises individuais
            
        Returns:
            Dict[str, Any]: Análise consolidada
        """
        consolidation = {
            'overall_quality': self._calculate_overall_quality(results),
            'key_findings': self._extract_key_findings(results),
            'priority_recommendations': self._generate_priority_recommendations(results),
            'confidence_assessment': self._assess_overall_confidence(results)
        }
        
        return consolidation
    
    def _calculate_overall_quality(self, results: Dict) -> float:
        """Calcula qualidade geral baseada em todas as análises."""
        scores = []
        
        if 'legal_analysis' in results:
            scores.append(results['legal_analysis']['confidence_score'])
        
        if 'document_review' in results:
            scores.append(results['document_review']['quality_score'])
        
        if 'compliance_check' in results:
            scores.append(results['compliance_check']['overall_compliance']['score'])
        
        return sum(scores) / len(scores) if scores else 0.5
    
    def _extract_key_findings(self, results: Dict) -> List[str]:
        """Extrai principais descobertas de todas as análises."""
        findings = []
        
        if 'legal_analysis' in results:
            legal = results['legal_analysis']
            findings.append(f"Categoria jurídica: {legal['legal_category']}")
            findings.append(f"Tipo normativo: {legal['normative_type']}")
        
        if 'document_review' in results:
            review = results['document_review']
            if review['quality_score'] < 0.7:
                findings.append("Qualidade do documento requer atenção")
        
        if 'compliance_check' in results:
            compliance = results['compliance_check']
            if compliance['overall_compliance']['critical_actions_needed']:
                findings.append("Ações críticas de conformidade necessárias")
        
        return findings
    
    def _generate_priority_recommendations(self, results: Dict) -> List[str]:
        """Gera recomendações prioritárias baseadas em todas as análises."""
        recommendations = []
        
        # Coletar recomendações de cada agente
        if 'document_review' in results:
            recommendations.extend(results['document_review']['recommendations'])
        
        if 'compliance_check' in results:
            recommendations.extend(results['compliance_check']['compliance_recommendations'])
        
        # Remover duplicatas e priorizar
        unique_recommendations = list(set(recommendations))
        return unique_recommendations[:5]  # Top 5 recomendações
    
    def _assess_overall_confidence(self, results: Dict) -> Dict[str, Any]:
        """Avalia confiança geral da análise."""
        confidence_scores = []
        
        if 'legal_analysis' in results:
            confidence_scores.append(results['legal_analysis']['confidence_score'])
        
        if 'document_review' in results:
            confidence_scores.append(results['document_review']['quality_score'])
        
        if 'compliance_check' in results:
            confidence_scores.append(results['compliance_check']['overall_compliance']['score'])
        
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5
        
        return {
            'score': overall_confidence,
            'level': self._get_confidence_level(overall_confidence),
            'factors': self._identify_confidence_factors(results)
        }
    
    def _get_confidence_level(self, score: float) -> str:
        """Determina nível de confiança baseado na pontuação."""
        if score >= 0.8:
            return 'Muito Alta'
        elif score >= 0.6:
            return 'Alta'
        elif score >= 0.4:
            return 'Média'
        else:
            return 'Baixa'
    
    def _identify_confidence_factors(self, results: Dict) -> List[str]:
        """Identifica fatores que afetam a confiança da análise."""
        factors = []
        
        # Verificar qualidade da análise estrutural
        if 'legal_analysis' in results:
            patterns = results['legal_analysis'].get('structural_analysis', {}).get('legislative_patterns', {})
            if sum(patterns.values()) > 5:
                factors.append("Documento possui estrutura legislativa clara")
            else:
                factors.append("Estrutura legislativa limitada identificada")
        
        # Verificar completude do documento
        if 'document_review' in results:
            completeness = results['document_review']['completeness_check']['score']
            if completeness > 0.8:
                factors.append("Documento completo e bem estruturado")
            else:
                factors.append("Documento pode ter elementos ausentes")
        
        return factors


# Função de conveniência para análise rápida
def analyze_legal_document(text: str, analysis_type: str = 'completa') -> Dict[str, Any]:
    """
    Função de conveniência para análise rápida de documentos legislativos.
    
    Args:
        text (str): Texto do documento a ser analisado
        analysis_type (str): Tipo de análise desejada
        
    Returns:
        Dict[str, Any]: Resultado da análise
    """
    orchestrator = CrewAIOrchestrator()
    return orchestrator.analyze_document(text, analysis_type)


# Exportar classes principais
__all__ = [
    'BaseAgent',
    'LegalAnalysisAgent', 
    'DocumentReviewAgent',
    'ComplianceAgent',
    'CrewAIOrchestrator',
    'analyze_legal_document'
]