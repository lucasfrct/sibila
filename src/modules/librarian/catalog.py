# flake8: noqa: E501

from src.modules.document import paragraph_metadata_retrieval as ParagraphRetrieval
from src.modules.document import paragraph_metadata_repository as ParagraphRepository


def query_generic(question: str = ""):

    print()
    print("CONSULTA SQL (PARAGRAFOS) -----------------------------------------------------------------------------------------------------------")  # noqa: E501
    res_sql = ParagraphRepository.query_metadata(question, 3)
    for res in res_sql:
        print("-> ", res.content)
    print()

    print("CONSULTA METADATA (PARAGRAFOS) ------------------------------------------------------------------------------------------------------------------")  # noqa: E501
    res_vec = ParagraphRetrieval.query_metadata(question, 3)
    for re in res_vec:
        print("-> ", re.content)
    print()

    print("CONSULTA EMBEDDING (PARAGRAFOS) ------------------------------------------------------------------------------------------------------------------")  # noqa: E501
    res_emb = ParagraphRetrieval.query_embeddings(question, 3)
    for r in res_emb:
        print("-> ", r.content)
    print()
