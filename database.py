
import sqlite3


def create_feedback_table(database_path="feedback.db"):
    """Create the feedback table if it does not already exist."""

    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY,
                review TEXT,
                label TEXT,
                score REAL,
                theme TEXT
            )
            """
        )
        connection.commit()
        

def save_feedback(review, label, score, theme, database_path="feedback.db"):
    """Save the feedback to the database."""

    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            INSERT INTO feedback (review, label, score, theme)
            VALUES (?, ?, ?, ?)
            """,
            (review, label, score, theme),
        )
        connection.commit()
    
        
def load_feedback(database_path="feedback.db"):
    """Load all feedback from the database."""

    with sqlite3.connect(database_path) as connection:
        cursor = connection.execute(
            """
            SELECT review, label, score, theme FROM feedback
            """
        )
        feedback_list = cursor.fetchall()
        return feedback_list
