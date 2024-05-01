import logging
import traceback
from typing import List

from src.document import service as DocService
from src.document import retrieval as DocRetrieval
from src.document import documentpdf as DocumentPDF
from src.document import repository as DocRepository


def register_info_by_path(path: str = "") -> bool:
    try:
        return DocRepository.save_info(DocumentPDF.info(path))
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return False


def register_in_batch(path: str = "") -> List[str]:
    try:
        # paths salvas
        paths = []

        for path_full in DocService.read(path):

            # if register_info_by_path(path_full) is False:
            #     continue

            paths.append(path_full)

            # salva metadados
            pages_metadatas = DocumentPDF.read_pages_with_details(path_full)
            for metadata in pages_metadatas:
                DocRepository.save_metadata(metadata)
                DocRetrieval.save_metadata(metadata)
                # DocRetrieval.save_metadata_with_embedings(metadata)

        return paths
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []


def query_generic(question: str = ""):

    print()
    print("CONSULTA SQL -----------------------------------------------------------------------------------------------------------")  # noqa: E501
    res_sql = DocRepository.query_metadata(question, 3)
    for res in res_sql:
        print("-> ", res.content)
    print()

    print("CONSULTA METADATA ------------------------------------------------------------------------------------------------------------------")  # noqa: E501
    res_vec = DocRetrieval.query_metadata(question, 3)
    for re in res_vec:
        print("-> ", re.content)
    print()

    print("CONSULTA EMBEDDING ------------------------------------------------------------------------------------------------------------------")  # noqa: E501
    res_emb = DocRetrieval.query_embeddings(question, 3)
    for r in res_emb:
        print("-> ", r.content)
    print()
