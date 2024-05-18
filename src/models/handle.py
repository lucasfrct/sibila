
def generate_embeddings(llm):
    info = "- - - > Embedding"

    step = (100 / len(llm.chunks))
    for i, chunk in enumerate(llm.chunks):
        llm.embeddings.append(llm.embed(chunk))
        print(f"{info} - {int(i*step)}%", end='\r', flush=True)

    print(f"{info} - 100%", end='\r', flush=True)
    print("\n", end='', flush=True)

    return llm.data


def set_chunks(chunks=None):
    if chunks is None:
        chunks = []
    return chunks
