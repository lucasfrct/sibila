# flake8: noqa: E501

import re
from typing import List, Dict, Tuple

from src.models.ollama import ModelOllama
from src.modules.nlp.featureextractor import FeatureExtractor
from src.modules.nlp.sentiment import sentiment_analysis, sentiment_noun_phrases, sentiment_tags

# Importação condicional do Docling
try:
    from src.modules.document.docling_reader import extract_structured_content
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False


categories = [
    "Direito Constitucional: Leis relacionadas à organização do Estado e aos direitos fundamentais dos cidadãos.",
    "Direito Internacional: Normas que regem as relações entre países e organismos internacionais.",
    "Direito Trabalhista: Leis que regulam as relações de trabalho e direitos dos trabalhadores.",
    "Direito Civil: Regras que regem as relações privadas, como contratos, obrigações e família.",
    "Direito Processual: Normas que regulam os procedimentos judiciais e administrativos.",
    "Direito Comercial/Empresarial: Regras sobre atividades comerciais e empresariais.",
    "Direito Administrativo: Regula a atuação da administração pública e seus agentes.",
    "Direito Tributário: Normas sobre a arrecadação de tributos pelo Estado.",
    "Direito Ambiental: Normas que visam à proteção do meio ambiente.",
    "Direito Penal: Normas que tratam de crimes e punições.",
]

normative_types = [
    "Lei",
    "Decreto",
    "Portaria",
    "Despacho",
    "Circular",
    "Resolução",
    "Deliberação",
    "Regulamento",
    "Lei Ordinária",
    "Ato Normativo",
    "Lei Complementar",
    "Medida Provisória",
    "Instrução Normativa",
    "Emenda Constitucional: sigla EC",
]

nomatives = [
    "Plena: Norma que trata de um assunto de forma completa e definitiva.",
    "Limitada: Norma que trata de um assunto de forma parcial.",
    "Continda: Norma que complementa outra norma.",
]


