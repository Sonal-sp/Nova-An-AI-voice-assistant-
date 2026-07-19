import fitz
import re


# ==========================================================
# Read PDF
# ==========================================================
def read_pdf(file):
    """
    Reads a PDF and returns:
    - full text
    - total pages
    """

    document = fitz.open(
        stream=file.read(),
        filetype="pdf",
    )

    text = ""

    for page in document:

        text += page.get_text()

    total_pages = len(document)

    document.close()

    return text, total_pages


# ==========================================================
# Split Text into Chunks
# ==========================================================
def split_text_into_chunks(
    text,
    chunk_size=1000,
    overlap=200,
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start += chunk_size - overlap

    return chunks


# ==========================================================
# Create Document Object
# ==========================================================
def create_document(file):

    text, pages = read_pdf(file)

    chunks = split_text_into_chunks(text)

    return {

        "filename": file.name,

        "pages": pages,

        "text": text,

        "chunks": chunks,

        "chunk_count": len(chunks),

    }


# ==========================================================
# Search One Document
# ==========================================================
def score_chunk(
    question,
    chunk,
):

    words = re.findall(
        r"\w+",
        question.lower(),
    )

    score = 0

    chunk_lower = chunk.lower()

    for word in words:

        score += chunk_lower.count(word)

    return score


# ==========================================================
# Search Across All Documents
# ==========================================================
def find_relevant_document_chunk(
    question,
    documents,
):

    best_document = None
    best_chunk = ""
    highest_score = 0

    for document in documents:

        for chunk in document["chunks"]:

            score = score_chunk(
                question,
                chunk,
            )

            if score > highest_score:

                highest_score = score

                best_chunk = chunk

                best_document = document

    return {

        "document": best_document,

        "chunk": best_chunk,

        "score": highest_score,

    }


# ==========================================================
# Statistics
# ==========================================================
def get_document_statistics(
    documents,
):

    total_files = len(documents)

    total_pages = sum(
        doc["pages"]
        for doc in documents
    )

    total_chunks = sum(
        doc["chunk_count"]
        for doc in documents
    )

    return {

        "files": total_files,

        "pages": total_pages,

        "chunks": total_chunks,

    }