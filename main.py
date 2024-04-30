import sys

sys.dont_write_bytecode = True

from src.librarian import librarian as Librarian

def run():

  print("Iniciando leitura de arquivos")
  
  paths = Librarian.paths("./bookcase")
  
  print(paths)

if __name__ == "__main__":
    run()