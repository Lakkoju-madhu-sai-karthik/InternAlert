import sqlite3


DATABASE_NAME = "internalert.db"


connection = sqlite3.connect(DATABASE_NAME)

cursor = connection.cursor()

cursor.execute("""
    SELECT
        id,
        title,
        company,
        location,
        stipend,
        deadline
    FROM internships
""")

internships = cursor.fetchall()

connection.close()


for internship in internships:

    print("------------------------------")

    print("ID:", internship[0])
    print("Title:", internship[1])
    print("Company:", internship[2])
    print("Location:", internship[3])
    print("Stipend:", internship[4])
    print("Deadline:", internship[5])