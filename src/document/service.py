import os
import sys
import logging
import traceback
from typing import List, Optional

from src.document import repository as DocRepository 
from src.document import documentpdf as DocumentPDF
# from src.document import retrieval as DocRetrieval 

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
        for path_name in read(path):
            path_full = os.path.normpath(os.path.join(path, path_name))
            
            if DocRepository.has_document(path_full):
                continue
            
            if not DocRepository.save(DocumentPDF.info(path)):
                continue
            
            all_meta = DocumentPDF.paragraphs_with_details(path_full)
            for meta in all_meta:
                if not DocRepository.save_metadata(meta):
                    continue
                # DocRetrieval.register(meta['content'], meta)
        
        query_generic("amor")
      
        
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return  None
    
def query_generic(question: str = ""):
    res_sql = DocRepository.query_metadata_include(question, 5)
    # res_vec = DocRetrieval.query_text(question, 5)
    
    print()
    print(len(res_sql), res_sql) 
    print()
    # print(len(res_vec), res_vec) 