import sys
import textwrap

from src.routines import migrate
from src.document import service as DocService
from src.document import retrieval as DocRetrieval
from src.document import repository as DocRepository

sys.dont_write_bytecode = True

def run():

  DocService.process_bath("./docs")


if __name__ == "__main__":
    migrate.tables()
    run()