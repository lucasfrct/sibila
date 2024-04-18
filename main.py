import sys

from src import process
from src.display import chart
from src.database import chromadb
from src.entities.agent import Agent
from src.database import sqlite

sys.dont_write_bytecode = True

def loadDocuments(): 
    PATH_DOCS = "./docs"
    
    print("\n", "########## Iniciando registro de documentos ##########", "\n")
    documents = process.get_documents(PATH_DOCS)
    documents_size = len(documents)
    for i, document in enumerate(documents): 
        print(f"    {i+1}/{documents_size}: {document.info}")

    print("\n", "########## Iniciando embedings de documentos ##########", "\n")
    models = process.embed_documents(documents)
    for i, model in enumerate(models): 
        # chromadb.save_model(model)
        chart(f"{model.doc.name}", model)
        print(f"    {i+1}: {model.doc.info}")


def run():

    # loadDocuments()
    # agent = Agent()
    
    # for line in sys.stdin:
    #     agent.question(line)

    doc = ("doc_name", "doc/doc.pdf", "pdf")
    sqlite.add_document(doc)
    docs = sqlite.get_documents()
    for task in docs:
        print(task)



if __name__ == "__main__":
    sqlite.table_documents()
    run()