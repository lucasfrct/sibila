# flake8: noqa: E501

import uuid
import logging
import traceback
from typing import List

from src.modules.database import chromadbvector
from src.modules.nlp.bow import relevant_words

COLLECTION = "redibitory_vides"

#################################################################
# COLEÇÂO: REDIBITORY VIDES
#################################################################

def save(name: str = "Vícios redibitórios", generative_clause: str = "",  redibitory: str = "") -> bool:
    """
    Salva uma BoW (bag of words) com relevâcia >= a 3 da cláusula geratriz para uma busca por similaridade. 
    O texto da cláusula geratriz e o vício da cláusula ficam salvos no metadata

    Args:
        name (str): nome do redibitório.
        generative_clause (str): Claúsula geratriz. A cláusula de referência para o apontamento do redibitório.
        redibitory (str): Contexto da descrição do vício redibitório.
        
    Returns:
        bool: Retorna falso para quando há algum erro e true para dado salvo.
    """
    try:
        meta = { "name": name, "clause": generative_clause, "redibitory": redibitory }
        collection = chromadbvector.collection(COLLECTION)
        collection.add(documents=[relevant_words(generative_clause)], metadatas=meta, ids=str(uuid.uuid4()))
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def query(clause: str = "", results: int = 5, cut: float = 1.2) -> List[dict]:
    """
    Consulta uma cláusula por similaridade convertendo o texto para uma BoW (bag of words) com relevâcia >= a 3. 
    O retorno esperado é uma lista vicio redibitórios relacionadas a cláusula geratriz.

    Args:
        clause (str): clásula para a consulta
        results (int): numero de redibitórios que devem ser retornadas
        cut (float): corte superior da distancia (proxidade) da clásula pesquisado.
        
    Returns:
        List[dict]: List[dic]: | dict: { id, distance, keys, name, clause, redibitory } | 
        Retorna uma lista de cláusulas com a cláusula inibitário relacionada.
    """
    try:
        collection = chromadbvector.collection(COLLECTION)
        result = collection.query(query_texts=[f"{relevant_words(clause)}"], n_results=results)
        return chromadbvector.result_to_dict(result, cut)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []




