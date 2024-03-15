from dotenv import load_dotenv
from openai import OpenAI
import chromadb
import uuid
import os

from document import Doc

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

prompt_template = """Você é um assistente de IA que responde as dúvidas dos usuários com bases nos documentos a baixo.
Os documentos abaixo apresentam as fontes atualizadas e devem ser consideradas como verdade.
Cite a fonte quando fornecer a informação. 
Documentos:
{documents}
"""

class Embedding:
    def __init__(self):
        
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)

        self.chunks = []
        self.metadatas = []
        self.embeddings = []

        self.model = "text-embedding-ada-002"
        self.collection = "my_collection"
        self.path = "./data"
        self.client = chromadb.PersistentClient(path=self.path)
        self.db = self.client.get_or_create_collection(name=self.collection)

    def document(self, doc: Doc):
        self.doc = doc
        self.chunks, self.metadatas = self.doc.chunks_and_metadatas

    def create(self, data = ""):
        embedding = self.openai_client.embeddings.create(input=data, model=self.model)
        return embedding.data[0].embedding

    def generate(self):
        print("        - - - > ", end='', flush=True)
        for i, chunk in enumerate(self.chunks):
            self.embeddings.append(self.create(chunk))
            print(".", end='', flush=True)

        print("\n", end='', flush=True)

    def save(self):
        self.record(self.chunks, self.metadatas, self.embeddings)

    def record(self, chunks, metadatas, embeddings):
        ids = self.create_ids(chunks)
        self.db.add(embeddings=embeddings, documents=chunks, metadatas=metadatas, ids=ids)
        print(f"        - - - > Dados do pdf {self.doc.name} gravados com suceeso! {len(chunks)} Chunks")

    def create_ids(self, chunks):
        return [str(uuid.uuid4()) for _ in chunks]

    @property
    def data(self):
        return self.chunks, self.metadatas, self.embeddings

    def query(self, question):
        query_embedding = self.create(question)
        results = self.db.query(query_embeddings=[query_embedding], n_results=3)
        return results

    def search(self, question):
        formatted_list = []

        relevant_documents = self.query(question)
        for i, doc in enumerate(relevant_documents["documents"][0]):
            formatted_list.append("[{}]: {}".format(relevant_documents["metadatas"][0][i]["source"], doc))
        
        documents_str = "\n".join(formatted_list)
        return documents_str

    def prompt(self, documents):
        return prompt_template.format(documents=documents)

    def run(self, question):

        prompt = self.prompt(self.search(question))
        chat_completion = self.openai_client.chat.completions.create(
            messages=[
                {"role": "system","content": f"{prompt}"},
                {"role": "user","content": f"{question}"}
            ],
            model="gpt-3.5-turbo",
            max_tokens=500,
            temperature=0
        )

        return chat_completion.choices[0].message.content

