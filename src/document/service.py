import os
import sys
import logging
import traceback
from typing import List, Optional

from src.document import pdfdoc as PDFDoc
from src.document.doc import Doc
from src.document import repository as DocRepository 
from src.document import retrieval as DocRetrival 

def read(path: str = "") -> List[str]:
    try:
        if not os.path.exists(path):
            raise ValueError("O path está inválido.")
        
        return os.listdir(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
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
    
def process_bath(path: str = ""):
    try:
        for path_name in read(path):
            path_full = os.path.normpath(os.path.join(path, path_name))
            
            if not DocRepository.has_document(path_full):
                continue
            
            all_meta = PDFDoc.lines_with_details(path_full, 1, 2)
            for meta in all_meta:
                DocRepository.save_metadata(meta)
                DocRetrival.register(meta['content'], meta)
        
        question = "amor"
        res_sql = DocRepository.query_metadata_include(question, 5)
        res_vec = DocRetrival.query_text(question, 5)
        
        print()
        print(len(res_sql), res_sql) 
        print()
        print(len(res_vec), res_vec) 
        
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return  None