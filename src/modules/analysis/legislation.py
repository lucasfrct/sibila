# flake8: noqa: E501

import re
from typing import List

from src.models.ollama import ModelOllama

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
    llm = ModelOllama()
    llm.out_reduction_rate = 100.0
    llm.penalty_rate = 10.0
    llm.max_tokens = 100
    prompt = """
        /clear
        Deve retornar somente o titulo escolhido.
        Não comentar sobre o texto.
        Não responda com a palavra título.
        Não deve comecar com o artigo ou o numero.
        Elimine o titulo que não se encaixa com o texto.
    """
    question = f"""
        De forma objetiva, qual o título para o artigo: {text[0:512]}.
        O título de conter no máximo 8 palavras
        Responseda somente título escolhido.
        Remova o texto de saudação ou despedida ou descriçao.
    """
    response = llm.question(prompt=prompt, question=question).strip()
    return re.sub(r'[\n;.\'"]', '', response).strip()


def define_categories(text: str) -> str:
    llm = ModelOllama()
    llm.max_tokens = 100
    llm.out_focus = 10.0
    llm.penalty_rate = 2.0
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
    response = llm.question(prompt=prompt, question=question).strip()
    return re.sub(r'[\n;.-]', '', response).strip()


def define_the_normative_type(text: str):
    llm = ModelOllama()
    llm.max_tokens = 200
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
    response = llm.question(prompt=prompt, question=question)
    return re.sub(r'[\n;.-]', '', response).strip()


def extract_entities(text: str):
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
