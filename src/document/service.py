import os
import sys
import logging
import traceback
from typing import List, Optional

from src.document import repository as DocRepository 
from src.document import documentpdf as DocumentPDF
from src.librarian import catalog as Catalog
from src.utils import archive as Archive

def read(path: str = "") -> List[str]:
    try:
       return Archive.paths(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []

def build(paths: [] = []) -> List[object]:
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
    
def builder(path: str = ""):
    try:
        if not os.path.exists(path):
            raise ValueError("O path está inválido.")
        
        return DocumentPDF.read_with_details(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None
    
def process_bath(path: str = ""):
    try:
       return Catalog.register_in_bath(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return  None
    
def query_generic(question: str = ""):
    Catalog.query_generic(question)