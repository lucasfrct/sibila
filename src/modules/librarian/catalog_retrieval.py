# flake8: noqa: E501

import logging
import traceback
from typing import List

from src.modules.database import chromadbvector
from src.modules.nlp.bow import relevant_words
from src.utils import string as String

COLLECTION = "catalogs"

#################################################################
# TABLE CATALOGS
#################################################################

def save(path: str = "", name: str = "", page: int = 1,  content: str = "") -> bool:
    """ salva o conteúdo no catálogo. """ 
    try:
        hash_id = String.hash(content)
        collection = chromadbvector.collection(COLLECTION)
        
        # verifica se o ID já existe na coleção
        if chromadbvector.conflict_id(collection, hash_id): 
            return True

        keys = relevant_words(content)
        meta = { "hash": hash_id, "path": path, "name": name, "page": page, "source":  f"{name}, pg. {page}", "content": content, "keys": keys }
        collection.add(ids=[hash_id], documents=[content], metadatas=[meta])
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def query(query: str = "", results: int = 5, threshold: float = 0.5) -> List[dict]:
    """ consulta no catálogo. """ 
    try:
        collection = chromadbvector.collection(COLLECTION)
        return chromadbvector.query(collection, query, results, threshold)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []