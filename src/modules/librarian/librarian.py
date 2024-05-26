# flake8: noqa: E501

import logging
import traceback
from typing import List

from src.utils import archive as Archive
from src.modules.document import service as DocService
from src.modules.document import document_info_repository as DocInfoRepository
from src.modules.document import paragraph_metadata_retrieval as ParagraphRetrieval
from src.modules.document import paragraph_metadata_repository as ParagraphRepository


def names(path: str = "") -> List[str]:
    """captura os nomes dos arquivos no caminho passado"""
    try:
        return Archive.names(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def paths(path: str = "") -> List[str]:
    """captura os paths dos arquivos no caminho passado"""
    try:
        return Archive.paths(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def register_info_by_path(path: str = "") -> bool:
    """registra as informaçoes de metadados do documento"""
    try:
        return DocInfoRepository.save_info(DocService.info(path))
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def register_in_bath(directory: str = "") -> List[str]:
    """Registra documentos PDF em lote para um diretório com os PDFs"""
    try:
        # paths salvas
        paths = []

        # lista dos pths no diretório
        for path in DocService.read(directory):

            # registra o documento para indexado, caso der um erro pula pra o proxímo
            if register_info_by_path(path) is False:
                continue

            # adiciona o path na lista de indexados
            paths.append(path)

            # extra os metadados do documento
            pargraphs = DocService.read_paragraphs_with_details(path)
            for paragraph in pargraphs:
                ParagraphRepository.save_metadata(paragraph)
                ParagraphRetrieval.save_metadata(paragraph)
                ParagraphRetrieval.save_embedings(paragraph)

        return paths
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []
