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

    DocService.process_bath("./docs")
    
    agent = Agent()
    
    agent.welcome()
    for line in sys.stdin:
        agent.consultant(line)


if __name__ == "__main__":
    migrate.tables()
    run()