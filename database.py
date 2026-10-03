import sqlite3

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "internalert.db")

def create_database():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Internships table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            stipend TEXT,
            duration TEXT,
            skills TEXT,
            deadline TEXT,
            apply_url TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Saved internships table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            internship_id INTEGER NOT NULL,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, internship_id),
            FOREIGN KEY (internship_id)
                REFERENCES internships(id)
                ON DELETE CASCADE
        )
    """)

    # Users / Profiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            degree TEXT,
            skills TEXT,
            location TEXT,
            remote_preference TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

    print("Database created successfully!")


if __name__ == "__main__":
    create_database()