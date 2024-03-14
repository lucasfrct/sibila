import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
import PyPDF2
import uuid

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHUNK_SIZE = 1000
OFFSET = 200
chromadb_path = "./data"

openai_client = OpenAI(api_key=OPENAI_API_KEY)
chroma_client = chromadb.PersistentClient(path=chromadb_path)
collection = chroma_client.get_or_create_collection(name="my_collection")

# ler um documento pdf do disco
def get_document(document_path):
    
    file = open(document_path, 'rb')
    reader = PyPDF2.PdfReader(file)

    document_text = ""
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        content = page.extract_text()
        document_text += content

    len(document_text)
    return document_text

## separa o documentos em palvras num array
def split_document(document_text):
    documents = []
    for i in range(0, len(document_text), CHUNK_SIZE):
        start = i
        end = i + 1000
        if start != 0:
            start = start - OFFSET
            end =  end - OFFSET
        documents.append(document_text[start:end])
    return documents

# trasnforma um texto em vetores
def get_embedding(text):
    embedding = openai_client.embeddings.create(input=text, model="text-embedding-ada-002")
    return embedding.data[0].embedding

# gera o vetor e o metadata de uma documento
def prepare_documents(documents, document_name):
    embeddings = []
    metadatas = []
    for i, doc in enumerate(documents):
        embeddings.append(get_embedding(doc))
        metadatas.append({"source": document_name, "partition" : i})

    return embeddings, metadatas

# gera id para cada documento
def create_ids(documents):
    return [str(uuid.uuid4()) for _ in documents]

# armazena dados no chromadb
def insert_data(documents, embeddings, metadatas, ids):
    collection.add(embeddings=embeddings, documents=documents, metadatas=metadatas, ids=ids)
    print(f"Data successfully entered! {len(documents)} Chunks")
    

def run():
    print("Running prep docs...")
    path = 'docs/'

    embeddings = []
    documents = []
    metadatas = []

    documents_names = os.listdir(path)
    documents_names_size = len(documents_names)
    
    for i, document_name in enumerate(documents_names): 
        
        print(f"{i+1}/{documents_names_size}: {document_name}")

        document = get_document(os.path.join(path, document_name))
        document_chunks = split_document(document)
        document_embeddings, document_metadatas = prepare_documents(document_chunks, document_name)
        documents.extend(document_chunks)
        embeddings.extend(document_embeddings)
        metadatas.extend(document_metadatas)
    
    ids = create_ids(documents)
    insert_data(documents, embeddings, metadatas, ids)
        
if __name__ == "__main__":
    run()