class LegislationAnalyzer:
    """
    Classe para análise aprimorada de textos legislativos combinando 
    ferramentas NLP tradicionais com análise por LLM.
    """
    
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.llm = ModelOllama()
        self._setup_llm()
    
    def _setup_llm(self):
        """Configura parâmetros padrão do LLM para análise legislativa."""
        self.llm.out_reduction_rate = 100.0
        self.llm.penalty_rate = 5.0
        self.llm.max_tokens = 200
    
    def analyze_text_structure(self, text: str) -> Dict:
        """
        Analisa a estrutura do texto usando NLP para extrair características.
        Versão simplificada que evita problemas de dependência.
        
        Args:
            text (str): Texto a ser analisado
            
        Returns:
            dict: Análise estrutural com entidades, tags e características
        """
        try:
            # Usar feature extractor para análise simples
            analysis = self.feature_extractor.syntax_analisys(text)
        except Exception:
            # Fallback para análise básica se houver erro
            analysis = {'tokens': [], 'entities': [], 'tags': []}
        
        # Análise de sentimento
        try:
            sentiment = sentiment_analysis(text)
            noun_phrases = sentiment_noun_phrases(text)
            pos_tags = sentiment_tags(text)
        except Exception:
            sentiment = "Neutral"
            noun_phrases = []
            pos_tags = []
        
        # Identificar padrões legislativos
        legislative_patterns = self._identify_legislative_patterns(text)
        
        return {
            'nlp_analysis': analysis,
            'sentiment': sentiment,
            'noun_phrases': noun_phrases,
            'pos_tags': pos_tags,
            'legislative_patterns': legislative_patterns,
            'confidence_score': self._calculate_confidence(analysis, legislative_patterns)
        }
    
    def _identify_legislative_patterns(self, text: str) -> Dict:
        """Identifica padrões específicos de textos legislativos."""
        patterns = {
            'article_references': len(re.findall(r'\bart\.?\s*\d+', text, re.IGNORECASE)),
            'paragraph_markers': len(re.findall(r'§\s*\d+', text)),
            'law_references': len(re.findall(r'lei\s+n[ºº°]?\s*\d+', text, re.IGNORECASE)),
            'dates': len(re.findall(r'\d{1,2}[\/\.-]\d{1,2}[\/\.-]\d{2,4}', text)),
            'roman_numerals': len(re.findall(r'\b[IVX]+\b', text)),
            'legal_verbs': len(re.findall(r'\b(estabelece|determina|regulamenta|dispõe|revoga|altera)\b', text, re.IGNORECASE))
        }
        return patterns
    
    def _calculate_confidence(self, nlp_analysis: Dict, patterns: Dict) -> float:
        """
        Calcula score de confiança baseado na análise NLP e padrões identificados.
        
        Args:
            nlp_analysis (dict): Resultado da análise NLP
            patterns (dict): Padrões legislativos identificados
            
        Returns:
            float: Score de confiança entre 0 e 1
        """
        confidence = 0.5  # Base confidence
        
        # Aumentar confiança baseado em padrões legislativos
        if patterns['article_references'] > 0:
            confidence += 0.2
        if patterns['paragraph_markers'] > 0:
            confidence += 0.1
        if patterns['law_references'] > 0:
            confidence += 0.1
        if patterns['legal_verbs'] > 0:
            confidence += 0.1
            
        # Considerar qualidade da análise NLP
        if 'entities' in nlp_analysis and nlp_analysis['entities']:
            confidence += 0.1
            
        return min(confidence, 1.0)
    
    def validate_category_with_nlp(self, text: str, proposed_category: str) -> Tuple[str, float]:
        """
        Valida categoria proposta usando análise NLP.
        
        Args:
            text (str): Texto do artigo
            proposed_category (str): Categoria proposta pelo LLM
            
        Returns:
            tuple: (categoria_validada, score_confiança)
        """
        analysis = self.analyze_text_structure(text)
        
        # Palavras-chave por categoria
        category_keywords = {
            'Direito Constitucional': ['constituição', 'fundamental', 'estado', 'cidadão', 'direitos'],
            'Direito Trabalhista': ['trabalho', 'empregado', 'salário', 'jornada', 'sindicato'],
            'Direito Civil': ['contrato', 'família', 'propriedade', 'obrigação', 'civil'],
            'Direito Penal': ['crime', 'pena', 'prisão', 'delito', 'punição'],
            'Direito Tributário': ['tributo', 'imposto', 'taxa', 'contribuição', 'arrecadação'],
            'Direito Ambiental': ['ambiente', 'poluição', 'recursos', 'sustentável', 'ecológico'],
            'Direito Administrativo': ['administração', 'público', 'servidor', 'processo', 'órgão']
        }
        
        text_lower = text.lower()
        confidence_scores = {}
        
        for category, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            confidence_scores[category] = score / len(keywords)
        
        # Encontrar melhor categoria baseada em keywords
        best_nlp_category = max(confidence_scores, key=confidence_scores.get)
        best_score = confidence_scores[best_nlp_category]
        
        # Validar se categoria proposta faz sentido
        proposed_cleaned = proposed_category.split(':')[0].strip()
        nlp_confidence = confidence_scores.get(proposed_cleaned, 0)
        
        # Usar categoria NLP se score for significativamente melhor
        if best_score > 0.3 and best_score > nlp_confidence * 1.5:
            return best_nlp_category, best_score
        elif nlp_confidence > 0.2:
            return proposed_category, nlp_confidence
        else:
            return proposed_category, analysis['confidence_score']
    
    def extract_entities_enhanced(self, text: str) -> List[str]:
        """
        Extração de entidades aprimorada combinando NLP e análise semântica.
        Versão robusta que lida com erros de dependência.
        
        Args:
            text (str): Texto para extração de entidades
            
        Returns:
            list: Lista de entidades identificadas
        """
        all_entities = []
        
        try:
            # Análise NLP para entidades
            nlp_analysis = self.feature_extractor.syntax_analisys(text)
            nlp_entities = nlp_analysis.get('entity', [])
            all_entities.extend(nlp_entities)
            
            # Filtrar entidades relevantes (substantivos, nomes próprios)
            if 'tags' in nlp_analysis:
                for word, tag in nlp_analysis['tags']:
                    if tag in ['NNP', 'NNPS', 'NN', 'NNS'] and len(word) > 2:
                        all_entities.append(word)
        except Exception:
            # Se análise NLP falhar, usar regex simples
            import re
            # Encontrar palavras capitalizadas (possíveis entidades)
            capitalized_words = re.findall(r'\b[A-Z][a-z]+\b', text)
            all_entities.extend(capitalized_words)
        
        try:
            # Combinar com noun phrases
            noun_phrases = sentiment_noun_phrases(text)
            all_entities.extend(list(noun_phrases))
        except Exception:
            pass
        
        # Unir e filtrar resultados
        all_entities = list(set(all_entities))
        
        # Filtrar entidades muito comuns em textos legislativos
        stop_entities = {'lei', 'artigo', 'parágrafo', 'inciso', 'alínea', 'art', 'texto', 'Art'}
        filtered_entities = [e for e in all_entities if e.lower() not in stop_entities and len(e) > 2]
        
        return filtered_entities[:5]  # Retornar top 5 entidades


