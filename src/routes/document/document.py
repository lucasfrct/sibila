from flask import request

from src.modules.document import service as DocService
from src.modules.response.response import Response


async def document_pages_details():
    path = request.args.get('path', default='', type=str).strip()
    init = request.args.get('init', default=1, type=int)
    final = request.args.get('final', default=0, type=int)

    if not path:
        return Response.error(400, "DOC001", "Parâmetro 'path' é obrigatório").result()

    pages = DocService.document_pages_with_details(path, init, final)
    pages_data = [page.dict() for page in pages]
    return Response.success(200, pages_data).result()
