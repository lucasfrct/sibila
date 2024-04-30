import logging
import traceback
from typing import List

from src.librarian import catalog as Catalog
from src.utils import archive as Archive


def names(path: str = "") -> List[str]:
    try:
        return Archive.names(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def paths(path: str = "") -> List[str]:
    try:
        return Archive.paths(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def register(path: str = "") -> List[str]:
    try:
        return Catalog.register_in_batch(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []