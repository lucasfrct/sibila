

from src.modules.response.response import Response
from src.modules.catalog import handles as Catolog


def corpus_generate(directory: str = 'dataset/library'):
    regitreds = Catolog.register_content_in_bath(directory)
    return Response.success(200, regitreds).result()
