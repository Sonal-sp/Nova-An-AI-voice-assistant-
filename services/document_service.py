import fitz
import re 
def read_pdf(file):
    document =fitz.open(stream=file.read(),filetype="pdf")
    text=""
    for page in document:
        text+=page.get_text()
    document.close()
    return text

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

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks

def find_relevant_chunk(question, chunks):
    """
    Find the chunk that best matches the user's question.
    """

    words = re.findall(r"\w+", question.lower())

    best_chunk = ""
    highest_score = 0

    for chunk in chunks:

        score = 0
        chunk_lower = chunk.lower()

        for word in words:
            score += chunk_lower.count(word)

        if score > highest_score:
            highest_score = score
            best_chunk = chunk

    return best_chunk