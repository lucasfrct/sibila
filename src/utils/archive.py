import os
import logging
import traceback
from io import BufferedReader
from typing import List, Optional


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


def reader(path: str = "") -> Optional[BufferedReader]:
    try:
        if not os.path.exists(path):
            raise ValueError("O path está inválido.")
        return open(os.path.normpath(path), 'rb')
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None
