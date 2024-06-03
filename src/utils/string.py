# flake8: noqa: E501

import re
from typing import List

def split_to_lines(content: str = "")-> List[str]:
    """quegra o conteúdo em linhas"""
    
    # Regex para identificar quebras de linha
    lines = re.split(r'\r?\n', content.strip())
    return [line.strip().encode('utf-8').decode('utf-8') for line in lines]

def split_to_phrases(content: str = "")-> List[str]:
    """transforms o conteúdo em freses"""
    
    # Regex para identificar pontos finais seguidos de um espaço ou fim da string
    phrases = re.split(r'(?<=\.)\s', content.strip())
    
    
    return [phrase.strip().encode('utf-8').decode('utf-8') for phrase in phrases]

def split_to_pargraphs(content: str = "") -> List[str]:
    """separa um texto em parágrafos"""
    
    paragraphs_split = re.split(r'(?:\r?\n){2,}', content.strip())
    paragraphs = []

    for paragraph in paragraphs_split:
        # Remove quebras de linha dentro dos parágrafos
        paragraph_unique = re.sub(r'\r?\n', ' ', paragraph).strip()
        paragraphs.append(paragraph_unique.encode('utf-8').decode('utf-8'))

    return paragraphs

def split_to_chunks(content: str = "", size: int = 1000)-> List[str]:
    """quebra o conteúdo em pedaços baseado em paragrafos"""
    
    paragraphs = split_to_pargraphs(content)
    chunks = []
    
    for paragraph in paragraphs:
        # transforma um parágrafo em chunks (pedaços de texto)
        cks = split_to_chunks_raw(paragraph.encode('utf-8').decode('utf-8'), size)
        chunks.extend(cks)
        
    return chunks

def split_to_chunks_raw(content: str = "", size: int = 1000) -> List[str]:
    """Quebra o texto em pedaços conforme definido"""
    
    # Regex para capturar chunks de tamanho específico
    pattern = re.compile(f'.{{1,{size}}}')
    return pattern.findall(content.encode('utf-8').decode('utf-8'))

def clean_lines(line: str = ""):
    """Limpa uma linha com muitos espços e saltos de \n"""
    
    return re.sub(r' +|\n+', ' ', line.encode('utf-8').decode('utf-8')).strip()
