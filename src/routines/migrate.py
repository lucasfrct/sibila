
from src.modules.document import document_info_repository as DocInfoRepository
from src.modules.document import page_metadata_repository as PageRepository


def tables():
    DocInfoRepository.table_documents_info()
    PageRepository.table_pages_metadatas()
