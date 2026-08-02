import logging
from typing import List, Dict, Any, Tuple, Optional
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

logger = logging.getLogger(__name__)

# ==========================================================
# Load Embedding Model (Loads only once)
# ==========================================================
try:
    model: SentenceTransformer = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("SentenceTransformer model 'all-MiniLM-L6-v2' loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load SentenceTransformer model: {e}")
    raise e


# ==========================================================
# Create Embeddings (Cosine Similarity with IndexFlatIP)
# ==========================================================
def create_embeddings(chunks: List[Dict[str, Any]]) -> Tuple[Optional[faiss.IndexFlatIP], List[Dict[str, Any]]]:
    """
    Creates L2-normalized FAISS IndexFlatIP embeddings for document chunks.

    Parameters
    ----------
    chunks : List[Dict[str, Any]]
        List of chunk dictionaries containing 'text', 'page', 'chunk_id'.

    Returns
    -------
    Tuple[Optional[faiss.IndexFlatIP], List[Dict[str, Any]]]
        FAISS IndexFlatIP instance and original chunk objects.
    """
    if not chunks:
        logger.warning("Empty chunks provided to create_embeddings.")
        return None, []

    try:
        texts = [chunk["text"] for chunk in chunks]

        embeddings = model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        ).astype(np.float32)

        # Normalize vectors for Cosine Similarity via Inner Product Index
        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings)

        logger.info(f"Successfully created FAISS IndexFlatIP with {len(chunks)} vectors.")
        return index, chunks

    except Exception as e:
        logger.error(f"Error creating FAISS embeddings: {e}")
        return None, chunks


# ==========================================================
# Semantic Search with Cosine Similarity Scores
# ==========================================================
def search_similar_chunks(
    question: str,
    index: Optional[faiss.IndexFlatIP],
    chunks: List[Dict[str, Any]],
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Returns top matching chunk dictionaries enriched with cosine similarity score.

    Parameters
    ----------
    question : str
        Search query string.
    index : Optional[faiss.IndexFlatIP]
        FAISS index object.
    chunks : List[Dict[str, Any]]
        Original list of chunk dictionaries.
    top_k : int
        Number of top matches to retrieve.

    Returns
    -------
    List[Dict[str, Any]]
        List of chunk dictionaries with attached 'score' (cosine similarity 0.0 - 1.0).
    """
    if index is None or not chunks or not question.strip():
        return []

    try:
        query_embedding = model.encode(
            [question],
            convert_to_numpy=True,
        ).astype(np.float32)

        faiss.normalize_L2(query_embedding)

        # Retrieve up to top_k elements (bounded by index total)
        k_retrieve = min(top_k, index.ntotal)
        if k_retrieve <= 0:
            return []

        scores, indices = index.search(query_embedding, k_retrieve)

        results: List[Dict[str, Any]] = []
        for raw_score, idx in zip(scores[0], indices[0]):
            if 0 <= idx < len(chunks):
                chunk_copy = dict(chunks[idx])
                # Cosine similarity bounds clipped to [0.0, 1.0]
                similarity = max(0.0, min(1.0, float(raw_score)))
                chunk_copy["score"] = similarity
                chunk_copy["vector_score"] = similarity
                results.append(chunk_copy)

        return results

    except Exception as e:
        logger.error(f"Error performing FAISS similarity search: {e}")
        return []