# Instância global do analisador
_analyzer = LegislationAnalyzer()


def split_into_articles(text: str) -> List[str]:
    """
    Divide o texto em artigos com base em uma expressão regular aprimorada que identifica 
    linhas que começam com "Art." seguido de um número, capturando o artigo completo
    incluindo parágrafos, incisos e alíneas até o próximo artigo.
    Args:
        text (str): O texto completo que será dividido em artigos.
    Returns:
        list: Uma lista de strings, onde cada string representa um artigo completo com
              todos os seus componentes (parágrafos, incisos, alíneas).
    """

    # Regex aprimorada para capturar "Art. 9º", "Art. 12", "Artigo 9º", etc.
    regex = re.compile(r'^\s*(?:Art\.?|Artigo)\s*\d+(?:[ºº°]|o)?\b', re.IGNORECASE | re.MULTILINE)

    articles_raw: List[str] = []
    content_current: List[str] = []

    for line in text.splitlines():
        line_stripped = line.strip()
        
        # Verifica se a linha é um novo artigo usando a regex
        match = regex.match(line)
        if match:
            # Se já temos conteúdo acumulado, adiciona à lista de artigos
            if content_current:
                content_art = '\n'.join(content_current).strip()
                if content_art:  # Só adiciona se não estiver vazio
                    articles_raw.append(content_art)
            
            # Inicia um novo artigo
            content_current = [line]
        else:
            # Adiciona linha ao artigo atual
            content_current.append(line)

    # Adiciona o último artigo se existir
    if content_current:
        content_art = '\n'.join(content_current).strip()
        if content_art:
            articles_raw.append(content_art)

    # Filtra apenas artigos válidos que começam com "Art" ou "Artigo"
    articles: List[str] = []
    for article in articles_raw:
        article_clean = article.strip()
        if article_clean and regex.match(article_clean):
            articles.append(article)

def split_into_articles_enhanced(text: str, document_path: str = None) -> List[str]:
    """
    Versão aprimorada que utiliza Docling para melhor extração de artigos quando disponível.
    Extrai artigos completos com todos os componentes estruturais (parágrafos, incisos, alíneas).
    
    Args:
        text (str): O texto completo que será dividido em artigos.
        document_path (str, optional): Caminho do documento para análise estruturada com Docling.
    
    Returns:
        list: Uma lista de strings, onde cada string representa um artigo completo.
    """
    
    # Se Docling estiver disponível e tivermos um caminho de arquivo, usar análise estruturada
    if DOCLING_AVAILABLE and document_path:
        try:
            structured_content = extract_structured_content(document_path)
            return _extract_articles_from_structured_content(structured_content, text)
        except Exception:
            # Fallback para método básico se Docling falhar
            pass
    
    # Usar método básico aprimorado
    return split_into_articles(text)


