from flask import Flask, request, jsonify

from src.models.ollama import ModelOllama
from src.modules.librarian import catalog as Catolog
from collections import deque

last_five_responses = deque(maxlen=5)

app = Flask(__name__)


@app.route('/api/v1/completions', methods=['POST'])
def completions():
    if not request.is_json:
        return jsonify({"erro": "Dados devem estar no formato JSON"}), 400

    dados = request.get_json()
    question = dados.get('question')
    prompt = dados.get('prompt')

    if not question:
        return jsonify({"erro": "Campo 'message' é obrigatório"}), 400
    
    docs = Catolog.search(question, 5, 0.3)

    llm = ModelOllama()
    response = llm.question(
        prompt=Catolog.prompt_search_in_docs(prompt, docs),
        question=question
    )
    
    # Armazena a resposta no deque
    last_five_responses.append(response)

    # Resposta de sucesso
    return jsonify({"response": f"{response}"}), 200


@app.route('/api/v1/completions/history', methods=['GET'])
def completions_history():
    # Converte o deque para uma lista para serialização JSON
    history = list(last_five_responses)
    return jsonify({"last_five_responses": history}), 200


@app.route('/api/v1/catalog', methods=['GET'])
def catalog():
    catalog_list = Catolog.list()
    return jsonify({"data": catalog_list}), 200


@app.route('/api/v1/catalog', methods=['POST'])
def catalog_register():
    regitreds = Catolog.register('dataset/library')
    return jsonify({"data": regitreds}), 200


@app.route('/api/v1/catalog/search', methods=['GET'])
def catalog_search():
    search_query = request.args.get('query', default='', type=str).strip()
    catalog_list = Catolog.search(search_query, 5, 0.3)
    return jsonify({"data": catalog_list}), 200
