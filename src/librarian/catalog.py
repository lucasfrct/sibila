import json
import logging
import traceback
from typing import List

from src.document import service as DocService
from src.document import retrieval as DocRetrieval
from src.document import documentpdf as DocumentPDF
from src.document import repository as DocRepository

def register_by_path(path: str = "") -> bool:
    try:
        return DocRepository.save(DocumentPDF.info(path))
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False
    
def register_in_bath(path: str = "") -> List[str]:
    try:
        paths = []
        for path_full in DocService.read(path):
    
            if register_by_path(path_full) == False:
                continue
            
            paths.append(path_full)
            # salva metadados
            all_meta = DocumentPDF.paragraphs_with_details(path_full)
            for meta in all_meta:
                DocRepository.save_metadata(meta)
                DocRetrieval.register(meta['content'], meta)
            
        return paths
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []
    
def query_generic(question: str = ""):
    res_sql = DocRepository.query_metadata_include(question, 3)
    res_vec = DocRetrieval.query_text(question, 3)
    
    print()
    print(json.dumps(res_sql, indent=2)) 
    print()
    print("------------------------------------------------------------------------------------------------------------------")
    print()
    print(json.dumps(res_vec, indent=2)) 