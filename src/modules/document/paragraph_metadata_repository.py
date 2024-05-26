# flake8: noqa: E501

import logging
import traceback
from typing import List

from src.modules.database import sqlitedb
from src.modules.document.paragraph_metadata import ParagraphMetadata

#################################################################
# TABLE PARAGRAPHS METADATAS
#################################################################


def table_paragraph_metadatas() -> bool:
    """cria a tabela de paragrafos com metadados"""
    try:
        conn = sqlitedb.client()
        conn.execute("""
            create table if not exists paragraphs_metadatas (
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


def save_metadata(meta: ParagraphMetadata) -> bool:
    """salva um paragrafo com metadados"""
    try:
        meta_save = meta.to_model()
        conn = sqlitedb.client()
        conn.execute("insert into paragraphs_metadatas (uuid, path, page, name, source, letters, content, size, lines, pages, chunks, mimetype, paragraphs) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", meta_save)  # noqa: E501
        conn.commit()
        return True

    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def list_metadata() -> List[ParagraphMetadata]:
    """lista paragrafos com metadados"""
    try:
        conn = sqlitedb.client()
        cursor = conn.execute("select * from paragraphs_metadatas")
        paragraphs = []
        for metadata_raw in cursor:
            paragraph = ParagraphMetadata()
            paragraph.from_model(metadata_raw)
            paragraphs.append(paragraph)

        if len(paragraphs) == 0:
            return []

        return paragraphs
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def query_metadata(term: str = "", results: int = 10) -> List[ParagraphMetadata]:
    """consulta um termo na lista de paragrafos com metadados"""
    try:
        conn = sqlitedb.client()
        cursor = conn.execute(f"select * from paragraphs_metadatas where content like '%{term}%' limit {results}")
        paragraphs = []
        for metadata_raw in cursor:
            paragraph = ParagraphMetadata()
            paragraph.from_model(metadata_raw)
            paragraphs.append(paragraph)

        if len(paragraphs) == 0:
            return []

        return paragraphs
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []