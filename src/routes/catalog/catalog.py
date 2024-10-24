
from flask import request


from src.modules.response.response import Response
from src.modules.catalog import handles as Catolog


def catalog_list(directory: str = 'dataset/library'):
    catalog_list = Catolog.list(directory)
    return Response.success(200, catalog_list).result()


def catalog_indexer(directory: str = 'dataset/library'):
    regitreds = Catolog.register_content_in_bath(directory)
    return Response.success(200, regitreds).result()


def catalog_search():
    search_query = request.args.get('query', default='', type=str).strip()
    catalog_list = Catolog.search(search_query, 5, 0.3)
    return Response.success(200, catalog_list).result()
