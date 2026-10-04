import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "internalert.db")


def add_internship(
    title,
    company,
    location,
    stipend,
    duration,
    skills,
    deadline,
    apply_url,
    description
):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO internships
        (
            title,
            company,
            location,
            stipend,
            duration,
            skills,
            deadline,
            apply_url,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        company,
        location,
        stipend,
        duration,
        skills,
        deadline,
        apply_url,
        description
    ))

    connection.commit()
    connection.close()

    print("✅ Internship added successfully!")


if __name__ == "__main__":

    add_internship(
        title="Sample Data Analyst Internship",
        company="Example Company",
        location="Remote",
        stipend="₹10,000/month",
        duration="3 Months",
        skills="Python, SQL, Excel",
        deadline="30-11-2026",
        apply_url="https://example.com",
        description="Sample internship for testing InternAlert."
    )