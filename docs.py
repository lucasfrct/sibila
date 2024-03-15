import os

from embedding import Embedding
from document import Doc


def run():

    print("\n", "########## Iniciando registro de documentos ##########", "\n")
    path = 'train/'

    documents_names = os.listdir(path)
    documents_names_size = len(documents_names)
    
    for i, document_name in enumerate(documents_names): 
        
        path_doc = os.path.join(path, document_name)
        doc = Doc(path_doc, document_name)

        print(f"{i+1}/{documents_names_size}: {document_name} | {doc.chunks} Chunks")
        
        embedding = Embedding()
        embedding.document(doc)
        embedding.metadata_generation()
        embedding.generate()
        embedding.save()
    
    print("\n")
        
if __name__ == "__main__":
    run()