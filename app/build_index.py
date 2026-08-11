import json
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables before importing modules
# that create API clients
load_dotenv(".env")

from app.ingest import load_documents, create_chunks
from app.semantic_search import build_semantic_documents


INDEX_PATH = Path("data/processed/semantic_index.json")


def build_index():
    source_documents = load_documents("data/raw")
    chunks = create_chunks(source_documents)

    evaluation_documents = []

    for global_id, chunk in enumerate(chunks):
        evaluation_documents.append({
            "id": global_id,
            "source": chunk["source"],
            "page": chunk["page"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"]
        })

    semantic_documents = build_semantic_documents(
        evaluation_documents
    )

    INDEX_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        INDEX_PATH,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            semantic_documents,
            f,
            ensure_ascii=False
        )

    print(
        f"Semantic index saved to {INDEX_PATH}"
    )

    print(
        f"Documents indexed: {len(semantic_documents)}"
    )


if __name__ == "__main__":
    build_index()