import os
import uuid
import chromadb

# path = "./data/chromadb"
def client(path: str = "./data/chromadb") -> chromadb.ClientAPI:
	try:
		if not os.path.exists(path):
			os.makedirs(path)
		return chromadb.PersistentClient(path=path)
	except Exception as e:
		logging.error(e)
		return None
	

# collection = "train"
def collection(collection_name: str) -> chromadb.Collection:
	return client().get_or_create_collection(name=collection_name)



def save_model(model):
	client = client()
	db = collection(client, 'train')
	return save(db, model.embeddings, model.chunks, model.metadatas)

def query(embedding, results: int = 3):
	client = client()
	db = collection(client, 'train')
	return db.query(query_embeddings=[embedding], n_results=results)