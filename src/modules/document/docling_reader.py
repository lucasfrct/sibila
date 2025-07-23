# flake8: noqa: E501
"""
Docling Document Reader Module
Este módulo contém funções para ler documentos usando Docling e extrair texto estruturado das páginas especificadas.
O Docling é especialmente otimizado para análise de documentos jurídicos e oferece melhor extração de texto e estrutura.

Funções:
    - reader(path: str = "") -> DoclingDocument: Faz a leitura de um documento e retorna o objeto Docling.
    - reader_pages(path: str = "", init: int = 1, final: int = 0) -> List[str]: Faz a leitura de um trecho de um arquivo e retorna as páginas em texto puro.
    - reader_content(path: str, init: int = 1, final: int = -1) -> str: Lê um arquivo e extrai todo o texto numa variável.
"""

from typing import List, Optional
import traceback
import logging
import csv
import os

try:
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.datamodel.document import ConversionResult
    from docling_core.types.doc import DoclingDocument, TableItem, TextItem
except ImportError:
    # Fallback para quando o Docling não estiver disponível
    logging.warning("Docling não disponível. Funcionalidade limitada.")
    DocumentConverter = None
    DoclingDocument = None

from src.utils import archive as Archive


def page_limit_mechanics(init: int = 1, final: int = -1, total: int = 1):
    """
    Aplica a mecânica de limite de páginas, garantindo que os valores estejam dentro dos limites válidos.
    """
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


def reader(path: str = "") -> Optional[ConversionResult]:
    """
    Faz a leitura de um documento usando Docling.
    Args:
        path (str): O caminho para o arquivo do documento.
    Returns:
        ConversionResult: Resultado da conversão do Docling se a leitura for bem-sucedida, caso contrário, retorna None.
    Raises:
        ValueError: Se o caminho fornecido for inválido.
    """
    try:
        if not Archive.exists(path):
            raise ValueError("O path está inválido.")

        if DocumentConverter is None:
            raise ImportError("Docling não está disponível.")

        # Configurar o conversor com opções específicas para análise jurídica
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True  # OCR para documentos escaneados
        pipeline_options.do_table_structure = True  # Detectar estrutura de tabelas
        pipeline_options.table_structure_options.do_cell_matching = True
        
        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        
        result = converter.convert(path)
        return result
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None


def reader_pages(path: str = "", init: int = 1, final: int = -1) -> List[str]:
    """
    Faz a leitura de um trecho de um arquivo e retorna as páginas em texto puro.
    Parâmetros:
        path (str): Caminho para o arquivo.
        init (int): Número da página inicial (1-indexado). Padrão é 1.
        final (int): Número da página final (1-indexado). Padrão é -1, que indica a última página.
    Retorna:
        List[str]: Lista de strings contendo o texto das páginas especificadas.
    Exceções:
        ValueError: Se o caminho do arquivo for inválido ou se não for possível ler o arquivo.
    """
    try:
        if not Archive.exists(path):
            raise ValueError("O path está inválido.")

        result = reader(path)
        if result is None:
            raise ValueError("Não foi possível ler o arquivo.")

        doc = result.document
        
        # Extrair texto por página
        pages_content = {}
        for item in doc.texts:
            if hasattr(item, 'prov') and item.prov:
                for prov_item in item.prov:
                    page_num = getattr(prov_item, 'page', 1)
                    if page_num not in pages_content:
                        pages_content[page_num] = []
                    pages_content[page_num].append(item.text)

        # Determinar número total de páginas
        total_pages = max(pages_content.keys()) if pages_content else 1
        init, final = page_limit_mechanics(init, final, total_pages)
        
        # Compilar páginas solicitadas
        pages = []
        for page_num in range(init, final + 1):
            if page_num in pages_content:
                page_text = "\n".join(pages_content[page_num])
            else:
                page_text = ""
            pages.append(page_text)

        return pages
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def reader_content(path: str, init: int = 1, final: int = -1) -> str:
    """
    Lê um arquivo e extrai o texto de suas páginas numa variável só.
    Args:
        path (str): O caminho para o arquivo.
        init (int): Página inicial (1-indexado). Padrão é 1.
        final (int): Página final (1-indexado). Padrão é -1 (última página).
    Returns:
        str: O conteúdo extraído do documento como uma string. 
    """
    try:
        result = reader(path)
        if result is None:
            return ""

        doc = result.document
        
        # Extrair todo o texto do documento
        all_text = []
        for item in doc.texts:
            all_text.append(item.text)
        
        return "\n".join(all_text)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return ""


def extract_structured_content(path: str) -> dict:
    """
    Extrai conteúdo estruturado do documento incluindo textos, tabelas e metadados.
    Esta função é específica do Docling e oferece análise mais rica para documentos jurídicos.
    
    Args:
        path (str): Caminho para o arquivo.
        
    Returns:
        dict: Dicionário contendo textos, tabelas, títulos e outros elementos estruturados.
    """
    try:
        result = reader(path)
        if result is None:
            return {}

        doc = result.document
        
        structured_content = {
            'texts': [],
            'tables': [],
            'titles': [],
            'figures': [],
            'metadata': {}
        }
        
        # Extrair textos estruturados
        for item in doc.texts:
            text_info = {
                'text': item.text,
                'label': getattr(item, 'label', 'text'),
                'page': None
            }
            
            # Tentar extrair informação de página
            if hasattr(item, 'prov') and item.prov:
                for prov_item in item.prov:
                    if hasattr(prov_item, 'page'):
                        text_info['page'] = prov_item.page
                        break
            
            if text_info['label'] in ['title', 'section_header']:
                structured_content['titles'].append(text_info)
            else:
                structured_content['texts'].append(text_info)
        
        # Extrair tabelas
        for item in doc.tables:
            if isinstance(item, TableItem):
                table_info = {
                    'table_data': item.data,
                    'caption': getattr(item, 'caption', ''),
                    'page': None
                }
                
                # Tentar extrair informação de página
                if hasattr(item, 'prov') and item.prov:
                    for prov_item in item.prov:
                        if hasattr(prov_item, 'page'):
                            table_info['page'] = prov_item.page
                            break
                
                structured_content['tables'].append(table_info)
        
        # Extrair metadados do documento
        if hasattr(doc, 'meta'):
            structured_content['metadata'] = doc.meta
            
        return structured_content
        
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return {}


def get_document_info(path: str) -> dict:
    """
    Extrai informações básicas do documento usando Docling.
    
    Args:
        path (str): Caminho para o arquivo.
        
    Returns:
        dict: Informações do documento incluindo número de páginas, tipo, etc.
    """
    try:
        result = reader(path)
        if result is None:
            return {}

        doc = result.document
        
        # Calcular número de páginas
        pages = set()
        for item in doc.texts:
            if hasattr(item, 'prov') and item.prov:
                for prov_item in item.prov:
                    if hasattr(prov_item, 'page'):
                        pages.add(prov_item.page)
        
        info = {
            'pages': len(pages) if pages else 1,
            'document_type': getattr(doc, 'document_type', 'unknown'),
            'title': '',
            'language': getattr(doc, 'language', 'unknown')
        }
        
        # Tentar extrair título
        for item in doc.texts:
            if hasattr(item, 'label') and item.label == 'title':
                info['title'] = item.text
                break
        
        return info
        
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return {}


# Funções auxiliares mantidas para compatibilidade com CSV
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