# flake8: noqa: E501

import os
import re
import string
import hashlib
import unicodedata
from typing import List

try:
    from nltk.tokenize import word_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    def word_tokenize(text):
        # Simple fallback tokenization
        return text.split()

from src.utils.stop_words import stopwords_pt


def split_to_lines(content: str = "") -> List[str]:
    """
    Divide o conteúdo fornecido em uma lista de linhas, removendo espaços em branco no início e no final de cada linha e garantindo a codificação em UTF-8.

    **Parâmetros:**
    - `content` (*str*, opcional): O conteúdo de texto a ser dividido em linhas. Padrão é uma string vazia "".

    **Retorna:**
    - `List[str]`: Uma lista de strings, cada uma representando uma linha do conteúdo original, sem espaços em branco extras e codificada em UTF-8.
    """

    # Regex para identificar quebras de linha
    line_breaks = r'(?:\r\n|[\n\r\x0b\x0c\u0085\u2028\u2029])'

    lines = re.split(line_breaks, content.strip())
    return [line.strip().encode('utf-8').decode('utf-8') for line in lines]


def split_to_phrases(content: str = "") -> List[str]:
    """
    Transforma o conteúdo em uma lista de frases.

    **Parâmetros:**
    - `content` (*str*, opcional): O texto a ser dividido em frases. O padrão é uma string vazia "".

    **Retorna:**
    - `List[str]`: Uma lista de frases extraídas do conteúdo original, sem espaços em branco extras e codificadas em UTF-8.
    """

    # Regex para identificar pontos finais seguidos de um espaço ou fim da string
    phrases = re.split(r'(?<=[.!?])\s+', content.strip())

    return [phrase.strip().encode('utf-8').decode('utf-8') for phrase in phrases]


def split_to_pargraphs(content: str = "") -> List[str]:
    """
    Separa um texto em parágrafos, considerando várias formas de separação de linha.

    Este método processa o conteúdo fornecido e divide-o em uma lista de parágrafos. 
    Ele considera diferentes tipos de quebras de linha e separações de parágrafo, garantindo 
    que todas as formas comuns de separação sejam tratadas. Além disso, remove quebras de linha 
    internas dentro de um parágrafo, substituindo-as por um espaço para manter a fluidez do texto.

    Parâmetros:
        content (str): O texto a ser separado em parágrafos.

    Retorna:
        List[str]: Uma lista de parágrafos processados, sem quebras de linha internas.
    """

    # Define um padrão que encontra o fim da linha
    line_breaks = r'(?:\r\n|\n|\r|\x0b|\x0c|\u0085|\u2028|\u2029)'

    # Define um padrão que captura duas ou mais quebras de linha (incluindo diferentes tipos)
    paragraph_breaks = r'(?:\r\n|\n|\r|\x0b|\x0c|\u0085|\u2028|\u2029){2,}'
    paragraphs_split = re.split(paragraph_breaks, content.strip())
    paragraphs = []

    for paragraph in paragraphs_split:
        # Remove todas as quebras de linha internas substituindo-as por um espaço
        paragraph_unique = re.sub(line_breaks, ' ', paragraph).strip()

        # Adiciona o parágrafo à lista
        paragraphs.append(paragraph_unique.encode('utf-8').decode('utf-8'))

    return paragraphs


def split_to_chunks(content: str = "", size: int = 1000, overlap: int = 0) -> List[str]:
    """
    Divide o conteúdo de um texto em pedaços (chunks) baseado em texto, com um tamanho máximo especificado e sobreposição opcional.

    Args:
        content (str): O conteúdo a ser dividido em pedaços, representado como uma string. Por padrão, está vazio.
        size (int): O tamanho máximo de cada chunk (pedaço de texto) em caracteres. O valor padrão é 1000.
        overlap (int): A quantidade de caracteres que cada chunk deve sobrepor o próximo. O valor padrão é 200.

    Returns:
        List[str]: Uma lista contendo os chunks (pedaços de texto) gerados.

    Descrição:
        A função primeiro divide o conteúdo em chunks de acordo com o tamanho especificado; 
        Cada chunk pode ter uma sobreposição com o próximo, definida pelo parâmetro `overlap`.
    """

    paragraphs = split_to_pargraphs(content)
    chunks = []

    for paragraph in paragraphs:
        # transforma um parágrafo em chunks (pedaços de texto)
        cks = split_to_chunks_raw(paragraph.encode(
            'utf-8').decode('utf-8'), size, overlap)
        chunks.extend(cks)

    return chunks


