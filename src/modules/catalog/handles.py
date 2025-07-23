# flake8: noqa: E501

import logging
import traceback
from typing import List

from src.utils import archive as Archive
from src.modules.document import service as DocService
from src.modules.document.document_info import DocumentInfo
from src.modules.analysis import legislation as Legislation
from src.modules.catalog import catalog_retrieval as CatalogRetrieval


""" Deve catalogar todo o conteúdo dentro do corpus de documentos. """

def names(path: str = "") -> List[str]:
    """
    captura os nomes dos arquivos no caminho passado

    Args:
        path (str): Caminho do diretório onde os nomes dos arquivos serão capturados. 
                    Se não for especificado, será utilizado um caminho padrão.

    Returns:
        List[str]: Lista de nomes de arquivos no caminho especificado. 
                   Retorna uma lista vazia em caso de erro.
    """
    try:
        return Archive.names(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def paths(path: str = "") -> List[str]:
    """
    Captura os caminhos dos arquivos no diretório especificado.

    Args:
        path (str): Caminho do diretório onde os arquivos serão procurados. 
                    Se não for especificado, será utilizado um caminho padrão.

    Returns:
        List[str]: Lista de caminhos dos arquivos encontrados no diretório.

    Exceções:
        Em caso de erro, será registrado no log e uma lista vazia será retornada.
    """
    try:
        return Archive.paths(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def register_info_by_path(path: str = "") -> DocumentInfo | None:
    """
    Registra informações de um documento a partir de um caminho especificado.

    Args:
        path (str): O caminho do documento. Valor padrão é uma string vazia.

    Returns:
        DocumentInfo | None: Retorna um objeto DocumentInfo se o registro for bem-sucedido, 
        caso contrário, retorna None.

    Exceções:
        Captura e registra qualquer exceção que ocorra durante o processo de registro.
    """
    try:
        doc = DocService.info(path)
        if DocService.info_save(doc) != True:
            return None
        return doc
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None


def register_info_in_bath(directory: str = "") -> List[DocumentInfo]:
    """
    Registra informações de documentos em lote a partir de um diretório especificado.
    Args:
        directory (str): O caminho do diretório contendo os documentos a serem registrados. 
                         Se não for especificado, será utilizado um diretório padrão.
    Returns:
        List[DocumentInfo]: Uma lista de objetos DocumentInfo representando os documentos registrados.
                            Retorna uma lista vazia em caso de erro.
    """

    try:
        # paths salvas
        docs = []

        # lista dos paths no diretório
        for path in DocService.dir(directory):

            # registra o documento para indexado, caso der um erro pula pra o proxímo
            doc = register_info_by_path(path)
            if doc is None:
                continue

            # adiciona o path na lista de indexados
            docs.append(doc)

        return docs
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def register_content_in_bath(directory: str):

    docs = register_info_in_bath(directory)

    saveds = []
    for dc in docs:
        d = dc.dict()
        content_file = open(d["path"], "r", encoding="utf-8")
        content = content_file.read()
        content_file.close()
        if CatalogRetrieval.save(d["path"], d["name"], d["pages"], content) is None:
            continue
        saveds.append(d["name"])

    return saveds


def register_legislation_in_bath(directory: str):

    # docs = register_info_in_bath(directory)
    pths = paths(directory)

    saveds = []
    for dc in pths:
        print("PTH: ", dc)
        if dc.__contains__("pdf.txt") is False:
            continue
        
        # d = dc.dict()
        # path_txt = d["path"] + ".txt"
        # DocService.convert_document_to_txt(d["path"], path_txt)
        
        content = DocService.open_txt(dc)
        if content is None:
            continue
        
        articles = Legislation.split_into_articles(content)
        for article in articles:
            print("-=-> ", article[:20], len(article))

        print("ARTIGOS: ", len(articles))
        
        # if CatalogRetrieval.save(d["path"], d["name"], d["pages"], content) is None:
        #     continue
        # saveds.append(d["name"])
        saveds.append(dc)

    return saveds


def list():
    return []


def search(term: str, results: int = 5, threshold: float = 0.3):
    return CatalogRetrieval.query(term, results, threshold)


def prompt_search_in_docs(prompt: str, docs) -> str:

    flat_docs = ""

    for doc in docs:
        flat_docs += "\n"
        flat_docs += f"Documento: {doc["name"]}"
        flat_docs += "\n"
        flat_docs += doc["content"]
        flat_docs += "\n"
        flat_docs += f"Fonte: {doc["source"]}"
        flat_docs += "\n"
        flat_docs += "\n\n"

    prompt = f"""
        Seu nome pe Cadmo.
        Você é um bibliotecário que responde a uma pergunta de um usuário.
        Voce tem acesso a um catálogo de documentos.
        Voce é extremamente certiro e não inventa frase nem trechos.
        Sempre que possível, você fornece a fonte e uma citação do texto na íntegra.
        Sua fonte de verdade são os documentos abaixo.
        Sempre cite trecho com começo meio e fim.

        {flat_docs}

        Com base nos documento responda:  {prompt}
    """

    return prompt
