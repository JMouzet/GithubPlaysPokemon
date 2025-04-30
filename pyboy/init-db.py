import sqlite3

with sqlite3.connect("/shared/db/inputs.db") as conn:
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Commit the changes and close the connection
    conn.commit()
