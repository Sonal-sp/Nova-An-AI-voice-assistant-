from rank_bm25 import BM25Okapi


def build_bm25_index(chunks):

    tokenized = [
        chunk["text"].lower().split()
        for chunk in chunks
    ]

    return BM25Okapi(tokenized)


def search_bm25(
    question,
    bm25,
    chunks,
    top_k=3,
):

    scores = bm25.get_scores(
        question.lower().split()
    )

    ranked = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True,
    )[:top_k]

    return [
        chunks[i]
        for i in ranked
    ]