# flake8: noqa: E501

import os
import logging
import traceback
from typing import List, Optional

from src.modules.database import sqlitedb
from src.modules.document.document_info import DocumentInfo

#################################################################
# TABLE INFO
#################################################################


def table_documents_info() -> bool:
    """
    Cria a tabela de informações do documento.

    Esta função cria uma tabela chamada 'documents_info' no banco de dados SQLite,
    se ela não existir. A tabela contém as seguintes colunas:
    - id: Identificador único do documento (chave primária, autoincremento).
    - path: Caminho do documento.
    - name: Nome do documento.
    - size: Tamanho do documento em bytes.
    - pages: Número de páginas do documento.
    - mimetype: Tipo MIME do documento.

    Returns:
        bool: Retorna True se a tabela for criada com sucesso, caso contrário, False.
    """
    """cria a tabela de iformaçoes do documento"""
    try:
        conn = sqlitedb.client()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT,
                name TEXT,
                size INTEGER,
                pages INTEGER,
                mimetype TEXT
            )
        """)
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def save(document: DocumentInfo) -> bool:
    """
    Salva informações do documento na tabela.
    Args:
        document (DocumentInfo): Objeto contendo as informações do documento a ser salvo.
    Returns:
        bool: Retorna True se o documento foi salvo com sucesso, caso contrário, retorna False.
    Raises:
        Exception: Loga qualquer exceção que ocorra durante a execução.
    """
    try:
        if document is None:
            return False

        path = document.path
        doc_data = show_by_path(path)

        if doc_data is not None:
            return False

        # extra o id da tupla
        _, *info = document.tuple()
        conn = sqlitedb.client()
        conn.execute(
            "insert into documents_info (path, name, size, pages, mimetype) values (?, ?, ?, ?, ?)", info)
        conn.commit()
        return True

    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def show_by_path(path: str = "") -> Optional[DocumentInfo]:
    """busca um documento por path"""
    try:
        path = os.path.normpath(path)
        docs = list_by_path(path)
        if (len(docs) == 0):
            return None
        return docs[0]
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None


def list_by_path(path: str = "") -> List[DocumentInfo]:
    """lista documenos por path"""
    try:
        path = os.path.normpath(path)
        conn = sqlitedb.client()
        cursor = conn.execute(
            "select * from documents_info where path=? LIMIT 1000", (path,))
        docs: List[DocumentInfo] = []
        for doc in cursor:
            docs.append(DocumentInfo(*doc))
        return docs
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def list() -> List[DocumentInfo]:
    """lista todos os docuemntos"""
    try:
        conn = sqlitedb.client()
        cursor = conn.execute("select * from documents_info")
        docs: List[DocumentInfo] = []
        for doc in cursor:
            docs.append(DocumentInfo(*doc))
        return docs
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def has_path(path: str = "") -> bool:
    """verifica se uma caminho para documeto existe"""
    try:
        if len(list_by_path(path)) == 0:
            return False
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False
