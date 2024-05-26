# import uuid
# import logging
# import traceback
# from typing import List

# from src.modules.database import chromadbvector
# from src.models.ollama import ModelOllama

# COLLECTION = "documents"
# COLLECTIONRESUME = "resume"

# #################################################################
# # TABLE EMBEDDINGS
# #################################################################
# def save_metadata_with_embedings(metadata: DocumentMetadata) -> bool:
#     """ salva na collection com embeddings. """  # noqa: E501
#     try:
#         model = ModelOllama()
#         chunks = metadata.chunk
#         embeddings = model.make(chunks)
#         meta = metadata.to_dict_model()
#         ids = [str(uuid.uuid4()) for _ in chunks]
#         collection = chromadbvector.collection(COLLECTION)
#         collection.add(embeddings=embeddings, documents=chunks, metadatas=meta, ids=ids)   # noqa: E501
#         return True
#     except Exception as e:
#         logging.error(f"{e}\n%s", traceback.format_exc())
#         return False


# def query_embeddings(consult: str = "", results: int = 5) -> List[DocumentMetadata]:  # noqa: E501
#     """ consulta com embeddings. """  # noqa: E501
#     try:
#         model = OllamaModel()
#         embeddings = model.embed(consult)
#         collection = chromadbvector.collection(COLLECTION)
#         result = collection.query(query_embeddings=[embeddings], n_results=results)  # noqa: E501
#         return retrieval_to_metadata(result)
#     except Exception as e:
#         logging.error(f"{e}\n%s", traceback.format_exc())
#         return []


# #################################################################
# # TABLE METADATA
# #################################################################
# def save_metadata(metadata: DocumentMetadata) -> bool:
#     """ salva os metadados. """  # noqa: E501
#     try:
#         uuid = metadata.uuid
#         text = metadata.content
#         meta = metadata.to_dict_model()
#         collection = chromadbvector.collection(COLLECTIONRESUME)
#         collection.add(documents=text, metadatas=meta, ids=uuid)
#         return True
#     except Exception as e:
#         logging.error(f"{e}\n%s", traceback.format_exc())
#         return False


# def query_metadata(consult: str = "", results: int = 5) -> List[DocumentMetadata]:  # noqa: E501
#     """ cnsulta os metadados. """  # noqa: E501
#     try:
#         collection = chromadbvector.collection(COLLECTIONRESUME)
#         result = collection.query(query_texts=[consult], n_results=results)
#         return retrieval_to_metadata(result)
#     except Exception as e:
#         logging.error(f"{e}\n%s", traceback.format_exc())
#         return []


# def retrieval_to_metadata(retrieval) -> List[DocumentMetadata]:
#     """ transforma uma resultados do banco numa metadata. """  # noqa: E501

#     retrieval_ids = retrieval['ids']
#     retrieval_metadatas = retrieval['metadatas']
#     retrieval_distances = retrieval['distances']

#     metadatas = []

#     if len(retrieval_ids) == 0:
#         return []

#     for i, ret_ids in enumerate(retrieval_ids):
#         for j, _id in enumerate(ret_ids):
#             metadata = DocumentMetadata()

#             if retrieval_metadatas is not None:
#                 meta = retrieval_metadatas[i][j]
#                 metadata.from_dict_model(meta)

#             metadata.uuid = _id
#             metadata.distance = retrieval_distances[i][j]

#             metadatas.append(metadata)

#     return metadatas


# #################################################################
# # TABLE TEXT
# #################################################################
# def save_text(text: str = "", metadata={}) -> bool:
#     """ salva um texto. """  # noqa: E501
#     try:
#         _uuid = str(uuid.uuid4())
#         collection = chromadbvector.collection(COLLECTIONRESUME)
#         collection.add(documents=text, metadatas=metadata, ids=_uuid)
#         return True
#     except Exception as e:
#         logging.error(f"{e}\n%s", traceback.format_exc())
#         return False

# # consulta com somente texto


# def query_text(consult: str = "", results: int = 5):
#     """ consulta um texto. """  # noqa: E501
#     try:
#         collection = chromadbvector.collection(COLLECTIONRESUME)
#         result = collection.query(query_texts=[consult], n_results=results)
#         return retrieval_to_metadata(result)
#     except Exception as e:
#         logging.error(f"{e}\n%s", traceback.format_exc())
#         return []


# #################################################################
# # TABLE COMBINADAS
# #################################################################
# def query(consult: str = "", results: int = 5) -> List[DocumentMetadata]:
#     """ busca com texto e embeddings combinado """  # noqa: E501

#     result: List[DocumentMetadata] = []
#     result.extend(query_embeddings(consult, results))
#     result.extend(query_metadata(consult, results))
#     result.extend(query_text(consult, results))
#     return result


# def to_text(docs: List[DocumentMetadata] = []) -> str:
#     """" formata a lista de documentos para um texto"""
#     documents = []
#     for doc in docs:
#         text = "\nID: {}\n[{}]: {}".format(doc.uuid, doc.source, doc.content)  # noqa: E501
#         documents.append(text)

#     return "\n".join(documents)
