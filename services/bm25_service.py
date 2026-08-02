import re
import logging
from typing import List, Dict, Any, Optional
from rank_bm25 import BM25Okapi

logger = logging.getLogger(__name__)


def tokenize_text(text: str) -> List[str]:
    """
    Tokenizes text by lowercasing, extracting alphanumeric words, and filtering out noise.

    Parameters
    ----------
    text : str
        Input string.

    Returns
    -------
    List[str]
        List of cleaned tokens.
    """
    if not text:
        return []
    words = re.findall(r"\w+", text.lower())
    # Keep words with length >= 2
    return [w for w in words if len(w) >= 2]


def build_bm25_index(chunks: List[Dict[str, Any]]) -> Optional[BM25Okapi]:
    """
    Builds a BM25 index from document chunks.

    Parameters
    ----------
    chunks : List[Dict[str, Any]]
        List of chunk objects containing 'text'.

    Returns
    -------
    Optional[BM25Okapi]
        BM25 index object or None if empty.
    """
    if not chunks:
        logger.warning("Empty chunks provided to build_bm25_index.")
        return None

    try:
        corpus = [tokenize_text(chunk.get("text", "")) for chunk in chunks]
        index = BM25Okapi(corpus)
        logger.info(f"Successfully built BM25 index for {len(chunks)} chunks.")
        return index
    except Exception as e:
        logger.error(f"Error building BM25 index: {e}")
        return None


def search_bm25(
    question: str,
    bm25: Optional[BM25Okapi],
    chunks: List[Dict[str, Any]],
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Searches BM25 index for query matches and returns top chunks with normalized keyword scores.

    Parameters
    ----------
    question : str
        Query string.
    bm25 : Optional[BM25Okapi]
        BM25 index.
    chunks : List[Dict[str, Any]]
        Original chunk list.
    top_k : int
        Number of top matches.

    Returns
    -------
    List[Dict[str, Any]]
        List of chunks with attached 'score' and 'bm25_score'.
    """
    if bm25 is None or not chunks or not question.strip():
        return []

    try:
        tokens = tokenize_text(question)
        if not tokens:
            return []

        scores = bm25.get_scores(tokens)
        if len(scores) == 0:
            return []

        # Find top_k indices sorted by score descending
        max_score = float(max(scores)) if len(scores) > 0 else 1.0
        if max_score <= 0:
            max_score = 1.0

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )[:top_k]

        results: List[Dict[str, Any]] = []
        for idx in ranked_indices:
            raw_score = float(scores[idx])
            if raw_score <= 0:
                continue

            chunk_copy = dict(chunks[idx])
            normalized_score = min(1.0, raw_score / max_score)
            chunk_copy["score"] = normalized_score
            chunk_copy["bm25_score"] = raw_score
            results.append(chunk_copy)

        return results

    except Exception as e:
        logger.error(f"Error performing BM25 search: {e}")
        return []