# flake8: noqa: E501

from dataclasses import dataclass, asdict, astuple
import traceback
import logging
import os

from src.modules.document.reader import reader
from src.utils import archive as Archive

@dataclass
class DocumentInfo:
    def __init__(self, path: str = "", name: str = "", size: int = 0, pages: int = 1, mimetype: str = "pdf"):
        self.id: int = 0
        self.path: str = path
        self.name: str = name
        self.size: int = size
        self.pages: int = pages
        self.mimetype: str = mimetype

    def dict(self):
        return asdict(self)

    def to_tuple(self):
        return astuple(self)

    def from_tuple(self, doc_tuple):
        _id, path, name, size, pages, mimetype = doc_tuple
        self.id = _id
        self.path = path
        self.name = name
        self.size = size
        self.pages = pages
        self.mimetype = mimetype
        return self

    def extract(self, path):
        try:
            if not Archive.exists(path):
                raise ValueError("O path está inválido.")

            # Obter metadados do PDF
            self.path = os.path.normpath(path)
            self.name = os.path.basename(path)
            self.size = os.path.getsize(path)

            pdf = reader(path)
            if pdf is None:
                return None

            self.pages = int(len(pdf.pages))
            return self.dict()
        except Exception as e:
            logging.error(f"{e}\n%s", traceback.format_exc())
            return None