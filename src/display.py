
import math
import numpy as np
from pyvis.network import Network
from sklearn.manifold import TSNE


def matrix_tsne(embeddings):

    # Converta sua lista de embeddings em uma matriz para o t-SNE
    embeddings_matrix = np.array(embeddings)

    # Reduza a dimensionalidade
    tsne = TSNE(n_components=2, perplexity=15, random_state=42, init='random', learning_rate=200.0)  # ou n_components=3 para 3D   # noqa: E501

    return tsne.fit_transform(embeddings_matrix.reshape(-1, 1))


def weight_matrix(mtx):
    weight = {}
    mtx_flat = [item for sublist in mtx for item in sublist]
    for emb in mtx_flat:
        if (emb in weight):
            weight[emb] += 1
        else:
            weight[emb] = 1

    return weight


def display(embeddings, chunks):

    embeddings_small = matrix_tsne(embeddings)
    chuncks_small = [word for chunk in chunks for word in chunk.split()]

    g = Network(
        height="850px",
        width="100%",
        bgcolor="#222222",
        font_color="white",
        notebook=True,
        cdn_resources="remote",
        directed=True
    )
    weight = weight_matrix(embeddings_small)

    connections = {}
    num_id = 0
    last_id = 0

    for embedding, chunk in zip(embeddings_small, chuncks_small):

        emb_l = embedding[0]
        emb_r = embedding[1]
        size = len(chunk)

        tensor = (math.sqrt(((emb_l ** 2) + (emb_r ** 2)))) / (emb_l + emb_r)
        key = int(tensor)

        val = size * tensor + 1

        if (emb_l in weight):
            val = val * weight[emb_l]

        if (emb_r in weight):
            val = val * weight[emb_r]

        if (size < 3):
            val = val * 0.1

        g.add_node(num_id, label=f"({key}) {chunk}", value=val, x=int(emb_l), y=int(emb_r))  # noqa: E501

        if (key in connections):
            g.add_edge(connections[key], num_id)
        else:
            connections[key] = num_id

        if (last_id != num_id and num_id > last_id):
            g.add_edge(last_id, num_id)

        last_id = num_id
        num_id = num_id + 1

    return g


def chart(name, model):
    graph = display(model.embeddings, model.chunks)
    graph.show(f"{name}.html")
