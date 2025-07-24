"""
Intelligent sampling strategies for visualization optimization.
Provides methods to reduce dataset size while preserving important relationships and patterns.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Union, Optional
import math


class IntelligentSampler:
    """Provides various intelligent sampling strategies for large datasets."""
    
    def __init__(self, max_samples: int = 1000, preserve_outliers: bool = True):
        """
        Initialize the sampler.
        
        Args:
            max_samples: Maximum number of samples to keep
            preserve_outliers: Whether to always include outlier points
        """
        self.max_samples = max_samples
        self.preserve_outliers = preserve_outliers
    
    def hierarchical_sampling(self, embeddings: List, chunks: List, 
                            levels: int = 3) -> Tuple[List, List, List[int]]:
        """
        Hierarchical sampling based on clustering at multiple levels.
        
        Args:
            embeddings: List of embedding vectors
            chunks: List of corresponding text chunks
            levels: Number of hierarchical levels
            
        Returns:
            Tuple of (sampled_embeddings, sampled_chunks, original_indices)
        """
        if len(embeddings) <= self.max_samples:
            return embeddings, chunks, list(range(len(embeddings)))
        
        embeddings_array = np.array(embeddings)
        n_samples = len(embeddings)
        
        # Calculate samples per level
        samples_per_level = self.max_samples // levels
        selected_indices = set()
        
        for level in range(levels):
            # Number of clusters for this level
            n_clusters = min(samples_per_level * (level + 1), n_samples // 2)
            
            if n_clusters <= 0:
                continue
                
            # Perform clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(embeddings_array)
            
            # Select representative points from each cluster
            for cluster_id in range(n_clusters):
                cluster_indices = np.where(cluster_labels == cluster_id)[0]
                if len(cluster_indices) == 0:
                    continue
                
                # Find point closest to cluster center
                cluster_center = kmeans.cluster_centers_[cluster_id]
                cluster_embeddings = embeddings_array[cluster_indices]
                distances = np.linalg.norm(cluster_embeddings - cluster_center, axis=1)
                closest_idx = cluster_indices[np.argmin(distances)]
                selected_indices.add(closest_idx)
                
                if len(selected_indices) >= self.max_samples:
                    break
            
            if len(selected_indices) >= self.max_samples:
                break
        
        # Add outliers if requested
        if self.preserve_outliers and len(selected_indices) < self.max_samples:
            outlier_indices = self._find_outliers(embeddings_array)
            for idx in outlier_indices:
                if idx not in selected_indices:
                    selected_indices.add(idx)
                    if len(selected_indices) >= self.max_samples:
                        break
        
        selected_indices = sorted(list(selected_indices))
        sampled_embeddings = [embeddings[i] for i in selected_indices]
        sampled_chunks = [chunks[i] for i in selected_indices]
        
        return sampled_embeddings, sampled_chunks, selected_indices
    
    def importance_based_sampling(self, embeddings: List, chunks: List,
                                importance_scores: Optional[List[float]] = None) -> Tuple[List, List, List[int]]:
        """
        Sample based on importance scores, preserving most important points.
        
        Args:
            embeddings: List of embedding vectors
            chunks: List of corresponding text chunks
            importance_scores: Optional pre-calculated importance scores
            
        Returns:
            Tuple of (sampled_embeddings, sampled_chunks, original_indices)
        """
        if len(embeddings) <= self.max_samples:
            return embeddings, chunks, list(range(len(embeddings)))
        
        if importance_scores is None:
            importance_scores = self._calculate_importance_scores(embeddings, chunks)
        
        # Sort by importance and take top samples
        indexed_scores = [(score, idx) for idx, score in enumerate(importance_scores)]
        indexed_scores.sort(reverse=True)
        
        selected_indices = [idx for _, idx in indexed_scores[:self.max_samples]]
        selected_indices.sort()
        
        sampled_embeddings = [embeddings[i] for i in selected_indices]
        sampled_chunks = [chunks[i] for i in selected_indices]
        
        return sampled_embeddings, sampled_chunks, selected_indices
    
    def adaptive_density_sampling(self, embeddings: List, chunks: List) -> Tuple[List, List, List[int]]:
        """
        Adaptive sampling based on local density of points.
        
        Args:
            embeddings: List of embedding vectors
            chunks: List of corresponding text chunks
            
        Returns:
            Tuple of (sampled_embeddings, sampled_chunks, original_indices)
        """
        if len(embeddings) <= self.max_samples:
            return embeddings, chunks, list(range(len(embeddings)))
        
        embeddings_array = np.array(embeddings)
        n_samples = len(embeddings)
        
        # Calculate local density for each point
        similarities = cosine_similarity(embeddings_array)
        densities = np.sum(similarities > 0.8, axis=1)  # Count similar neighbors
        
        # Sort by density (ascending - prefer diverse points)
        density_indices = np.argsort(densities)
        
        selected_indices = []
        
        # Select points with different density levels
        step = max(1, len(density_indices) // self.max_samples)
        for i in range(0, len(density_indices), step):
            selected_indices.append(density_indices[i])
            if len(selected_indices) >= self.max_samples:
                break
        
        # Add high-importance outliers if space available
        if len(selected_indices) < self.max_samples:
            outlier_indices = self._find_outliers(embeddings_array)
            for idx in outlier_indices:
                if idx not in selected_indices:
                    selected_indices.append(idx)
                    if len(selected_indices) >= self.max_samples:
                        break
        
        selected_indices.sort()
        sampled_embeddings = [embeddings[i] for i in selected_indices]
        sampled_chunks = [chunks[i] for i in selected_indices]
        
        return sampled_embeddings, sampled_chunks, selected_indices
    
    def smart_sampling(self, embeddings: List, chunks: List, 
                      strategy: str = "auto") -> Tuple[List, List, List[int]]:
        """
        Intelligent sampling that combines multiple strategies.
        
        Args:
            embeddings: List of embedding vectors
            chunks: List of corresponding text chunks
            strategy: Sampling strategy ("auto", "hierarchical", "importance", "density")
            
        Returns:
            Tuple of (sampled_embeddings, sampled_chunks, original_indices)
        """
        if len(embeddings) <= self.max_samples:
            return embeddings, chunks, list(range(len(embeddings)))
        
        if strategy == "auto":
            # Choose strategy based on data size and characteristics
            if len(embeddings) > 10000:
                strategy = "hierarchical"
            elif len(embeddings) > 5000:
                strategy = "density"
            else:
                strategy = "importance"
        
        if strategy == "hierarchical":
            return self.hierarchical_sampling(embeddings, chunks)
        elif strategy == "importance":
            return self.importance_based_sampling(embeddings, chunks)
        elif strategy == "density":
            return self.adaptive_density_sampling(embeddings, chunks)
        else:
            raise ValueError(f"Unknown sampling strategy: {strategy}")
    
    def _calculate_importance_scores(self, embeddings: List, chunks: List) -> List[float]:
        """Calculate importance scores for each embedding/chunk pair."""
        scores = []
        embeddings_array = np.array(embeddings)
        
        # Calculate scores based on multiple factors
        for i, (embedding, chunk) in enumerate(zip(embeddings, chunks)):
            score = 0.0
            
            # Factor 1: Text length (longer chunks might be more important)
            text_length = len(chunk.split())
            score += min(text_length / 10.0, 2.0)  # Cap at 2.0
            
            # Factor 2: Embedding magnitude (higher magnitude = more distinctive)
            embedding_norm = np.linalg.norm(embedding)
            score += embedding_norm
            
            # Factor 3: Uniqueness (distance from other embeddings)
            if len(embeddings_array) > 1:
                distances = np.linalg.norm(embeddings_array - np.array(embedding), axis=1)
                # Remove distance to self
                distances = distances[distances > 0]
                if len(distances) > 0:
                    avg_distance = np.mean(distances)
                    score += avg_distance
            
            scores.append(score)
        
        return scores
    
    def _find_outliers(self, embeddings_array: np.ndarray, 
                      outlier_fraction: float = 0.1) -> List[int]:
        """Find outlier points in the embedding space."""
        if len(embeddings_array) < 3:
            return []
        
        # Calculate distances from centroid
        centroid = np.mean(embeddings_array, axis=0)
        distances = np.linalg.norm(embeddings_array - centroid, axis=1)
        
        # Find points that are far from the center
        threshold = np.percentile(distances, 90)
        outlier_indices = np.where(distances >= threshold)[0]
        
        # Limit number of outliers
        max_outliers = max(1, int(len(embeddings_array) * outlier_fraction))
        if len(outlier_indices) > max_outliers:
            # Keep the most extreme outliers
            extreme_indices = np.argsort(distances[outlier_indices])[-max_outliers:]
            outlier_indices = outlier_indices[extreme_indices]
        
        return outlier_indices.tolist()


def optimize_sampling_for_size(embeddings: List, chunks: List, 
                             target_size: int = 1000) -> Tuple[List, List, List[int]]:
    """
    Convenience function to optimize sampling for a target dataset size.
    
    Args:
        embeddings: List of embedding vectors
        chunks: List of corresponding text chunks
        target_size: Target number of samples
        
    Returns:
        Tuple of (sampled_embeddings, sampled_chunks, original_indices)
    """
    sampler = IntelligentSampler(max_samples=target_size)
    return sampler.smart_sampling(embeddings, chunks)