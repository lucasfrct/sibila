# flake8: noqa: E501

from flask import Blueprint


from src.routes.corpus.corpus import corpus_generate, corpus_list
from src.routes.dataset.dataset import dataset_dir_list
from src.routes.health import health


app = Blueprint('app', __name__)


@app.route('/api/v1/health', methods=['GET'])
async def api_v1_health():
    return await health()


@app.route('/api/v1/dataset', methods=['GET'])
async def api_v1_dataset():
    return dataset_dir_list()


@app.route('/api/v1/corpus', methods=['GET'])
async def api_v1_corpus_list():
    return corpus_list()


@app.route('/api/v1/corpus/generate', methods=['POST'])
async def api_v1_corpus_generate():
    return  await corpus_generate()

# @app.route('/api/v1/catalog/search', methods=['GET'])
# async def api_v1_catalog_search():
#     return await catalog_search()

# @app.route('/api/v1/catalog/indexer', methods=['POST'])
# async def api_v1_catalog_indexer():
#     return await catalog_indexer()


# @app.route('/api/v1/catalog', methods=['GET'])
# async def api_v1_catalog():
#     return catalog_list()


# @app.route('/api/v1/completions', methods=['POST'])
# async def api_v1_completions():
#     return await completions()


# @app.route('/api/v1/completions/history', methods=['GET'])
# async def api_v1_completions_history():
#     return await completions_history()



