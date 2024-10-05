# flake8: noqa: E501

import logging
import traceback
from typing import List

from src.modules.database import chromadbvector
from src.modules.nlp.bow import relevant_words
from src.utils import string as String

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
        justification (str): Justificativa da hipótese.

    Returns:
        bool: Retorna falso para quando há algum erro e true para dado salvo.
    """
    try:
        hash_id = String.hash(justification)
        collection = chromadbvector.collection(COLLECTION)
        
        # verifica se o ID já existe na coleção
        if chromadbvector.conflict_id(collection, hash_id): 
            return True
        
        meta = { "name": name, "clause": clause, "justification": justification }
        collection.add(ids=[hash_id], documents=[relevant_words(clause)], metadatas=[meta])
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def query(query: str = "", results: int = 5, threshold: float = 0.5) -> List[dict]:
    """
    Consulta um cláusula por similaridade convertendo o texto para uma BoW (bag of words) com relevâcia >= a 3. 
    O retorno esperado é a claúsula e a justificativa da hipótese.

    Args:
        query (str): texto da consulta (texto que se assemelha a uma cláusula)
        results (int): numero de hipóteses que devem ser retornadas
        threshold (float): corte superior para a distancia euclidiana (proximidade) dos resultados encontrados.
        os valores de threshold variam de 0 a 1;
        
    Returns:
        List[dict]: List[dic]: | dict: { id, distance, keys, name, clause, justification } | 
        Retorna uma lista de cláusulas com hipoteses.
    """
    try:
        collection = chromadbvector.collection(COLLECTION)
        result = collection.query(query_texts=[f"{relevant_words(query)}"], n_results=results)
        return chromadbvector.result_to_dict(result, threshold)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []




