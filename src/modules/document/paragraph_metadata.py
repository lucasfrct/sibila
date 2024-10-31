# flake8: noqa: E501

from typing import Dict, List, Mapping
from dataclasses import dataclass
import json
import uuid

from src.utils import string as String
from src.modules.nlp.bow import generate_bow

@dataclass
class ParagraphMetadata:
    def __init__(
        self, 
        uuid: str = "", 
        path: str = "", 
        page: int = 0, 
        name: str = "", 
        source: str = "", 
        letters: int = 0, 
        content: str = "", 
        distance: float = 0.0, 
        mimetype: str = "",
        size: int = 0,
        phrase: List[str] = [],
        phrases: int = 0,
    ):

        # informçao do paragrafo
        self.uuid: str = uuid               # identificador do paragrafo
        self.path: str = path               # caminho do arquivo
        self.page: int = page               # numero da página no arquivo
        self.name: str = name               # nome do arquivo
        self.source: str = source           # fonte da informaçao
        self.letters: int = letters         # total de letras
        self.content: str = content         # conteúdo íntegro do paragrafo

        # distancia do vetor                #! (não guardar na base de dados)
        self.distance: float = distance     # distancia vetorial
        self.mimetype: str = mimetype       # extenção do arquivo
        self.size: int = size               # tamanho do arquivo em bytes

        # lista de frases                   #! (não guardar na base de dados)
        # frases são textos recortados do início até que encontre um ponto final
        self.phrase: List[str] = phrase     # lista de frases
        self.phrases: int = phrases         # total de frases

        # lista de linas                    #! (não guardar na base de dados)
        # linhas são pedaços de textos até que encontre um \n ou zr (slato de linha)
        self.line: List[str] = []           # lista das linhas
        self.lines: int = 0                 # total de linas

        # lista de chunks                   #! (não guardar na base de dados)
        # chaunks são pedaços de texto quebrados dentro de um parágrafo para armazenamento em vetor
        self.chunk: List[str] = []          # lita pedaços do paragrafo
        self.chunks: int = 0                # total de chuncks

    def new_uuid(self):
        self.uuid = str(uuid.uuid4())
        return self.uuid
    
    def dict(self):
         return self.__dict__

    def tuple(self):
        return tuple(self.__dict__.values())
    
    def data_retrieval(self):
        return { "uuid": self.uuid, "path": self.path, "name": self.name, "source": self.source, "mimetype": self.mimetype, "content": self.content }
    
    def from_retrieval(self, data: Mapping[str, str]):
        self.uuid = data['uuid']
        self.name = data['name']
        self.path = data['path']
        self.source = data['source']

    def generate_phrases(self) -> List[str]:
        """transforma o conteúdo em freses"""
        self.phrase = String.split_to_phrases(self.content)
        self.phrases = len(self.phrase)
        return self.phrase
    
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
    
    def generate_bow(self):
        """ funçao para exrair bag of words"""
        return generate_bow(self.content)
        
    
    def generate_dataset(self):
        """Função para gerar pares de perguntas e respostas"""
      
        # extrair as palavras principais do BoW 
        words = self.generate_bow()
            
        main_words: List[str] = []
        for word in words.keys():
            if(words[word] >= 3):
                main_words.append(word)
        
        dataset: List[dict] = []
        
        # gerar dataset
        for phrase in self.phrase :
            question = f"Usuário: {str(uuid.uuid4())} O que diz  {phrase[:90]}?"
            answer = f"Assistente: {self.content.strip()} [Fonte: {self.source}]"
            dataset.append({"prompt": question, "response": answer})
        
        for phrase in self.phrase :
            question = f"Usuário: {str(uuid.uuid4())} segundo {phrase[:90]}?"
            answer = f"Assistente: {self.content.strip()} [Fonte: {self.source}]"
            dataset.append({"prompt": question, "response": answer})
            
        for line in self.line :
            question = f"Usuário: {str(uuid.uuid4())} Conforme  {line[:60]}"
            answer = f"Assistente: {self.content.strip()} [Fonte: {self.source}]"
            dataset.append({"prompt": question, "response": answer})
            
        for chunk in self.chunk :
            question = f"Usuário: {str(uuid.uuid4())} caso {chunk[:30]}?"
            answer = f"Assistente: {self.content.strip()} [Fonte: {self.source}]"
            dataset.append({"prompt": question, "response": answer})
            
        for word in main_words :
            question = f"Usuário: {str(uuid.uuid4())} sobre {word}"
            answer = f"Assistente: {self.content.strip()} [Fonte: {self.source}]"
            dataset.append({"prompt": question, "response": answer})
            
        question = f"Usuário: para as pallavras chaves {' '.join(main_words)}"
        answer = f"Assistente: {self.content.strip()} [Fonte: {self.source}]"
        dataset.append({"prompt": question, "response": answer})
            
        return dataset

    # Função para salvar o dataset em formato JSON
    def export_dataset(self):
        file_path = './dataset/train/paragraphs.json'
        dataset = self.generate_dataset()
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=4)
