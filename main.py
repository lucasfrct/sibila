import sys

from src import process
from src.database import chromadb
from src.display import chart
from src.entities.agent import Agent

sys.dont_write_bytecode = True

def run():

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

    print()
    agent = Agent()
    
    for line in sys.stdin:
        agent.question(line)


if __name__ == "__main__":
    run()