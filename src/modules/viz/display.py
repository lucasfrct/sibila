
import math
import numpy as np
from pyvis.network import Network
from sklearn.manifold import TSNE
from .optimized_display import (
    OptimizedGraphGenerator, create_smart_constellation, quick_viz,
    matrix_tsne_optimized, display_optimized, chart_optimized
)
from .sampling import optimize_sampling_for_size


def matrix_tsne(embeddings, use_optimized=True):
    """
    Enhanced t-SNE implementation with optimization options.
    
    Args:
        embeddings: List of embedding vectors
        use_optimized: Whether to use the optimized version (recommended)
    """
    if use_optimized:
        return matrix_tsne_optimized(embeddings)
    
    # Original implementation (fixed reshape issue)
    embeddings_matrix = np.array(embeddings)
    
    # Fix: Only reshape if embeddings are 1D
    if embeddings_matrix.ndim == 1:
        embeddings_matrix = embeddings_matrix.reshape(-1, 1)
    elif embeddings_matrix.ndim > 2:
        # Flatten if more than 2D
        embeddings_matrix = embeddings_matrix.reshape(embeddings_matrix.shape[0], -1)

    # Auto-adjust perplexity based on data size
    n_samples = embeddings_matrix.shape[0]
    perplexity = min(15, max(5, max(1, n_samples - 1)))  # Ensure perplexity < n_samples
    
    tsne = TSNE(
        n_components=2, 
        perplexity=perplexity, 
        random_state=42, 
        init='random', 
        learning_rate=200.0
    )

    return tsne.fit_transform(embeddings_matrix)


def weight_matrix(mtx, use_optimized=True):
    """
    Calculate weights for matrix elements with optimization options.
    
    Args:
        mtx: Input matrix or nested list
        use_optimized: Whether to use optimized calculation
    """
    if use_optimized and isinstance(mtx, (list, np.ndarray)):
        # Optimized version using numpy - handle heterogeneous data
        try:
            if isinstance(mtx, list):
                # Handle nested lists with different lengths
                flat_list = []
                for sublist in mtx:
                    if isinstance(sublist, (list, tuple, np.ndarray)):
                        flat_list.extend(sublist)
                    else:
                        flat_list.append(sublist)
                
                # Convert to numpy array if all elements are numeric
                flat_array = np.array(flat_list)
                unique_vals, counts = np.unique(flat_array, return_counts=True)
                return dict(zip(unique_vals, counts))
            else:
                # Handle numpy array
                flat_array = mtx.flatten()
                unique_vals, counts = np.unique(flat_array, return_counts=True)
                return dict(zip(unique_vals, counts))
        except (ValueError, TypeError):
            # Fall back to original implementation if numpy fails
            pass
    
    # Original implementation
    weight = {}
    mtx_flat = [item for sublist in mtx for item in sublist]
    for emb in mtx_flat:
        if (emb in weight):
            weight[emb] += 1
        else:
            weight[emb] = 1

    return weight


def display(embeddings, chunks, use_optimized=True, max_nodes=1000, **kwargs):
    """
    Enhanced display function with intelligent sampling and optimization.
    
    Args:
        embeddings: List of embedding vectors
        chunks: List of text chunks
        use_optimized: Whether to use optimized graph generation
        max_nodes: Maximum number of nodes (for sampling)
        **kwargs: Additional parameters for graph customization
    """
    if use_optimized:
        return display_optimized(embeddings, chunks, max_nodes=max_nodes, **kwargs)
    
    # Original implementation with fixes
    embeddings_small = matrix_tsne(embeddings, use_optimized=False)
    chunks_small = [word for chunk in chunks for word in chunk.split()]

    g = Network(
        height="850px",
        width="100%",
        bgcolor="#222222",
        font_color="white",
        notebook=True,
        cdn_resources="remote",
        directed=True
    )
    weight = weight_matrix(embeddings_small, use_optimized=False)

    connections = {}
    num_id = 0
    last_id = 0

    for embedding, chunk in zip(embeddings_small, chunks_small):

        emb_l = embedding[0]
        emb_r = embedding[1]
        size = len(chunk)

        # Fix potential division by zero
        if emb_l + emb_r != 0:
            tensor = (math.sqrt(((emb_l ** 2) + (emb_r ** 2)))) / (emb_l + emb_r)
        else:
            tensor = math.sqrt(((emb_l ** 2) + (emb_r ** 2)))
            
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


def chart(name, model, use_optimized=True, **kwargs):
    """
    Enhanced chart function with optimization options.
    
    Args:
        name: Base name for the output file
        model: Model object with embeddings and chunks attributes
        use_optimized: Whether to use optimized graph generation
        **kwargs: Additional parameters for graph customization
    """
    if use_optimized:
        chart_optimized(name, model, **kwargs)
    else:
        graph = display(model.embeddings, model.chunks, use_optimized=False, **kwargs)
        graph.show(f"{name}.html")


# New easy-to-use functions for constellation generation
def create_constellation(embeddings, chunks, title="Text Constellation", **kwargs):
    """
    Easy function to create a constellation graph.
    
    Args:
        embeddings: List of embedding vectors
        chunks: List of text chunks
        title: Graph title
        **kwargs: Additional customization parameters
        
    Returns:
        Pyvis Network object
    """
    return create_smart_constellation(embeddings, chunks, title=title, **kwargs)


def save_constellation(embeddings, chunks, filename="constellation.html", 
                      title="Text Constellation", **kwargs):
    """
    Create and save a constellation graph in one function call.
    
    Args:
        embeddings: List of embedding vectors
        chunks: List of text chunks
        filename: Output HTML filename
        title: Graph title
        **kwargs: Additional customization parameters
        
    Returns:
        Path to saved file
    """
    return quick_viz(embeddings, chunks, filename, **kwargs)


def sample_and_visualize(embeddings, chunks, max_nodes=1000, 
                        sampling_strategy="auto", **kwargs):
    """
    Sample large datasets and create optimized visualizations.
    
    Args:
        embeddings: List of embedding vectors
        chunks: List of text chunks
        max_nodes: Maximum number of nodes to display
        sampling_strategy: Sampling strategy ("auto", "hierarchical", "importance", "density")
        **kwargs: Additional parameters
        
    Returns:
        Tuple of (graph, sampling_info)
    """
    # Apply sampling if needed
    if len(embeddings) > max_nodes:
        sampled_embeddings, sampled_chunks, indices = optimize_sampling_for_size(
            embeddings, chunks, max_nodes
        )
        sampling_info = {
            'original_size': len(embeddings),
            'sampled_size': len(sampled_embeddings),
            'selected_indices': indices,
            'reduction_ratio': len(sampled_embeddings) / len(embeddings)
        }
    else:
        sampled_embeddings, sampled_chunks = embeddings, chunks
        sampling_info = {
            'original_size': len(embeddings),
            'sampled_size': len(embeddings),
            'selected_indices': list(range(len(embeddings))),
            'reduction_ratio': 1.0
        }
    
    graph = create_smart_constellation(
        sampled_embeddings, sampled_chunks, 
        max_nodes=max_nodes, 
        sampling_strategy=sampling_strategy,
        **kwargs
    )
    
    return graph, sampling_info
