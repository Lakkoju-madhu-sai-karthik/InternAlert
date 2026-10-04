import sqlite3
import os


# Always use the database in the project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "internalert.db")


def add_internship():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    title = "Business Development Intern"
    company = "SKILL VEDANTH EDTECH SOLUTIONS PRIVATE LIMITED"
    location = "Bengaluru, Karnataka"
    stipend = "₹18,000/month"
    duration = "6 Months"
    skills = "Business Development,Communication"
    deadline = "30 Oct 2026"
    apply_url = "https://internship.aicte-india.org/internships/1-INTERNSHIP_17911224296ac25bfd12c31"
    description = (
        "Business Development Intern at SKILL VEDANTH EDTECH SOLUTIONS PRIVATE LIMITED. "
        "This is a 6-month full-time onsite internship in Bengaluru, Karnataka. "
        "The internship starts on 15 November 2026. "
        "There are 45 positions available and selected interns may receive 26 academic credits. "
        "Monthly stipend is ₹18,000. Applications are open until 30 October 2026."
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