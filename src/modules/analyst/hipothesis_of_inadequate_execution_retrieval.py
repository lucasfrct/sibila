# flake8: noqa: E501

import uuid
import logging
import traceback
from typing import List

from src.modules.database import chromadbvector
from src.modules.nlp.bow import relevant_words

COLLECTION = "hipothesis_of_inadequate_execution"

#################################################################
# COLEÇÂO: HIPOTHESIS OF INADEQUARE EXECUTION
#################################################################

def save(name: str = "Hipótese de execução inadequada", clause: str = "",  justification: str = "") -> bool:
    """
    Salva uma BoW (bag of words) com relevâcia >= a 3 da cláusula para uma busca por similaridade. 
    O texto da cláusula e a justificativa da hipótese ficam salvos no metadata

    Args:
        name (str): Nome da hipótese
        clause (str): Clásula da hipótese
        justification (str): cJustificativa da hipótese.

    Returns:
        bool: Retorna falso para quando há algum erro e true para dado salvo.
    """
    try:
        meta = { "name": name, "clause": clause, "justification": justification }
        collection = chromadbvector.collection(COLLECTION)
        collection.add(documents=[relevant_words(clause)], metadatas=meta, ids=str(uuid.uuid4()))
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def query(query: str = "", results: int = 5, cut: float = 1.2) -> List[dict]:
    """
    Consulta um cláusula por similaridade convertendo o texto para uma BoW (bag of words) com relevâcia >= a 3. 
    O retorno esperado é a claúsula e a justificativa da hipótese.

    Args:
        query (str): texto da consulta (texto que se assemelha a uma cláusula)
        results (int): numero de hipóteses que devem ser retornadas
        cut (float): corte superior da distancia (proxidade) da clásula pesquisado.
        
    Returns:
        List[dict]: List[dic]: | dict: { id, distance, keys, name, clause, justification } | 
        Retorna uma lista de cláusulas com hipoteses.
    """
    try:
        collection = chromadbvector.collection(COLLECTION)
        result = collection.query(query_texts=[f"{relevant_words(query)}"], n_results=results)
        return chromadbvector.result_to_dict(result, cut)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []




