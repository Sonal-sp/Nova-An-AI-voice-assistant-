import logging
import math
from typing import List, Dict, Any, Optional
import numpy as np

logger = logging.getLogger(__name__)

# Global lazy singleton instance
_cross_encoder_instance = None
_cross_encoder_attempted: bool = False


def _get_cross_encoder():
    """
    Lazy loads CrossEncoder model if cached locally, avoiding network latency.
    """
    global _cross_encoder_instance, _cross_encoder_attempted

    if _cross_encoder_attempted:
        return _cross_encoder_instance

    _cross_encoder_attempted = True
    try:
        from sentence_transformers import CrossEncoder
        logger.info("Checking local CrossEncoder model cache...")
        _cross_encoder_instance = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2",
            local_files_only=True,
        )
        logger.info("Local CrossEncoder loaded successfully.")
    except Exception:
        logger.info("Local CrossEncoder cache miss. Utilizing instant embedding dot-product re-ranking.")
        _cross_encoder_instance = None

    return _cross_encoder_instance


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def rerank_candidates(
    query: str,
    candidates: List[Dict[str, Any]],
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Re-ranks retrieved candidates against query using CrossEncoder or fast offline vector dot-product.

    Parameters
    ----------
    query : str
        User search query string.
    candidates : List[Dict[str, Any]]
        Candidate chunks from RRF retrieval.
    top_k : int
        Number of top re-ranked chunks to return.

    Returns
    -------
    List[Dict[str, Any]]
        Re-ranked chunk dictionaries with updated 'score' and 'rerank_score'.
    """
    if not candidates or not query.strip():
        return []

    # 1. Attempt CrossEncoder re-ranking if locally available
    reranker = _get_cross_encoder()
    if reranker is not None:
        try:
            pairs = [[query, chunk["text"]] for chunk in candidates]
            scores = reranker.predict(pairs)

            ranked: List[Dict[str, Any]] = []
            for chunk, raw_score in zip(candidates, scores):
                chunk_copy = dict(chunk)
                norm_score = max(0.0, min(1.0, sigmoid(float(raw_score))))
                chunk_copy["rerank_score"] = norm_score
                chunk_copy["score"] = norm_score
                ranked.append(chunk_copy)

            ranked.sort(key=lambda item: item["rerank_score"], reverse=True)
            return ranked[:top_k]
        except Exception as e:
            logger.warning(f"CrossEncoder prediction failed: {e}. Falling back to embedding re-ranking.")

    # 2. Fast Offline Vector Dot-Product Re-ranking (0ms latency fallback)
    try:
        from services.embedding_service import model

        query_emb = model.encode([query], convert_to_numpy=True).astype(np.float32)
        norm_q = np.linalg.norm(query_emb, axis=1, keepdims=True)
        query_emb = query_emb / (norm_q + 1e-9)

        texts = [chunk["text"] for chunk in candidates]
        cand_embs = model.encode(texts, convert_to_numpy=True).astype(np.float32)
        norm_c = np.linalg.norm(cand_embs, axis=1, keepdims=True)
        cand_embs = cand_embs / (norm_c + 1e-9)

        sims = np.dot(cand_embs, query_emb.T).flatten()

        ranked = []
        for chunk, sim in zip(candidates, sims):
            chunk_copy = dict(chunk)
            score_val = max(0.0, min(1.0, float(sim)))
            chunk_copy["rerank_score"] = score_val
            chunk_copy["score"] = score_val
            ranked.append(chunk_copy)

        ranked.sort(key=lambda item: item["rerank_score"], reverse=True)
        return ranked[:top_k]

    except Exception as e:
        logger.error(f"Embedding re-ranking failed: {e}. Returning candidate order.")
        return candidates[:top_k]
