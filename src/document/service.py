import sys
import os
import logging
import traceback
from typing import List,  Optional

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

def build(paths: [] = []) -> List[Doc]:
    try:
        documents = []

        for _, path in enumerate(paths): 
            if not path:
                continue
            
            document = builder(path)
            if document == None:
                continue

            documents.append(document)

        return documents
    except Exception as e:
        logging.error(e)
        return []
    
def builder(path: str = "") -> Optional[Doc]:
    try:
        if not os.path.exists(path):
            raise ValueError("O path está inválido.")
        
        path = os.path.normpath(path)
        name = os.path.basename(path)
        return Doc(name, path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None
    