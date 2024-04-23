import sys
import textwrap

from src.routines import migrate
from src.document import service as DocService
from src.document import retrieval as DocRetrieval
from src.document import repository as DocRepository

sys.dont_write_bytecode = True

def run():

  DocService.process_bath("./docs")
  
  question = "operacional"
  res_sql = DocRepository.query_metadata_include(question, 1)
  res_vec = DocRetrieval.query_text(question, 1)
    
  print()
  print(len(res_sql), res_sql) 
  print()
  print(len(res_vec), res_vec) 


if __name__ == "__main__":
    migrate.tables()
    run()