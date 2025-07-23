# flake8: noqa: E501

from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Value
from datetime import datetime
from typing import Any, Callable
from typing import List
from time import sleep
import asyncio


from src.modules.analysis import legislation as Legislation
from src.modules.document import service as DocService
from src.utils.array import ArrayControl
from src.utils.clock import delta_time
from src.utils.log import log_info

global counter
counter = Value('i', 0)

arr_control = ArrayControl()

directory_soruce = './dataset/corpus'

def doc_with_articles(path: str, page_init: int = 1, page_final: int = -1):
    """
    Extrai informações de um documento PDF e divide seu conteúdo em artigos.
    Args:
        path (str): O caminho para o arquivo PDF.
        page_init (int, opcional): A página inicial para extração. Padrão é 1.
        page_final (int, opcional): A página final para extração. Padrão é -1, que indica até a última página.
    Returns:
        dict: Um dicionário contendo informações do documento e os artigos extraídos.
        None: Se as informações do documento não puderem ser obtidas.
    """

    doc_info = DocService.info(path)
    if doc_info is None:
        return None

    doc = doc_info.dict()
    doc_file = DocService.pdf_content(doc['path'], page_init, page_final)

    doc['articles'] = Legislation.split_into_articles(doc_file)
    doc['total_articles'] = len(doc['articles'])

    return doc


def annotate_the_article(text: str):
    return {
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


def take_notes(articles: List[str]):
    annotations = []
    for i, article in enumerate(articles):
        time_article_init = datetime.now()
        annotations.append(annotate_the_article(article))
        log_info(f"{i:04}", f"{article[0:48]}...", delta_time(time_article_init))
    return articles
        

# async def process_task(executor, articles: List[dict], doc_articles: List[dict], task: Callable[[int, str], dict], index_position: int, text: str):
#     global arr_control

#     loop = asyncio.get_event_loop()
#     article = await loop.run_in_executor(executor, task, index_position, text)
#     doc_articles[index_position] = article

#     items = arr_control.fetch_contiguous_items(doc_articles)
#     path = "dataset/corpus/contituicao_federativa_do_brasil_comentada.csv"
#     DocService.save_csv(path, items, 'a')

#     for item in items:
#         articles.append(item)


# async def process_anotations(path_source: str, path_corpus: str, max_concurrent_tasks: int = 100) -> List[str]:
#     global counter
#     global arr_control

#     page_init = 1
#     page_final = -1
#     article_initial = ''
#     article_final = ''

#     print("*****************************************************************************")
#     articles = []

#     # time_init = datetime.now()

#     # log_info("", "Documentos iniciados")
#     # docs = doc_with_articles(path_source, page_init, page_final)
#     # log_info("", "Documentos carregados", delta_time(time_init))


#     # tasks = []
#     # executor = ThreadPoolExecutor(max_workers=max_concurrent_tasks)
#     # time_init = datetime.now()

#     # counter.value = 0
#     # for doc in docs:
#     #     log_info("", "Anotação iniciada", delta_time(time_init))

#     #     doc_with_articles(path_source, page_init, page_final)
        
#     #     arr_control.reset()
#     #     doc_arts = arr_control.slice_between_match(
#     #         article_initial, article_final, doc['articles'])
#     #     doc_articles = [None] * len(doc_arts)

#     #     for i, text in enumerate(doc_arts):
#     #         tasks.append(process_task(executor, articles, doc_articles, generate_anotation_to_aticle, i, text))

#     # await asyncio.gather(*tasks)

#     # log_info("", "Anotação finalizada ........................",
#     #          delta_time(time_init))
#     print("*****************************************************************************")
#     return articles


# def generate_anotations(path_source: str = 'dataset/sources', path_corpus: str = "dataset/corpus"):
#     global arr_control
#     arr_control.reset()
#     asyncio.run(process_anotations(path_source, path_corpus, 10))
    

