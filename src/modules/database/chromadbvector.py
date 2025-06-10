# flake8: noqa: E501

import os
import logging
import chromadb
import traceback
from typing import List


def client(path: str = "./data/.chromadb") -> chromadb.ClientAPI:
    """ 
    Cliente para ChromaDB 
    
    Args:
        path (str): caminho em disco para o arquivo
        
    Returns:
        chromadb.ClientAPI: RRetorna uma cliente da instancia de ChromaDB.
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return chromadb.PersistentClient(path=path)
    except Exception as e:
        logging.error(e)
        return None


def collection(collection_name: str) -> chromadb.Collection:
    """
    Inicia uma coleção do ChromaDB.

    Args:
        collection_name (str): nome da coleçao.
        
    Returns:
        chromadb.Collection: retorna um objeto de coleç do ChromaDB
    """
    return client().get_or_create_collection(name=collection_name)


def conflict_id(collection: chromadb.Collection, id: str = ""):
    """
    Verifica se o ID fornecido já existe na coleção.

    Recupera itens da coleção correspondentes ao ID fornecido e determina
    se há algum conflito com base na existência do ID.

    Parâmetros:
        collection: O objeto de coleção que fornece um método `get`.
        id (str, opcional): O ID para verificar conflito. O padrão é uma string vazia.

    Retorna:
        bool: True se o ID existe na coleção (indicando conflito), False caso contrário.
    """
    
    results = collection.get(ids=[id])
    return len(results['ids']) > 0

def query(collection: chromadb.Collection, query: str = "", results: int = 5, threshold: float = 0.5) -> List[dict]:
    """
    Consulta por similaridade convertendo o texto para uma BoW (bag of words) com relevâcia >= a 3. 
    O retorno esperado é um array de textos.

    Args:
        collection (chromadb.Collection): coleçao do bancod e dados
        query (str): texto da consulta
        results (int): numero de respostas
        threshold (float): corte superior para a distancia euclidiana (proximidade) dos resultados encontrados.
        os valores de threshold variam de 0 a 1;
        
    Returns:
        List[dict]: List[dic]:
    """
    try:
        result = collection.query(query_texts=[query], n_results=results)
        return result_to_dict(result, threshold)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []
    
def result_to_dict(result: chromadb.QueryResult, threshold: float = 0.5) -> List[dict]:
    """
    Recebe um objeto do ChromaDB e  transforma numa lista de dicionários

    Args:
        result (chromadb.QueryResult): resultado da consulta no chromaDB.
        threshold (float): corte superior para a distancia euclidiana (proximidade) dos resultados encontrados.
        os valores de threshold variam de 0 a 1;

    Returns:
        List[dic]: | dict: { id, distance, keys ...metadata } | retorna uma lista dicionários (cada dicionário é uma documento encontrado)
    """
    
    retrieval_ids = result['ids']
    retrieval_metadatas = result['metadatas']
    retrieval_distances = result['distances']
    retrieval_documents = result['documents']
    
    # obtem um dicionário com as propriedades
    list_docs = []
    for ids, metadatas, distances, documents in zip(retrieval_ids, retrieval_metadatas, retrieval_distances, retrieval_documents):
        for _id, metadata, distance, document in zip(ids, metadatas, distances, documents):

            # Converter distância euclidianan em similaridade
            similarity_score = 1 / (1 + distance)
            
            if similarity_score <= threshold:
                continue
            
            if "keys" in metadata and metadata["keys"]:
                metadata["keys"] = metadata["keys"].split()
                
            doc = { "id": _id, "distance": similarity_score } 
            doc.update(metadata)    
            list_docs.append(doc)
        
    # remove documentos com conteúdo repetido
    content_unique = set()
    docs = []
    for d in list_docs:
        if 'content' not in d:
            docs.append(d)
            continue
        
        content = d['content']
        if content not in content_unique:
            docs.append(d)
            content_unique.add(content)    
    
    return docs
