import sqlite3
from pathlib import Path
from datetime import datetime


DB_PATH = Path("data/monitoring/revenue_ai_copilot.db")


def get_connection():
    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            latency_seconds REAL,
            source_count INTEGER,
            feedback INTEGER
        )
        """
    )

    conn.commit()
    conn.close()


def log_interaction(
    question,
    answer,
    latency_seconds,
    source_count
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interactions (
            created_at,
            question,
            answer,
            latency_seconds,
            source_count,
            feedback
        )
        VALUES (?, ?, ?, ?, ?, NULL)
        """,
        (
            datetime.utcnow().isoformat(),
            question,
            answer,
            latency_seconds,
            source_count
        )
    )

    interaction_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return interaction_id


def save_feedback(
    interaction_id,
    feedback
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE interactions
        SET feedback = ?
        WHERE id = ?
        """,
        (
            feedback,
            interaction_id
        )
    )

    conn.commit()
    conn.close()