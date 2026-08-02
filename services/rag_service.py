import logging
from typing import List, Dict, Any, Tuple, Optional

from services.embedding_service import search_similar_chunks
from services.bm25_service import search_bm25
from services.reranker_service import rerank_candidates

logger = logging.getLogger(__name__)


# ==========================================================
# Reciprocal Rank Fusion (RRF)
# ==========================================================
def reciprocal_rank_fusion(
    faiss_results: List[Dict[str, Any]],
    bm25_results: List[Dict[str, Any]],
    k: int = 60,
    top_candidates_count: int = 10,
) -> List[Dict[str, Any]]:
    """
    Combines dense FAISS search ranks and sparse BM25 search ranks using Reciprocal Rank Fusion.

    Formula: RRF(d) = sum(1 / (k + rank(d))) for rankers

    Parameters
    ----------
    faiss_results : List[Dict[str, Any]]
        List of chunks from FAISS vector search.
    bm25_results : List[Dict[str, Any]]
        List of chunks from BM25 search.
    k : int
        RRF smoothing constant (default: 60).
    top_candidates_count : int
        Number of top candidate chunks to return for re-ranking.

    Returns
    -------
    List[Dict[str, Any]]
        Candidate chunks ordered by RRF score descending.
    """
    rrf_scores: Dict[Tuple, float] = {}
    chunk_map: Dict[Tuple, Dict[str, Any]] = {}

    def get_chunk_key(chunk: Dict[str, Any]) -> Tuple:
        return (
            chunk.get("document", ""),
            chunk.get("page", 0),
            chunk.get("chunk_id", 0),
            chunk.get("text", "")[:100],
        )

    # 1. Process FAISS ranks
    for rank, chunk in enumerate(faiss_results, start=1):
        key = get_chunk_key(chunk)
        chunk_map[key] = chunk
        rrf_scores[key] = rrf_scores.get(key, 0.0) + (1.0 / (k + rank))

    # 2. Process BM25 ranks
    for rank, chunk in enumerate(bm25_results, start=1):
        key = get_chunk_key(chunk)
        chunk_map[key] = chunk
        rrf_scores[key] = rrf_scores.get(key, 0.0) + (1.0 / (k + rank))

    # Sort keys by RRF score descending
    sorted_keys = sorted(rrf_scores.keys(), key=lambda key: rrf_scores[key], reverse=True)

    candidates: List[Dict[str, Any]] = []
    for key in sorted_keys[:top_candidates_count]:
        chunk_copy = dict(chunk_map[key])
        chunk_copy["rrf_score"] = rrf_scores[key]
        candidates.append(chunk_copy)

    return candidates


