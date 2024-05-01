import sys
import json

from src.librarian import librarian as Librarian
from src.routines import migrate as Migrate
from src.agent.agent import Agent

sys.dont_write_bytecode = True


# execuçao principal
def run():
    # paths = Librarian.register("./bookcase")
    # if len(paths) == 0:
    #     print()
    #     print(" * Nehum novo livro encontrado")
    # else:
    #     print()
    #     print(" Lista de livros adcionados: ")
    #     for path in paths:
    #         print(" - ", path)

    agent = Agent()
    agent.welcome()
    print(agent.intentions("Quero reservar um voo para Paris"))
    for line in sys.stdin:
        # agent.question(line)
        print()
        print(json.dumps(agent.digest(line), indent=4, ensure_ascii=False))
        

if __name__ == "__main__":
    Migrate.tables()
    run()
