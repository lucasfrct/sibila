# flake8: noqa: E501

import os
import logging
import traceback
from typing import List, Optional

from src.modules.database import sqlitedb
from src.modules.catalog.catalog import Catalog

#################################################################
# TABLE CATALOGS
#################################################################

TABLE = "catalogs"


def table_catalogs() -> bool:
    """
    Cria a tabela de catálogo no banco de dados SQLite.
    A função tenta criar uma tabela chamada 'catalogs' com as seguintes colunas:
    - id: Identificador único do catálogo (chave primária, autoincremento).
    - path: Caminho do arquivo do catálogo.
    - name: Nome do catálogo.
    - size: Tamanho do catálogo.
    - pages: Número de páginas do catálogo.
    - mimetype: Tipo MIME do catálogo.
    - title: Título do arquivo.
    - resume: Resumo do arquivo.
    - categories: Categorias associadas ao catálogo.
    Retorna:
        bool: True se a tabela for criada com sucesso, False caso ocorra algum erro.
    """

    try:
        conn = sqlitedb.client()
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT,
                name TEXT,
                size INTEGER,
                pages INTEGER,
                mimetype TEXT,
                title TEXT,
                resume TEXT,
                categories TEXT
            )
        """)
        return True
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")
        return False


def save(catalog: Catalog) -> bool:
    """
    Salva informações do item do catálogo na tabela.
    Args:
        catalog (Catalog): Objeto contendo as informações do item do catálogo a ser salvo.
    Returns:
        bool: Retorna True se o item do catálogo foi salvo com sucesso, caso contrário, retorna False.
    """
    try:
        if catalog is None:
            return False

        path = catalog.path
        catalog_data = show_by_path(path)

        if catalog_data is not None:
            return False

        # extra o id da tupla
        _, *info = catalog.tuple()
        conn = sqlitedb.client()
        conn.execute(
            f"insert into {TABLE} (path, name, size, pages, mimetype, title, resume, categories) values (?, ?, ?, ?, ?, ?, ?, ?)",
            info
        )
        conn.commit()
        return True

    except AttributeError as e:
        logging.error(f"Erro de atributo no catálogo: {e}\n{traceback.format_exc()}")
        return False
    except Exception as e:
        logging.error(f"Erro ao salvar catálogo: {e}\n{traceback.format_exc()}")
        return False


def show_by_path(path: str = "") -> Optional[Catalog]:
    """
    Busca um item do catálogo pelo caminho especificado.

    Args:
        path (str): O caminho do item no catálogo. Padrão é uma string vazia.

    Returns:
        Optional[Catalog]: O item do catálogo encontrado ou None se nenhum item for encontrado.
    """

    try:
        path = os.path.normpath(path)
        docs = list_by_path(path, 1)
        if (len(docs) == 0):
            return None
        return docs[0]
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")
        return None


def list_by_path(path: str = "", limit: int = 1000) -> List[Catalog]:
    """
    Lista os items do catálogo com base no caminho fornecido.
    Args:
        path (str): O caminho para filtrar os catálogos. Padrão é uma string vazia.
        limit (int): O número máximo de items do catálogo a serem retornados. Padrão é 1000.
    Returns:
        List[Catalog]: Uma lista de objetos Catalog correspondentes ao caminho fornecido.
    """

    try:
        path = os.path.normpath(path)
        conn = sqlitedb.client()
        cursor = conn.execute(
            f"select * from {TABLE} where path=? LIMIT {limit}",
            (path,)
        )
        docs: List[Catalog] = []
        for doc in cursor:
            docs.append(Catalog(*doc))
        return docs
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")
        return []


def list(limit: int = 1000) -> List[Catalog]:
    """
    Lista os items de catálogo do banco de dados com um limite opcional.
    Args:
        limit (int, opcional): O número máximo de items do catálogo a serem retornados. O padrão é 1000.
    Returns:
        List[Catalog]: Uma lista de objetos Catalog. Retorna uma lista vazia em caso de erro.
    """

    try:
        conn = sqlitedb.client()
        cursor = conn.execute(f"select * from {TABLE} LIMIT {limit}")
        docs: List[Catalog] = []
        for doc in cursor:
            docs.append(Catalog(*doc))
        return docs
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")
        return []


def has_path(path: str = "") -> bool:
    """
    Verifica se um caminho específico possui arquivos ou diretórios.
    Args:
        path (str): O caminho a ser verificado. Por padrão, é uma string vazia.
    Returns:
        bool: Retorna True se o caminho contiver arquivos ou diretórios, caso contrário, retorna False.
    """

    try:
        if len(list_by_path(path, 1)) == 0:
            return False
        return True
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")
        return False
