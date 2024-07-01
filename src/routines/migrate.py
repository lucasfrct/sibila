# flake8: noqa: E501

import logging
import traceback

from src.modules.document import document_info_repository as DocInfoRepository
from src.modules.document import paragraph_metadata_repository as ParagraphRepository

def tables():
    try:
        DocInfoRepository.table_documents_info()
        ParagraphRepository.table_paragraphs_metadatas()
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
