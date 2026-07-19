import fitz


# ==========================================================
# Read PDF
# ==========================================================
def read_pdf(file):
    """
    Extract all text from a PDF.
    """

    document = fitz.open(
        stream=file.read(),
        filetype="pdf",
    )

    text = ""

    for page in document:

        text += page.get_text()

    pages = len(document)

    document.close()

    return text, pages


# ==========================================================
# Split into Chunks
# ==========================================================
def split_text_into_chunks(
    text,
    chunk_size=1000,
    overlap=200,
):
    """
    Split text into overlapping chunks.
    """

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
    """
    Creates a document dictionary from an uploaded PDF.
    """

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
# Statistics
# ==========================================================
def get_document_statistics(documents):
    """
    Returns overall document statistics.
    """

    total_pages = 0
    total_chunks = 0

    for document in documents:

        total_pages += document["pages"]

        total_chunks += document["chunk_count"]

    return {

        "files": len(documents),

        "pages": total_pages,

        "chunks": total_chunks,

    }