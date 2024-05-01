import sys

from src.routines import migrate
from src.agent.agent import Agent
from src.document import service as DocService

sys.dont_write_bytecode = True


def run():

    DocService.process_bath("./library")
    agent = Agent()
    agent.welcome()
    for line in sys.stdin:
        agent.consult(line)


if __name__ == "__main__":
    migrate.tables()
    run()