def split_to_chunks_raw(content: str = "", size: int = 1000, overlap: int = 0) -> List[str]:
    """"
    Divide um texto em pedaços de tamanho fixo, com sobreposição opcional entre os pedaços.

    Args:
        content (str): O texto a ser dividido em chunks. Por padrão, está vazio.
        size (int): O número máximo de caracteres por chunk (pedaço de texto). O valor padrão é 1000.
        overlap (int): A quantidade de caracteres de sobreposição entre os chunks. O valor padrão é 200.

    Returns:
        List[str]: Uma lista contendo os chunks (pedaços de texto) gerados.

    Descrição:
        A função utiliza uma expressão regular para dividir o conteúdo em pedaços de tamanho máximo `size`. A expressão regular 
        é configurada para capturar blocos de texto de até `size` caracteres, sem considerar a sobreposição.
        O conteúdo é primeiro codificado e decodificado como 'utf-8' para garantir que caracteres especiais sejam corretamente processados.
    """

    # valor limit de onde overlap começa a valer
    cut_overlap = 10

    if size <= overlap:
        overlap = int(size * 0.4)

    if overlap <= cut_overlap:
        overlap = 0

    chunks = []
    start = 0
    content_length = len(content)

    while start < content_length:

        # Define o fim do chunk com base no size e no overlap
        end = min(start + size, content_length)

        # Busca o último ponto final antes de tamnaho (size) do chunk
        last_period = content.rfind('.', start, end)

        # Se houver um ponto final, ajusta o final do chunk para ele
        if last_period != -1:
            end = last_period + 1

        # Remove espaços em branco no início e no fim
        chunk = content[start:end].strip()
        chunks.append(chunk)

        # Avança o início para o próximo chunk, levando em conta o overlap
        new_start = end - overlap

        # Se não houver parágrafo, usa o início calculado normalmente
        start = new_start

        if overlap <= cut_overlap:
            # Busca o primeiro início de parágrafo (\n\n) antes de 200 caracteres no overlap
            first_paragraph_start = content.rfind(
                '\n\n', max(0, new_start - overlap), new_start)

            # Se houver um início de parágrafo, ajusta o novo início para ele
            if first_paragraph_start != -1:
                # Pula os dois caracteres de nova linha
                start = first_paragraph_start + 2

    return chunks


def clean_lines(line: str = "") -> str:
    """
    Remove espaços e quebras de linha extras de uma string.
    Esta função limpa uma linha de texto removendo múltiplos espaços consecutivos e quebras de linha (`\n`), 
    substituindo-os por um único espaço. 
    Também remove pontuações no início e no fim da linha resultante.

    Parâmetros:
        line (str): A linha de texto a ser limpa.

    Retorna:
        str: A linha de texto limpa, sem espaços ou quebras de linha extras e sem pontuações nas extremidades.
    """

    # Normaliza caracteres unicode para decompor caracteres compostos
    line = unicodedata.normalize('NFKC', line)

    # Remove caracteres de controle e não imprimíveis
    line = ''.join(ch for ch in line if unicodedata.category(ch)[0] != 'C')

    # Substitui todos os tipos de espaços em branco por um único espaço
    line = re.sub(r'\s+', ' ', line).strip()

    # Remove espaços antes de pontuação
    line = re.sub(
        r'\s+([{}])'.format(re.escape(string.punctuation)), r'\1', line)

    # Remove pontuações duplicadas
    line = re.sub(
        r'([{}])\1+'.format(re.escape(string.punctuation)), r'\1', line)

    line = re.sub(r' +|\n+', ' ', line.encode('utf-8').decode('utf-8')).strip()

    # Remove pontuações no início e fim da linha
    line = line.strip(string.punctuation)

    return line


def clean(text: str = "") -> str:
    """
    Limpa o texto para processamento, removendo sinais de pontuação, caracteres não alfanuméricos e espaços extras.

    Esta função remove todos os caracteres que não sejam letras, números ou espaços em branco do texto fornecido.
    Além disso, substitui múltiplos espaços por um único espaço e remove espaços no início e no fim da string.

    Parâmetros:
        text (str): O texto a ser limpo.

    Retorna:
        str: O texto limpo e normalizado, pronto para processamento.
    """

    # Normaliza caracteres unicode para decompor caracteres compostos
    text = unicodedata.normalize('NFKD', text)

    # Remover sinais de pontuação e caracteres não alfanuméricos. Isso remove tudo exceto letras, números e espaços
    text = re.sub(r'[^\w\s]', '', text)

    # Remover espaços extras
    clean_text = re.sub(r'\s+', ' ', text).strip()

    return clean_lines(clean_text)


