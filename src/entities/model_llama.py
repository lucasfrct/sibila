
import concurrent.futures
import ollama
import uuid
import os

from src.entities.document import Doc
from src.prompts import prompts
from src.database import chromadb

class ModelLlama:
    def __init__(self):

        self.ollama = ollama
        self.chunks = []
        self.metadatas = []
        self.embeddings = []
        self.model = 'llama2'
    
    @property
    def data(self):
        return self.embeddings, self.chunks, self.metadatas

    def embed(self, data: str = ""):
        embedding = self.ollama.embeddings(model=self.model, prompt=data)
        return embedding["embedding"]

    def generate(self):
        info = "        - - - > Embedding"
        step = (100 / len(self.chunks))
        for i, chunk in enumerate(self.chunks):
            self.embeddings.append(self.embed(chunk))
            print(f"{info} - {int(i*step)}%", end='\r', flush=True)

        print(f"{info} - 100%", end='\r', flush=True)
        print("\n", end='', flush=True)

        return self.data

    def query_to_docs(self, result) -> str:

        # uris = result['uris']
        # data = result['data']
        # distances = result['distances']

        ids_container = result['ids']
        documents_container = result['documents']
        metadatas_container = result['metadatas']

        formatted_list = []
        for ids, doc, metas in zip(ids_container, documents_container, metadatas_container):
            for id, chunk, meta in zip(ids, doc, metas):
                formatted_list.append("\n{}\n[{}]: {}".format(id, meta["source"], chunk))

        return "\n".join(formatted_list)

    def question(self, question: str, documents: str) -> str:
        chat_completion = self.completion(prompts.generic(documents), question)
        return chat_completion["message"]["content"]

    def completion(self, prompt: str, question: str):
         return self.ollama.chat(
            model=self.model,
            messages=[
                { "role": "system", "content": f"{prompt}" },
                { "role": "user", "content": f"{question}" }
            ],
            options={ "temperature": 0.5 },
        )

