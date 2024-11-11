# flake8: noqa: E501

from flask import request

from src.modules.response.response import Response
from src.modules.document import service as DocService


def dataset_dir_list():

    directory = request.args.get('dir', default='', type=str).strip() or './dataset/library'

    paths = DocService.dir(directory)
    docs = []
    
    for path in paths:
        doc_info = DocService.info(path)
        if doc_info is None:
            continue
        docs.append(doc_info.dict())

    return Response.success(200, docs).result()

