import os
import numpy as np
import json
from pathlib import Path

from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity


EMBEDDING_MODEL = "text-embedding-3-small"

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def get_embeddings_batch(texts, model=EMBEDDING_MODEL):
    response = openai_client.embeddings.create(
        model=model,
        input=texts
    )

    return [
        item.embedding
        for item in response.data
    ]


def embed_query(query, model=EMBEDDING_MODEL):
    response = openai_client.embeddings.create(
        model=model,
        input=query
    )

    return response.data[0].embedding


def build_semantic_documents(documents, batch_size=50):
    semantic_documents = []

    for start in range(0, len(documents), batch_size):
        batch = documents[start:start + batch_size]

        texts = [
            document["text"]
            for document in batch
        ]

        embeddings = get_embeddings_batch(texts)

        for document, embedding in zip(batch, embeddings):
            semantic_documents.append({
                **document,
                "embedding": embedding
            })

    return semantic_documents


def semantic_search(
    query,
    semantic_documents,
    top_k=5
):
    query_embedding = embed_query(query)

    document_embeddings = np.array([
        document["embedding"]
        for document in semantic_documents
    ])

    similarities = cosine_similarity(
        [query_embedding],
        document_embeddings
    )[0]

    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []

    for index in top_indices:
        document = semantic_documents[index].copy()

        document["score"] = float(
            similarities[index]
        )

        results.append(document)

    return results

def load_semantic_index(
    index_path="data/processed/semantic_index.json"
):
    path = Path(index_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Semantic index not found: {index_path}"
        )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)