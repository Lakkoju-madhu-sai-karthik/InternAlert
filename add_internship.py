import sqlite3
import os


# Always use the database in the project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "internalert.db")


def add_internship():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    title = "Python Internship"
    company = "Learntricks Edutech"
    location = "Work From Home"
    stipend = "₹12,000 - ₹15,000/month"
    duration = "2 Months"
    skills = "Python, Django, HTML, CSS, JavaScript, React, Angular, jQuery, PHP, Node.js"
    deadline = "17 Oct 2026"
    apply_url = "https://unstop.com/internships/python-internship-unstop-tech-fair-2025-learntricks-edutech-1765719"
    description = (
        "Python Internship at Learntricks Edutech. "
        "This is a 2-month part-time work-from-home internship with "
        "5 working days per week. The stipend is ₹12,000 to ₹15,000 per month. "
        "Interns may work with Python, Django, HTML, CSS, JavaScript and "
        "other frontend/backend technologies. College-pursuing students can apply."
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