import sys

sys.dont_write_bytecode = True

from src.librarian import librarian as Librarian
from src.routines import migrate as Migrate

def run():

  print("Iniciando leitura de arquivos")
  
  paths = Librarian.register("./bookcase")
  
  print(paths)

if __name__ == "__main__":
    Migrate.tables()
    run()