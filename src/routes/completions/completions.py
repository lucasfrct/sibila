# flake8: noqa: E501

from flask import request

from src.models.ollama import ModelOllama
from src.modules.response.response import Response
from src.modules.catalog import handles as Catolog


def completions():
    if not request.is_json:
        return Response.error(400, "COM000", "Campo 'question' é obrigatório").result()

    dados = request.get_json()
    question = dados.get('question') or ""
    prompt = dados.get('prompt') or ""

    if not question:
        return Response.error(400, "COM002", "Campo 'question' é obrigatório").result()

    docs = Catolog.search(question, 5, 0.3)

    llm = ModelOllama()
    response = llm.question(
        prompt=Catolog.prompt_search_in_docs(prompt, docs),
        question=question
    )

    # Resposta de sucesso
    return Response.success(200, f"{response}").result()


def completions_history():
    history = ModelOllama.history()
    return Response.success(200, {"history": history}).result()
