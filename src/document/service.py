import sys
import os
import logging
from typing import List

from src.document.doc import Doc

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