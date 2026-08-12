import sqlite3
import pandas as pd
import streamlit as st

from pathlib import Path


DB_PATH = Path("data/monitoring/revenue_ai_copilot.db")


st.set_page_config(
    page_title="Revenue AI Copilot Monitoring",
    page_icon="📊",
    layout="wide"
)


st.title("Revenue AI Copilot — Monitoring")

st.caption(
    "Application usage, performance, and user feedback."
)


@st.cache_data(ttl=30)
def load_data():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT
            id,
            created_at,
            question,
            latency_seconds,
            source_count,
            feedback
        FROM interactions
        ORDER BY created_at
        """,
        conn
    )

    conn.close()

    return df


df = load_data()


if df.empty:
    st.info("No monitoring data available yet.")
    st.stop()


df["created_at"] = pd.to_datetime(df["created_at"])


total_questions = len(df)
avg_latency = df["latency_seconds"].mean()

feedback_count = df["feedback"].notna().sum()

positive_feedback = (
    (df["feedback"] == 1).sum()
)

negative_feedback = (
    (df["feedback"] == -1).sum()
)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Questions",
    total_questions
)

col2.metric(
    "Average Latency",
    f"{avg_latency:.2f}s"
)

col3.metric(
    "Feedback Responses",
    feedback_count
)

col4.metric(
    "Positive Feedback",
    positive_feedback
)

st.divider()

st.header("Monitoring Dashboard")


# --------------------------------------------------
# 1. Questions over time
# --------------------------------------------------

st.subheader("1. Questions Over Time")

questions_over_time = (
    df.set_index("created_at")
    .resample("D")
    .size()
    .rename("questions")
)

st.line_chart(questions_over_time)


# --------------------------------------------------
# 2. Latency over time
# --------------------------------------------------

st.subheader("2. Response Latency")

latency_over_time = (
    df[["created_at", "latency_seconds"]]
    .set_index("created_at")
)

st.line_chart(latency_over_time)


# --------------------------------------------------
# 3. Feedback distribution
# --------------------------------------------------

st.subheader("3. User Feedback")

feedback_labels = df["feedback"].map({
    1: "Helpful",
    -1: "Not Helpful"
})

feedback_distribution = (
    feedback_labels
    .dropna()
    .value_counts()
)

if not feedback_distribution.empty:
    st.bar_chart(feedback_distribution)
else:
    st.info("No user feedback available yet.")


# --------------------------------------------------
# 4. Retrieved sources per question
# --------------------------------------------------

st.subheader("4. Retrieved Sources")

sources_per_question = (
    df[["id", "source_count"]]
    .set_index("id")
)

st.bar_chart(sources_per_question)


# --------------------------------------------------
# 5. Latency Distribution
# --------------------------------------------------

st.subheader("5. Latency Distribution")

latency_bins = pd.cut(
    df["latency_seconds"],
    bins=5
)

latency_distribution = (
    latency_bins
    .value_counts()
    .sort_index()
)

latency_distribution.index = (
    latency_distribution.index.astype(str)
)

st.bar_chart(latency_distribution)