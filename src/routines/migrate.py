# flake8: noqa: E501

from src.modules.document import document_info_repository as DocInfoRepository
from src.modules.document import paragraph_metadata_repository as ParagraphRepository


def tables():
    DocInfoRepository.table_documents_info()
    ParagraphRepository.table_paragraphs_metadatas()
