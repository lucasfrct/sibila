# flake8: noqa: E501

import logging
import traceback
from typing import List

from src.utils import archive as Archive
from src.modules.document import service as DocService
from src.modules.document.document_info import DocumentInfo
from src.modules.document import document_info_repository as DocInfoRepository

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


def register_info_by_path(path: str = "") -> DocumentInfo | None:
    """registra as informaçoes de metadados do documento"""
    try:
        doc = DocService.info(path)
        if DocInfoRepository.save(doc) != True:
            return None
        return doc
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None


def register_info_in_bath(directory: str = "") -> List[DocumentInfo]:
    """Registra documentos PDF em lote para um diretório com os PDFs"""
    try:
        # paths salvas
        docs = []

        # lista dos pths no diretório
        for path in DocService.read(directory):

            # registra o documento para indexado, caso der um erro pula pra o proxímo
            doc = register_info_by_path(path) 
            if doc is None:
                continue

            # adiciona o path na lista de indexados
            docs.append(doc)


        return docs
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def list() -> List[DocumentInfo] :
    """list"""
    try:
        return DocInfoRepository.list()
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False