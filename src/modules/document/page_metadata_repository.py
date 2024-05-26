# flake8: noqa: E501

import logging
import traceback
from typing import List

from src.modules.database import sqlitedb
from src.modules.document.page_metadata import PageMetadata

#################################################################
# TABLE PAGES METADATAS
#################################################################


def table_pages_metadatas() -> bool:
    """cria a tabela de paginas com metadados"""
    try:
        conn = sqlitedb.client()
        conn.execute("""
            create table if not exists pages_metadatas (
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


def save_metadata(meta: PageMetadata) -> bool:
    """salva uma página com metadados"""
    try:
        meta_save = meta.to_model()
        conn = sqlitedb.client()
        conn.execute("insert into pages_metadatas (uuid, path, page, name, source, letters, content, size, lines, pages, chunks, mimetype, paragraphs) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", meta_save)  # noqa: E501
        conn.commit()
        return True

    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def list_metadata() -> List[PageMetadata]:
    """lista paginas com metadados"""
    try:
        conn = sqlitedb.client()
        cursor = conn.execute("select * from pages_metadatas")
        pages = []
        for metadata_raw in cursor:
            page = PageMetadata()
            page.from_model(metadata_raw)
            pages.append(page)

        if len(pages) == 0:
            return []

        return pages
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def query_metadata(term: str = "", results: int = 10) -> List[PageMetadata]:
    """consulta uma termo na lista de paginas com metadados"""
    try:
        conn = sqlitedb.client()
        cursor = conn.execute(f"select * from pages_metadatas where content like '%{term}%' limit {results}")
        pages = []
        for metadata_raw in cursor:
            page = PageMetadata()
            page.from_model(metadata_raw)
            pages.append(page)

        if len(pages) == 0:
            return []

        return pages
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []