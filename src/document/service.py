import sys
import os
import logging
from typing import List

from src.document.doc import Doc
# from src import process

def read(path: str = "./docs") -> List[Doc]:
    try:

        if not os.path.exists(path):
            raise ValueError("O path está inválido.")
        
        names = os.listdir(path)
        documents = []

        for _, name in enumerate(names): 
            if not name:
                continue

            doc_path = os.path.normpath(os.path.join(path, name))
            documents.append(Doc(name, doc_path))

        return documents
    except Exception as e:
        logging.error(e)
        return []


def load(path: str = '.'): 
    
    # print("\n", "########## Iniciando registro de documentos ##########", "\n")
    # documents = process.get_documents(path)
    # documents_size = len(documents)
    # for i, document in enumerate(documents): 
    #     print(f"    {i+1}/{documents_size}: {document.info}")

    # print("\n", "########## Iniciando embedings de documentos ##########", "\n")
    # for i, document in enumerate(documents):
        
    #     doc_data = sqlite.get_documents_by_path(document.name)
    #     if(len(doc_data) > 0):
    #         print(f"    {i+1}: {document.info} ****EMBEDED****\n")
    #         continue

    #     model = process.embed_document(document)
    #     doc = (document.name.lower(), document.name, "pdf")

    #     sqlite.add_document(doc)
    #     chromadb.save_model(model)

    #     chart(f"{document.name}", model)
    #     print(f"    {i+1}: {document.info}")
    pass





