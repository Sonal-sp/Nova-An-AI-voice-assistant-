from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ==========================================================
# Load Embedding Model (Loads only once)
# ==========================================================
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==========================================================
# Create Embeddings
# ==========================================================
def create_embeddings(chunks):
    """
    Creates FAISS embeddings for document chunks.

    Parameters
    ----------
    chunks : list
        List of chunk dictionaries.

    Returns
    -------
    index
        FAISS index

    chunks
        Original chunk objects
    """

    if not chunks:
        return None, []

    # ---------------------------------------
    # Embed ONLY the chunk text
    # ---------------------------------------
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False,
    ).astype(np.float32)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(embeddings)

    return index, chunks


# ==========================================================
# Semantic Search
# ==========================================================
def search_similar_chunks(
    question,
    index,
    chunks,
    top_k=3,
):
    """
    Returns the top matching chunk dictionaries.

    Each result contains:
    text
    page
    chunk_id
    """

    if (
        index is None
        or not chunks
    ):
        return []

    query_embedding = model.encode(
        [question],
        convert_to_numpy=True,
    ).astype(np.float32)

    distances, indices = index.search(
        query_embedding,
        top_k,
    )

    results = []

    for idx in indices[0]:

        if idx < len(chunks):

            results.append(
                chunks[idx]
            )

    return results