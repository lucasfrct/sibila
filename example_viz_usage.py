#!/usr/bin/env python3
"""
Example usage of the enhanced viz module for creating text relationship constellations.
This example demonstrates how to use the improved viz module with sample legal text data.
"""
import sys
import os
sys.path.append('src')

import numpy as np
from modules.viz import (
    create_constellation, quick_viz, sample_and_visualize
)

def main():
    """Demonstrate practical usage of the enhanced viz module."""
    
    # Sample Brazilian legal text data (simulated)
    legal_chunks = [
        "Art. 1º A República Federativa do Brasil constitui-se em Estado Democrático de Direito",
        "Art. 2º São Poderes da União o Legislativo o Executivo e o Judiciário",
        "Art. 3º Constituem objetivos fundamentais da República Federativa do Brasil",
        "Art. 4º O Brasil rege-se nas suas relações internacionais pelos seguintes princípios",
        "Art. 5º Todos são iguais perante a lei sem distinção de qualquer natureza",
        "Parágrafo único Todo o poder emana do povo que o exerce por meio de representantes",
        "inciso I a soberania nacional e a independência do país",
        "inciso II a cidadania e os direitos fundamentais da pessoa humana",
        "inciso III a dignidade da pessoa humana e os valores sociais",
        "inciso IV os valores sociais do trabalho e da livre iniciativa",
        "direitos fundamentais liberdade igualdade fraternidade",
        "poder legislativo federal estadual municipal",
        "poder executivo presidente governador prefeito",
        "poder judiciário tribunais juízes magistrados",
        "constituição federal lei fundamental do país",
        "democracia participativa representativa direta",
        "estado democrático de direito soberania popular",
        "direitos humanos proteção universal",
        "princípios fundamentais república federativa",
        "organização do estado federação união estados municípios"
    ]
    
    # Generate sample embeddings (in practice, these would come from your embedding model)
    np.random.seed(42)
    embeddings = []
    
    for i, chunk in enumerate(legal_chunks):
        # Create realistic embeddings based on content themes
        base_vector = np.random.rand(8)
        
        # Add semantic clustering
        if "art" in chunk.lower() or "artigo" in chunk.lower():
            base_vector += np.array([0.3, 0.1, 0.0, 0.0, 0.2, 0.1, 0.0, 0.0])
        if "poder" in chunk.lower():
            base_vector += np.array([0.0, 0.3, 0.2, 0.1, 0.0, 0.0, 0.1, 0.0])
        if "direito" in chunk.lower() or "direitos" in chunk.lower():
            base_vector += np.array([0.1, 0.0, 0.3, 0.2, 0.0, 0.1, 0.0, 0.2])
        if "república" in chunk.lower() or "federal" in chunk.lower():
            base_vector += np.array([0.2, 0.1, 0.0, 0.3, 0.1, 0.0, 0.0, 0.1])
        
        embeddings.append(base_vector.tolist())
    
    print("🇧🇷 Enhanced Viz Module - Brazilian Legal Text Example")
    print("=" * 60)
    print(f"📊 Dataset: {len(embeddings)} legal text segments")
    print(f"🔤 Sample text: '{legal_chunks[0][:50]}...'")
    
    # Example 1: Simple constellation creation
    print("\n1️⃣ Creating basic legal constellation...")
    graph = create_constellation(
        embeddings, legal_chunks,
        title="Brazilian Constitutional Framework"
    )
    print(f"   ✅ Created graph with {len(graph.nodes)} nodes")
    
    # Example 2: Quick visualization with automatic optimization
    print("\n2️⃣ Quick visualization with intelligent sampling...")
    filename = quick_viz(
        embeddings, legal_chunks,
        "brazilian_legal_constellation.html",
        max_nodes=15  # Limit for clear visualization
    )
    print(f"   ✅ Saved interactive visualization: {filename}")
    print(f"   🌐 Open '{filename}' in your browser to explore!")
    
    # Example 3: Advanced sampling and analysis
    print("\n3️⃣ Advanced sampling with detailed analysis...")
    graph, sampling_info = sample_and_visualize(
        embeddings, legal_chunks,
        max_nodes=12,
        sampling_strategy="importance",
        title="Key Legal Concepts Network",
        similarity_threshold=0.6
    )
    
    print(f"   📈 Analysis Results:")
    print(f"      Original size: {sampling_info['original_size']} segments")
    print(f"      Sampled size: {sampling_info['sampled_size']} segments")
    print(f"      Reduction: {(1-sampling_info['reduction_ratio'])*100:.1f}%")
    print(f"      Graph nodes: {len(graph.nodes)}")
    
    # Example 4: Show which segments were selected
    if 'selected_indices' in sampling_info:
        selected_texts = [legal_chunks[i] for i in sampling_info['selected_indices'][:5]]
        print(f"\n   🎯 Top selected segments:")
        for i, text in enumerate(selected_texts):
            print(f"      {i+1}. {text[:60]}...")
    
    print("\n" + "=" * 60)
    print("✨ VISUALIZATION COMPLETE!")
    print("💡 Key Features Demonstrated:")
    print("   • Intelligent sampling preserves important legal concepts")
    print("   • Automatic relationship detection finds semantic connections")
    print("   • Interactive graphs show text relationships visually")
    print("   • Performance optimization handles large document sets")
    print("\n🚀 The enhanced viz module is ready for your legal document analysis!")

if __name__ == "__main__":
    main()