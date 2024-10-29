# flake8: noqa: E501

from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Value
from datetime import datetime
from typing import Callable
from typing import List
from time import sleep
import asyncio

from src.modules.analysis import legislation as Legislation
from src.modules.document import service as DocService
from src.utils.clock import delta_time
from src.utils.log import log_info

global counter
counter = Value('i', 0)


def sources(directory: str = 'dataset/sources'):
    """
    Retorna uma lista de caminhos de arquivos em um diretório especificado.
    Args:
        directory (str): O caminho do diretório onde os arquivos estão localizados. 
    Returns:
        list: Uma lista de caminhos de arquivos no diretório especificado.
    """
    list_paths = DocService.dir(directory)
    return list_paths


def sources_info(directory: str = 'dataset/sources'):
    """
    Obtém informações sobre as fontes de documentos em um diretório especificado.
    Args:
        directory (str): O caminho do diretório onde as fontes estão localizadas. 
    Returns:
        list: Uma lista de dicionários contendo informações sobre cada documento.
    """
    list_paths = sources(directory)
    docs = []
    for path in list_paths:
        doc_info = DocService.info(path)
        if doc_info is None:
            continue
        docs.append(doc_info.dict())
    return docs


def massive(directory: str = 'dataset/sources', init: int = 1, final: int = -1):
    docs = sources_info(directory)
    for doc in docs:
        doc['content'] = DocService.pdf_content(doc['path'], init, final)
    return docs


def docs_with_articles(directory: str = 'dataset/sources', init: int = 1, final: int = -1):
    docs = massive(directory, init, final)
    for doc in docs:
        doc['articles'] = Legislation.split_into_articles(doc['content'])
        doc['total_articles'] = len(doc['articles'])
        del doc['content']

    return docs


def generate_anotation_by_aticle(index_position: int, text: str):
    global counter

    time_article_init = datetime.now()
    article = {
        "text": text,
        "subject": Legislation.set_a_title(text),
        # "sumamry": Legislation.summarize(text),
        # "entities": Legislation.extract_entities(text),
        # "categories": Legislation.define_categories(text),
        # "penalties": Legislation.extract_the_penalties(text),
        # "definition": Legislation.define_the_legal_terms(text),
        # "dates": Legislation.extract_legal_dates_and_deadlines(text),
        # "normativeTipe": Legislation.define_the_normative_type(text),
    }
    path = "dataset/corpus/contituicao_federal.csv"
    DocService.save_csv(path, [article], 'a')

    with counter.get_lock():
        counter.value += 1

    i = f"{counter.value:04}"
    p = f"{index_position:04}"

    log_info(f"{i}", f"{p} {text[0:48]}...", delta_time(time_article_init))
    sleep(0.001 * (index_position % 10))

    return article


async def process_task(executor, articles: List[str], task: Callable[[int, str], dict], index_position: int, text: str):
    loop = asyncio.get_event_loop()
    article = await loop.run_in_executor(executor, task, index_position, text)
    print("------ article: ", article['text'][0:64], " ----------- ")
    articles[index_position] = article


async def process_anotations(directory: str = 'dataset/sources', max_concurrent_tasks: int = 100) -> List[str]:
    global counter

    page_init = 1
    page_final = 12

    print("*****************************************************************************")

    time_init = datetime.now()

    log_info("", "Documentos iniciados")
    docs = docs_with_articles(directory, page_init, page_final)
    log_info("", "Documentos carregados", delta_time(time_init))

    articles = [None] * sum(len(doc['articles']) for doc in docs)

    tasks = []
    executor = ThreadPoolExecutor(max_workers=max_concurrent_tasks)
    time_init = datetime.now()

    counter.value = 0
    for doc in docs:
        log_info("", "Anotação iniciada", delta_time(time_init))
        for i, text in enumerate(doc['articles']):
            tasks.append(process_task(executor, articles, generate_anotation_by_aticle, i, text))

    await asyncio.gather(*tasks)

    log_info("", "Anotação finalizada ......................................................", delta_time(time_init))
    print("*****************************************************************************")
    return articles


def generate_anotations(directory: str = 'dataset/sources'):
    return asyncio.run(process_anotations(directory, 10))
