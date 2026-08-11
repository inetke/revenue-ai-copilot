import streamlit as st

from dotenv import load_dotenv

# Load environment variables BEFORE importing app modules
load_dotenv(".env", override=True)

from app.semantic_search import load_semantic_index
from app.rag import rag_answer

st.set_page_config(
    page_title="Revenue AI Copilot",
    page_icon="🏨",
    layout="centered"
)


@st.cache_resource
def load_index():
    return load_semantic_index()


semantic_documents = load_index()


st.title("Revenue AI Copilot")

st.write(
    "Ask questions about hotel Revenue Management "
    "using the available specialized knowledge base."
)


question = st.text_area(
    "Ask a Revenue Management question",
    placeholder="e.g. How can hotels improve revenue during periods of low demand?"
)


if st.button("Ask Revenue AI Copilot"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching the knowledge base..."):
            result = rag_answer(
                question,
                semantic_documents,
                top_k=5
            )

        st.subheader("Answer")
        st.write(result["answer"])

        st.subheader("Sources")

        for document in result["retrieved_documents"]:
            st.write(
                f'**{document["source"]}** — '
                f'page {document["page"]} '
                f'(similarity: {document["score"]:.3f})'
            )