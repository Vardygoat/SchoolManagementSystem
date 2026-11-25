import sqlite3
from db_config import DB_PATH

TARGET_STUDENTS = 50
TARGET_TEACHERS = 10
TARGET_COURSES = 10

TEACHERS = [
    ("Olivia", "Martin", "2018-08-12", "olivia.martin@school.org", "555-0101", "Mathematics"),
    ("Liam", "Walker", "2019-03-21", "liam.walker@school.org", "555-0102", "Physics"),
    ("Emma", "Thompson", "2017-11-05", "emma.thompson@school.org", "555-0103", "English"),
    ("Noah", "Perez", "2020-01-18", "noah.perez@school.org", "555-0104", "Computer Science"),
    ("Ava", "Evans", "2016-06-20", "ava.evans@school.org", "555-0105", "Biology"),
    ("Ethan", "Murphy", "2015-02-14", "ethan.murphy@school.org", "555-0106", "History"),
    ("Sophia", "Carter", "2018-09-30", "sophia.carter@school.org", "555-0107", "Chemistry"),
    ("Mason", "Ramirez", "2019-10-10", "mason.ramirez@school.org", "555-0108", "Geography"),
    ("Isabella", "Brooks", "2020-05-27", "isabella.brooks@school.org", "555-0109", "Art"),
    ("Lucas", "Nguyen", "2017-04-06", "lucas.nguyen@school.org", "555-0110", "Physical Education"),
]

COURSES = [
    ("Algebra I", "Fundamentals of algebra and equation solving.", 4),
    ("Biology Basics", "Introduction to cell biology, ecology, and genetics.", 3),
    ("Creative Writing", "Develop narrative skills, essays, and poetry.", 2),
    ("Computer Science I", "Programming fundamentals and problem solving.", 4),
    ("World History", "Survey of major historical civilizations and events.", 3),
    ("Chemistry", "Foundational chemistry principles and laboratory work.", 4),
    ("Physics", "Mechanics, motion, forces, and energy.", 4),
    ("Geography", "Earth systems, maps, and human-environment interaction.", 2),
    ("Art Studio", "Drawing, painting, and design fundamentals.", 2),
    ("Health & Fitness", "Exercise, wellness, and team sports.", 1),
]

