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
## TABLE EMBEDDINGS
#################################################################
# salva na collection com embeddings
def save_metadata_with_embedings(metadata: DocumentMetadata):
	try: 
		model = OllamaModel()
		chunks = metadata.chunk
		embeddings = model.make(chunks)
		meta = metadata.to_dict_model()
		ids = [str(uuid.uuid4()) for _ in chunks]
		collection = chromadbvector.collection(COLLECTION)
		collection.add(embeddings=embeddings, documents=chunks, metadatas=meta, ids=ids)
		return True
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return False

# consulta com embeddings
def query_embeddings(consultant: str = "", results: int = 10):
	try: 
		model = OllamaModel()
		embeddings = model.embed(consultant)
		collection = chromadbvector.collection(COLLECTION)
		result = collection.query(query_embeddings=[embeddings], n_results=results)
		return result
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return []

#################################################################
## TABLE METADATA
#################################################################
def save_metadata(metadata: DocumentMetadata)-> bool:
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

def query_metadata(consult: str = "", results: int = 10)-> List[DocumentMetadata]:
	try: 
		collection = chromadbvector.collection(COLLECTIONRESUME)
		result = collection.query(query_texts=[consult], n_results=results)
		return retrieval_to_metadata(result)
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return []

def retrieval_to_metadata(retrieval)-> List[DocumentMetadata]:
    
    retrieval_ids = retrieval['ids']
    retrieval_metadatas = retrieval['metadatas']
    retrieval_distances = retrieval['distances']
    
    metadatas = []
    
    if len(retrieval_ids)== 0:
        return []
    
    for i, ret_ids in enumerate(retrieval_ids):
        for j, _id in enumerate(ret_ids):
            metadata = DocumentMetadata()
            
            if retrieval_metadatas != None:
                meta = retrieval_metadatas[i][j]
                metadata.from_dict_model(meta)
            
            metadata.uuid = _id
            metadata.distance = retrieval_distances[i][j]
                
            metadatas.append(metadata)
    
    return metadatas

#################################################################
## TABLE TEXT
#################################################################
def save_text(text: str = "", metadata = {})-> bool:
	try: 
		uuid = str(uuid.uuid4())
		collection = chromadbvector.collection(COLLECTIONRESUME)
		collection.add(documents=text, metadatas=metadata, ids=uuid)
		return True
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return False

# consulta com somente texto
def query_text(consult: str = "", results: int = 10)-> []:
	try: 
		collection = chromadbvector.collection(COLLECTIONRESUME)
		result = collection.query(query_texts=[consult], n_results=results)
		return result
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return []


#################################################################
## TABLE COMBINADAS
#################################################################
# busca com texto e embeddings combinado
def query(consultant: str = "",  embeddings = [], results: int = 10):
	searchs = []
	searchs.extend(query_text(consultant, results))
	searchs.extend(query_embeddings(embeddings, results))
	return list_unique(searchs)
	
# remove documentos repetidos na lista
def list_unique(list_items: []):

	keys = set()
	unique = []

	for _, item in enumerate(list_items):
		value = item['document']

		if value not in keys:
			keys.add(value)
			unique.append(item)
	
	return unique

# formata a lista de documentos para um texto
def docs_to_text(docs = []) -> str:

	formatted_list = []
	for doc in docs:
		formatted_list.append("\n{}\n[{}]: {}".format(doc['id'], doc["source"], doc['document']))

	return "\n".join(formatted_list)