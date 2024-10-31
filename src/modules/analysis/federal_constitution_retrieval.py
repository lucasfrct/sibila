# flake8: noqa: E501

import uuid
import logging
import traceback
from typing import List

from src.modules.database import chromadbvector
from src.modules.nlp.bow import relevant_words

COLLECTION = "federal_conctitution"

#################################################################
# COLEÇÂO: FEDERAL CONSTITUTION
#################################################################

def save(path: str = "", name: str = "Constituição Federal do Brasil", page: int = 1,  content: str = "") -> bool:
    """
    Salva uma BoW (bag of words) com relevâcia >= a 3 dá páginas para uma busca por similaridade. 
    O texto completo fica salvo no meta data junto com a fonte de infromação

    Args:
        path (str): caminho em disco para o arquivo
        name (str): nome do documento.
        page (int): página do documento.
        content (str): conteúdo em texto da página.

    Returns:
        bool: Retorna falso para quando há algum erro e true para dado salvo.
    """
    try:
        meta = { "path": path, "name": name, "page": page, "source":  f"{name}, pg. {page}", "content": content }
        collection = chromadbvector.collection(COLLECTION)
        collection.add(documents=[relevant_words(content)], metadatas=meta, ids=str(uuid.uuid4()))
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def query(query: str = "", results: int = 5, cut: float = 1.2) -> List[dict]:
    """
    Consulta por similaridade convertendo o texto para uma BoW (bag of words) com relevâcia >= a 3.
    O retorno esperado é a páginas da constituição. 

    Args:
        query (str): texto da consulta (texto trecho da constituição)
        results (int): numero de documentos (páginas) que devem ser retornrnados 
        cut (float): corte superior da distancia (proxidade) do documento pesquisado.
        
    Returns:
        List[dict]: List[dic]: | dict: { id, distance, keys, path, name, page, source, content } | 
        Retorna uma lista de páginas da constinuição.
    """
    try:
        collection = chromadbvector.collection(COLLECTION)
        result = collection.query(query_texts=[f"{query} {relevant_words(query)}"], n_results=results)
        return chromadbvector.result_to_dict(result, cut)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []




