import os
import logging
import traceback
from typing import List

# from src.librarian import catalog as Catalog
from src.utils import archive as Archive

def names(path: str = "") -> List[str]:
    try:
        return Archive.read(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []
    
def paths(path: str = "") -> List[str]:
    try:
        return [os.path.normpath(f"{path}/{name}") for name in names(path)]
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []
    
# def register(path: str = "") -> List[str]:
#     try:
#         return Catalog.register_in_bath(path)
#     except Exception as e:
#         logging.error(f"{e}\n%s", traceback.format_exc())
#         return []