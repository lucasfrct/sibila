# flake8: noqa: E501

from typing import List, Optional
import traceback
import logging
import uuid
import os

from src.modules.document.paragraph_metadata import ParagraphMetadata
from src.modules.document.phrase_metadata import PharseMetadata
from src.modules.document.document_info import DocumentInfo
from src.modules.document.page_metadata import PageMetadata
from src.modules.document.reader import reader
from src.utils import archive as Archive
from src.utils import string as String


def read(path: str = "") -> List[str]:
    try:
        paths = []
        paths_raw = Archive.paths(path)
        for p in paths_raw:
            if os.path.isdir(p):
                continue
            paths.append(os.path.normpath(p))
        return paths
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def build(paths=[]) -> List[object]:
    try:
        documents = []

        for _, path in enumerate(paths):
            if not path:
                continue

            document = builder(path)
            if document is None:
                continue

            documents.append(document)

        return documents
    except Exception as e:
        logging.error(e)
        return []


def builder(path: str = ""):
    """faz leitura de um documento PDF"""
    return reader(path)


def info(path: str) -> Optional[DocumentInfo]:
    """extra informaçoes de um PDF"""
    try:
        doc = DocumentInfo()
        doc.extract(path)
        return doc
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None


def read_pages_with_details(path: str = "", init: int = 1, final: int = 0) -> List[PageMetadata]:
    """ faz a lietura das páginas em pdf extraindo os metadados"""
    try:
        if not Archive.exists(path):
            raise ValueError("O path está inválido.")

        inf = info(path)
        if inf is None:
            return []

        pdf = reader(path)
        if pdf is None:
            raise ValueError("Não foi possível ler o arquivo pdf.")

        total = inf.pages

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
        pages: List[PageMetadata] = []
        for num in range(init - 1, final):

            page_raw = pdf.pages[num]
            content = page_raw.extract_text()

            page = PageMetadata()

            page.uuid = str(uuid.uuid4())
            page.path = path
            page.page = int(num + 1)
            page.name = inf.name
            page.source = f"{page.name}, pg. {page.page}"
            page.letters = len(content)
            page.content = content

            page.size = inf.size
            page.distance = 0
            page.mimetype = "pdf"
            page.pages - inf.pages

            page.generate_paragraphs()
            page.generate_phrases()
            page.generate_lines()
            page.generate_chunks()

            pages.append(page)

        pdf.close()
        return pages
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def read_paragraphs_with_details(path: str = "", init: int = 1, final: int = 0) -> List[ParagraphMetadata]:
    """extrai os paragrafos com os detlhes do doumento"""
    try:

        pages = read_pages_with_details(path, init, final)

        paragraphs: List[ParagraphMetadata] = []
        for page in pages:
            for i, content in enumerate(page.paragraph):

                paragraph = ParagraphMetadata()

                paragraph.uuid = str(uuid.uuid4())
                paragraph.path = page.path
                paragraph.page = page.page
                paragraph.name = page.name
                paragraph.source = page.source
                paragraph.letters = len(content)
                paragraph.content = content

                paragraph.distance = 0
                paragraph.mimetype = page.mimetype
                paragraph.size = page.size

                paragraph.generate_phrases()
                paragraph.generate_lines()
                paragraph.generate_chunks()

                paragraphs.append(paragraph)

        return paragraphs
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def read_phrases_with_details(path: str = "", init: int = 1, final: int = 0) -> List[PharseMetadata]:
    """extrai as frases com os detalhes dos docuemnto"""
    try:

        paragraphs = read_paragraphs_with_details(path, init, final)

        phrases: List[PharseMetadata] = []
        for paragraph in paragraphs:

            phrase = PharseMetadata()

            phrase.uuid = str(uuid.uuid4())
            phrase.path = paragraph.path
            phrase.page = paragraph.page
            phrase.name = paragraph.name
            phrase.source = paragraph.source
            phrase.letters = len(paragraph.content)
            phrase.content = paragraph.content

            phrase.distance = 0
            phrase.mimetype = paragraph.mimetype
            phrase.size = paragraph.size

            phrase.generate_lines()
            phrase.generate_chunks()

            phrases.append(phrase)

        return phrases
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def read_lines_with_details(path: str = "", init: int = 1, final: int = 0) -> List[object]:
    try:
        paragraphs = read_paragraphs_with_details(path, init, final)
        lines = []
        for paragraph in paragraphs:
            lns = paragraph.line
            for i, content in enumerate(lns):
                chunks = String.split_to_chunks(content)
                line = {
                    'path': paragraph.path,
                    'page': paragraph.page,
                    'content': content,
                    'name': paragraph.name,
                    'letters': len(content),
                    'uuid': str(uuid.uuid4()),
                    'source': f"{paragraph.name}, pg. {paragraph.page}, ln {i+1}",
                    'num': i+1,
                    'chunk': chunks,
                    'lines': len(lns),
                    'chunks': len(chunks),
                    'size': paragraph.size,
                    'mimetype': paragraph.mimetype,
                }
                lines.append(line)
        return lines
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def to_pdf(path: str = "", path_out: str = ""):
    """transform um texto em um documento pdf"""

    # Criar instância da classe FPDF que é a base para a criação do documento
    pdf = FPDF()

    # Adicionar uma página ao PDF
    pdf.add_page()

    # Definir a fonte e o tamanho da fonte que será usada
    pdf.set_font("Arial", size=12)

    # Abrir o arquivo de texto e ler cada linha
    with open(path, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            # Adicionar a linha ao PDF
            pdf.cell(200, 10, txt=linha, ln=True)

    # Salvar o PDF criado
    pdf.output(path_out)

    return path_out
