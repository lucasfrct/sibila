
import logging
import traceback
from typing import List, Optional

from src.database import sqlitedb
from src.document.documentpdf import DocumentInfo, DocumentMetadata


#################################################################
# TABLE INFO
#################################################################
def table_documents_info() -> bool:
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

#################################################################
# TABLE METADATA
#################################################################


def table_documents_metadatas() -> bool:
    try:
        conn = sqlitedb.client()
        conn.execute("""
            create table if not exists documents_metadatas (
                uuid text primary key,
                path text,
                page interger,
                name text,
                source text,
                letters interger,
                content text,

                size interger,
                lines interger,
                pages interger,
                chunks interger,
                mimetype text,
                paragraphs interger
            )
        """)
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def save_metadata(meta: DocumentMetadata) -> bool:
    try:
        meta_save = meta.to_model()
        conn = sqlitedb.client()
        conn.execute("insert into documents_metadatas (uuid, path, page, name, source, letters, content, size, lines, pages, chunks, mimetype, paragraphs) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", meta_save)  # noqa: E501
        conn.commit()
        return True

    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def list_metadata() -> List[DocumentMetadata]:
    try:
        conn = sqlitedb.client()
        cursor = conn.execute("select * from documents_metadatas")
        metadatas = []
        for metadata_raw in cursor:
            metadata = DocumentMetadata()
            metadata.from_model(metadata_raw)
            metadatas.append(metadata)

        if len(metadatas) == 0:
            return []

        return metadatas
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def query_metadata(term: str = "", results: int = 10) -> List[DocumentMetadata]:  # noqa: E501
    try:
        conn = sqlitedb.client()
        cursor = conn.execute(f"select * from documents_metadatas where content like '%{term}%' limit {results}") 	# noqa: E501
        metadatas = []
        for metadata_raw in cursor:
            metadata = DocumentMetadata()
            metadata.from_model(metadata_raw)
            metadatas.append(metadata)

        if len(metadatas) == 0:
            return []

        return metadatas
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []
