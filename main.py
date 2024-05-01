import sys

from src.librarian import librarian as Librarian
from src.routines import migrate as Migrate

sys.dont_write_bytecode = True


# execuçao principal
def run():
    paths = Librarian.register("./bookcase")
    if len(paths) == 0:
        print("Nehum novo livro encontrado")
    else:
        print("Lista de livros adcionados: ", paths)

    Librarian.search("casa")


if __name__ == "__main__":
    Migrate.tables()
    run()
