
import ollama
from src.models import handle


class ModelOllama:
    def __init__(self, model: str = "splitpierre/bode-alpaca-pt-br"):

        self.client = ollama
        self.embeddings = []
        self.model = model
        self.chunks = []

    def set_chunks(self, chunks=None):
        self.chunks = handle.set_chunks(chunks)
        return self.data

    def make(self, chunks=[]):
        self.set_chunks(chunks)
        self.generate()
        return self.embeddings

    @property
    def data(self):
        return self.chunks, self.embeddings

    def embed(self, data: str = ""):
        embedding = self.client.embeddings(model=self.model, prompt=data)
        return embedding["embedding"]

    def generate(self):
        return handle.generate_embeddings(self)

    def question(self, prompt: str, question: str = "") -> str:
        chat = self.completion(prompt, question)
        return chat["message"]["content"]

    def completion(self, prompt: str, question: str):
        return self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": f"{prompt}"},
                {"role": "user", "content": f"{question}"}
            ],
            options={"temperature": 0.5},
        )