STUDENTS = [
    ("Alexander", "Smith", "2008-03-15", "alexander.smith@student.school.org", "555-1001", "1 Oak Street", "Springfield", "10001"),
    ("Mia", "Johnson", "2009-07-24", "mia.johnson@student.school.org", "555-1002", "5 Pine Avenue", "Rivertown", "10002"),
    ("Ethan", "Williams", "2008-01-08", "ethan.williams@student.school.org", "555-1003", "12 Maple Road", "Laketown", "10003"),
    ("Harper", "Jones", "2007-11-30", "harper.jones@student.school.org", "555-1004", "23 Willow Lane", "Hillview", "10004"),
    ("Aiden", "Brown", "2008-10-12", "aiden.brown@student.school.org", "555-1005", "34 Cedar Street", "Brookfield", "10005"),
    ("Abigail", "Davis", "2009-02-17", "abigail.davis@student.school.org", "555-1006", "41 Birch Boulevard", "Mapleton", "10006"),
    ("Logan", "Miller", "2008-06-29", "logan.miller@student.school.org", "555-1007", "54 Elm Street", "Riverside", "10007"),
    ("Charlotte", "Wilson", "2009-12-03", "charlotte.wilson@student.school.org", "555-1008", "61 Aspen Court", "Sunnyvale", "10008"),
    ("Jackson", "Moore", "2007-09-19", "jackson.moore@student.school.org", "555-1009", "72 Poplar Drive", "Fairview", "10009"),
    ("Amelia", "Taylor", "2008-04-22", "amelia.taylor@student.school.org", "555-1010", "83 Cherry Street", "Westfield", "10010"),
    ("Lucas", "Anderson", "2009-08-13", "lucas.anderson@student.school.org", "555-1011", "94 Spruce Avenue", "Eastwood", "10011"),
    ("Evelyn", "Thomas", "2007-05-20", "evelyn.thomas@student.school.org", "555-1012", "105 Hickory Lane", "Brookwood", "10012"),
    ("Mason", "Jackson", "2008-02-07", "mason.jackson@student.school.org", "555-1013", "116 Walnut Road", "Northview", "10013"),
    ("Ella", "White", "2009-11-28", "ella.white@student.school.org", "555-1014", "127 Chestnut Boulevard", "Crestwood", "10014"),
    ("Avery", "Harris", "2008-12-08", "avery.harris@student.school.org", "555-1015", "138 Sycamore Street", "Southgate", "10015"),
    ("Oliver", "Martin", "2009-03-05", "oliver.martin@student.school.org", "555-1016", "149 Magnolia Drive", "Lakeside", "10016"),
    ("Sofia", "Thompson", "2007-10-11", "sofia.thompson@student.school.org", "555-1017", "150 Redwood Court", "Garden City", "10017"),
    ("Elijah", "Garcia", "2008-01-31", "elijah.garcia@student.school.org", "555-1018", "161 Palm Street", "Hillcrest", "10018"),
    ("Aria", "Martinez", "2009-06-27", "aria.martinez@student.school.org", "555-1019", "172 Sequoia Lane", "Oakwood", "10019"),
    ("Benjamin", "Robinson", "2008-11-09", "benjamin.robinson@student.school.org", "555-1020", "183 Dogwood Avenue", "Riverview", "10020"),
    ("Luna", "Clark", "2007-04-16", "luna.clark@student.school.org", "555-1021", "194 Juniper Street", "Parkside", "10021"),
    ("Henry", "Rodriguez", "2009-09-23", "henry.rodriguez@student.school.org", "555-1022", "205 Cedar Court", "Meadowbrook", "10022"),
    ("Chloe", "Lewis", "2008-07-14", "chloe.lewis@student.school.org", "555-1023", "216 Fir Street", "Valleyview", "10023"),
    ("Sebastian", "Lee", "2007-12-02", "sebastian.lee@student.school.org", "555-1024", "227 Laurel Avenue", "Westlake", "10024"),
    ("Mila", "Walker", "2009-05-06", "mila.walker@student.school.org", "555-1025", "238 Maple Lane", "Cedar Grove", "10025"),
    ("Jack", "Hall", "2008-08-18", "jack.hall@student.school.org", "555-1026", "249 Birch Court", "Elmwood", "10026"),
    ("Grace", "Allen", "2007-02-12", "grace.allen@student.school.org", "555-1027", "250 Pine Street", "Harmony", "10027"),
    ("Owen", "Young", "2009-01-28", "owen.young@student.school.org", "555-1028", "261 Oak Boulevard", "Park Hill", "10028"),
    ("Scarlett", "Hernandez", "2008-03-09", "scarlett.hernandez@student.school.org", "555-1029", "272 Cedar Drive", "Pinecrest", "10029"),
    ("Wyatt", "King", "2009-10-30", "wyatt.king@student.school.org", "555-1030", "283 Willow Street", "Forestville", "10030"),
    ("Zoe", "Wright", "2007-06-11", "zoe.wright@student.school.org", "555-1031", "294 Elm Avenue", "Shoreline", "10031"),
    ("Caleb", "Lopez", "2008-02-26", "caleb.lopez@student.school.org", "555-1032", "305 Maple Court", "Brookside", "10032"),
    ("Nora", "Hill", "2009-11-16", "nora.hill@student.school.org", "555-1033", "316 Chestnut Road", "Linden", "10033"),
    ("Luke", "Scott", "2008-04-04", "luke.scott@student.school.org", "555-1034", "327 Pine Lane", "Shady Oaks", "10034"),
    ("Lily", "Green", "2007-08-27", "lily.green@student.school.org", "555-1035", "338 Cedar Avenue", "Riverbend", "10035"),
    ("Nathan", "Adams", "2009-05-19", "nathan.adams@student.school.org", "555-1036", "349 Birch Street", "Meadow Lane", "10036"),
    ("Hannah", "Baker", "2008-09-02", "hannah.baker@student.school.org", "555-1037", "350 Oak Drive", "Willow Creek", "10037"),
    ("Isaac", "Nelson", "2007-01-12", "isaac.nelson@student.school.org", "555-1038", "361 Maple Boulevard", "Highland", "10038"),
    ("Zara", "Carter", "2009-03-25", "zara.carter@student.school.org", "555-1039", "372 Pine Court", "Coveview", "10039"),
    ("Ryan", "Mitchell", "2008-12-07", "ryan.mitchell@student.school.org", "555-1040", "383 Spruce Street", "Fairfield", "10040"),
    ("Leah", "Perez", "2007-07-18", "leah.perez@student.school.org", "555-1041", "394 Aspen Avenue", "Creekside", "10041"),
    ("Hunter", "Roberts", "2009-02-03", "hunter.roberts@student.school.org", "555-1042", "405 Redwood Road", "Greenfield", "10042"),
    ("Riley", "Turner", "2008-06-22", "riley.turner@student.school.org", "555-1043", "416 Cherry Drive", "Lakeview", "10043"),
    ("Madison", "Phillips", "2009-10-14", "madison.phillips@student.school.org", "555-1044", "427 Oak Street", "Stonebridge", "10044"),
    ("David", "Campbell", "2008-11-26", "david.campbell@student.school.org", "555-1045", "438 Birch Lane", "Ridgefield", "10045"),
    ("Victoria", "Parker", "2007-05-03", "victoria.parker@student.school.org", "555-1046", "449 Maple Avenue", "Sunnyside", "10046"),
    ("Wyatt", "Evans", "2009-09-11", "wyatt.evans2@student.school.org", "555-1047", "450 Willow Court", "Hillside", "10047"),
    ("Ella", "Edwards", "2008-01-19", "ella.edwards@student.school.org", "555-1048", "461 Oak Road", "Pleasantville", "10048"),
    ("Samuel", "Collins", "2009-04-29", "samuel.collins@student.school.org", "555-1049", "472 Pine Street", "Valley Grove", "10049"),
    ("Grace", "Stewart", "2007-12-21", "grace.stewart@student.school.org", "555-1050", "483 Cedar Lane", "Hillbrook", "10050"),
]

