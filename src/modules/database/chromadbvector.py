import os
import chromadb
import logging


def client(path: str = "./data/chromadb") -> chromadb.ClientAPI:
    """ cliente para chroma DB """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return chromadb.PersistentClient(path=path)
    except Exception as e:
        logging.error(e)
        return None


def collection(collection_name: str) -> chromadb.Collection:
    """ Inicia uma coleçoa para chorma DB"""
    return client().get_or_create_collection(name=collection_name)
