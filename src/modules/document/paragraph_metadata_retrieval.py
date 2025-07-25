# flake8: noqa: E501

import uuid
import logging
import traceback
from typing import List

from src.modules.document.paragraph_metadata import ParagraphMetadata
from src.modules.database import chromadbvector
from src.models.ollama import ModelOllama

COLLECTION = "paragraphs"

#################################################################
# TABLE PARAGRAPHS EMBEDDINGS
#################################################################

def save(paragraph: ParagraphMetadata) -> bool:
    """ salva os paragrafos. """ 
    try:
        uuid = paragraph.uuid
        text = paragraph.content
        paragraph_dict = paragraph.data_retrieval()
        collection = chromadbvector.collection(COLLECTION)
        collection.add(documents=text, metadatas=paragraph_dict, ids=uuid)
        return True
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")
        return False


def query(query: str = "", results: int = 5) -> List[ParagraphMetadata]:
    """ consulta os paragrafos. """ 
    try:
        collection = chromadbvector.collection(COLLECTION)
        result = collection.query(query_texts=[query], n_results=results)
        return retrieval_to_paragraphs(result)
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")
        return []


def save_with_embedings(metadata: ParagraphMetadata) -> bool:
    """ salva na collection com embeddings. """
    try:
        model = ModelOllama()
        chunks = metadata.chunk
        embeddings = model.make(chunks)
        paragraph_dict = metadata.data_retrieval()
        ids = [str(uuid.uuid4()) for _ in chunks]
        collection = chromadbvector.collection(COLLECTION)
        collection.add(embeddings=embeddings, documents=chunks, metadatas=paragraph_dict, ids=ids)
        return True
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")
        return False


def query_with_embeddings(consult: str = "", results: int = 5) -> List[ParagraphMetadata]:
    """ consulta com embeddings. """
    try:
        model = ModelOllama()
        embeddings = model.embed(consult)
        collection = chromadbvector.collection(COLLECTION)
        result = collection.query(
            query_embeddings=[embeddings], n_results=results)
        return retrieval_to_paragraphs(result)
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")
        return []


def retrieval_to_paragraphs(retrieval) -> List[ParagraphMetadata]:
    """ transforma uma resultados do banco numa metadata. """  # noqa: E501

    retrieval_ids = retrieval['ids']
    retrieval_metadatas = retrieval['metadatas']
    retrieval_distances = retrieval['distances']
    retrieval_documents = retrieval['documents']
    
    metadatas = []

    if len(retrieval_ids) == 0:
        return []

    for i, ret_ids in enumerate(retrieval_ids):
        for j, _id in enumerate(ret_ids):
            metadata = ParagraphMetadata()

            if retrieval_metadatas is not None:
                meta = retrieval_metadatas[i][j]
                metadata.from_retrieval(meta)

            metadata.uuid = _id
            metadata.distance = retrieval_distances[i][j]
            metadata.content = retrieval_documents[i][j]

            metadatas.append(metadata)

    return metadatas
