# flake8: noqa: E501

import logging
import traceback
from typing import List

from src.modules.database import sqlitedb
from src.modules.document.paragraph_metadata import ParagraphMetadata

#################################################################
# TABLE PARAGRAPHS METADATAS
#################################################################


def table_paragraphs_metadatas() -> bool:
    """cria a tabela de paragrafos com metadados"""
    try:
        conn = sqlitedb.client()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS paragraphs_metadatas (
                uuid TEXT PRIMARY KEY,
                path TEXT,
                page INTEGER,
                name TEXT,
                source TEXT,
                letters INTEGER,
                content TEXT,
                
                distance REAL,
                mimetype TEXT,
                size INTEGER,

                phrases INTEGER,
                lines INTEGER,
                chunks INTEGER
            )
        """)
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def save(paragraph: ParagraphMetadata) -> bool:
    """salva um paragrafo com metadados"""
    try:
        paragraph_list = list(paragraph.tuple())
        rm_positions = [10, 12, 14]
        for pos in sorted(rm_positions, reverse=True):
            del paragraph_list[pos]
            
        paragraph = tuple(paragraph_list)
        conn = sqlitedb.client()
        conn.execute("""insert into 
            paragraphs_metadatas (uuid, path, page, name, source, letters, content, distance, mimetype, size, phrases, lines, chunks) 
            values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
        paragraph)
        conn.commit()
        return True

    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def list() -> List[ParagraphMetadata]:
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


def query(term: str = "", results: int = 10) -> List[ParagraphMetadata]:
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