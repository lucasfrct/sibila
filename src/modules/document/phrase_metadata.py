# flake8: noqa: E501

from dataclasses import dataclass, asdict, astuple
from typing import List

from src.utils import string as String

@dataclass
class PharseMetadata:
    def __init__(
        self, 
        uuid: str = None, 
        path: str = None, 
        page: int = 0, 
        name: str = None, 
        source: str = None, 
        letters: int = 0, 
        content: str = None, 
        distance: float = 0.0, 
        mimetype: str = None,
        size: int = 0,
        line: List[str] = [],
        lines: int = 0,
    ):

        # informçao do paragrafo
        self.uuid: str = uuid               # identificador da frase
        self.path: str = path               # caminho do arquivo
        self.page: int = page               # numero da página no arquivo
        self.name: str = name               # nome do arquivo
        self.source: str = source           # fonte da informaçao
        self.letters: int = letters         # total de letras
        self.content: str = content         # conteúdo íntegro da frase

        # distancia do vetor    #! (não guardar na base de dados)
        self.distance: float = distance     # distancia vetorial
        self.mimetype: str = mimetype       # extenção do arquivo
        self.size: int = size               # tamanho do arquivo em bytes

        # lista de linas        #! (não guardar na base de dados)
        # linhas são pedaços de textos até que encontre um \n ou zr (slato de linha)
        self.line: List[str] = line         # lista das linhas
        self.lines: int = lines             # total de linas

        # lista de chunks       #! (não guardar na base de dados)
        # chaunks são pedaços de texto quebrados dentro de um parágrafo para armazenamento em vetor
        self.chunk: List[str] = []          # lita pedaços do paragrafo
        self.chunks: int = 0                # total de chuncks

    def dict(self):
        return asdict(self)

    def to_tuple(self):
        return astuple(self)
    
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

