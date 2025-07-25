# flake8: noqa: E501

import logging
import traceback
from typing import List

from src.modules.catalog.catalog import Catalog
from src.modules.database import chromadbvector
from src.modules.nlp.bow import relevant_words
from src.utils import string as String

COLLECTION = "catalogs"

#################################################################
# TABLE CATALOGS
#################################################################


def save(catalog: Catalog, content: str = "") -> bool:
    """
    Salva o conteúdo do item no catálogo.
    Args:
        catalog (Catalog): O item do catálogo onde o conteúdo será salvo.
        content (str, opcional): O conteúdo a ser salvo no catálogo. Padrão é uma string vazia.
    Returns:
        bool: Retorna True se o conteúdo foi salvo com sucesso ou se o ID já existe na coleção, 
              caso contrário, retorna False.
    """
    try:
        hash_id = String.hash(content)
        collection = chromadbvector.collection(COLLECTION)

        # verifica se o ID já existe na coleção
        if chromadbvector.conflict_id(collection, hash_id):
            return True

        keys = relevant_words(content)
        meta = {"hash": hash_id, "path": catalog.path, "title": catalog.title, "name": catalog.name, "page": catalog.page,
                "source":  f"{catalog.name}, pg. {catalog.page}", "content": content, "keys": keys}
        collection.add(ids=[hash_id], documents=[content], metadatas=[meta])
        return True
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")
        return False


def query(query: str = "", results: int = 5, threshold: float = 0.5) -> List[dict]:
    """
    Consulta no catálogo.

    Args:
        query (str): A consulta a ser realizada no catálogo. Padrão é uma string vazia.
        results (int): O número de resultados a serem retornados. Padrão é 5.
        threshold (float): O limiar de similaridade para os resultados. Padrão é 0.5.

    Returns:
        List[dict]: Uma lista de dicionários contendo os resultados da consulta.
    """
    try:
        collection = chromadbvector.collection(COLLECTION)
        return chromadbvector.query(collection, query, results, threshold)
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")
        return []
