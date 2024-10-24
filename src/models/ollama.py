# flake8: noqa: E501

import ollama

from src.models import handle
from collections import deque

    
HISTORY = deque(maxlen=5)
class ModelOllama:
    def __init__(self, model: str = "sibila"):
        """
        Inicializa uma instância da classe.
        Args:
            model (str): O nome do modelo a ser utilizado. O valor padrão é "sibila".
        Atributos:
            client: Cliente para interagir com o serviço Ollama.
            embeddings (list): Lista para armazenar embeddings.
            model (str): Nome do modelo.
            chunks (list): Lista para armazenar chunks de dados.
        """

        self.client = ollama
        self.embeddings = []
        self.model = model
        self.chunks = []
        self.temperature = 0.5
        self.history_size = 5

    def set_chunks(self, chunks=None):
        """
        Define os chunks para o objeto atual.

        Args:
            chunks (opcional): Os chunks a serem definidos. Pode ser qualquer valor que a função handle.set_chunks aceite.

        Retorna:
            self.data: Os dados do objeto após definir os chunks.
        """
        self.chunks = handle.set_chunks(chunks)
        return self.data

    def make(self, chunks=[]):
        """
        Gera embeddings a partir dos chunks fornecidos.

        Args:
            chunks (list, optional): Lista de chunks a serem processados. O padrão é uma lista vazia.
        Returns:
            list: Embeddings gerados a partir dos chunks.
        """
        self.set_chunks(chunks)
        self.generate()
        return self.embeddings

    @property
    def data(self):
        """
        Propriedade que retorna os dados do modelo.

        Retorna:
            tuple: Uma tupla contendo os chunks e embeddings.
        """
        return self.chunks, self.embeddings

    def embed(self, prompt: str = ""):
        """
        Gera uma incorporação (embedding) para o texto fornecido.

        Args:
            data (str): O texto para o qual a incorporação será gerada. Padrão é uma string vazia.

        Returns:
            list: A incorporação gerada para o texto fornecido.
        """
        embedding = self.client.embeddings(model=self.model, prompt=prompt)
        return embedding["embedding"]

    def generate(self):
        """
        Gera embeddings utilizando a função handle.generate_embeddings.

        Retorna:
            Embeddings gerados pela função handle.generate_embeddings.
        """
        self.embeddings = handle.generate_embeddings(self, self.chunks)
        return self.data

    def question(self, prompt: str, question: str = "") -> str:
        """
        Gera uma resposta para uma pergunta baseada em um prompt fornecido.
        Args:
            prompt (str): O texto base para gerar a resposta.
            question (str, opcional): A pergunta específica a ser respondida. Padrão é uma string vazia.
        Returns:
            str: A resposta gerada para a pergunta.
        """
        chat = self.completion(prompt, question)
        response = chat["message"]["content"]

        # Armazena a resposta no deque (últimas 5 respostas)
        HISTORY.append(response)
        
        return response

    def completion(self, prompt: str, question: str):
        """
        Gera uma resposta baseada no prompt e na pergunta fornecidos.

        Args:
            prompt (str): O prompt inicial que define o contexto da conversa.
            question (str): A pergunta feita pelo usuário que precisa de uma resposta.

        Returns:
            dict: A resposta gerada pelo modelo de chat.
        """
        return self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": f"{prompt}"},
                {"role": "user", "content": f"{question}"}
            ],
            options={"temperature": self.temperature},
        )

    @staticmethod
    def history():
        """
        Método estático que retorna o histórico das últimas cinco respostas.

        Este método converte o deque `last_five_responses` em uma lista para facilitar a serialização em JSON.

        Retorna:
            list: Lista contendo as últimas cinco respostas.
        """
        # Converte o deque para uma lista para serialização JSON
        return list(HISTORY)
    
    
