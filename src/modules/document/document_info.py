# flake8: noqa: E501

from dataclasses import dataclass
import traceback
import logging
import os

from src.modules.document.reader import reader
from src.utils import archive as Archive

@dataclass
class DocumentInfo:
    def __init__(self, id: int = 0 , path: str = "", name: str = "", size: int = 0, pages: int = 1, mimetype: str = ""):
        self.id: int = id
        self.path: str = os.path.normpath(path)
        self.name: str = name
        self.size: int = size
        self.pages: int = pages
        self.mimetype: str = mimetype

    def dict(self):
        return self.__dict__

    def tuple(self):
        return tuple(self.__dict__.values())

    def from_tuple(self, doc):
        """Transforma uma tupla na clase"""
        props = list(self.__dict__.keys())
        for prop, val in zip(props, doc):
            setattr(self, prop, val)
        
        return self

    def extract(self, path):
        try:
            if not Archive.exists(path):
                raise ValueError("O path está inválido.")

            # Obter metadados do PDF
            self.path = os.path.normpath(path)
            self.name = os.path.basename(path)
            self.size = os.path.getsize(path)
            
            _, ext = os.path.splitext(path)
            self.mimetype = ext.replace(".", "")

            pdf = reader(path)
            if pdf is None:
                return None

            self.pages = int(len(pdf.pages))
            return self.dict()
        except Exception as e:
            logging.error(f"{e}\n%s", traceback.format_exc())
            return None