def _extract_articles_from_structured_content(structured_content: dict, fallback_text: str) -> List[str]:
    """
    Extrai artigos do conteúdo estruturado fornecido pelo Docling.
    
    Args:
        structured_content (dict): Conteúdo estruturado do Docling.
        fallback_text (str): Texto para fallback se a extração estruturada falhar.
    
    Returns:
        list: Lista de artigos extraídos.
    """
    
    if not structured_content or 'texts' not in structured_content:
        return split_into_articles(fallback_text)
    
    # Regex aprimorada para identificar artigos
    article_regex = re.compile(r'^\s*(?:Art\.?|Artigo)\s*\d+(?:[ºº°]|o)?\b', re.IGNORECASE | re.MULTILINE)
    
    articles: List[str] = []
    current_article: List[str] = []
    
    # Organizar textos por página para manter ordem
    texts_by_page = {}
    for text_item in structured_content['texts']:
        page = text_item.get('page', 1) or 1
        if page not in texts_by_page:
            texts_by_page[page] = []
        texts_by_page[page].append(text_item['text'])
    
    # Processar textos em ordem de página
    all_texts = []
    for page in sorted(texts_by_page.keys()):
        all_texts.extend(texts_by_page[page])
    
    for text_block in all_texts:
        lines = text_block.split('\n')
        
        for line in lines:
            line_stripped = line.strip()
            
            # Verificar se é início de um novo artigo
            if article_regex.match(line_stripped):
                # Salvar artigo anterior se existir
                if current_article:
                    article_content = '\n'.join(current_article).strip()
                    if article_content:
                        articles.append(article_content)
                
                # Iniciar novo artigo
                current_article = [line]
            elif current_article:  # Se estamos dentro de um artigo
                # Adicionar linha ao artigo atual
                current_article.append(line)
    
    # Adicionar último artigo se existir
    if current_article:
        article_content = '\n'.join(current_article).strip()
        if article_content:
            articles.append(article_content)
    
    # Se não encontramos artigos com método estruturado, usar fallback
    if not articles:
        return split_into_articles(fallback_text)
    
    return articles


def extract_article_components(article_text: str) -> dict:
    """
    Extrai componentes estruturais de um artigo (caput, parágrafos, incisos, alíneas).
    
    Args:
        article_text (str): Texto do artigo completo.
    
    Returns:
        dict: Dicionário com componentes do artigo organizados.
    """
    
    components = {
        'caput': '',
        'paragraphs': [],  # Parágrafos (§)
        'items': [],       # Incisos (I, II, III)
        'subitems': [],    # Alíneas (a, b, c)
        'full_text': article_text
    }
    
    lines = article_text.split('\n')
    current_section = 'caput'
    current_content = []
    
    # Regex para identificar diferentes componentes
    paragraph_regex = re.compile(r'^\s*§\s*\d+[ºº°]?', re.IGNORECASE)
    paragraph_unique_regex = re.compile(r'^\s*Parágrafo\s+único', re.IGNORECASE)
    item_regex = re.compile(r'^\s*[IVX]+\s*[-–]', re.IGNORECASE)
    subitem_regex = re.compile(r'^\s*[a-z]\)\s*', re.IGNORECASE)
    
    for line in lines:
        line_stripped = line.strip()
        
        if paragraph_regex.match(line_stripped) or paragraph_unique_regex.match(line_stripped):
            # Salvar seção anterior
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
            
            # Iniciar novo parágrafo
            current_section = 'paragraph'
            current_content = [line]
            
        elif item_regex.match(line_stripped):
            # Salvar seção anterior
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
            
            # Iniciar novo inciso
            current_section = 'item'
            current_content = [line]
            
        elif subitem_regex.match(line_stripped):
            # Salvar seção anterior
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
            
            # Iniciar nova alínea
            current_section = 'subitem'
            current_content = [line]
            
        else:
            # Continuar seção atual
            current_content.append(line)
    
    # Salvar última seção
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


def set_a_title(text: str) -> str:
    """
    Versão aprimorada que usa análise NLP para identificar palavras-chave
    e gerar títulos mais precisos.
    """
    # Análise NLP para extrair características importantes
    nlp_analysis = _analyzer.analyze_text_structure(text)
    
    # Extrair palavras-chave do texto usando TF-IDF e entidades
    keywords = []
    if 'nlp_analysis' in nlp_analysis and 'hot' in nlp_analysis['nlp_analysis']:
        hot_words = list(nlp_analysis['nlp_analysis']['hot'].keys())[:3]
        keywords.extend(hot_words)
    
    # Adicionar noun phrases relevantes
    if 'noun_phrases' in nlp_analysis:
        relevant_phrases = [str(phrase) for phrase in nlp_analysis['noun_phrases']][:2]
        keywords.extend(relevant_phrases)
    
    # Usar keywords como contexto para o LLM
    keywords_context = ', '.join(keywords) if keywords else ''
    
    llm = ModelOllama()
    llm.out_reduction_rate = 100.0
    llm.penalty_rate = 10.0
    llm.max_tokens = 100
    
    prompt = f"""
        /clear
        Deve retornar somente o titulo escolhido.
        Não comentar sobre o texto.
        Não responda com a palavra título.
        Não deve comecar com o artigo ou o numero.
        Elimine o titulo que não se encaixa com o texto.
        {f'Palavras-chave importantes: {keywords_context}' if keywords_context else ''}
    """
    
    question = f"""
        De forma objetiva, qual o título para o artigo: {text[0:512]}.
        O título de conter no máximo 8 palavras
        Responseda somente título escolhido.
        Remova o texto de saudação ou despedida ou descriçao.
        {f'Use as palavras-chave: {keywords_context}' if keywords_context else ''}
    """
    
    response = llm.question(prompt=prompt, question=question).strip()
    title = re.sub(r'[\n;.\'"]', '', response).strip()
    
    # Validar qualidade do título
    if len(title.split()) > 8:
        # Se título muito longo, tentar encurtar usando apenas keywords
        if keywords:
            short_title = ' '.join(keywords[:4])
            return short_title.title() if short_title else title[:50]
    
    return title


