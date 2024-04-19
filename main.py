import sys
import textwrap

from src.routines import migrate
from src.entities.agent import Agent
from src.document import service as DocService
from src.entities.ollama_model import OllamaModel 
from src.document import retrieval as DocRetrieval
from src.document import repository as DocRepository

sys.dont_write_bytecode = True


def run():

    # model = OllamaModel()

    for doc in DocService.read():
        if not DocRepository.has_path(doc.path):
            # doc.set_embeddings(model.make(doc.get_chunks))
            # DocRetrieval.save(doc)
            DocRepository.save(doc)

        print(doc.info)

    # agent = Agent()
    
    # agent.welcome()
    # for line in sys.stdin:
    #     agent.question(line)


if __name__ == "__main__":
    migrate.tables()
    run()