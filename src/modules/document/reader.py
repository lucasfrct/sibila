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
import csv
import os

import pdfplumber

from src.utils import archive as Archive


def page_limit_mechanics(init: int = 1, final: int = -1, total: int = 1):

    if init >= total:
        init = total - 1

    if init <= 0:
        init = 1

    if final > total:
        final = total

    if final <= -1:
        final = total

    if (final < init):
        final = init

    return init, final


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


def reader_pages(path: str = "", init: int = 1, final: int = -1) -> List[str]:
    """
    Faz a leitura de um trecho de um arquivo PDF e retorna as páginas em texto puro.
    Parâmetros:
        path (str): Caminho para o arquivo PDF.
        init (int): Número da página inicial (1-indexado). Padrão é 1.
        final (int): Número da página final (1-indexado). Padrão é -1, que indica a última página do PDF.
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

        init, final = page_limit_mechanics(init, final, len(pdf.pages))
        # Carrega apenas as páginas especificadas na memória
        pages = []
        for num in range(init - 1, final):
            page = pdf.pages[num].extract_text()
            pages.append(page)

        return pages
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def reader_content(path: str, init: int = 1, final: int = -1) -> str:
    """
    Lê um arquivo PDF e extrai o texto de suas páginas numa variável só.
    Args:
        path (str): O caminho para o arquivo PDF.
        max_pages (int, opcional): O número máximo de páginas a serem lidas. 
    Returns:
        str: O conteúdo extraído do PDF como uma string. 
    """
    pdf = reader(path)
    if pdf is None:
        return ""

    content = ""
    init, final = page_limit_mechanics(init, final, len(pdf.pages))
    for num in range(init - 1, final):
        content += pdf.pages[num].extract_text().strip() + "\n"
    return content


def writer_dictionaries_to_csv(path: str, dictionaries: List[dict], mode: str = 'w') -> bool:
    try:

        if len(dictionaries) == 0:
            return False

        new_fieldnames = dictionaries[0].keys()
        file_exists = os.path.exists(path)

        header_needs_update = False

        if file_exists:
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                current_header = next(reader, None)
                header_needs_update = current_header != list(new_fieldnames)

        write_mode = 'w' if not file_exists or header_needs_update else mode

        with open(path, mode=write_mode, newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=new_fieldnames)

            if not file_exists or header_needs_update:
                writer.writeheader()

            writer.writerows(dictionaries)
        return True
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def read_csv_to_dictionaries(path: str):
    try:
        with open(path, mode='r', encoding='utf-8') as file_csv:
            _reader = csv.DictReader(file_csv)
            data = {col: [] for col in _reader.fieldnames}
            for line in _reader:
                for key, val in line.items():
                    data[key].append(val)
        return data
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False