def define_categories(text: str) -> str:
    """
    Versão aprimorada que combina análise NLP com LLM para maior precisão.
    Identifica categorias de legislação com validação estatística.
    """
    llm = ModelOllama()
    llm.max_tokens = 100
    llm.out_focus = 10.0
    llm.penalty_rate = 2.0
    
    # Primeiro, fazer análise NLP para validação
    nlp_analysis = _analyzer.analyze_text_structure(text)
    
    prompt = f"""
        /clear
        Responda com objetividade somente categorias informadas.
        Elimine a categoria que não se encaixa.
        Categorias de legislação:
        {"\n ".join(categories)}
    """

    question = f"""
        Escolha de forma precisa e estrita uma ou mais categorias para o artigo: '{text}'
        Forneça as categorias separadas por vírgula.
        Prefira sempre escolher a categoria mais específica.
        Se não hover categoria retorne: '-'
        Remova o texto de saudação ou despedida.
    """
    
    # Obter resposta do LLM
    llm_response = llm.question(prompt=prompt, question=question).strip()
    llm_category = re.sub(r'[\n;.-]', '', llm_response).strip()
    
    # Validar com análise NLP
    validated_category, confidence = _analyzer.validate_category_with_nlp(text, llm_category)
    
    # Se confiança for muito baixa, retornar análise conservadora
    if confidence < 0.3:
        return '-'
    
    return validated_category


def define_the_normative_type(text: str):
    """
    Versão aprimorada que combina análise de padrões textuais com LLM 
    para identificação mais precisa do tipo normativo.
    """
    # Análise de padrões para identificar tipo normativo
    text_lower = text.lower()
    
    # Padrões específicos por tipo normativo
    type_patterns = {
        'Lei': ['lei n', 'lei ordinária', 'lei complementar'],
        'Decreto': ['decreto n', 'decreto-lei'],
        'Portaria': ['portaria n', 'portaria'],
        'Medida Provisória': ['medida provisória', 'mp n'],
        'Emenda Constitucional': ['emenda constitucional', 'ec n', 'emenda à constituição'],
        'Resolução': ['resolução n'],
        'Instrução Normativa': ['instrução normativa', 'in n'],
        'Circular': ['circular n'],
        'Deliberação': ['deliberação n']
    }
    
    # Verificar padrões
    pattern_scores = {}
    for norm_type, patterns in type_patterns.items():
        score = sum(1 for pattern in patterns if pattern in text_lower)
        if score > 0:
            pattern_scores[norm_type] = score
    
    # Se encontramos padrão claro, usar resultado direto
    if pattern_scores:
        best_pattern_type = max(pattern_scores, key=pattern_scores.get)
        if pattern_scores[best_pattern_type] >= 1:
            return best_pattern_type
    
    # Usar LLM para casos ambíguos
    llm = ModelOllama()
    llm.max_tokens = 150
    llm.out_focus = 10.0
    llm.penalty_rate = 2.0

    prompt = f"""
        /clear
        Lista de tipos de normativos:
        {"\n ".join(normative_types)}
        Não inventar tipo normativo quando não conseguir relacionar.
        Elimine o normativo que não se encaixa.
        Não deve explicar o que é um normativo.
        A sigla EC siginifica emenda constitucional.
    """

    question = f"""
        Classifique um tipo normativo para o seguinte texto: '{text}'.
        Retorne somente um do normativo.
        Remova o texto de saudação ou despedida.
        Se não hover normativo, retorne: Lei
    """
    
    llm_response = llm.question(prompt=prompt, question=question)
    llm_result = re.sub(r'[\n;.-]', '', llm_response).strip()
    
    # Validar resposta do LLM
    valid_types = [t.split(':')[0].strip() for t in normative_types]
    if llm_result in valid_types:
        return llm_result
    
    # Fallback para análise de padrão ou Lei como padrão
    return best_pattern_type if pattern_scores else 'Lei'