REGISTRATION_PLAN = [2, 3, 2, 3, 2, 3, 2, 3, 2, 3]


def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def get_count(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0]


def seed_teachers(cursor):
    current = get_count(cursor, 'Teachers')
    if current >= TARGET_TEACHERS:
        print(f'Teachers already >= {TARGET_TEACHERS} ({current})')
        return

    to_add = TARGET_TEACHERS - current
    print(f'Adding {to_add} teacher(s) to reach {TARGET_TEACHERS}')
    for teacher in TEACHERS[current:TARGET_TEACHERS]:
        cursor.execute(
            "INSERT OR IGNORE INTO Teachers (first_name, last_name, hire_date, email, phone, department) VALUES (?, ?, ?, ?, ?, ?)",
            teacher
        )


def seed_courses(cursor):
    current = get_count(cursor, 'Courses')
    if current >= TARGET_COURSES:
        print(f'Courses already >= {TARGET_COURSES} ({current})')
        return

    teacher_ids = [row[0] for row in cursor.execute("SELECT teacher_id FROM Teachers ORDER BY teacher_id").fetchall()]
    if not teacher_ids:
        raise RuntimeError('No teachers available for course assignment')

    print(f'Adding {TARGET_COURSES - current} course(s) to reach {TARGET_COURSES}')
    for idx, course in enumerate(COURSES[current:TARGET_COURSES]):
        teacher_id = teacher_ids[idx % len(teacher_ids)]
        cursor.execute(
            "INSERT INTO Courses (course_name, description, credits, teacher_id) VALUES (?, ?, ?, ?)",
            (course[0], course[1], course[2], teacher_id)
        )


def seed_students(cursor):
    current = get_count(cursor, 'Students')
    if current >= TARGET_STUDENTS:
        print(f'Students already >= {TARGET_STUDENTS} ({current})')
        return

    print(f'Adding {TARGET_STUDENTS - current} student(s) to reach {TARGET_STUDENTS}')
    for student in STUDENTS[current:TARGET_STUDENTS]:
        cursor.execute(
            "INSERT OR IGNORE INTO Students (first_name, last_name, date_of_birth, email, phone, address, town, post_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            student
        )


def seed_registrations(cursor):
    student_ids = [row[0] for row in cursor.execute("SELECT student_id FROM Students ORDER BY student_id").fetchall()]
    course_ids = [row[0] for row in cursor.execute("SELECT course_id FROM Courses ORDER BY course_id").fetchall()]

    if not student_ids or not course_ids:
        print('Skipping registrations because students or courses are missing.')
        return

    existing = set(cursor.execute("SELECT student_id, course_id FROM Registrations").fetchall())
    inserts = 0
    for i, student_id in enumerate(student_ids):
        plan = REGISTRATION_PLAN[i % len(REGISTRATION_PLAN)]
        for offset in range(plan):
            course_id = course_ids[(i + offset) % len(course_ids)]
            if (student_id, course_id) in existing:
                continue
            grade = 70 + ((student_id + course_id) % 31)
            cursor.execute(
                "INSERT OR IGNORE INTO Registrations (student_id, course_id, grade) VALUES (?, ?, ?)",
                (student_id, course_id, grade)
            )
            inserts += 1
    print(f'Added {inserts} registration(s)')


def main():
    connection = connect_db()
    cursor = connection.cursor()
    try:
        seed_teachers(cursor)
        seed_courses(cursor)
        seed_students(cursor)
        seed_registrations(cursor)
        connection.commit()
        print('Database seeding complete.')

        counts = {table: get_count(cursor, table) for table in ['Students', 'Teachers', 'Courses', 'Registrations']}
        print('Final counts:', counts)
    except Exception as error:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    main()
