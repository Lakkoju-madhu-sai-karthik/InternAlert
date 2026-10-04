import sqlite3
import os


# Always use the database in the project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "internalert.db")


def add_internship():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    title = "Software Developer Intern"
    company = "TALENTBRAINY"
    location = "Pan India, Tamil Nadu"
    stipend = "₹10,000/month"
    duration = "6 Months"
    skills = "Full Stack Developer, Python, Java"
    deadline = "25 Oct 2026"
    apply_url = "https://internship.aicte-india.org/internships/1-INTERNSHIP_17910209776ac0cfb158fec"
    description = (
        "Software Developer Intern opportunity at TALENTBRAINY. "
        "This is a 6-month full-time remote internship open across India, "
        "with the cohort beginning on 1 November 2026. "
        "There are 30 positions available. "
        "Selected interns may receive academic credit (26 credits). "
        "Applications are open until 25 October 2026."
    )

    # Check if internship already exists
    cursor.execute("""
        SELECT id
        FROM internships
        WHERE apply_url = ?
    """, (apply_url,))

    existing = cursor.fetchone()

    if existing:

        print("⚠️ This internship is already in the database.")

        connection.close()
        return

    # Add internship
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
    add_internship()