def extract_entities(text: str):
    """
    Versão aprimorada que combina análise NLP com LLM para extração de entidades.
    Reduz falsos positivos através de validação estatística.
    """
    # Primeiro extrair entidades usando NLP
    nlp_entities = _analyzer.extract_entities_enhanced(text)
    
    # Se temos entidades confiáveis do NLP, usar como base
    if nlp_entities:
        # Validar com LLM apenas as entidades encontradas
        llm = ModelOllama()
        llm.max_tokens = 150
        llm.out_focus = 10.0
        llm.penalty_rate = 2.0
        
        entities_text = ', '.join(nlp_entities)
        prompt = """
            /clear
            Valide as entidades encontradas em texto legislativo.
            Mantenha apenas entidades relevantes como: Pessoas, empresas e órgãos públicos.
            Remova entidades genéricas ou muito comuns.
        """
        question = f"""
            Das seguintes entidades encontradas: {entities_text}
            Retorne apenas as mais relevantes para análise legislativa, separadas por vírgula.
            Máximo 3 entidades.
            Se nenhuma for relevante, retorne: '-'
        """
        
        validated_response = llm.question(prompt=prompt, question=question).replace('\n', '').strip()
        return validated_response if validated_response and validated_response != '-' else ', '.join(nlp_entities[:3])
    
    # Fallback para método original se NLP não encontrar entidades
    llm = ModelOllama()
    llm.max_tokens = 200
    llm.out_focus = 10.0
    llm.penalty_rate = 2.0
    prompt = """
        /clear
        Extraia do texto somente as entidades presentes.
        Exemplo de entidades: Pessoas, empresas e órgãos públicos.
    """
    question = f"""
        Retorne no máximo 3 das entidades presentes no texto: '{text}'.
        Responda com objetividade somente os nomes entidades encontradas separadas por vírgula.
        Remova o texto de saudação ou despedida.
        Se não houver entidade retorne: '-'
    """
    return llm.question(prompt=prompt, question=question).replace('\n', '').strip()


def extract_the_penalties(text: str):
    llm = ModelOllama()
    llm.max_tokens = 200
    llm.out_focus = 10.0
    llm.penalty_rate = 2.0
    prompt = """
        /clear
        Extraia do texto somente as penalidades presentes.
        Exemplo de penalidades: Multas, prisão e advertências.
        Responda com objetividade somente penalidades encontradas.
    """
    question = f"""
        Retorne as penalidades presentes no texto: '{text}'.
        Remova o texto de saudação ou despedida.
        Se não houver penalidade retorne: '-'
    """
    return llm.question(prompt=prompt, question=question).replace('\n', '').strip()


def define_the_legal_terms(text: str):
    llm = ModelOllama()
    llm.max_tokens = 1000
    llm.out_focus = 8.0
    llm.penalty_rate = 1.5
    prompt = """
        /clear
        Extraia do texto somente os termos jurídicos incomuns.
        Reponda objetivamente com o termo.
        A resposta deve estar no fomato: 
        '   1. termo: explicação. 
            2. termo: explicação.
        '
    """
    question = f"""
        /clear
        Retorne no máximo 3 termos jurídicos presentes no texto: '{text}'.
        Para cada termo forneça uma explicação curta.
        Repara os termos por vírgula.
        Remova o texto de saudação ou despedida.
        Se não houver termo retorne: '-'
    """
    return llm.question(prompt=prompt, question=question).replace('\n', '').strip()


