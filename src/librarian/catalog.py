import os
import logging
import traceback
from typing import List

from src.document import repository as DocRepository
from src.document import service as DocService
from src.document import documentpdf as PDFDoc
from src.document.documentpdf import Documentpdf as DocumentPDF

def register_by_path(path: str = "") -> bool:
    try:
    	# if DocRepository.has_document(path) == True:
        #     return True
        return DocRepository.save(DocumentPDF(os.path.basename(path), path))
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False
    
def register_in_bath(path: str = "") -> List[str]:
    try:
        paths = []
        for path_name in DocService.read(path):
            path_full = os.path.normpath(os.path.join(path, path_name))
            
            if register_by_path(path_full):
                continue
            
            paths.append(path_full)
            # salva metadados
            all_meta = PDFDoc.paragraphs_with_details(path_full)
            for meta in all_meta:
                DocRepository.save_metadata(meta)
                # DocRetrieval.register(meta['content'], meta)
                
            
        return paths
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []