# flake8: noqa: E501

from datetime import datetime
from flask import request
import os

from src.utils.log import log_info
from src.utils.clock import delta_time
from src.utils import string as String
from src.modules.corpus import corpus as Corpus
from src.modules.response.response import Response
from src.modules.document import service as DocService


def corpus_list():
    """
    Lista os documentos presentes no diretório de corpus.
    Esta função percorre o diretório especificado e coleta informações sobre
    cada documento encontrado. As informações dos documentos são obtidas
    através do serviço `DocService` e são retornadas em uma lista.
    Returns:
        dict: Um dicionário contendo o status da resposta e a lista de 
        documentos com suas respectivas informações.
    """

    paths = DocService.dir(Corpus.directory_soruce)
    docs = []

    for path in paths:
        doc_info = DocService.info(path)
        if doc_info is None:
            continue
        docs.append(doc_info.dict())

    return Response.success(200, docs).result()


async def corpus_generate():

    path: str = request.args.get('path', default='', type=str)
    page_start: int = request.args.get('page_start', default=1, type=int)
    page_end: int = request.args.get('page_end', default=-1, type=int)


    if not path or path == '':
        return Response.error(400, 'COR000', 'O camonho do arquivo não foi informado.').result()

    path = os.path.normpath(path)
    
    if not DocService.is_file(path):
        return Response.error(400, 'COR001', 'O caminho informado não é um arquivo.').result()
    
    paths_corpus = DocService.dir(Corpus.directory_soruce)
    for path_corpus in paths_corpus:
        print("-> ", path_corpus, path)
        if String.path_name(path_corpus) == String.path_name(path):
            return Response.error(409, 'COR002', 'O documento já foi transformado numa corpus.').result()
    
    time_init = datetime.now()

    log_info("", "Documento: iniciando loadding....", delta_time(time_init))
    doc = Corpus.doc_with_articles(path, page_start, page_end)
    log_info("", "Documento: loading terminado em: ", delta_time(time_init))
    
    if doc is None or doc['total_articles'] == 0:
        return Response.error(400, 'COR001', 'O documentos não possui artigos.').result()
    
    time_init = datetime.now()
    log_info("", "Anotação iniciada", delta_time(time_init))

    annotations = Corpus.take_notes(doc['articles'])
    
    log_info("", "Anotação finalizada",delta_time(time_init))

    return Response.success(201, annotations).result()
    # return Response.success(201, path).result()
