"""
Optimized visualization functions with intelligent sampling and improved algorithms.
Provides enhanced graph constellation generation for text relationships.
"""
import math
import numpy as np
from pyvis.network import Network
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Dict, Optional, Union
import networkx as nx
from .sampling import IntelligentSampler, optimize_sampling_for_size


class OptimizedGraphGenerator:
    """Enhanced graph generator with intelligent sampling and relationship detection."""
    
    def __init__(self, max_nodes: int = 1000, sampling_strategy: str = "auto"):
        """
        Initialize the graph generator.
        
        Args:
            max_nodes: Maximum number of nodes in the graph
            sampling_strategy: Sampling strategy to use ("auto", "hierarchical", "importance", "density")
        """
        self.max_nodes = max_nodes
        self.sampling_strategy = sampling_strategy
        self.sampler = IntelligentSampler(max_samples=max_nodes)
    
    def enhanced_tsne(self, embeddings: List, perplexity: Optional[int] = None) -> np.ndarray:
        """
        Enhanced t-SNE implementation with automatic parameter tuning.
        
        Args:
            embeddings: List of embedding vectors
            perplexity: t-SNE perplexity parameter (auto-calculated if None)
            
        Returns:
            2D coordinates from t-SNE
        """
        embeddings_array = np.array(embeddings)
        
        # Fix the reshape issue from original code
        if embeddings_array.ndim == 1:
            embeddings_array = embeddings_array.reshape(-1, 1)
        
        n_samples = len(embeddings_array)
        
        # Handle edge cases
        if n_samples == 0:
            raise ValueError("Cannot perform t-SNE on empty dataset")
        if n_samples == 1:
            return np.array([[0.0, 0.0]])
        
        # Auto-calculate perplexity based on dataset size
        if perplexity is None:
            perplexity = min(30, max(5, n_samples // 3))
        
        # Ensure perplexity is not too large for the dataset
        perplexity = min(perplexity, n_samples - 1)
        
        # Adjust parameters based on dataset size
        learning_rate = 200.0 if n_samples < 1000 else 'auto'
        max_iter = 1000 if n_samples < 5000 else 300
        
        tsne = TSNE(
            n_components=2,
            perplexity=perplexity,
            random_state=42,
            init='random',
            learning_rate=learning_rate,
            max_iter=max_iter,
            n_jobs=None  # Use single core to avoid issues
        )
        
        return tsne.fit_transform(embeddings_array)
    
    def calculate_smart_weights(self, embeddings: List, chunks: List,
                              tsne_coords: np.ndarray) -> Dict[int, float]:
        """
        Calculate intelligent weights based on multiple factors.
        
        Args:
            embeddings: Original embedding vectors
            chunks: Text chunks
            tsne_coords: 2D coordinates from t-SNE
            
        Returns:
            Dictionary mapping indices to weight values
        """
        weights = {}
        embeddings_array = np.array(embeddings)
        
        for i, (embedding, chunk, coord) in enumerate(zip(embeddings, chunks, tsne_coords)):
            weight = 1.0
            
            # Factor 1: Text content importance
            text_length = len(chunk.split())
            weight *= (1.0 + text_length / 20.0)  # Longer texts get higher weight
            
            # Factor 2: Embedding magnitude (more distinctive embeddings)
            embedding_norm = np.linalg.norm(embedding)
            weight *= (1.0 + embedding_norm)
            
            # Factor 3: Position uniqueness in t-SNE space
            coord_norm = np.linalg.norm(coord)
            weight *= (1.0 + coord_norm / 100.0)
            
            # Factor 4: Rarity (distance from other points)
            if len(embeddings_array) > 1:
                similarities = cosine_similarity([embedding], embeddings_array)[0]
                # Remove self-similarity
                similarities = similarities[similarities < 0.999]
                if len(similarities) > 0:
                    avg_similarity = np.mean(similarities)
                    # Lower similarity = higher weight (more unique)
                    weight *= (2.0 - avg_similarity)
            
            weights[i] = max(0.1, min(weight, 10.0))  # Clamp between 0.1 and 10.0
        
        return weights
    
    def detect_relationships(self, embeddings: List, chunks: List,
                           similarity_threshold: float = 0.7) -> List[Tuple[int, int, float]]:
        """
        Detect relationships between text chunks based on embedding similarity.
        
        Args:
            embeddings: List of embedding vectors
            chunks: List of text chunks
            similarity_threshold: Minimum similarity to create an edge
            
        Returns:
            List of (source_idx, target_idx, weight) tuples
        """
        relationships = []
        embeddings_array = np.array(embeddings)
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(embeddings_array)
        
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                similarity = similarity_matrix[i][j]
                
                if similarity >= similarity_threshold:
                    # Additional relationship checks
                    chunk_i, chunk_j = chunks[i], chunks[j]
                    
                    # Check for common words (semantic relationship)
                    words_i = set(chunk_i.lower().split())
                    words_j = set(chunk_j.lower().split())
                    common_words = words_i.intersection(words_j)
                    
                    # Boost similarity if there are common meaningful words
                    if common_words:
                        similarity *= (1.0 + len(common_words) * 0.1)
                    
                    relationships.append((i, j, similarity))
        
        return relationships
    
    def create_constellation_graph(self, embeddings: List, chunks: List,
                                 title: str = "Text Relationships Constellation",
                                 **kwargs) -> Network:
        """
        Create an optimized constellation graph with intelligent sampling.
        
        Args:
            embeddings: List of embedding vectors
            chunks: List of text chunks
            title: Graph title
            **kwargs: Additional parameters for customization
            
        Returns:
            Pyvis Network object
        """
        # Apply intelligent sampling if needed
        if len(embeddings) > self.max_nodes:
            print(f"Applying intelligent sampling: {len(embeddings)} -> {self.max_nodes} nodes")
            sampled_embeddings, sampled_chunks, indices = self.sampler.smart_sampling(
                embeddings, chunks, self.sampling_strategy
            )
        else:
            sampled_embeddings, sampled_chunks, indices = embeddings, chunks, list(range(len(embeddings)))
        
        # Generate 2D coordinates
        tsne_coords = self.enhanced_tsne(sampled_embeddings)
        
        # Calculate intelligent weights
        weights = self.calculate_smart_weights(sampled_embeddings, sampled_chunks, tsne_coords)
        
        # Detect relationships
        relationships = self.detect_relationships(
            sampled_embeddings, sampled_chunks,
            kwargs.get('similarity_threshold', 0.7)
        )
        
        # Create the graph
        graph = Network(
            height=kwargs.get('height', '850px'),
            width=kwargs.get('width', '100%'),
            bgcolor=kwargs.get('bgcolor', '#1a1a1a'),
            font_color=kwargs.get('font_color', 'white'),
            notebook=kwargs.get('notebook', True),
            cdn_resources="remote",
            directed=kwargs.get('directed', False)
        )
        
        # Add nodes with optimized positioning and styling
        for i, (coord, chunk) in enumerate(zip(tsne_coords, sampled_chunks)):
            x, y = coord
            weight = weights.get(i, 1.0)
            
            # Create node label (truncate if too long)
            label = chunk[:50] + "..." if len(chunk) > 50 else chunk
            
            # Calculate node size based on weight and text importance
            node_size = max(10, min(50, weight * 5))
            
            # Color based on position and weight
            color = self._calculate_node_color(x, y, weight)
            
            graph.add_node(
                i,
                label=label,
                title=chunk,  # Full text on hover
                value=node_size,
                x=int(x * 10),  # Scale coordinates
                y=int(y * 10),
                color=color,
                font={'size': max(12, min(20, int(weight * 2)))},
                borderWidth=2,
                borderWidthSelected=4
            )
        
        # Add edges based on detected relationships
        for source, target, similarity in relationships:
            edge_weight = similarity * 3  # Scale for visibility
            graph.add_edge(
                source, target,
                weight=edge_weight,
                width=max(1, edge_weight),
                color={'color': f'rgba(255,255,255,{similarity * 0.8})'},
                title=f"Similarity: {similarity:.3f}"
            )
        
        # Configure physics for better layout
        graph.set_options("""
        var options = {
          "physics": {
            "enabled": true,
            "stabilization": {"iterations": 100},
            "barnesHut": {
              "gravitationalConstant": -8000,
              "centralGravity": 0.3,
              "springLength": 95,
              "springConstant": 0.04,
              "damping": 0.09
            }
          },
          "interaction": {
            "hover": true,
            "tooltipDelay": 200,
            "hideEdgesOnDrag": true
          }
        }
        """)
        
        return graph
    
    def _calculate_node_color(self, x: float, y: float, weight: float) -> str:
        """Calculate node color based on position and weight."""
        # Normalize coordinates for color calculation
        norm_x = (x + 100) / 200  # Assuming t-SNE coords in roughly [-100, 100]
        norm_y = (y + 100) / 200
        
        # Base color on position with weight influence
        r = int(255 * norm_x * (weight / 5.0))
        g = int(255 * norm_y * (weight / 5.0))
        b = int(255 * (1 - norm_x) * (weight / 5.0))
        
        # Clamp values
        r = max(50, min(255, r))
        g = max(50, min(255, g))
        b = max(50, min(255, b))
        
        return f'rgb({r},{g},{b})'


# Convenience functions for easy usage
def create_smart_constellation(embeddings: List, chunks: List,
                             max_nodes: int = 1000,
                             sampling_strategy: str = "auto",
                             **kwargs) -> Network:
    """
    Create a smart constellation graph with one function call.
    
    Args:
        embeddings: List of embedding vectors
        chunks: List of text chunks
        max_nodes: Maximum number of nodes
        sampling_strategy: Sampling strategy
        **kwargs: Additional graph parameters
        
    Returns:
        Pyvis Network object
    """
    generator = OptimizedGraphGenerator(max_nodes=max_nodes, sampling_strategy=sampling_strategy)
    return generator.create_constellation_graph(embeddings, chunks, **kwargs)


def quick_viz(embeddings: List, chunks: List, filename: str = "constellation.html",
              max_nodes: int = 1000) -> str:
    """
    Quick visualization function - create and save graph in one call.
    
    Args:
        embeddings: List of embedding vectors
        chunks: List of text chunks
        filename: Output HTML filename
        max_nodes: Maximum number of nodes
        
    Returns:
        Path to the saved HTML file
    """
    graph = create_smart_constellation(embeddings, chunks, max_nodes=max_nodes)
    graph.show(filename)
    return filename


# Updated versions of original functions for backward compatibility
def matrix_tsne_optimized(embeddings: List, **kwargs) -> np.ndarray:
    """Optimized version of the original matrix_tsne function."""
    generator = OptimizedGraphGenerator()
    return generator.enhanced_tsne(embeddings, **kwargs)


def display_optimized(embeddings: List, chunks: List, **kwargs) -> Network:
    """Optimized version of the original display function."""
    return create_smart_constellation(embeddings, chunks, **kwargs)


def chart_optimized(name: str, model, **kwargs) -> None:
    """Optimized version of the original chart function."""
    graph = display_optimized(model.embeddings, model.chunks, **kwargs)
    graph.show(f"{name}.html")