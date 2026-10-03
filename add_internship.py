import sqlite3


DATABASE_NAME = "internalert.db"


def add_internship():

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
        "Software Developer Intern",
        "TALENTBRAINY",
        "Pan India, Tamil Nadu",
        "₹10,000/month",
        "6 Months",
        "Full Stack Developer,Python,Java",
        "25 Oct 2026",
        "https://internship.aicte-india.org/internships/1-INTERNSHIP_17910209776ac0cfb158fec",
        "Software Developer Intern opportunity at TALENTBRAINY. This is a 6-month full-time remote internship open across India, with the cohort beginning on 1 November 2026. There are 30 positions available. Selected interns may receive academic credit (26 credits). Applications are open until 25 October 2026."
    ))

    connection.commit()

    connection.close()

    print("Internship added successfully!")


if __name__ == "__main__":
    add_internship()