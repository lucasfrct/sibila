# flake8: noqa: E501

from typing import List
import traceback
import logging

import pdfplumber

from src.utils import archive as Archive


def reader(path: str = ""):
    """faz leitura de uma documento PDF"""
    try:
        if not Archive.exists(path):
            raise ValueError("O path está inválido.")

        return pdfplumber.open(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None


def reader_pages(path: str = "", init: int = 1, final: int = 0) -> List[str]:
    """faz leitura de um trecho do PDF retornado as páginas em texto puro"""
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
