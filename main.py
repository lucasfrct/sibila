import sys

from src.librarian import librarian as Librarian
from src.routines import migrate as Migrate

sys.dont_write_bytecode = True


# execuçao principal
def run():
    print("Iniciando leitura de arquivos")
    paths = Librarian.register("./bookcase")
    print(paths)


if __name__ == "__main__":
    Migrate.tables()
    run()
