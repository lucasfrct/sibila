
from abc import ABC, abstractmethod


class ModelLLM(ABC):
    @abstractmethod
    def embed(self):
        pass
