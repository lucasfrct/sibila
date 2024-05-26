import os
import logging
import traceback
from io import BufferedReader
from typing import List, Optional


def names(path: str = "") -> List[str]:
    """retorna os nomes num diretório"""
    try:
        path = os.path.normpath(path)
        if not os.path.exists(path):
            raise ValueError("O path está inválido.")
        return os.listdir(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def paths(path: str = "") -> List[str]:
    """le os pths de uma diretório"""
    try:
        return [os.path.normpath(f"{path}/{name}") for name in names(path)]
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def reader(path: str = "") -> Optional[BufferedReader]:
    """le um arquivo em disco"""
    try:
        if not os.path.exists(path):
            raise ValueError("O path está inválido.")
        return open(os.path.normpath(path), 'rb')
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None


def exists(path: str = "") -> bool:
    """verifica o path"""
    try:
        if not os.path.exists(path):
            raise ValueError("O path está inválido.")
        return True
    except Exception:
        return False
