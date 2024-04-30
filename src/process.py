import os
from typing import List

from src.entities.model_llama import ModelLlama
from src.document.documentpdf import Doc
from src.display import display

def get_documents(path: str) -> List[Doc]:

    documents_names = os.listdir(path)
    documents = []
    
    for i, document_name in enumerate(documents_names): 
        path_doc = os.path.join(path, document_name)
        documents.append(Doc(path_doc, document_name))    

    return documents


def embed_document(doc: Doc):
    model = ModelLlama()
    model.chunks, model.metadatas = doc.chunks_and_metadatas
    # embedding.metadata_generation()
    model.generate()
    return model

    
