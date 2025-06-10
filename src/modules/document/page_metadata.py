# flake8: noqa: E501

from dataclasses import dataclass, asdict, astuple
from typing import List

from src.utils import string as String

@dataclass
class PageMetadata:
    def __init__(self):

        self.uuid = ""          # identificador do arquivo
        self.path = ""          # caminho do arquivo
        self.page = 0           # numero da página no arquivo
        self.name = ""          # nome do arquivo
        self.source = ""        # fonte da informaçao
        self.letters = 0        # total de letras
        self.content = ""       # conteúdo íntegro

        # distancia do vetor    #! (não guardar na base de dados)
        self.distance = 0.0     # vetor de distnacia
        self.mimetype = ""      # extenção do arquivo
        self.pages = 0          # total de páginas
        self.size = 0           # tamanho do arquivo em bytes

        # lista de paragrafos   #! (não guardar na base de dados)
        # paragrafos são textos do início até que encontre um linha em branco
        self.paragraph = []     # lista de paragrafos
        self.paragraphs = 0     # total de paragrafos

        # lista de frases       #! (não guardar na base de dados)
        # frases são textos recortados do início até que encontre um ponto final
        self.phrase = []        # lista de frases
        self.phrases = 0        # total de frases

        # lista de linas        #! (não guardar na base de dados)
        self.line = []          # lista das linhas
        self.lines = 0          # total de linas

        # lista de chunks       #! (não guardar na base de dados)
        # chaunks são pedaços de texto quebrados dentro de um parágrafo para armazenamento em vetor
        self.chunk = []         # lista dos pedaços
        self.chunks = 0         # total de chuncks

    def dict(self):
        """Retorna o docuemto de metadado com um dicionário"""
        return asdict(self)

    def to_dict_model(self):
        """transforma num dicionario para salvar na base de dados SQL"""
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
            'phrases': str(self.phrases),
            'paragraphs': str(self.paragraphs),
        }

    def from_dict_model(self, model):
        """transforma um dicionario da base de dados SQL na classe"""
        self.uuid = model['uuid']
        self.path = model['path']
        self.page = int(model['page'])
        self.name = model['name']
        self.source = model['source']
        self.letters = int(model['letters'])
        self.content = model['content']
        self.distance = 0.0

        self.line = String.split_to_lines(self.content)
        self.size = int(model['size'])
        self.lines = len(self.line)
        self.pages = int(model['pages'])
        self.chunk = String.split_to_chunks(self.content, 2000)
        self.chunks = int(model['chunks'])
        self.mimetype = model['mimetype']
        self.phrase = String.split_to_phrases(self.content)
        self.phrases = int(model['phrases'])
        self.paragraph = String.split_to_pargraphs(self.content)
        self.paragraphs = int(model['paragraphs'])

    def to_tuple(self):
        """transforma aclassse numa tupla"""
        return astuple(self)

    def from_tuple(self, meta_tuple):
        """transforma uma tupla na classe"""
        uuid, path, page, name, source, letters, content, distance, line, size, lines, pages, chunk, chunks, mimetype, phrase, phrases, paragraph, paragraphs = meta_tuple

        self.uuid = uuid
        self.path = path
        self.page = page
        self.name = name
        self.source = source
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
        self.phrase = phrase
        self.phrases = phrases
        self.paragraph = paragraph
        self.paragraphs = paragraphs

        return self

    def to_model(self):
        """transforma a classe numa tupla para a base de dados SQL"""

        return (self.uuid, self.path, self.page, self.name, self.source, self.letters, self.content, self.size, self.lines, self.pages, self.chunks, self.mimetype, self.phrases, self.paragraphs)

    def from_model(self, model_tuple):
        """transforma a tupla da base de dados SQL na classe"""

        uuid, path, page, name, source, letters, content, size, lines, pages, chunks, mimetype, phrases, paragraphs = model_tuple

        self.uuid = uuid
        self.path = path
        self.page = page
        self.name = name
        self.source = source
        self.letters = letters
        self.content = content
        self.distance = 0.0

        self.line = String.split_to_lines(self.content)
        self.size = size
        self.lines = lines
        self.pages = pages
        self.chunk = String.split_to_chunks(self.content, 2000)
        self.chunks = chunks
        self.mimetype = mimetype
        self.phrase = String.split_to_phrases(self.content)
        self.phrases = phrases
        self.paragraph = String.split_to_pargraphs(self.content)
        self.paragraphs = paragraphs

        return self

    def generate_paragraphs(self) -> List[str]:
        """separa um texto em parágrafos"""
        self.paragraph = String.split_to_pargraphs(self.content)
        self.paragraphs = len(self.paragraph)
        return self.paragraph

    def generate_phrases(self) -> List[str]:
        """transforma o conteúdo em freses"""
        self.phrase = String.split_to_phrases(self.content)
        self.phrases = len(self.phrase)
        return self.phrases

    def generate_lines(self) -> List[str]:
        """quebra o conteúdo em linhas removendo linhas vazias"""
        lines_clean: List[str] = []
        lines = String.split_to_lines(self.content)
        for line in lines:
            line = line.strip()
            if not line:
                continue

            lines_clean.append(String.clean_lines(line))
        self.line = lines_clean
        self.lines = len(self.line)
        return self.line
    
    def generate_chunks(self)-> List[str]:
        """quebra o conteúdo em pedaços de 2000 caracteres"""
        self.chunk = String.split_to_chunks(self.content, 2000)
        self.chunks = len(self.chunk)
        return self.chunk

