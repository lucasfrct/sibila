import sys
import textwrap

from src.routines import migrate
# from src.entities.agent import Agent
from src.document import service as DocService
from src.document import repository as DocRepository
from src.document import retrieval as DocRetrieval
from src.process import embed_document

sys.dont_write_bytecode = True


def run():

    for doc in DocService.read():
        if not DocRepository.has_path(doc.path):
            # model = embed_document(doc)
            # doc.set_embeddings(model.embeddings)
            DocRetrieval.save(doc)
            DocRepository.save(doc)

        print(doc.info)

    
    result = DocRetrieval.consult("dados")

    print(result)
    print()
    
    # ids = result['ids'][0]
    # distances = result['distances'][0]
    # metadatas = result['metadatas'][0]
    # documents = result['documents'][0]
    # uris = result['uris']
    # data = result['data']
    # embeddings = result['embeddings']

    # for id, dis, mt, do in zip(ids, distances, metadatas, documents):

    #     print("id: ", id, " - distance: ", dis)
    #     print(do)
    #     print("meta: ", mt)
    #     print("uris: ", uris)
    #     print("data: ", data)
    #     print("embeddings: ", embeddings)
    #     print()



    
    # agent = Agent()
    
    # for line in sys.stdin:
    #     agent.question(line)



if __name__ == "__main__":
    migrate.tables()
    run()