# ==========================================================
# Confidence Score Calculation
# ==========================================================
def calculate_confidence_score(ranked_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates overall RAG retrieval confidence score (0 - 100%) and level (High/Medium/Low).

    Parameters
    ----------
    ranked_chunks : List[Dict[str, Any]]
        Final re-ranked chunks.

    Returns
    -------
    Dict[str, Any]
        Dictionary with 'score' (percentage) and 'level' ('High' | 'Medium' | 'Low').
    """
    if not ranked_chunks:
        return {"score": 0.0, "level": "Low"}

    # Top chunk score carries 60% weight, top 3 average carries 40% weight
    top_score = ranked_chunks[0].get("score", 0.0)
    top_3_scores = [c.get("score", 0.0) for c in ranked_chunks[:3]]
    avg_score = sum(top_3_scores) / len(top_3_scores)

    combined = (top_score * 0.6) + (avg_score * 0.4)
    percentage = round(combined * 100.0, 1)

    if percentage >= 70.0:
        level = "High"
    elif percentage >= 45.0:
        level = "Medium"
    else:
        level = "Low"

    return {
        "score": percentage,
        "level": level,
    }


# ==========================================================
# Central Multi-Document RAG Retrieval
# ==========================================================
def retrieve_advanced_rag_context(
    documents: List[Dict[str, Any]],
    query: str,
    top_k: int = 4,
) -> Dict[str, Any]:
    """
    Orchestrates Multi-Document Advanced RAG retrieval across all loaded PDFs:
    1. Multi-document FAISS & BM25 search
    2. Reciprocal Rank Fusion (RRF)
    3. Cross-Encoder re-ranking
    4. RAG Confidence Score computation
    5. Citation extraction & Prompt context formatting

    Parameters
    ----------
    documents : List[Dict[str, Any]]
        List of document objects stored in st.session_state.
    query : str
        User search query string.
    top_k : int
        Number of final chunks to include in context.

    Returns
    -------
    Dict[str, Any]
        Structured dictionary containing:
        - document_context: Formatted markdown string for LLM system prompt.
        - citations: List of citation objects.
        - confidence: Dict with 'score' and 'level'.
        - chunks_retrieved: Count of chunks.
    """
    empty_result = {
        "document_context": None,
        "citations": [],
        "confidence": {"score": 0.0, "level": "Low"},
        "chunks_retrieved": 0,
    }

    if not documents or not query.strip():
        return empty_result

    try:
        global_faiss_results: List[Dict[str, Any]] = []
        global_bm25_results: List[Dict[str, Any]] = []

        # 1. Multi-Document Search across all loaded files
        for doc in documents:
            filename = doc.get("filename", "Unknown PDF")
            chunks = doc.get("chunks", [])
            faiss_index = doc.get("faiss_index")
            bm25_index = doc.get("bm25_index")

            # Enrich chunk representations with document metadata if missing
            enriched_chunks = []
            for c in chunks:
                c_copy = dict(c)
                c_copy["document"] = filename
                enriched_chunks.append(c_copy)

            if faiss_index is not None:
                faiss_matches = search_similar_chunks(
                    question=query,
                    index=faiss_index,
                    chunks=enriched_chunks,
                    top_k=5,
                )
                global_faiss_results.extend(faiss_matches)

            if bm25_index is not None:
                bm25_matches = search_bm25(
                    question=query,
                    bm25=bm25_index,
                    chunks=enriched_chunks,
                    top_k=5,
                )
                global_bm25_results.extend(bm25_matches)

        if not global_faiss_results and not global_bm25_results:
            return empty_result

        # Sort individual global candidate pools
        global_faiss_results.sort(key=lambda item: item.get("score", 0.0), reverse=True)
        global_bm25_results.sort(key=lambda item: item.get("score", 0.0), reverse=True)

        # 2. Reciprocal Rank Fusion (RRF)
        rrf_candidates = reciprocal_rank_fusion(
            faiss_results=global_faiss_results,
            bm25_results=global_bm25_results,
            k=60,
            top_candidates_count=10,
        )

        # 3. Cross-Encoder Re-ranking
        final_ranked_chunks = rerank_candidates(
            query=query,
            candidates=rrf_candidates,
            top_k=top_k,
        )

        if not final_ranked_chunks:
            return empty_result

        # 4. Confidence Score Calculation
        confidence_info = calculate_confidence_score(final_ranked_chunks)

        # 5. Group by Document & Build Prompt Context + Citations
        doc_grouped: Dict[str, List[Dict[str, Any]]] = {}
        citations: List[Dict[str, Any]] = []
        seen_citation_keys = set()

        for chunk in final_ranked_chunks:
            doc_name = chunk.get("document", "Document")
            if doc_name not in doc_grouped:
                doc_grouped[doc_name] = []
            doc_grouped[doc_name].append(chunk)

            cit_key = (doc_name, chunk.get("page", 1), chunk.get("chunk_id", 0))
            if cit_key not in seen_citation_keys:
                seen_citation_keys.add(cit_key)
                rel_score = round(chunk.get("score", 0.0) * 100.0, 1)
                citations.append(
                    {
                        "document": doc_name,
                        "page": chunk.get("page", 1),
                        "chunk_id": chunk.get("chunk_id", 0),
                        "score": rel_score,
                        "text": chunk.get("text", "")[:250] + "...",
                    }
                )

        context_blocks = []
        for doc_name, chunks in doc_grouped.items():
            chunk_texts = [f"[Page {c.get('page', 1)}]: {c.get('text', '')}" for c in chunks]
            block = f"### Document: {doc_name}\n" + "\n\n".join(chunk_texts)
            context_blocks.append(block)

        document_context = "\n\n------------------------\n\n".join(context_blocks)

        logger.info(
            f"Advanced RAG retrieved {len(final_ranked_chunks)} chunks with {confidence_info['level']} confidence ({confidence_info['score']}%)."
        )

        return {
            "document_context": document_context,
            "citations": citations,
            "confidence": confidence_info,
            "chunks_retrieved": len(final_ranked_chunks),
        }

    except Exception as e:
        logger.error(f"Error in retrieve_advanced_rag_context: {e}")
        return empty_result
