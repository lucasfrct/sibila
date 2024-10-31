# flake8: noqa: E501

from typing import List, Optional
import traceback
import logging
import uuid
import os

import pdfplumber
from fpdf import FPDF

from src.modules.document import document_info_repository as DocInfoRepository
from src.modules.document.paragraph_metadata import ParagraphMetadata
from src.modules.document.phrase_metadata import PharseMetadata
from src.modules.document.page_metadata import PageMetadata
from src.modules.document.document_info import DocumentInfo
from src.modules.document.reader import page_limit_mechanics, read_csv_to_dictionaries, reader as PDFReader, reader_content, writer_dictionaries_to_csv
from src.utils import archive as Archive
from src.utils import string as String


def dir(path: str = "") -> List[str]:
    """
    Lê os caminhos dos arquivos em um diretório especificado.

    Args:
        path (str): O caminho do diretório a ser lido. Se não for especificado, será utilizado um caminho padrão.

    Returns:
        List[str]: Uma lista de caminhos de arquivos normalizados. Se ocorrer um erro, retorna uma lista vazia.

    Exceções:
        Registra qualquer exceção que ocorra durante a leitura dos caminhos dos arquivos.
    """
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


def info(path: str) -> Optional[DocumentInfo]:
    """
    Extraí informações de um arquivo.

    Args:
        path (str): O caminho para o arquivo.

    Returns:
        Optional[DocumentInfo]: Um objeto DocumentInfo contendo as informações extraídas do documento,
        ou None se ocorrer um erro durante a extração.

    Exceções:
        Gera um log de erro se ocorrer uma exceção durante a extração das informações do documento.
    """
    try:
        doc = DocumentInfo()
        doc.extract(path)
        return doc
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None


def info_save(document: DocumentInfo):
    """
    Salva as informações de um documento.

    Args:
        document (DocumentInfo): Objeto contendo as informações do documento a ser salvo.

    Returns:
        O resultado da operação de salvamento realizado pelo repositório DocInfoRepository.
    """
    return DocInfoRepository.save(document)


def build(paths=[]) -> List[object]:
    """
    Constrói uma lista de documentos a partir de uma lista de caminhos fornecidos.
    Args:
        paths (list): Lista de caminhos de arquivos para construir os documentos.
    Returns:
        List[object]: Lista de documentos construídos. Retorna uma lista vazia em caso de erro.
    Exceções:
        Loga qualquer exceção que ocorra durante a construção dos documentos.
    """
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


def pdf_reader(path: str = "") -> (pdfplumber.PDF | None):
    """
    Faz a leitura de um documento PDF.

    Args:
        path (str): O caminho para o arquivo PDF. Padrão é uma string vazia.

    Returns:
        O resultado da função reader aplicada ao caminho fornecido.
    """
    return PDFReader(path)


def pdf_content(path: str, init: int = 1, final: int = -1) -> str:
    """
    Lê um arquivo PDF e extrai o texto de suas páginas numa variável só.
    Args:
        path (str): O caminho para o arquivo PDF.
        max_pages (int, opcional): O número máximo de páginas a serem lidas. 
    Returns:
        str: O conteúdo extraído do PDF como uma string. 
    """
    return reader_content(path, init, final)


def pdf_pages_with_details(path: str = "", init: int = 1, final: int = 0) -> List[PageMetadata]:
    """
    Lê as páginas de um arquivo PDF e extrai os metadados.
    Args:
        path (str): Caminho para o arquivo PDF.
        init (int): Número da página inicial (1-indexado). Padrão é 1.
        final (int): Número da página final (1-indexado). Padrão é 0, que indica a última página.
    Returns:
        List[PageMetadata]: Lista de objetos PageMetadata contendo os metadados das páginas lidas.
    Raises:
        ValueError: Se o caminho do arquivo for inválido ou se não for possível ler o arquivo PDF.
        Exception: Para outros erros durante a leitura e extração dos metadados.
    Nota:
        - Se o número da página inicial for maior ou igual ao total de páginas, ele será ajustado para a última página.
        - Se o número da página inicial for menor ou igual a 0, ele será ajustado para 1.
        - Se o número da página final for maior que o total de páginas, ele será ajustado para o total de páginas.
        - Se o número da página final for menor ou igual a 0, ele será ajustado para o total de páginas.
        - Se o número da página final for menor que o número da página inicial, ele será ajustado para o número da página inicial.
    """
    try:
        if not Archive.exists(path):
            raise ValueError("O path está inválido.")

        inf = info(path)
        if inf is None:
            return []

        pdf = PDFReader(path)
        if pdf is None:
            raise ValueError("Não foi possível ler o arquivo pdf.")

        total = inf.pages

        init, final = page_limit_mechanics(init, final, total)

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