def tokenize(text: str = "") -> List[str]:
    """
    Transforma o texto em uma lista de tokens (palavras), utilizando a tokenização de palavras do NLTK para o português.
    Esta função recebe uma string de texto e a divide em tokens individuais usando a função `word_tokenize` da biblioteca NLTK, configurada para o idioma português. Em seguida, filtra os tokens para incluir apenas aqueles compostos por caracteres alfabéticos, excluindo números, pontuação e outros símbolos.

    Parâmetros:
        text (str): O texto a ser tokenizado.

    Retorna:
        List[str]: Uma lista de tokens (palavras) extraídos do texto.
    """
    tokens = word_tokenize(text, language='portuguese')
    return [str(token) for token in tokens if token.isalpha()]


def normalize(text: str = "") -> List[str]:
    """ normaliza o texto corriginjo palavra com grafia errada """

    # words_white = ["vc", "pv", 'fds', 'blz', 'tmj', 'pdc', 's2', 'sdds', 'sqn', 'mlr', 'tldg', 'tb', 'bj', 'obg', 'pfv', 'msg', 'add']
    # words_black = ["none", "None"]
    # words = [str(word).lower() for word in tokenize(text) if word is not None]
    # normalized_text = []
    # spell = SpellChecker(language='pt')

    # for word in words:
    #     correct_word = spell.correction(word)
    #     if word in words_white or correct_word in words_white:
    #         correct_word = word
    #     if word in words_black or correct_word in words_black:
    #         continue
    #     if word is None:
    #         continue
    #     if correct_word is None:
    #         correct_word = word
    #     normalized_text.append(str(correct_word))

    # return normalized_text
    return []


def lemmatization(text: str = "") -> List[str]:
    # nlp = spacy.load('pt_core_news_sm')
    # doc = nlp(str([str(word) for word in tokenize(text)]))
    # return [token.lemma_ for token in doc if token.pos_ == 'NOUN']
    return []


def removal_stopwords(text: str = "") -> str:
    """ 
    Remove as stopwords de um texto fornecido.

    Esta função processa uma string de texto realizando os seguintes passos:
    1. **Tokenização**: Divide o texto em uma lista de tokens (palavras) usando a função `tokenize`.
    2. **Limpeza dos Tokens**: Aplica a função `clean_lines` em cada token para remover pontuação e caracteres indesejados.
    3. **Remoção de Stopwords**: Filtra os tokens removendo aqueles que estão presentes na lista `stopwords_pt`, contendo as stopwords em português.
    4. **Reconstrução do Texto**: Junta os tokens restantes em uma única string, separada por espaços.

    Parâmetros:
        text (str): O texto a ser processado e do qual as stopwords serão removidas.

    Retorna:
        str: O texto resultante após a remoção das stopwords, como uma única string.
    """

    # Tokenização
    tokens = tokenize(text)

    # Remover pontuação
    tokens = [clean_lines(word) for word in tokens]

    # Remover stopwords
    tokens = [word for word in tokens if word.lower() not in stopwords_pt]

    return ' '.join(tokens)


def unique(contents: List[str] = []) -> List[str]:
    """ remove documentos com conteúdo repetido """
    content_unique = set()
    results: List[str] = []
    for content in contents:
        if content not in content_unique:
            results.append(content)
            content_unique.add(content)
    return results


def hash(text: str = "") -> str:
    text_bytes = text.encode('utf-8')
    hash_obj = hashlib.sha3_256()
    hash_obj.update(text_bytes)
    return hash_obj.hexdigest()


def size_to_label(size: int):
    """
        Converte um tamanho em bytes para uma string legível com a unidade apropriada (B, KB, MB, GB).

        Parâmetros:
        size (int): O tamanho em bytes.

        Retorna:
        str: Uma string representando o tamanho com a unidade apropriada.
    """
    if size < 1024:
        return f'{size} B'
    if size < 1024 * 1024:
        return f'{size / 1024:.2f} KB'
    if size < 1024 * 1024 * 1024:
        return f'{size / 1024 / 1024:.2f} MB'
    return f'{size / 1024 / 1024 / 1024:.2f} GB'


def path_name(path: str)-> str:
    """
    Retorna o nome do arquivo sem a extensão a partir de um caminho fornecido.

    Args:
        path (str): O caminho completo do arquivo.

    Returns:
        str: O nome do arquivo sem a extensão.
        """
    return os.path.splitext(os.path.basename(path))[0]