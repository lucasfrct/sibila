
import ollama

from src.prompts import prompts

class OllamaModel:
    def __init__(self, model: str = "llama2"):

        self.ollama = ollama
        self.chunks = []
        self.embeddings = []
        self.model = model

    def set_chunks(self, chunks = None):
        if chunks is None:
            chunks = []
            
        self.chunks = chunks
        return self.data

    def make(self, chunks = []):
        self.set_chunks(chunks)
        self.generate()
        return self.embeddings
        
    @property
    def data(self):
        return  self.chunks, self.embeddings

    def embed(self, data: str = "") -> []:
        embedding = self.ollama.embeddings(model=self.model, prompt=data)
        return embedding["embedding"]

    def generate(self):
        info = "- - - > Embedding"

        step = (100 / len(self.chunks))
        for i, chunk in enumerate(self.chunks):
            self.embeddings.append(self.embed(chunk))
            print(f"{info} - {int(i*step)}%", end='\r', flush=True)

        print(f"{info} - 100%", end='\r', flush=True)
        print("\n", end='', flush=True)

        return self.data

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

