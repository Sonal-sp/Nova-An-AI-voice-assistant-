from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ---------------------------------------------------
# Load embedding model only once
# ---------------------------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------------------------------------------
# Create embeddings for PDF chunks
# ---------------------------------------------------
def create_embeddings(chunks):
    """
    Converts PDF chunks into embeddings and
    builds a FAISS index.

    Returns:
        index: FAISS index
        chunks: Original chunks
    """

    if not chunks:
        return None, []

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=False,
    )

    embeddings = embeddings.astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index, chunks


# ---------------------------------------------------
# Search most relevant chunks
# ---------------------------------------------------
def search_similar_chunks(
    question,
    index,
    chunks,
    top_k=3,
):
    """
    Returns the most relevant chunks for a question.
    """

    if index is None or not chunks:
        return ""

    query_embedding = model.encode(
        [question],
        convert_to_numpy=True,
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k,
    )

    results = []

    for idx in indices[0]:

        if idx < len(chunks):

            results.append(chunks[idx])

    return "\n\n".join(results)