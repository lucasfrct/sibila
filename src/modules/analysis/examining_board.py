# flake8: noqa: E501

"""
    EXAMINING BOARD: banca examinadoara
    Este arquivo tem o papel de ser a banca examinadora que elabora as perguntas e gera o questionário.
"""


import re
from typing import List

from src.models.ollama import ModelOllama
from src.modules.analysis import federal_constitution_retrieval as FederalContitutionRetrieval


# questões para serem aplicas a um artigo
common_questions = [
    "Existe ambiguidade na sequinte lei?",
    "Qual é o principal objetivo deste artigo?",
    "Quais as conseqûencias prátcias da seguinte lei?",
    "Quais direitos ou garantias são assegurados por este artigo?",
    "Qual o ponto de insconsistência mais crítico na seguinte lei?",
]

# questão apra se prguntar para a IA treinada
constextual_questions = [
    "Quais são os direitos garantidos pela Constituição de 1988 em relação à liberdade de expressão?",
    "Qual é a importância do princípio da função social da propriedade na Constituição de 1988?",
    "Quais mudanças significativas a Constituição de 1988 trouxe para o sistema de saúde no Brasil?",
]


def ask_a_question(docs: str, article: str, ask: str ) -> str:
    """
	Faz uma pergunta a partir de um conjunto de documentos e um artigo específico.

	Args:
		docs (str): Texto contendo os documentos a serem analisados.
		ask (str): Pergunta a ser feita com base nos documentos.
		article (str): Artigo específico que deve ser considerado na resposta.

	Returns:
		str: Resposta gerada pelo modelo, sem texto de saudação, despedida ou descrição.
   	"""
    
    llm = ModelOllama()
    llm.out_reduction_rate = 100.0
    llm.penalty_rate = 10.0
    llm.max_tokens = 100
    prompt = f"""
        /clear
        Usando somente os textos abaixo, responda:
        # Documentos:
        {docs}
    """
    question = f"""
		# Questão
        {ask} responda segundo a artigo: {article[0:512]}.
        Remova o texto de saudação ou despedida ou descrição.
    """
    response = llm.question(prompt=prompt, question=question).strip()
    return re.sub(r'[\n;.\'"]', '', response).strip()

def question_maker(article: str)-> str:
    """
    Gera uma pergunta para um artigo específico.
    Args:
        article (str): O artigo que será utilizado para gerar a pergunta.
    Returns:
        str: A pergunta gerada.
    """
    llm = ModelOllama()
    llm.out_reduction_rate = 100.0
    llm.penalty_rate = 10.0
    llm.max_tokens = 100
    prompt = f"""
        /clear
        Usando somente os textos abaixo, responda:
        # Documentos:
        {article}
    """
    question = f"""
        # Questão
        Faça uma pergunta objetiva de teor jurídico sobre o seguinte artigo: {article[0:1024]}.
        Remova o texto de saudação ou despedida ou descrição.
    """
    response = llm.question(prompt=prompt, question=question).strip()
    return re.sub(r'[\n;.\'"]', '', response).strip()


def questionnaire(article: str)-> List[dict]:
    """
    Gera respostas para um conjunto de perguntas comuns com base em um artigo fornecido.
    Args:
        article (str): O artigo que será utilizado para gerar as respostas.
    Returns:
        list: Uma lista contendo as perguntas e suas respectivas respostas.
    """
    
    common_questions.append(question_maker(article))
    
    resp = []
    for question in common_questions:
        
        docs = FederalContitutionRetrieval.query_in_dimencions(question)
        docs.extend(FederalContitutionRetrieval.query_in_dimencions(article))
        documents = "\n".join(docs)
        
        response = ask_a_question(documents, article, question)
        resp.append({ "prompt": question, "completion": response })
    return resp
