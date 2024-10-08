# flake8: noqa: E501
import os

from src.modules.librarian import librarian as Librarian
from src.modules.librarian import catalog_retrieval as CatalogRetrieval

def register(directory: str): 
    
    docs = Librarian.register_info_in_bath(directory)
    
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
    
def list():
    docs = Librarian.list()
    return [doc.dict()["name"] for doc in docs]

def search(term: str, results: int = 5, threshold: float = 0.3):
    return CatalogRetrieval.query(term, results, threshold)

def prompt_search_in_docs(prompt: str, docs) -> str:
    
    flat_docs = ""
    
    for doc in docs:
        flat_docs +="\n"
        flat_docs += f"Documento: {doc["name"]}"
        flat_docs +="\n"
        flat_docs += doc["content"]
        flat_docs +="\n"
        flat_docs += f"Fonte: {doc["source"]}"
        flat_docs +="\n"
        flat_docs +="\n\n"
        
    prompt = f"""
        Você é uma bibliotecário que responde a uma pergunta de um usuário.
        Voce tem acesso a um catálogo de documentos.
        Voce é extremamente certiro e não inventas frase nem trechos.
        Sempre que possível, você fornece a fonte e uma citação do texto na íntegra.
        Sua fonte de verdade são os documentos abaixo.
        Sempre cite trecho com momeço meio e fim, mesmo que tentaha que voltar uma pouco no texto ou avançar apra terminar uma frase.
        
        {flat_docs}
        
        Com base nos documento responda:  {prompt}
    """
    
    return prompt
