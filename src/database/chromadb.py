import uuid
import chromadb

# path = "./data"
def client_vector(path: str) -> chromadb.ClientAPI:
	path = "./data"
	return chromadb.PersistentClient(path=path)
	

# collection = "train"
def collection(client: chromadb.ClientAPI, collection_name: str) -> chromadb.Collection:
	return client.get_or_create_collection(name=collection_name)

def save(collection: chromadb.Collection, embeddings, chunks, metadatas):
	ids = [str(uuid.uuid4()) for _ in chunks]
	collection.add(embeddings=embeddings, documents=chunks, metadatas=metadatas, ids=ids)
	return "Dados gravados com suceeso!"

def save_model(model):
	client = client_vector('./data')
	db = collection(client, 'train')
	return save(db, model.embeddings, model.chunks, model.metadatas)

def query(embedding, results: int = 3):
	client = client_vector('./data')
	db = collection(client, 'train')
	return db.query(query_embeddings=[embedding], n_results=results)