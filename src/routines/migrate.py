
from src.document import repository as DocumentRepository

def tables():
	DocumentRepository.table_documents_info()
	DocumentRepository.table_documents_metadatas()