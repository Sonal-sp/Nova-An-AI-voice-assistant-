import logging
from typing import List, Dict, Any, Tuple, Optional
import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

logger = logging.getLogger(__name__)


# ==========================================================
# Cached Model Loader
# ==========================================================
@st.cache_resource(show_spinner=False)
def get_embedding_model() -> SentenceTransformer:
    """
    Loads and caches the SentenceTransformer model to prevent redundant reloads.
    """
    logger.info("Loading SentenceTransformer model 'all-MiniLM-L6-v2'...")
    return SentenceTransformer("all-MiniLM-L6-v2")


try:
    model: SentenceTransformer = get_embedding_model()
except Exception as e:
    logger.error(f"Failed to load SentenceTransformer model: {e}")
    model = None


# ==========================================================
# Create Embeddings (Cosine Similarity with IndexFlatIP)
# ==========================================================
def create_embeddings(chunks: List[Dict[str, Any]]) -> Tuple[Optional[faiss.IndexFlatIP], List[Dict[str, Any]]]:
    """
    Creates L2-normalized FAISS IndexFlatIP embeddings for document chunks.
    """
    if not chunks:
        logger.warning("Empty chunks provided to create_embeddings.")
        return None, []

    emb_model = get_embedding_model()
    if emb_model is None:
        return None, chunks

    try:
        texts = [chunk["text"] for chunk in chunks]

        embeddings = emb_model.encode(
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
    """
    if index is None or not chunks or not question.strip():
        return []

    emb_model = get_embedding_model()
    if emb_model is None:
        return []

    try:
        query_embedding = emb_model.encode(
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
                similarity = max(0.0, min(1.0, float(raw_score)))
                chunk_copy["score"] = similarity
                chunk_copy["vector_score"] = similarity
                results.append(chunk_copy)

        return results

    except Exception as e:
        logger.error(f"Error performing FAISS similarity search: {e}")
        return []