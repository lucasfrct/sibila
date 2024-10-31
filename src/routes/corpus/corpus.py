# flake8: noqa: E501

import threading

from src.modules.response.response import Response
from src.modules.corpus import corpus as Corpus


async def corpus_generate(directory: str = 'dataset/sources'):
    thread = threading.Thread(target=Corpus.generate_anotations, args=(directory))
    thread.daemon = True 
    thread.start()
    return Response.success(200, "Gerador de corpus iniciado").result()
