# flake8: noqa: E501


from src.modules.response.response import Response
from src.modules.corpus import corpus as Corpus


def corpus_generate(directory: str = 'dataset/sources'):
    Corpus.generate_anotations(directory)
    return Response.success(200, "Gerador de corpus iniciado").result()