def pdf_paragraphs_with_details(path: str = "", init: int = 1, final: int = 0) -> List[ParagraphMetadata]:
    """
    Extrai os parágrafos com os detalhes do documento.
    Args:
        path (str): Caminho para o arquivo do documento. Padrão é uma string vazia.
        init (int): Número da página inicial para leitura. Padrão é 1.
        final (int): Número da página final para leitura. Padrão é 0, que indica leitura até o final do documento.
    Returns:
        List[ParagraphMetadata]: Lista de objetos ParagraphMetadata contendo os detalhes dos parágrafos extraídos.
    """
    try:

        pages = pdf_pages_with_details(path, init, final)

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


def pdf_phrases_with_details(path: str = "", init: int = 1, final: int = 0) -> List[PharseMetadata]:
    """
    Extrai as frases com os detalhes dos documentos.
    Args:
        path (str): O caminho para o arquivo de entrada. Padrão é uma string vazia.
        init (int): O número inicial da página para leitura. Padrão é 1.
        final (int): O número final da página para leitura. Padrão é 0, que indica leitura até o final.
    Returns:
        List[PharseMetadata]: Uma lista de objetos PharseMetadata contendo os detalhes das frases extraídas.
    """
    try:

        paragraphs = pdf_phrases_with_details(path, init, final)

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
    """
    Lê linhas de um documento com detalhes adicionais.

    Args:
        path (str): Caminho para o arquivo do documento. Padrão é uma string vazia.
        init (int): Número da linha inicial para leitura. Padrão é 1.
        final (int): Número da linha final para leitura. Padrão é 0, que indica leitura até o final do documento.

    Returns:
        List[object]: Uma lista de dicionários, onde cada dicionário contém detalhes sobre uma linha do documento, incluindo:
            - path (str): Caminho do parágrafo.
            - page (int): Número da página do parágrafo.
            - content (str): Conteúdo da linha.
            - name (str): Nome do parágrafo.
            - letters (int): Número de letras na linha.
            - uuid (str): UUID único para a linha.
            - source (str): Fonte da linha no formato "nome, pg. página, ln linha".
            - num (int): Número da linha dentro do parágrafo.
            - chunk (List[str]): Lista de pedaços da linha.
            - lines (int): Número total de linhas no parágrafo.
            - chunks (int): Número total de pedaços na linha.
            - size (int): Tamanho do parágrafo.
            - mimetype (str): Tipo MIME do parágrafo.

    Raises:
        Exception: Em caso de erro, registra o erro no log e retorna uma lista vazia.
    """
    try:
        paragraphs = pdf_paragraphs_with_details(path, init, final)
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


def convert_to_pdf(path: str = "", path_out: str = ""):
    """
    Converte um arquivo de texto em um documento PDF.
    Args:
        path (str): Caminho para o arquivo de texto de entrada.
        path_out (str): Caminho para salvar o arquivo PDF gerado.
    Returns:
        str: Caminho do arquivo PDF gerado.
    """

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


def convert_pdf_to_txt(path: str, path_out: str):
    """
    Converte um arquivo PDF em texto e salva o conteúdo em um arquivo de saída.
    Args:
        path (str): O caminho do arquivo PDF de entrada.
        path_out (str): O caminho do arquivo de saída onde o texto extraído será salvo.
    Raises:
        ValueError: Se o caminho do arquivo PDF de entrada for inválido.
        Exception: Para qualquer outra exceção que ocorra durante o processamento.
    Retorna:
        None: Em caso de erro durante a conversão.
    """
    try:
        if not Archive.exists(path):
            raise ValueError("O path está inválido.")
        pdf = pdf_reader(path)

        for page in pdf.pages:
            content = page.extract_text()
            with open(path_out, "a", encoding="utf-8") as file:
                file.write(content)
                file.write("\n")
        pdf.close()

    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None


def open_txt(path: str) -> str | None:
    """
    Abre um arquivo de texto no caminho especificado e retorna seu conteúdo.
    Args:
        path (str): O caminho do arquivo de texto a ser aberto.
    Returns:
        str: O conteúdo do arquivo de texto.
        None: Se ocorrer um erro ao abrir ou ler o arquivo.
    Raises:
        ValueError: Se o caminho do arquivo for inválido.
    """
    try:
        if not Archive.exists(path):
            raise ValueError("O path )" + path + ") está inválido.")
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None


def save_csv(path: str, dictionaties: List[dict], mode: str = 'w') -> bool:
    try:
        return writer_dictionaries_to_csv(path, dictionaties, mode)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def read_csv(path: str):
    try:
        return read_csv_to_dictionaries(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False
