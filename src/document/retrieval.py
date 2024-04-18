import os
import uuid
import logging
import traceback
from array import array
from typing import List, Tuple

from src.database import chromadbvector
from src.document.doc import Doc

COLLECTION = "documents"

def save(document: Doc):
	try: 
		chunks, embeddings, metadatas = document.chunks_embedings_and_metadatas
		ids = [str(uuid.uuid4()) for _ in chunks]
		collection = chromadbvector.collection(COLLECTION)
		collection.add(embeddings=embeddings, documents=chunks, metadatas=metadatas, ids=ids)
		return True
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return False

def query(embeddings, results: int = 3):
	try: 
		collection = chromadbvector.collection(COLLECTION)
		result = collection.query(query_embeddings=[embeddings], n_results=results)
		return extract_result(result)
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return {}

def consult(consult: str = "", results: int = 5):
	try: 
		collection = chromadbvector.collection(COLLECTION)
		result = collection.query(query_texts=[consult], n_results=results)
		return extract_result(result)
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return []
	
def extract_result(result):
	
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
		ids[0], 
		uris[0], 
		data[0], 
		distances[0], 
		metadatas[0], 
		documents[0], 
		embeddings[0]
	):

		doc = {}
		doc['id'] = _id
		doc['uri'] = _uri
		doc['data'] = _data
		doc['distance'] = _distance
		doc['document'] = _document
		doc['embedding'] = _embedding

		doc.update(_metadata)
		
		result_data.append(doc)

	return result_data
	
