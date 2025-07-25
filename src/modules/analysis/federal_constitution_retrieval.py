# flake8: noqa: E501

import logging
import traceback
from typing import List

from src.modules.database import chromadbvector
from src.modules.nlp.bow import relevant_words
from src.utils import string as String

COLLECTION = "federal_conctitution"

#################################################################
# COLEÇÂO: FEDERAL CONSTITUTION
#################################################################


def save_by_constellation(content: str, metadata: str) -> bool:
    """
    Salva uma constelação de palavras usando BoW (bag of words) com relevâcia >= a 3. 
    O texto completo fica salvo no meta data junto com a fonte de infromação

    Args:
        path (str): caminho em disco para o arquivo
        content (str): conteúdo em texto da página.

    Returns:
        bool: Retorna falso para quando há algum erro e true para dado salvo.
    """
    try:
        hash_id = String.hash(content)
        collection = chromadbvector.collection(COLLECTION)

        # verifica se o ID já existe na coleção
        if chromadbvector.conflict_id(collection, hash_id):
            return True

        keys = relevant_words(content)
        meta = {"content": content, 'metadata': metadata}
        collection.add(ids=[hash_id], documents=[keys], metadatas=[meta])
        return True
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")
        return False


def query_by_constellation(query: str = "", results: int = 5, threshold: float = 0.5) -> List[dict]:
    """
    Converte o termo de consulta numa constelação com BoW (bag of words) com relevãncia >= a 3.
    O retorno é uma conteúdo completo que represnta a consulta de termos 

    Args:
        query (str): A consulta a ser realizada no catálogo. Padrão é uma string vazia.
        results (int): O número de resultados a serem retornados. Padrão é 5.
        threshold (float): O limiar de similaridade para os resultados. Padrão é 0.5.

    Returns:
        List[dict]: List[dic]: { path: str, content: str }
    """
    try:
        collection = chromadbvector.collection(COLLECTION)
        return chromadbvector.query(collection, relevant_words(query), results, threshold)
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")
        return []


def save(content: str, metatada: str) -> bool:
    """
    salva o conteúdo
    O texto completo fica salvo no meta data junto com a fonte de infromação

    Args:
        path (str): caminho em disco para o arquivo
        content (str): conteúdo em texto da página.

    Returns:
        bool: Retorna falso para quando há algum erro e true para dado salvo.
    """
    try:

        hash_id = String.hash(content)
        collection = chromadbvector.collection(COLLECTION)

        # verifica se o ID já existe na coleção
        if chromadbvector.conflict_id(collection, hash_id):
            return True

        meta = {"content": content, "metadata": metatada}
        collection.add(ids=[hash_id], documents=[content], metadatas=[meta])
        return True
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")
        return False


def query(query: str = "", results: int = 5, threshold: float = 0.5) -> List[dict]:
    """
    Consulta por similaridade.

    Args:
        query (str): A consulta a ser realizada no catálogo. Padrão é uma string vazia.
        results (int): O número de resultados a serem retornados. Padrão é 5.
        threshold (float): O limiar de similaridade para os resultados. Padrão é 0.5.

    Returns:
        List[dict]: List[dic]: { path: content }
    """
    try:
        collection = chromadbvector.collection(COLLECTION)
        return chromadbvector.query(collection, query, results, threshold)
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")
        return []


def save_in_dimensions(content: str, metadata: str) -> bool:
    save(content, metadata)
    save_by_constellation(content, metadata)


def query_in_dimencions(question: str) -> List[dict]:

    docs = query(question)
    docs.extend(query_by_constellation(question))

    return docs


def catalog_article(article: dict):
    text = article['text']
    save_in_dimensions(text, text)
    save_in_dimensions(article['dates'], text)
    save_in_dimensions(article['subject'], text)
    save_in_dimensions(article['sumamry'], text)
    save_in_dimensions(article['entities'], text)
    save_in_dimensions(article['penalties'], text)
    save_in_dimensions(article['categories'], text)
    save_in_dimensions(article['definition'], text)
    save_in_dimensions(article['normativeTipe'], text)


def catalog_articles(articles: List[dict]):
    for article in articles:
        catalog_article(article)
