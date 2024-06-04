# flake8: noqa: E501

import uuid
import logging
import traceback
from typing import List

from src.modules.database import chromadbvector
from src.modules.nlp.bow import generate_bow

COLLECTION = "catalogs"

#################################################################
# TABLE CATALOGS
#################################################################

def save(path: str = "", name: str = "", page: int = 1,  content: str = "") -> bool:
    """ salva o conteúdo no catálogo. """ 
    try:
        _uuid = str(uuid.uuid4())
        text = text_relevant(content)         
        meta = { "uuid": _uuid, "path": path, "name": name, "page": page, "source":  f"{name}, pg. {page}", "content": content }
        collection = chromadbvector.collection(COLLECTION)
        collection.add(documents=[text], metadatas=meta, ids=_uuid)
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def query(query: str = "", results: int = 5, cut: float = 1.2) -> List[dict]:
    """ consulta no catálogo. """ 
    try:
        collection = chromadbvector.collection(COLLECTION)
        text = f"{query} {text_relevant(query)}" 
        result = collection.query(query_texts=[text], n_results=results)
        return retrieval_to_dict(result, cut)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []

def text_relevant(content: str = "") -> str:
    bow = generate_bow(content)
    main_words = []
    for word in bow.keys():
        freq = bow[word]
        if(freq >= 3):
            main_words.append(word)
            
    return ' '.join(main_words)

def retrieval_to_dict(retrieval, cut: float = 1.2) -> List[dict]:
    """ transforma uma resultados em dicionários. """  # noqa: E501

    retrieval_ids = retrieval['ids']
    retrieval_metadatas = retrieval['metadatas']
    retrieval_distances = retrieval['distances']
    retrieval_documents = retrieval['documents']
    
    # obtem um dicionário com as proíedades
    list_docs = []
    for ids, metadatas, distances, documents in zip(retrieval_ids, retrieval_metadatas, retrieval_distances, retrieval_documents):
        for _id, metadata, distance, document in zip(ids, metadatas, distances, documents):
            if distance > cut:
                continue
            
            doc = { "id": _id, "distance": distance, "keys": document.split() } 
            doc.update(metadata)    
            list_docs.append(doc)
    
    # remove documentos com conteúdo repetido
    content_unique = set()
    docs = []
    for d in list_docs:
        if 'content' not in d:
            continue
        
        content = d['content']
        if content not in content_unique:
            docs.append(d)
            content_unique.add(content)
    
    return docs

