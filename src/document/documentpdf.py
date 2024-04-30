
from typing import List, Optional
import traceback
import logging
import uuid
import re
import os

import pdfplumber

from src.utils import string as String

class DocumentInfo:
    def __init__(self, path: str = "", name: str = "", size: int = 0, pages: int = 1, mimetype: str = "pdf"):
        self.id = 0
        self.path = path
        self.name = name
        self.size = size
        self.pages = pages
        self.mimetype = mimetype

    def dict(self):
        return { 'id': self.id, 'path': self.path, 'name': self.name, 'size': self.size, 'pages': self.pages, 'mimetype': self.mimetype }
    
    def to_tuple(self):
        return (self.path, self.name, self.size, self.pages, self.mimetype) 
    
    def from_tuple(self, doc_tuple):
        _id, path, name, size, pages, mimetype = doc_tuple
        self.id = _id
        self.path = path
        self.name = name
        self.size = size
        self.pages = pages
        self.mimetype = mimetype
        return self
    
    def extract(self, path):
        try:
            if not os.path.exists(path):
                raise ValueError("O path está inválido.")
            
            # Obter metadados do PDF
            self.path = os.path.normpath(path)    
            self.name = os.path.basename(path)
            self.size = int(os.path.getsize(path))

            pdf = reader(path)
            if pdf == None:
                return None
            
            self.pages = int(len(pdf.pages))
            return self.dict()
        except Exception as e:
            logging.error(f"{e}\n%s", traceback.format_exc())
            return None
    
class DocumentMetadata:
    def __init__(self):
        
        self.uuid = ""          # identificador do arquivo
        self.path = ""          # caminho do arquivo
        self.page = 0           # numero da página no arquivo
        self.name = ""          # nome do arquivo
        self.source = ""        # fonte da informaçao
        self.letters = 0        # total de letras
        self.content = ""       # conteúdo íntegro
        self.distance = 0.0     # distancia do vetor    #! (não guardar na base de dados)
        
        self.line = []          # lista de linas        #! (não guardar na base de dados)
        self.size = 0           # tamanho do arquivo em bytes
        self.lines = 0          # total de linas
        self.pages = 0          # total de páginas
        self.chunk = []         # lista de chunks       #! (não guardar na base de dados)
        self.chunks = 0         # total de chuncks
        self.mimetype = ""      # extenção do arquivo
        self.paragraph = []     # lista de paragrafos   #! (não guardar na base de dados)
        self.paragraphs = 0     # total de paragrafos

    def dict(self):
        return { 
            'uuid': self.uuid, 
            'path': self.path, 
            'page': self.page, 
            'name': self.name, 
            'source': self.source, 
            'letters': self.letters, 
            'content': self.content, 
            'distance': self.distance, 
            
            'line': self.line, 
            'size': self.size, 
            'lines': self.lines, 
            'pages': self.pages, 
            'chunk': self.chunk, 
            'chunks': self.chunks, 
            'mimetype': self.mimetype,
            'paragraph': self.paragraph,
            'paragraphs': self.paragraphs,
        }
       
    # transforma num dicionario para salvar na base de dados SQL 
    def to_dict_model(self):
        return { 
            'uuid': self.uuid, 
            'path': self.path, 
            'page': str(self.page), 
            'name': self.name, 
            'source': self.source, 
            'letters': str(self.letters), 
            'content': self.content, 
             
            'size': str(self.size), 
            'lines': str(self.lines), 
            'pages': str(self.pages), 
            'chunks': str(self.chunks), 
            'mimetype': self.mimetype,
            'paragraphs': str(self.paragraphs),
        }
    
    ## transforma um dicionario da base de dados SQL na classe 
    def from_dict_model(self, model):
        self.uuid = model['uuid']
        self.path = model['path']
        self.page = int(model['page'])
        self.name = model['name']
        self.source = model['source']
        self.letters = int(model['letters'])
        self.content = model['content']
        self.distance = 0.0
        
        self.line = self.split_to_line(self.content)
        self.size = int(model['size'])
        self.lines = len(self.line)
        self.pages = int(model['pages'])
        self.chunk = String.split_to_chunks(self.content)
        self.chunks = int(model['chunks'])
        self.mimetype = model['mimetype']
        self.paragraph = self.split_to_pargraph(self.content)
        self.paragraphs = int(model['paragraphs'])
        
    # transforma aclassse num tupla
    def to_tuple(self):
        return (
            self.uuid, 
            self.path, 
            self.page, 
            self.name, 
            self.source, 
            self.letters, 
            self.content, 
            self.distance, 
            
            self.line, 
            self.size, 
            self.lines, 
            self.pages, 
            self.chunk, 
            self.chunks, 
            self.mimetype,
            self.paragraph,
            self.paragraphs
        ) 
    
    # transforma uma tupla na classe
    def from_tuple(self, meta_tuple):
        uuid, path, page, name, source, letters, content, distance, line, size, lines, pages, chunk, chunks, mimetype, paragraph, paragraphs = meta_tuple
        
        self.uuid = uuid
        self.path = path
        self.page = page
        self.name = name
        self.source= source
        self.letters = letters
        self.content = content
        self.distance = distance
        
        self.line = line
        self.size = size
        self.lines = lines
        self.pages = pages
        self.chunk = chunk
        self.chunks = chunks
        self.mimetype = mimetype
        self.paragraph = paragraph
        self.paragraphs = paragraphs
        
        return self

    # transforma a classe numa tupla par a base de dados SQL
    def to_model(self):
        return (self.uuid, self.path, self.page, self.name, self.source, self.letters, self.content, self.size, self.lines, self.pages, self.chunks, self.mimetype, self.paragraphs)

    # transforma a tupla da base de dados SQL na classe
    def from_model(self, model_tuple):
        uuid, path, page, name, source, letters, content, size, lines, pages, chunks, mimetype, paragraphs = model_tuple

        self.uuid = uuid
        self.path = path
        self.page = page
        self.name = name
        self.source= source
        self.letters = letters
        self.content = content
        self.distance = 0.0
        
        self.line = self.split_to_line(self.content)
        self.size = size
        self.lines = lines
        self.pages = pages
        self.chunk = String.split_to_chunks(self.content)
        self.chunks = chunks
        self.mimetype = mimetype
        self.paragraph = self.split_to_pargraph(self.content)
        self.paragraphs = paragraphs
        
        return self
    
    def split_to_line(self, content):
        return content.split('\n')
    
    def split_to_pargraph(self, content):
        return content.split('\n\n')
    
