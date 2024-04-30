
from typing import List
import traceback
import logging
import uuid
import re
import os

import PyPDF2

from src.utils import archive as Archive


def reader(path: str = ""):
    try:
        file = Archive.reader(path)
        if file == None:
            return None
        
        return PyPDF2.PdfReader(file)
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None

def info(path: str):
    try:
        if not os.path.exists(path):
            raise ValueError("O path está inválido.")
        
        # Obter metadados do PDF
        path = os.path.normpath(path)    
        name = os.path.basename(path)
        size = os.path.getsize(path)

        pdf = reader(path)
        if pdf == None:
            return None
        
        pages = len(pdf.pages)
        return { 'path': path, 'name': name, 'size': size, 'pages': pages, 'mimetype': "pdf" }
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return None
      
def read(path: str = "", init: int = 1, final: int = 0)-> []:
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
    
def read_with_details(path: str = "", init: int = 1, final: int = 0)-> []:
    try:
        if not os.path.exists(path):
            raise ValueError("O path está inválido.")
        
        inf = info(path)
        if inf == None:
            return []
    
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
            
            content = pdf.pages[num].extract_text()
            chunks = split_to_chunks(content)
        
            paragraph_raw = [] 
            paragraph_long = content.split("\n\n")
            for p in paragraph_long:
                paragraph_raw.extend(p.split('\n \n'))
            
            paragraph_clean = []
            for para in paragraph_raw:
                para = para.strip()
                
                if not para:
                    continue
                
                para = re.sub(r' {2,}', ' ', para)
                para = re.sub(r'\n{2,}', ' ', para)
                para = para.strip()
                
                if not para:
                    continue
                
                paragraph_clean.append(para)
            
            lines_clean = []
            for paragraph in paragraph_clean:
                paragraph = paragraph.strip()
                
                if not paragraph:
                    continue
                
                lines = paragraph.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    line = re.sub(r' {2,}', ' ', line)
                    line = re.sub(r'\n{1,}', ' ', line)
                    line = line.strip(' \n')
                    lines_clean.append(line)
                
                      
            metadata = {
                'path': path,
                'page': num + 1,
                'content': content,
                'name': inf['name'],
                'letters': len(content),
                'uuid': str(uuid.uuid4()),
                'source': f"{inf['name']}, pg. {num + 1}",

                'chunck': chunks,
                'line': lines_clean,
                'size': inf['size'],
                'chunks': len(chunks),
                'pages': inf['pages'],
                'lines':  len(lines_clean),
                'paragraph': paragraph_clean,
                'paragraphs': len(paragraph_clean),
                'mimetype': 'pdf',
            }
            
            pages.append(metadata)
        
        return pages
    except Exception as e:
        logging.error(f"{e}\n%s", traceback.format_exc())
        return []

def paragraphs_with_details(path: str = "", init: int = 1, final: int = 0)-> []:
    try:
        
        pages = read_with_details(path, init, final)

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
                
                chunks = split_to_chunks(content)
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

def lines_with_details(path: str = "", init: int = 1, final: int = 0)-> []:
    try:
        
        paragraphs = paragraphs_with_details(path, init, final)

        lines = []
        for paragraph in paragraphs:
            lns = paragraph['line']
            for i, content in enumerate(lns):
                
                chunks = split_to_chunks(content)

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
    
def split_to_chunks(content: str= "", size: int = 1000) -> List[str]:
   return [content[i:i+size].ljust(size) for i in range(0, len(content), size)]

def transform_to_chuncks_and_metadatas(datails):
    for detail in datails:
        print(detail)