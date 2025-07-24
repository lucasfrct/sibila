# flake8: noqa: E501

from dataclasses import dataclass
import traceback
import logging
import os

try:
    from src.modules.document.docling_reader import get_document_info
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False
    from src.modules.document.reader import reader

from src.utils import archive as Archive
from src.utils import string as String

@dataclass
class DocumentInfo:
    def __init__(self, id: int = 0 , path: str = "", name: str = "", size: int = 0, pages: int = 1, mimetype: str = ""):
        """
        Inicializa uma nova instância da classe.

        Parâmetros:
            id (int): Identificador único do documento. Valor padrão é 0.
            path (str): Caminho do arquivo do documento. Valor padrão é uma string vazia.
            name (str): Nome do documento. Valor padrão é uma string vazia.
            size (int): Tamanho do documento em bytes. Valor padrão é 0.
            pages (int): Número de páginas do documento. Valor padrão é 1.
            mimetype (str): Tipo MIME do documento. Valor padrão é uma string vazia.
        """
        self.id: int = id
        self.path: str = os.path.normpath(path)
        self.name: str = name
        self.size: int = size
        self.pages: int = pages
        self.mimetype: str = mimetype
        self.sizeLabel: str = String.size_to_label(size)

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

    def extract(self, path):
        """
        Extrai informações de um documento no caminho especificado usando Docling ou PDF.
        Args:
            path (str): O caminho do arquivo do documento.
        Returns:
            dict: Um dicionário contendo as informações extraídas do documento, 
                  incluindo nome, tamanho, tipo MIME e número de páginas.
            None: Retorna None se ocorrer um erro durante a extração.
        """
        try:
            if not Archive.exists(path):
                raise ValueError("O path está inválido.")

            # Obter metadados do arquivo
            self.path = os.path.normpath(path)
            self.name = os.path.basename(path)
            self.size = os.path.getsize(path)
            self.sizeLabel: str = String.size_to_label(self.size)
            
            _, ext = os.path.splitext(path)
            self.mimetype = ext.replace(".", "")

            if DOCLING_AVAILABLE:
                # Usar Docling para obter informações do documento
                doc_info = get_document_info(path)
                if doc_info:
                    self.pages = doc_info.get('pages', 1)
                    if 'document_type' in doc_info:
                        self.mimetype = doc_info['document_type']
                else:
                    self.pages = 1
            elif "pdf" in self.mimetype.lower():
                # Fallback para PDF
                pdf = reader(path)
                if pdf is None:
                    return None
                self.pages = int(len(pdf.pages))
            else:
                self.pages = 1
                
            # Retorna um dicionário com as informações extraídas
            return self.dict()
        except Exception as e:
            logging.error(f"{e}\n%s", traceback.format_exc())
            return None