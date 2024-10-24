# flake8: noqa: E501

import uuid
import logging
import traceback
from typing import List

from src.modules.database import chromadbvector
from src.modules.nlp.bow import relevant_words

COLLECTION = "null_hipothesis"

#################################################################
# COLEÇÂO: NULL HIPOTHESIS
#################################################################

def save(name: str = "Hipotses de nulidade", generative_clause: str = "",  hipothesis: str = "") -> bool:
    """
    Salva uma BoW (bag of words) com relevâcia >= a 3 da cláusula geratriz para uma busca por similaridade. 
    O texto da cláusula geratriz e a hipothese ficam salvos no metadata

    Args:
        name (str): nome da hipóteses
        generative_clause (str): Claúsula geratriz. A cláusula de referência para o apontamento da hipótese.
        redibitory (str): Contexto da descrição do vício redibitório.
        
    Returns:
        bool: Retorna falso para quando há algum erro e true para dado salvo.
    """
    try:
        meta = { "name": name, "clause": generative_clause, "hipothesis": hipothesis }
        collection = chromadbvector.collection(COLLECTION)
        collection.add(documents=[relevant_words(generative_clause)], metadatas=meta, ids=str(uuid.uuid4()))
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def query(clause: str = "", results: int = 5, cut: float = 1.2) -> List[dict]:
    """
    Consulta uma cláusula por similaridade convertendo o texto para uma BoW (bag of words) com relevâcia >= a 3. 
    O retorno esperado é uma lista de hipótesees relacionadas a cláusula geratriz.

    Args:
        clause (str): clásula para a consulta
        results (int): numero de hipóteses que devem ser retornadas
        cut (float): corte superior da distancia (proxidade) da clásula pesquisado.
        
    Returns:
        List[dict]: List[dic]: | dict: { id, distance, keys, name, clause, hipothesis } | 
        Retorna uma lista de cláusulas com a cláusula inibitário relacionada.
    """
    try:
        collection = chromadbvector.collection(COLLECTION)
        result = collection.query(query_texts=[f"{relevant_words(clause)}"], n_results=results)
        return chromadbvector.result_to_dict(result, cut)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []




