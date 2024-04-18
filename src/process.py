import os
from typing import List

from src.entities.model_llama import ModelLlama
from src.entities.document import Doc
from src.display import display

def get_documents(path: str) -> List[Doc]:

    documents_names = os.listdir(path)
    documents = []
    
    for i, document_name in enumerate(documents_names): 
        path_doc = os.path.join(path, document_name)
        documents.append(Doc(path_doc, document_name))    

    return documents


def embed_documents(docs: List[Doc]):
    models = []
    for doc in docs: 
        model = ModelLlama()
        model.document(doc)
        # embedding.metadata_generation()
        model.generate()
        models.append(model)
    
    return models
