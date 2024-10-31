# flake8: noqa: E501

from openai import OpenAI
from src.config import open_ai as config
from src.models import handle


class ModelOpenAI:

    def __init__(self, model: str = "gpt-3.5-turbo"):

        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
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
        embedding = self.client.embeddings.create(input=data, model="text-embedding-ada-002")  # noqa: E501
        return embedding.data[0].embedding

    def generate(self):
        return handle.generate_embeddings(self)

    def question(self, prompt: str, question: str = "") -> str:
        chat = self.completion(prompt, question)
        return chat.choices[0].message.content

    def completion(self, prompt: str, question: str):
        return self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"{prompt}"},
                {"role": "user", "content": f"{question}"}
            ],
            model="gpt-3.5-turbo",
            max_tokens=1000,
            temperature=0.5
        )
