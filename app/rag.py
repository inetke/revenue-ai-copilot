import os

from openai import OpenAI

from app.semantic_search import semantic_search


RAG_SYSTEM_PROMPT = """
You are Revenue AI Copilot, an assistant specialized in hotel Revenue Management.

Answer the user's question using ONLY the provided context.

Strict requirements:
- Focus specifically on the user's question.
- Use only claims that are directly supported by the provided context.
- Do not use external knowledge.
- Do not infer additional benefits, consequences, or recommendations.
- Do not combine unrelated information simply because it appears in the same retrieved chunk.
- Pay close attention to conditions and scenarios mentioned in the question.
- If the question refers to a specific condition such as low demand, high demand, peak season, or weak occupancy, only include recommendations that explicitly apply to that same condition.
- Ignore information that applies to the opposite or a different scenario.
- Prefer a short and precise answer over a broad answer.
- Cite the source and page for every important claim.
- If the available context does not fully answer the question, clearly say so.
"""


groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def build_rag_context(results):
    context_parts = []

    for result in results:
        context_parts.append(
            f"""
Source: {result["source"]}
Page: {result["page"]}
Text: {result["text"]}
""".strip()
        )

    return "\n\n---\n\n".join(context_parts)


def rag_answer(
    question,
    semantic_documents,
    top_k=5,
    model="llama-3.1-8b-instant"
):
    results = semantic_search(
        question,
        semantic_documents,
        top_k=top_k
    )

    context = build_rag_context(results)

    user_prompt = f"""
Question:
{question}

Context:
{context}

Important:
Use only claims that are directly supported by the context.
Do not add general Revenue Management knowledge.
""".strip()

    response = groq_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": RAG_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0
    )

    return {
        "question": question,
        "answer": response.choices[0].message.content,
        "retrieved_documents": results
    }