def extract_legal_dates_and_deadlines(text: str):
    """
    Versão aprimorada que combina regex para extração precisa de datas 
    com validação por LLM, reduzindo falsos positivos.
    """
    # Padrões regex mais precisos para datas e prazos
    date_patterns = [
        r'\d{1,2}[\/\.-]\d{1,2}[\/\.-]\d{2,4}',  # DD/MM/YYYY
        r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}',     # DD de mês de YYYY
        r'\w+\s+de\s+\d{4}',                     # mês de YYYY
        r'\d{1,2}\s+\w+\s+\d{4}'                # DD mês YYYY
    ]
    
    deadline_patterns = [
        r'\d+\s+(?:dias?|meses?|anos?)',         # X dias/meses/anos
        r'prazo\s+de\s+\d+\s+(?:dias?|meses?|anos?)',  # prazo de X dias
        r'até\s+\d+\s+(?:dias?|meses?|anos?)',   # até X dias
        r'no\s+prazo\s+de\s+\d+',               # no prazo de X
        r'dentro\s+de\s+\d+\s+(?:dias?|meses?|anos?)'  # dentro de X dias
    ]
    
    found_dates = []
    found_deadlines = []
    
    # Extrair datas usando regex
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        found_dates.extend(matches)
    
    # Extrair prazos usando regex
    for pattern in deadline_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        found_deadlines.extend(matches)
    
    # Combinar resultados regex
    regex_results = found_dates + found_deadlines
    
    # Se encontramos datas/prazos por regex, validar com LLM
    if regex_results:
        # Limitar a 5 resultados mais relevantes
        top_results = list(set(regex_results))[:5]
        
        llm = ModelOllama()
        llm.max_tokens = 150
        llm.out_focus = 10.0
        llm.penalty_rate = 2.0
        
        results_text = ', '.join(top_results)
        prompt = """
            /clear
            Valide as datas e prazos encontrados em texto legislativo.
            Mantenha apenas datas/prazos legalmente relevantes.
            Remova referências a artigos ou números sem contexto temporal.
        """
        question = f"""
            Das seguintes datas/prazos encontrados: {results_text}
            Retorne apenas os relevantes para análise legislativa.
            Se nenhum for relevante, retorne: '-'
        """
        
        validated = llm.question(prompt=prompt, question=question).replace('\n', '').strip()
        
        if validated and validated != '-':
            return re.sub(r'[\n;.-]', '', validated).strip()
        else:
            # Se LLM rejeita, mas regex encontrou, retornar resultado limpo
            return ', '.join(top_results) if top_results else '-'
    
    # Fallback para método original se regex não encontrar nada
    llm = ModelOllama()
    llm.max_tokens = 200
    llm.out_focus = 10.0
    llm.penalty_rate = 2.0
    prompt = """
        /clear
        Encontre as datas ou prazos no texto.    
        As datas ou prazos podem estar em formatos numéricos como: 'DD/MM/AAAA ou DD.MM.AAAA' de exemplo.
        As datas ou prazos podem estar em textos como: '12 de março de 2021' de exemplo. 
        As datas ou prazos podem ser números seguidos de unidades de tempo como: 'dias', 'meses', 'anos' de exemplo. 
        Desconsidere números de artigos ou numeros sem vinculo com prazos ou datas.
        Desconsidere os algarismos romanos.
    """
    question = f"""
        Remova o texto de saudação ou despedida.
        Forneça somente as datas ou prazos diretamente.
        Encontre datas ou prazos no seguite texto: '{text}'
        Não invente datas ou prazos.
        Se não houver data ou prazo retorne: '-'
    """
    response = llm.question(
        prompt=prompt, question=question).replace('\n', '').strip()
    return re.sub(r'[\n;.-]', '', response).strip()


def summarize(text: str):
    llm = ModelOllama()
    llm.max_tokens = 300
    llm.diversification_rate = 0.9
    prompt = """
        /clear
        Um resumo deve conter menos de 20 por cento do texto original.
        Tente extrair apenas a essência do texto em invenções ou rodeios.
        Responda com objetividade um resumo do artigo.
        Revise o resumo para garantir que não ultrapasse 20% do texto original.
    """
    question = f"""
        Retorne somente um resumo do artigo: '{text}'.
        O resumo deve ser em lingugem simples e menos jurídica.
        Remova o texto de saudação ou despedida.
        Revise o resumo para garantir que não contenha informações falsas.
    """
    return llm.question(prompt=prompt, question=question).strip()
