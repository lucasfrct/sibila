# flake8: noqa: E501

import re
from typing import List

from src.models.ollama import ModelOllama


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
    "Emenda Constitucional",
]

nomatives = [
    "Plena: Norma que trata de um assunto de forma completa e definitiva.",
    "Limitada: Norma que trata de um assunto de forma parcial.",
    "Continda: Norma que complementa outra norma.",
]


def split_into_articles(text: str)-> List[str]:
    """
    Divide o texto em artigos com base em uma expressão regular que identifica 
    linhas que começam com "Art." seguido de um número.
    Args:
        text (str): O texto completo que será dividido em artigos.
    Returns:
        list: Uma lista de strings, onde cada string representa um artigo separado.
    """

    # Regex para capturar "Art. 9o" e "Art. 12"
    regex = re.compile(r'\bArt\.\s*\d+(?:o\b)?', re.IGNORECASE)

    articles_raw: List[str] = []
    content_current: List[str] = []

    for line in text.splitlines():

        # Verifica se a linha é um novo artigo usando a regex
        match = regex.match(line)
        if match:
            content_art = '\n'.join(content_current).strip()
            articles_raw.append(content_art)
            content_current = []
            content_current.append(line)
        else:
            content_current.append(line)

    articles: List[str] = []
    for article in articles_raw:
        if article.strip().lower().startswith('art'):
            articles.append(article)
            
    return articles


def set_a_title(text: str) -> str:
    llm = ModelOllama()
    prompt = """
        /clear
        O título de conter no máximo 8 palavras
        Elimine o titulo que não se encaixa com o texto.
        Deve retornar somente o titulo escolhido.
        Não comentar sobre o texto.
        Não responda com a palavra título.
        Não deve comecar com o artigo ou o numero.
    """
    question = f"""
        De forma objetiva, qual o título para o artigo: {text[0:512]}.
        Responseda somente título escolhido.
        Remova o texto de saudação ou despedida ou descriçao.
    """
    response = llm.question(prompt=prompt, question=question).strip()
    return re.sub(r'[\n;.\'"]', '', response).strip()


def define_categories(text: str) -> str:
    llm = ModelOllama()
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
    
    # - exemplo: (EC no 19/98)
    prompt = f"""
        /clear
        Lista de tipos de normativos: 
        {"\n ".join(normative_types)}
        Não inventar tipo normativo quando não conseguir relacionar.
        Elimine o normativo que não se encaixa.
        Não deve explicar o que é um normativo.
    """

    question = f"""
        Classifique um tipo normativo para o seguinte texto: '{text}'.
        Retorne somente um do normativo.
        Remova o texto de saudação ou despedida.
        Se não hover categoria retorne: '-'
    """
    response = llm.question(prompt=prompt, question=question)
    return re.sub(r'[\n;.-]', '', response).strip()


def extract_entities(text: str):
    llm = ModelOllama()
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
    response = llm.question(prompt=prompt, question=question).replace('\n', '').strip()
    return re.sub(r'[\n;.-]', '', response).strip()


def summarize(text: str):
    llm = ModelOllama()
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