# flake8: noqa: E501

from dataclasses import dataclass
import traceback
import logging
import os

from src.modules.document.reader import reader
from src.utils import archive as Archive

@dataclass
class Catalog:
    def __init__(
        self, 
        id: int = 0 , 
        path: str = "", 
        name: str = "", 
        size: int = 0, 
        pages: int = 1, 
        mimetype: str = "", 
        title: str = "", 
        resume: str = "", 
        categories: str = "", 
    ):
        """
        Inicializa uma nova instância da classe.
        """
        self.id: int = id
        self.path: str = os.path.normpath(path)
        self.name: str = name
        self.size: int = size
        self.pages: int = pages
        self.mimetype: str = mimetype
        self.title: str = title
        self.resume: str = resume
        self.categories: str = categories

    def dict(self):
        """
        Retorna um dicionário que representa os atributos do objeto.

        Returns:
            dict: Um dicionário contendo os atributos do objeto.
        """
        return self.__dict__

    def tuple(self):
        """
        Converte os valores dos atributos do objeto em uma tupla.

        Retorna:
            tuple: Uma tupla contendo os valores dos atributos do objeto.
        """
        return tuple(self.__dict__.values())

    def from_tuple(self, doc):
        """
        Transforma uma tupla em uma instância da classe.
        Args:
            doc (tuple): Tupla contendo os valores a serem atribuídos às propriedades da instância.
        Returns:
            self: A instância da classe com as propriedades atualizadas.
        """
        props = list(self.__dict__.keys())
        for prop, val in zip(props, doc):
            setattr(self, prop, val)
        
        return self

        """
        Extrai informações de um documento no caminho especificado.
        Args:
            path (str): O caminho do arquivo do documento.
        Returns:
            dict: Um dicionário contendo as informações extraídas do documento, 
                  incluindo nome, tamanho, tipo MIME e número de páginas (se for um PDF).
            None: Retorna None se ocorrer um erro durante a extração.
        """
        try:
            if not Archive.exists(path):
                raise ValueError("O path está inválido.")

            # Obter metadados do arquivo
            self.path = os.path.normpath(path)
            self.name = os.path.basename(path)
            self.size = os.path.getsize(path)
            
            _, ext = os.path.splitext(path)
            self.mimetype = ext.replace(".", "")

            if "pdf" in self.mimetype.lower():
                # Obter número de páginas do PDF
                pdf = reader(path)
                if pdf is None:
                    return None

                self.pages = int(len(pdf.pages))
                
            # Retorna um dicionário com as informações extraídas
            return self.dict()
        except Exception as e:
            logging.error(f"{e}\n%s", traceback.format_exc())
            return None