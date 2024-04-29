import os
import sys
import logging
import traceback
from typing import List, Optional

from src.librarian import catalog as Catalog

def names(path: str = "") -> List[str]:
    try:
        path = os.path.normpath(path)
        if not os.path.exists(path):
            raise ValueError("O path está inválido.")
        
        return os.listdir(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []
    
def paths(path: str = "") -> List[str]:
    try:
        return [os.path.normpath(f"{path}/{name}") for name in names(path)]
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []
    
def register(path: str = "") -> List[str]:
    try:
        return Catalog.register_in_bath(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []