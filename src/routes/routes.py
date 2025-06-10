# flake8: noqa: E501

from flask import Blueprint


from src.routes.catalog.catalog import catalog_indexer, catalog_list, catalog_search
from src.routes.completions.completions import completions, completions_history
from src.routes.corpus.corpus import corpus_generate
from src.routes.document.document import document_pages_details
from src.routes.health import health


app = Blueprint('app', __name__)


@app.route('/api/v1/health', methods=['GET'])
async def api_v1_health():
    return await health()


@app.route('/api/v1/completions', methods=['POST'])
async def api_v1_completions():
    return await completions()


@app.route('/api/v1/completions/history', methods=['GET'])
async def api_v1_completions_history():
    return await completions_history()


@app.route('/api/v1/catalog/search', methods=['GET'])
async def api_v1_catalog_search():
    return await catalog_search()


@app.route('/api/v1/catalog', methods=['GET'])
async def pai_v1_catalog():
    return await catalog_list()


@app.route('/api/v1/catalog/indexer', methods=['POST'])
async def api_v1_catalog_indexer():
    return await catalog_indexer()


@app.route('/api/v1/corpus/generate', methods=['POST'])
async def api_v1_corpus_generate():
    return await corpus_generate()


@app.route('/api/v1/document/pages', methods=['GET'])
async def api_v1_document_pages_details():
    return await document_pages_details()
