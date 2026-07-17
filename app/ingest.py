import re
from pathlib import Path
from pypdf import PdfReader


def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk.strip())

        start = end - overlap

    return chunks

def load_documents(pdf_dir="data/raw"):
    documents = []

    pdf_files = list(Path(pdf_dir).glob("*.pdf"))

    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)

        for page_number, page in enumerate(reader.pages):
            text = page.extract_text()

            if text:
                documents.append({
                    "source": pdf_file.name,
                    "page": page_number + 1,
                    "text": clean_text(text)
                })

    return documents

def create_chunks(documents):
    chunks = []

    for doc in documents:
        text_chunks = chunk_text(doc["text"])

        for chunk_id, chunk in enumerate(text_chunks):
            if len(chunk) > 200:
                chunks.append({
                    "source": doc["source"],
                    "page": doc["page"],
                    "chunk_id": chunk_id,
                    "text": chunk
                })

    return chunks