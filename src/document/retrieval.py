import uuid
import logging
import traceback

from src.database import chromadbvector

COLLECTION = "documents"
COLLECTIONRESUME = "resume"


def save(document):
    """salva em duas collections, uma para texto puro e outra para embeddings"""
    try: 
        if not save_embedings(document):
            return False
        
        return save_text(document)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False

# salva na collection com embeddings
def save_embedings(document):
	try: 
		chunks, embeddings, metadatas = document.chunks_embedings_and_metadatas

		ids = [str(uuid.uuid4()) for _ in chunks]
		collection = chromadbvector.collection(COLLECTION)
		collection.add(embeddings=embeddings, documents=chunks, metadatas=metadatas, ids=ids)
		return True
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return False

# sava na collection somente os textos
def save_text(document):
	try: 
		chunks, metadatas = document.chunks_and_metadatas
		ids = [str(uuid.uuid4()) for _ in chunks]
		collection = chromadbvector.collection(COLLECTIONRESUME)
		collection.add(documents=chunks, metadatas=metadatas, ids=ids)
		return True
  
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return False

def register(text: str, metadatas = None):
	try: 

		_id = str(uuid.uuid4())
		collection = chromadbvector.collection(COLLECTIONRESUME)
  
		if metadatas:
			meta = {
				'letters': str(metadatas['letters']),
				'pages': str(metadatas['pages']),
				'page': str(metadatas['page']),
				'source': metadatas['source'],
				'path': metadatas['path'],
				'name': metadatas['name'],
			}
			collection.add(documents=[text], metadatas=meta, ids=[_id])
			return True
		
		collection.add(documents=[text], ids=[_id])
		return True
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return False
 
# consulta com embeddings
def query_embeddings(embeddings = [], results: int = 10):
	try: 
		collection = chromadbvector.collection(COLLECTION)
		result = collection.query(query_embeddings=[embeddings], n_results=results)
		return extract_result(result)
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return []

# consulta com somente texto
def query_text(consult: str = "", results: int = 10)-> []:
	try: 
		collection = chromadbvector.collection(COLLECTIONRESUME)
		result = collection.query(query_texts=[consult], n_results=results)
		return extract_result(result)
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return []

# busca com texto e embeddings combinado
def query(consultant: str = "",  embeddings = [], results: int = 10):
	searchs = []
	searchs.extend(query_text(consultant, results))
	searchs.extend(query_embeddings(embeddings, results))
	return list_unique(searchs)
	
# forma o objeto de result padronizado
def extract_result(result)-> []:
 
	ids = result['ids']
	uris = result['uris']
	data = result['data']
	distances = result['distances']
	metadatas = result['metadatas']
	documents = result['documents']
	embeddings = result['embeddings']

	if ids == None or len(ids) == 0:
		return []

	ids = ids[0]

	if uris == None:
		uris = [["" for _ in ids]]

	if data == None:
		data = [["" for _ in ids]]

	if distances == None:
		distances = [["" for _ in ids]]

	if metadatas == None:
		metadatas = [["" for _ in ids]]

	if documents == None:
		documents = [["" for _ in ids]]

	if embeddings == None:
		embeddings = [["" for _ in ids]]

	result_data = []

	for _id, _uri, _data, _distance, _metadata, _document, _embedding in zip(
		ids, 
		uris[0], 
		data[0], 
		distances[0], 
		metadatas[0], 
		documents[0], 
		embeddings[0]
	):

		doc = {}
		doc['uuid'] = _id
		doc['uri'] = _uri
		doc['data'] = _data
		doc['distance'] = _distance
		doc['document'] = _document
		doc['embedding'] = _embedding

		if _metadata:
			doc.update(_metadata)
		
		result_data.append(doc)

	return result_data
	
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
def docs_to_text(result = []) -> str:

	formatted_list = []
	for doc in result:
		formatted_list.append("\n{}\n[{}]: {}".format(doc['id'], doc["source"], doc['document']))

	return "\n".join(formatted_list)

def lines_to_text(lines = []) -> str:

	formatted_list = []
	for line in lines:
		content = line.get('content', line.get('document'))
		formatted_list.append("\n{}\n[{}]: {}".format(line['uuid'], line["source"], content))

	return "\n".join(formatted_list)