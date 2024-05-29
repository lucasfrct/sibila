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
    """cria a tabela de iformaçoes do documwnto"""
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
    """salva informaçoa do documento na tabela"""
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
    """busca uma documento por path"""
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
        cursor = conn.execute("select * from documents")
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
