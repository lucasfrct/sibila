# flake8: noqa: E501


from src.models.llm_model import ModelLLM

def generate_embeddings(ollama: ModelLLM, chunks = []):
    """
    Gera embeddings para os chunks fornecidos pelo objeto LLM.
    Args:
        llm: Um objeto que contém os chunks de texto e métodos para gerar embeddings.
    Returns:
        Os dados do objeto LLM após a geração dos embeddings.
    Exibe o progresso da geração dos embeddings no console.
    """
    
    info = "- - - > Embedding"

    step = (100 / len(ollama.chunks))
    
    embeddings = []
    
    for i, chunk in enumerate(chunks):
        embeddings.append(ollama.embed(chunk))
        print(f"{info} - {int(i*step)}%", end='\r', flush=True)

    print(f"{info} - 100%", end='\r', flush=True)
    print("\n", end='', flush=True)

    return embeddings


def set_chunks(chunks=None):
    if chunks is None:
        chunks = []
    return chunks
