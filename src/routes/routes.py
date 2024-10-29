# flake8: noqa: E501

from flask import Blueprint


from src.routes.catalog.catalog import catalog_indexer, catalog_list, catalog_search
from src.routes.completions.completions import completions, completions_history
from src.routes.corpus.corpus import corpus_generate
from src.routes.health import health


app = Blueprint('app', __name__)


@app.route('/api/v1/health', methods=['GET'])
def api_v1_health():
    return health()


@app.route('/api/v1/completions', methods=['POST'])
def api_v1_completions():
    return completions()


@app.route('/api/v1/completions/history', methods=['GET'])
def api_v1_completions_history():
    return completions_history()


@app.route('/api/v1/catalog/search', methods=['GET'])
def api_v1_catalog_search():
    return catalog_search()


@app.route('/api/v1/catalog', methods=['GET'])
def pai_v1_catalog():
    return catalog_list()


@app.route('/api/v1/catalog/indexer', methods=['POST'])
def api_v1_catalog_indexer():
    return catalog_indexer()


@app.route('/api/v1/corpus/generate', methods=['POST'])
def api_v1_corpus_generate():
    return corpus_generate()
