import streamlit as st
import time

from dotenv import load_dotenv

# Load environment variables before importing app modules
load_dotenv(".env", override=True)

from app.semantic_search import load_semantic_index
from app.rag import rag_answer

from app.monitoring import (
    init_db,
    log_interaction,
    save_feedback
)

st.set_page_config(
    page_title="Revenue AI Copilot",
    page_icon="🏨",
    layout="centered"
)


@st.cache_resource
def load_index():
    return load_semantic_index()


semantic_documents = load_index()

init_db()

with st.sidebar:
    st.title("Revenue AI Copilot")

    st.markdown(
        """
        AI-powered assistant specialized in **Hotel Revenue Management**.

        ### Knowledge Base
        The assistant uses a curated collection of Revenue Management documents covering:

        - Pricing strategies
        - Demand forecasting
        - Market segmentation
        - Distribution
        - Revenue KPIs
        - Revenue optimization

        ### How it works

        **Semantic Search**  
        Finds the most relevant information in the knowledge base.

        **RAG**  
        Provides retrieved context to the language model.

        **Grounded Generation**  
        Generates answers based only on the retrieved sources.
        """
    )

    st.divider()

    if st.button(
        "Clear conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()


# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("Revenue AI Copilot")

st.caption(
    "AI assistant for hotel Revenue Management, powered by a specialized knowledge base."
)

if not st.session_state.messages:
    st.markdown("#### Try asking")

    col1, col2 = st.columns(2)

    with col1:
        example_1 = st.button(
            "What is RevPAR?",
            use_container_width=True
        )

        example_2 = st.button(
            "How does dynamic pricing work?",
            use_container_width=True
        )

    with col2:
        example_3 = st.button(
            "How can hotels increase revenue?",
            use_container_width=True
        )

        example_4 = st.button(
            "What is market segmentation?",
            use_container_width=True
        )

# Show previous messages
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and "sources" in message:
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.markdown(
                        f'**{source["source"]}** — '
                        f'page {source["page"]} '
                        f'· similarity {source["score"]:.3f}'
                    )

            if "interaction_id" in message:
                feedback_col1, feedback_col2 = st.columns(2)

                with feedback_col1:
                    if st.button(
                        "👍 Helpful",
                        key=f"history_helpful_{message['interaction_id']}_{i}"
                    ):
                        save_feedback(
                            message["interaction_id"],
                            1
                        )
                        st.success("Thanks for your feedback.")

                with feedback_col2:
                    if st.button(
                        "👎 Not helpful",
                        key=f"history_not_helpful_{message['interaction_id']}_{i}"
                    ):
                        save_feedback(
                            message["interaction_id"],
                            -1
                        )
                        st.success("Thanks for your feedback.")

# User input
question = st.chat_input(
    "Ask a Revenue Management question..."
)

if not st.session_state.messages:
    if example_1:
        question = "What is RevPAR?"
    elif example_2:
        question = "How does dynamic pricing work?"
    elif example_3:
        question = "How can hotels increase revenue?"
    elif example_4:
        question = "What is market segmentation?"

if question:
    # Save + display user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Searching the knowledge base..."):
            start_time = time.perf_counter()

            result = rag_answer(
                question,
                semantic_documents,
                top_k=5
            )

            latency_seconds = (
                time.perf_counter() - start_time
            )

        st.markdown(result["answer"])

        sources = [
            {
                "source": document["source"],
                "page": document["page"],
                "score": document["score"]
            }
            for document in result["retrieved_documents"]
        ]

        interaction_id = log_interaction(
            question=question,
            answer=result["answer"],
            latency_seconds=latency_seconds,
            source_count=len(sources)
        )

        with st.expander("Sources"):
            for source in sources:
                st.markdown(
                    f'**{source["source"]}** — '
                    f'page {source["page"]} '
                    f'· similarity {source["score"]:.3f}'
                )

        feedback_col1, feedback_col2 = st.columns(2)

        with feedback_col1:
            if st.button(
                "👍 Helpful",
                key=f"helpful_{interaction_id}"
            ):
                save_feedback(
                    interaction_id,
                    1
                )
                st.success("Thanks for your feedback.")

        with feedback_col2:
            if st.button(
                "👎 Not helpful",
                key=f"not_helpful_{interaction_id}"
            ):
                save_feedback(
                    interaction_id,
                    -1
                )
                st.success("Thanks for your feedback.")        

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": sources,
        "interaction_id": interaction_id
    })

    st.rerun()