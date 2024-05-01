import uuid
import logging
import traceback
from typing import List

from src.database import chromadbvector
from src.document.documentpdf import DocumentMetadata
from src.entities.ollama_model import OllamaModel

COLLECTION = "documents"
COLLECTIONRESUME = "resume"


#################################################################
# TABLE EMBEDDINGS
#################################################################
# salva na collection com embeddings


def save_metadata_with_embedings(metadata: DocumentMetadata) -> bool:
    try:
        model = OllamaModel()
        chunks = metadata.chunk
        embeddings = model.make(chunks)
        meta = metadata.to_dict_model()
        ids = [str(uuid.uuid4()) for _ in chunks]
        collection = chromadbvector.collection(COLLECTION)
        collection.add(embeddings=embeddings, documents=chunks, metadatas=meta, ids=ids)   # noqa: E501
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False

# consulta com embeddings


def query_embeddings(consult: str = "", results: int = 5) -> List[DocumentMetadata]:  # noqa: E501
    try:
        model = OllamaModel()
        embeddings = model.embed(consult)
        collection = chromadbvector.collection(COLLECTION)
        result = collection.query(query_embeddings=[embeddings], n_results=results)  # noqa: E501
        return retrieval_to_metadata(result)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


#################################################################
# TABLE METADATA
#################################################################


def save_metadata(metadata: DocumentMetadata) -> bool:
    try:
        uuid = metadata.uuid
        text = metadata.content
        meta = metadata.to_dict_model()
        collection = chromadbvector.collection(COLLECTIONRESUME)
        collection.add(documents=text, metadatas=meta, ids=uuid)
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def query_metadata(consult: str = "", results: int = 5) -> List[DocumentMetadata]:  # noqa: E501
    try:
        collection = chromadbvector.collection(COLLECTIONRESUME)
        result = collection.query(query_texts=[consult], n_results=results)
        return retrieval_to_metadata(result)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def retrieval_to_metadata(retrieval) -> List[DocumentMetadata]:

    retrieval_ids = retrieval['ids']
    retrieval_metadatas = retrieval['metadatas']
    retrieval_distances = retrieval['distances']

    metadatas = []

    if len(retrieval_ids) == 0:
        return []

    for i, ret_ids in enumerate(retrieval_ids):
        for j, _id in enumerate(ret_ids):
            metadata = DocumentMetadata()

            if retrieval_metadatas is not None:
                meta = retrieval_metadatas[i][j]
                metadata.from_dict_model(meta)

            metadata.uuid = _id
            metadata.distance = retrieval_distances[i][j]

            metadatas.append(metadata)

    return metadatas


#################################################################
# TABLE TEXT
#################################################################


def save_text(text: str = "", metadata={}) -> bool:
    try:
        _uuid = str(uuid.uuid4())
        collection = chromadbvector.collection(COLLECTIONRESUME)
        collection.add(documents=text, metadatas=metadata, ids=_uuid)
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False

# consulta com somente texto


def query_text(consult: str = "", results: int = 5):
    try:
        collection = chromadbvector.collection(COLLECTIONRESUME)
        result = collection.query(query_texts=[consult], n_results=results)
        return retrieval_to_metadata(result)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


#################################################################
# TABLE COMBINADAS
#################################################################
# busca com texto e embeddings combinado
def query(consult: str = "", results: int = 5) -> List[DocumentMetadata]:
    result = []
    result.extend(query_embeddings(consult, results))
    result.extend(query_metadata(consult, results))
    result.extend(query_text(consult, results))
    return list_unique(result)

# remove documentos repetidos na lista


def list_unique(documents: List[DocumentMetadata] = []) -> List[DocumentMetadata]:  # noqa: E501

    # keys = set()
    # unique = []

    # for _, item in enumerate(list_items):
    #     value = item['document']

    #     if value not in keys:
    #         keys.add(value)
    #         unique.append(item)

    # return unique
    return documents

# formata a lista de documentos para um texto


def to_text(docs: List[DocumentMetadata] = []) -> str:
    documents = []
    for doc in docs:
        text = "\nID: {}\n[{}]: {}".format(doc.uuid, doc.source, doc.content)  # noqa: E501
        documents.append(text)

    return "\n".join(documents)
