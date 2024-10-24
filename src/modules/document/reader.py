# flake8: noqa: E501
""" 
PDF Document Reader Module
Este módulo contém funções para ler documentos PDF e extrair texto puro das páginas especificadas.
Funções:
    - reader(path: str = "") -> pdfplumber.PDF: Faz a leitura de um documento PDF e retorna o objeto PDF.
    - reader_pages(path: str = "", init: int = 1, final: int = 0) -> List[str]: Faz a leitura de um trecho de um arquivo PDF e retorna as páginas em texto puro.
"""

from typing import List
import traceback
import logging

import pdfplumber

from src.utils import archive as Archive


def reader(path: str = "") -> pdfplumber.PDF:
    """
    Faz a leitura de um documento PDF.
    Args:
        path (str): O caminho para o arquivo PDF.
    Returns:
        pdfplumber.PDF: Objeto PDF se a leitura for bem-sucedida, caso contrário, retorna None.
    Raises:
        ValueError: Se o caminho fornecido for inválido.
    """
    """faz leitura de uma documento PDF"""
    try:
        if not Archive.exists(path):
            raise ValueError("O path está inválido.")

        return pdfplumber.open(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None


def reader_pages(path: str = "", init: int = 1, final: int = 0) -> List[str]:
    """
    Faz a leitura de um trecho de um arquivo PDF e retorna as páginas em texto puro.
    Parâmetros:
        path (str): Caminho para o arquivo PDF.
        init (int): Número da página inicial (1-indexado). Padrão é 1.
        final (int): Número da página final (1-indexado). Padrão é 0, que indica a última página do PDF.
    Retorna:
        List[str]: Lista de strings contendo o texto das páginas especificadas.
    Exceções:
        ValueError: Se o caminho do arquivo for inválido ou se não for possível ler o arquivo PDF.
    """
    try:
        if not Archive.exists(path):
            raise ValueError("O path está inválido.")

        pdf = reader(path)
        if pdf is None:
            raise ValueError("Não foi possível ler o arquivo pdf.")

        total = len(pdf.pages)

        if init >= total:
            init = total - 1

        if init <= 0:
            init = 1

        if final > total:
            final = total

        if final <= 0:
            final = total

        if (final < init):
            final = init

        # Carrega apenas as páginas especificadas na memória
        pages = []
        for num in range(init - 1, final):
            page = pdf.pages[num].extract_text()
            pages.append(page)

        return pages
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []
