import fitz


# ==========================================================
# Read PDF
# ==========================================================
def read_pdf(file):
    """
    Reads a PDF and returns:
    - Full text
    - Total pages
    - PyMuPDF document object
    """

    pdf = fitz.open(
        stream=file.read(),
        filetype="pdf",
    )

    pages = len(pdf)

    return pdf, pages


# ==========================================================
# Split One Page into Chunks
# ==========================================================
def split_page_into_chunks(
    text,
    page_number,
    chunk_size=1000,
    overlap=200,
    start_chunk_id=0,
):
    """
    Creates metadata-rich chunks from a single page.
    """

    chunks = []

    start = 0
    chunk_id = start_chunk_id

    while start < len(text):

        end = start + chunk_size

        chunk_text = text[start:end]

        chunks.append(
            {
                "text": chunk_text,
                "page": page_number,
                "chunk_id": chunk_id,
            }
        )

        chunk_id += 1

        start += chunk_size - overlap

    return chunks, chunk_id


# ==========================================================
# Create Document
# ==========================================================
def create_document(file):
    """
    Reads a PDF and creates a metadata-rich document object.
    """

    pdf, pages = read_pdf(file)

    full_text = ""
    all_chunks = []

    chunk_counter = 0

    for page_index, page in enumerate(pdf):

        page_text = page.get_text()

        full_text += page_text

        page_chunks, chunk_counter = split_page_into_chunks(
            text=page_text,
            page_number=page_index + 1,
            start_chunk_id=chunk_counter,
        )

        all_chunks.extend(page_chunks)

    pdf.close()

    return {
        "filename": file.name,
        "pages": pages,
        "text": full_text,
        "chunks": all_chunks,
        "chunk_count": len(all_chunks),
    }


# ==========================================================
# Statistics
# ==========================================================
def get_document_statistics(documents):
    """
    Returns document statistics.
    """

    total_pages = sum(
        doc["pages"]
        for doc in documents
    )

    total_chunks = sum(
        doc["chunk_count"]
        for doc in documents
    )

    return {
        "files": len(documents),
        "pages": total_pages,
        "chunks": total_chunks,
    }