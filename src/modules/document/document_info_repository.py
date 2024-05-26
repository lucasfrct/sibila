# flake8: noqa: E501

import logging
import traceback
from typing import List, Optional

from src.modules.database import sqlitedb
from src.modules.document.document_info import DocumentInfo

#################################################################
# TABLE INFO
#################################################################

def table_documents_info() -> bool:
    """cria a tabela de iformçoes do documwnto"""
    try:
        conn = sqlitedb.client()
        conn.execute("""
            create table if not exists documents_info (
                id text primary key,
                path text,
                name text,
                size interger,
                pages interger,
                mimetype text
            )
        """)
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def save_info(document: DocumentInfo) -> bool:
    try:
        if document is None:
            return False

        path = document.path
        doc_data = show_info_by_path(path)

        if doc_data is not None:
            return False

        info = document.to_tuple()
        conn = sqlitedb.client()
        conn.execute("insert into documents_info (path, name, size, pages, mimetype) values (?, ?, ?, ?, ?)", info)  # noqa: E501
        conn.commit()
        return True

    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def show_info_by_path(path: str = "") -> Optional[DocumentInfo]:
    try:
        docs_raw = list_raw(path)
        docs = []
        for doc_raw in docs_raw:
            docs.append(doc_raw)

        if (len(docs) == 0):
            return None

        doc = DocumentInfo()
        doc.from_tuple(docs[0])
        return doc
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None


def list_info() -> List[DocumentInfo]:
    try:
        conn = sqlitedb.client()
        cursor = conn.execute("select * from documents")
        docs = []
        for doc_raw in cursor:
            doc = DocumentInfo()
            doc.from_tuple(doc_raw)
            docs.append(doc)

        if len(docs) == 0:
            return []

        return docs
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def list_raw(path: str = "") -> List[object]:
    try:
        conn = sqlitedb.client()
        cursor = conn.execute(
            "select * from documents_info where path=?", (path,))
        docs = []
        for doc in cursor:
            docs.append(doc)

        return docs
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def has_document(path: str = "") -> bool:
    try:
        if len(list_raw(path)) == 0:
            return False
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False