## faz leitura de uma documento PDF   
def reader(path: str = ""):
    try:
        if not os.path.exists(path):
            raise ValueError("O path está inválido.")
        
        return pdfplumber.open(path)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None

## extra informaçoes de um PDF 
def info(path: str) -> Optional[DocumentInfo]:
    try:
        doc = DocumentInfo()
        doc.extract(path)
        return doc 
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None
    
## faz leitura de um trecho do PDF retornado as páginas em texto puro  
def read(path: str = "", init: int = 1, final: int = 0)-> List[str]:
    try:
        if not os.path.exists(path):
            raise ValueError("O path está inválido.")
    
        pdf = reader(path)
        if pdf == None:
            raise ValueError("Não foi possível ler o arquivo pdf.")
    
        total = len(pdf.pages)
        
        if init >= total:
            init = total - 1
            
        if init <= 0:
            init = 1
        
        if final > total:
            final = total
            
        if final <= 0:
            final = total
            
        if(final < init):
            final = init
       
        # Carrega apenas as páginas especificadas na memória
        pages = []
        for num in range(init - 1, final):
            page = pdf.pages[num].extract_text()
            pages.append(page)
        
        return pages
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []
   
##  faz a lietura das páginas em pdf extraindo os metadados
def read_pages_with_details(path: str = "", init: int = 1, final: int = 0)-> List[DocumentMetadata]:
    try:
        if not os.path.exists(path):
            raise ValueError("O path está inválido.")
        
        inf = info(path)
        if inf == None:
            return []
    
        pdf = reader(path)
        if pdf == None:
            raise ValueError("Não foi possível ler o arquivo pdf.")
    
        total = inf.pages
        
        if init >= total:
            init = total - 1
            
        if init <= 0:
            init = 1
        
        if final > total:
            final = total
            
        if final <= 0:
            final = total
            
        if(final < init):
            final = init
       
        # Carrega apenas as páginas especificadas na memória
        pages = []
        for num in range(init - 1, final):
            
            page_raw = pdf.pages[num]
            content = page_raw.extract_text()
            chunk_list = String.split_to_chunks(content)
            
            page = DocumentMetadata()
            
            page.uuid = str(uuid.uuid4())
            page.path = path
            page.page = int(num + 1)
            page.name = inf.name
            page.source = f"{page.name}, pg. {page.page}"
            page.letters = len(content)
            page.content = content
            
            page.line = page.split_to_line(content)
            page.size = inf.size
            page.lines = len(page.line)
            page.pages - inf.pages
            page.chunk = chunk_list
            page.chunks = len(page.chunk)
            page.mimetype = "pdf"
            page.paragraph = page.split_to_pargraph(content)
            page.paragraphs = len(page.paragraph)
                    
            pages.append(page)
        
        pdf.close()
        return pages
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []

def paragraphs_with_details(path: str = "", init: int = 1, final: int = 0)-> List[object]:
    try:
        
        pages = read_pages_with_details(path, init, final)

        paragraphs = []
        for page in pages:
            for i, content in enumerate(page['paragraph']):
                
                lines_clean = []
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    line = re.sub(r' {2,}', ' ', line)
                    line = re.sub(r'\n{1,}', ' ', line)
                    line = line.strip(' \n')
                    lines_clean.append(line)
                
                chunks = String.split_to_chunks(content)
                paragraph = {
                    'path': page['path'],
                    'page': page['page'],
                    'content': content,
                    'name': page['name'],
                    'letters': len(content),
                    'uuid': str(uuid.uuid4()),
                    'source': f"{page['name']}, pg. {page['page']}, pr. {i+1}",
                    
                    'num': i + 1,
                    'chunk': chunks,
                    'line': lines_clean,
                    'size': page['size'],
                    'chunks': len(chunks),
                    'pages': page['pages'],
                    'lines':  len(lines_clean),
                    'mimetype': 'pdf',
                }
                
                paragraphs.append(paragraph)
                
        return paragraphs
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []

def lines_with_details(path: str = "", init: int = 1, final: int = 0)-> List[object]:
    try:
        
        paragraphs = paragraphs_with_details(path, init, final)

        lines = []
        for paragraph in paragraphs:
            lns = paragraph['line']
            for i, content in enumerate(lns):
                
                chunks = String.split_to_chunks(content)

                line = {
                    'path': paragraph['path'],
                    'page': paragraph['page'],
                    'content': content,
                    'name': paragraph['name'],
                    'letters': len(content),
                    'uuid': str(uuid.uuid4()), 
                    'source': f"{paragraph['name']}, pg. {paragraph['page']}, ln {i+1}",
                    
                    'num': i+1,
                    'chunk': chunks,
                    'lines': len(lns),
                    'chunks': len(chunks),
                    'size': paragraph['size'],
                    'pages': paragraph['pages'],
                    'mimetype': 'pdf',
                }
                
                lines.append(line)
                
        return lines
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []

def transform_to_chuncks_and_metadatas(datails):
    for detail in datails:
        print(detail)