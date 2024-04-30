import os
import logging
import traceback
from typing import List

def read(path: str = "") -> List[str]:
    try:
        path = os.path.normpath(path)
        if not os.path.exists(path):
            raise ValueError("O path está inválido.")
        
        return os.listdir(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []