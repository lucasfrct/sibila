import sys
import textwrap

from src.routines import migrate
# from src.entities.agent import Agent
from src.document import service as DocService
from src.document import repository as DocRepository
from src.document import retrieval as DocRetrieval
from src.entities.ollama_model import OllamaModel 

sys.dont_write_bytecode = True


def run():

    model = OllamaModel()

    for doc in DocService.read():
        if not DocRepository.has_path(doc.path):
            doc.set_embeddings(model.make(doc.get_chunks))
            DocRetrieval.save(doc)
            DocRepository.save(doc)

        print(doc.info)

    
    result = DocRetrieval.query(model.embed("como ter acesso rápido a informação"))
    
    print()

    for doc in result:

        print("id: ", doc['id'], " - distance: ", doc['distance'])
        # print("meta: ", mt)
        # print("uris: ", uris)
        # print("data: ", data)
        print("document: ", doc['document'])
        print()



    
    # agent = Agent()
    
    # for line in sys.stdin:
    #     agent.question(line)



if __name__ == "__main__":
    migrate.tables()
    run()