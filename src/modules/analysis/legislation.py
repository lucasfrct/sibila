# flake8: noqa: E501

    # 1. Lê o arquivo de constituiçao federal
    # 2. Quebra o texto em artigos
    #   2.1  Salva as palavras princials do artigo no banco de dados vetorial com o artigo em metadados
    #   2.3  Cria uma resumo do artigo
    #   2.4  Salva o resumo do artigo no banco de dados vetorial com o artigo no metadados
    #   2.5  Define keywords de assuntos e tópicos para o artigo
    #   2.6  Salva as keywords no banco de dados vetorial com o artigo no metadados
    #   2.7  Define 5 casos de uso para o artigo
    #   2.8  Salva os casos de uso no banco de dados vetorial com o artigo no metadados
    #   2.5  Defina 5 intenções expressas no artigo
    #   2.6  Salva as intenções no banco de dados vetorial com o artigo no metadados
    #   2.7  Define 5 ações possíveis para o artigo
    #   2.8  Salva as ações no banco de dados vetorial com o artigo no metadados
    #   2.9  Define 5 consequências possíveis para o artigo  
    #   2.10 Salva as consequências no banco de dados vetorial com o artigo no metadados
    #   2.11 Define 5 exceções para o artigo
    #   2.12 Salva as exceções no banco de dados vetorial com o artigo no metadados
    #   2.13 Define 5 obrigações para o artigo
    #   2.14 Salva as obrigações no banco de dados vetorial com o artigo no metadados
    #   2.15 Define 5 proibições para o artigo
    #   2.16 Salva as proibições no banco de dados vetorial com o artigo no metadados
    #   2.17 Define 5 permissões para o artigo
    #   2.18 Salva as permissões no banco de dados vetorial com o artigo no metadados
    #   2.19 Define 5 direitos para o artigo
    #   2.20 Salva os direitos no banco de dados vetorial com o artigo no metadados
    #   2.21 Define 5 deveres para o artigo
    #   2.22 Salva os deveres no banco de dados vetorial com o artigo no metadados
    #   2.23 Define 5 garantias para o artigo
    #   2.24 Salva as garantias no banco de dados vetorial com o artigo no metadados
    #   2.25 Define 5 sanções para o artigo
    #   2.26 Salva as sanções no banco de dados vetorial com o artigo no metadados
    #   2.27 Define 5 penalidades para o artigo
    #   2.28 Salva as penalidades no banco de dados vetorial com o artigo no metadados
    #   2.29 Define 5 responsabilidades para o artigo
    #   2.30 Salva as responsabilidades no banco de dados vetorial com o artigo no metadados
    #   2.31 Define 5 artigos relacionados para o artigo
    #   2.32 Salva o artigos no banco de dados vetorial com os artigos relacionados no metadados
    
    
from src.modules.analysis import federal_constitution_retrieval as FederalConstitutionRetrieval
import re

def federal_constitution():
    """ Constituiçao Federal: componente para buscar leis na constituiçao que tenham semelhança com o texto passado """
    return FederalConstitutionRetrieval

def split_into_articles(text: str):
    
    # Regex para capturar "Art. 9o" e "Art. 12"
    regex = re.compile(r'\bArt\.\s*\d+(?:o\b)?', re.IGNORECASE)
    
    articles = [] 
    content_current = [] 

    for line in text.splitlines():
        
        # Verifica se a linha é um novo artigo usando a regex
        match = regex.match(line)
        if match:
            articles.append('\n'.join(content_current))
            content_current = []
            content_current.append(line)
        else: 
            content_current.append(line)

    return articles




