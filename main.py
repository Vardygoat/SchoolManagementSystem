# main.py
import sys
import tkinter as tk
from datetime import datetime

from sqlalchemy import false
from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.registration import Registration

login = True
while login:
    acc = input("login: ")
    pwd = input("password: ")
    if acc != "admin" or pwd != "admin123":
        print("Invalid password or username. Try again.")    
    elif acc == "admin" and pwd == "admin123":
        print("Login successful. Welcome, admin!")
        break

def print_table(header, data):
    # Utility function to print data in a tabular format in the console
    if not data:
        print("  No records found.")
        return
    # Calculate column widths
    col_widths = [len(str(h)) for h in header]
    for row in data:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    # Create a separator line based on column widths
    separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    # Print header
    print(separator)
    header_row = "| " + " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(header)) + " |"
    print(header_row)
    print(separator)
    # Print data rows
    for row in data:
        row_str = "| " + " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)) + " |"
        print(row_str)
    print(separator)


def get_date_input(prompt):
    # Utility function to get a date in YYYY-MM-DD format
    while True:
        date_str = input(prompt).strip()
        if not date_str:
            return None
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("  Invalid date format. Please use YYYY-MM-DD.")


def get_int_input(prompt, min_val=None, max_val=None):
    #function to get an integer input with optional min and max validation
    while True:
        try:
            val = int(input(prompt).strip())
            if min_val is not None and val < min_val:
                print(f"  Value must be >= {min_val}")
                continue
            if max_val is not None and val > max_val:
                print(f"  Value must be <= {max_val}")
                continue
            return val
        except ValueError:
            print("  Invalid input. Please enter an integer.")


def get_float_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = float(input(prompt).strip())
            if min_val is not None and val < min_val:
                print(f"  Value must be >= {min_val}")
                continue
            if max_val is not None and val > max_val:
                print(f"  Value must be <= {max_val}")
                continue
            return val
        except ValueError:
            print("  Invalid input. Please enter a number.")


def get_nonempty_string(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("  This field cannot be empty.")


# ===========Students 
def manage_students():
    while True:
        print("\n=== Manage Students ===")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by Name")
        print("4. Update Student")
        print("5. Delete Student")
        print("0. Back to Main Menu")
        choice = input("Your choice: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            # add student
            first = get_nonempty_string("First name: ")
            last = get_nonempty_string("Last name: ")
            dob = get_date_input("Date of birth (YYYY-MM-DD, optional): ")
            email = get_nonempty_string("Email: ")
            phone = input("Phone (optional): ").strip() or None
            address = input("Address (optional): ").strip() or None
            town = input("Town (optional): ").strip() or None
            postcode = input("Post code (optional): ").strip() or None
            try:
                s = Student(first_name=first, last_name=last, date_of_birth=dob,
                            email=email, phone=phone, address=address, town=town, post_code=postcode)
                s.add()
                print("  Student added successfully.")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "2":
            # View all students
            try:
                students = Student.get_all()
                if not students:
                    print("  No students found.")
                    continue
                header = ["ID", "First Name", "Last Name", "DOB", "Email", "Town"]
                data = [(s.student_id, s.first_name, s.last_name,
                         s.date_of_birth or "", s.email, s.town or "") for s in students]
                print_table(header, data)
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "3":
            # Search by name
            search = input("Enter name to search (partial): ").strip()
            if not search:
                print("  Search term cannot be empty.")
                continue
            try:
                found = Student.search_by_name(search)
                if not found:
                    print("  No matching students.")
                else:
                    header = ["ID", "First Name", "Last Name", "Email"]
                    data = [(s.student_id, s.first_name, s.last_name, s.email) for s in found]
                    print_table(header, data)
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "4":
            # Update student
            sid = get_int_input("Student ID to update: ")
            try:
                s = Student()
                existing = s.get_by_id(sid)
                if not existing:
                    print(f"  Student with ID {sid} not found.")
                    continue
                print("Leave field empty to keep current value.")
                first = input(f"First name [{existing.first_name}]: ").strip()
                last = input(f"Last name [{existing.last_name}]: ").strip()
                dob = get_date_input(f"Date of birth [{existing.date_of_birth or ''}]: ")
                email = get_nonempty_string(f"Email [{existing.email}]: ")
                phone = input(f"Phone [{existing.phone or ''}]: ").strip() or None
                address = input(f"Address [{existing.address or ''}]: ").strip() or None
                town = input(f"Town [{existing.town or ''}]: ").strip() or None
                postcode = input(f"Post code [{existing.post_code or ''}]: ").strip() or None

                s.student_id = sid
                s.first_name = first if first else existing.first_name
                s.last_name = last if last else existing.last_name
                s.date_of_birth = dob if dob else existing.date_of_birth
                s.email = email if email else existing.email
                s.phone = phone if phone is not None else existing.phone
                s.address = address if address is not None else existing.address
                s.town = town if town is not None else existing.town
                s.post_code = postcode if postcode is not None else existing.post_code
                s.update()
                print("  Student updated successfully.")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "5":
            sid = get_int_input("Student ID to delete: ")
            try:
                s = Student()
                s.delete(sid)   # используем метод delete, который принимает id
                print("  Student deleted successfully.")
            except Exception as e:
                print(f"  Error: {e}")

        else:
            print("  Invalid choice.")


# =========Teachers
def manage_teachers():
    while True:
        print("\n=== Manage Teachers ===")
        print("1. Add Teacher")
        print("2. View All Teachers")
        print("3. Search Teacher by Name")
        print("4. Search Teacher by Department")
        print("5. Update Teacher")
        print("6. Delete Teacher")
        print("0. Back to Main Menu")
        choice = input("Your choice: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            first = get_nonempty_string("First name: ")
            last = get_nonempty_string("Last name: ")
            hire = get_date_input("Hire date (YYYY-MM-DD, optional): ")
            email = get_nonempty_string("Email: ")
            phone = input("Phone (optional): ").strip() or None
            dept = input("Department (optional): ").strip() or None
            try:
                t = Teacher(first_name=first, last_name=last, hire_date=hire,
                            email=email, phone=phone, department=dept)
                t.add()
                print("  Teacher added successfully.")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "2":
            try:
                teachers = Teacher.get_all()
                if not teachers:
                    print("  No teachers found.")
                    continue
                header = ["ID", "First Name", "Last Name", "Email", "Department"]
                data = [(t.teacher_id, t.first_name, t.last_name, t.email, t.department or "") for t in teachers]
                print_table(header, data)
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "3":
            search = input("Enter name to search: ").strip()
            if not search:
                continue
            try:
                found = Teacher.search_by_name(search)
                if not found:
                    print("  No matching teachers.")
                else:
                    header = ["ID", "First Name", "Last Name", "Email", "Department"]
                    data = [(t.teacher_id, t.first_name, t.last_name, t.email, t.department or "") for t in found]
                    print_table(header, data)
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "4":
            dept = input("Enter department name (partial): ").strip()
            if not dept:
                continue
            try:
                all_teachers = Teacher.get_all()
                matched = [t for t in all_teachers if dept.lower() in (t.department or "").lower()]
                if not matched:
                    print("  No teachers in that department.")
                else:
                    header = ["ID", "Name", "Email", "Department"]
                    data = [(t.teacher_id, f"{t.first_name} {t.last_name}", t.email, t.department or "") for t in matched]
                    print_table(header, data)
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "5":
            tid = get_int_input("Teacher ID to update: ")
            try:
                t = Teacher()
                existing = t.get_by_id(tid)
                if not existing:
                    print(f"  Teacher with ID {tid} not found.")
                    continue
                print("Leave field empty to keep current value.")
                first = input(f"First name [{existing.first_name}]: ").strip()
                last = input(f"Last name [{existing.last_name}]: ").strip()
                hire = get_date_input(f"Hire date [{existing.hire_date or ''}]: ")
                email = get_nonempty_string(f"Email [{existing.email}]: ")
                phone = input(f"Phone [{existing.phone or ''}]: ").strip() or None
                dept = input(f"Department [{existing.department or ''}]: ").strip() or None
                t.teacher_id = tid
                t.first_name = first if first else existing.first_name
                t.last_name = last if last else existing.last_name
                t.hire_date = hire if hire else existing.hire_date
                t.email = email if email else existing.email
                t.phone = phone if phone is not None else existing.phone
                t.department = dept if dept is not None else existing.department
                t.update()
                print("  Teacher updated successfully.")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "6":
            tid = get_int_input("Teacher ID to delete: ")
            try:
                t = Teacher()
                t.delete(tid)
                print("  Teacher deleted successfully.")
            except Exception as e:
                print(f"  Error: {e}")

        else:
            print("  Invalid choice.")


# ==============Courses
def manage_courses():
    while True:
        print("\n=== Manage Courses ===")
        print("1. Add Course")
        print("2. View All Courses")
        print("3. Search Course by Name")
        print("4. Update Course")
        print("5. Delete Course")
        print("0. Back to Main Menu")
        choice = input("Your choice: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            name = get_nonempty_string("Course name: ")
            desc = input("Description (optional): ").strip() or None
            credits = get_int_input("Credits (1-10): ", 1, 10)
            teacher_id = get_int_input("Teacher ID (optional, 0 for none): ", 0)
            if teacher_id == 0:
                teacher_id = None
            try:
                c = Course(course_name=name, description=desc, credits=credits, teacher_id=teacher_id)
                c.add()
                print("  Course added successfully.")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "2":
            try:
                courses = Course.get_all()
                if not courses:
                    print("  No courses found.")
                    continue
                header = ["ID", "Course Name", "Credits", "Teacher"]
                data = [(c.course_id, c.course_name, c.credits, getattr(c, 'teacher_name', 'Not assigned')) for c in courses]
                print_table(header, data)
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "3":
            search = input("Enter course name (partial): ").strip()
            if not search:
                continue
            try:
                found = Course.search_by_name(search)
                if not found:
                    print("  No matching courses.")
                else:
                    header = ["ID", "Course Name", "Credits", "Teacher"]
                    data = [(c.course_id, c.course_name, c.credits, getattr(c, 'teacher_name', 'Not assigned')) for c in found]
                    print_table(header, data)
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "4":
            cid = get_int_input("Course ID to update: ")
            try:
                c = Course()
                existing = c.get_by_id(cid)
                if not existing:
                    print(f"  Course with ID {cid} not found.")
                    continue
                print("Leave field empty to keep current value.")
                name = input(f"Course name [{existing.course_name}]: ").strip()
                desc = input(f"Description [{existing.description or ''}]: ").strip() or None
                credits = input(f"Credits [{existing.credits}]: ").strip()
                teacher_id = input(f"Teacher ID [{existing.teacher_id or 'None'}]: ").strip()
                c.course_id = cid
                c.course_name = name if name else existing.course_name
                c.description = desc if desc is not None else existing.description
                c.credits = int(credits) if credits else existing.credits
                c.teacher_id = int(teacher_id) if teacher_id else existing.teacher_id
                c.update()
                print("  Course updated successfully.")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "5":
            cid = get_int_input("Course ID to delete: ")
            try:
                c = Course()
                c.delete(cid)
                print("  Course deleted successfully.")
            except Exception as e:
                print(f"  Error: {e}")

        else:
            print("  Invalid choice.")


# ===========Registrations
def manage_registrations():
    while True:
        print("\n=== Manage Registrations ===")
        print("1. Register Student to Course")
        print("2. Update Grade")
        print("3. Drop Student from Course (Delete Registration)")
        print("4. View All Registrations")
        print("5. View Registrations by Student")
        print("6. View Registrations by Course")
        print("0. Back to Main Menu")
        choice = input("Your choice: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            sid = get_int_input("Student ID: ")
            cid = get_int_input("Course ID: ")
            try:
                reg = Registration(student_id=sid, course_id=cid)
                reg.register()
                print("  Student registered to course successfully.")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "2":
            rid = get_int_input("Registration ID: ")
            grade = get_float_input("Grade (0-100): ", 0, 100)
            try:
                reg = Registration()
                reg.update_grade(rid, grade)
                print("  Grade updated successfully.")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "3":
            rid = get_int_input("Registration ID to delete: ")
            try:
                reg = Registration(registration_id=rid)
                reg.delete()
                print("  Registration deleted (student dropped from course).")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "4":
            try:
                regs = Registration.get_all()
                if not regs:
                    print("  No registrations found.")
                    continue
                header = ["Reg ID", "Student Name", "Course Name", "Grade", "Registration Date"]
                data = [(r.registration_id, r.student_name, r.course_name, r.grade or "N/A", r.registration_date) for r in regs]
                print_table(header, data)
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "5":
            sid = get_int_input("Student ID: ")
            try:
                regs = Registration.get_by_student(sid)
                if not regs:
                    print("  No registrations for this student.")
                    continue
                header = ["Reg ID", "Course Name", "Grade", "Registration Date"]
                data = [(r.registration_id, r.course_name, r.grade or "N/A", r.registration_date) for r in regs]
                print_table(header, data)
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "6":
            cid = get_int_input("Course ID: ")
            try:
                regs = Registration.get_by_course(cid)
                if not regs:
                    print("  No registrations for this course.")
                    continue
                header = ["Reg ID", "Student Name", "Grade", "Registration Date"]
                data = [(r.registration_id, r.student_name, r.grade or "N/A", r.registration_date) for r in regs]
                print_table(header, data)
            except Exception as e:
                print(f"  Error: {e}")

        else:
            print("  Invalid choice.")


# ================ Main Menu Program Loop
def main():
    print("\n" + "=" * 50)
    print("   SCHOOL MANAGEMENT SYSTEM")
    print("=" * 50)
    while True:
        print("\n--- Main Menu ---")
        print("1. Manage Students")
        print("2. Manage Teachers")
        print("3. Manage Courses")
        print("4. Manage Registrations")
        print("0. Exit Program")
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Exiting program. Goodbye!")
            sys.exit(0)
        elif choice == "1":
            manage_students()
        elif choice == "2":
            manage_teachers()
        elif choice == "3":
            manage_courses()
        elif choice == "4":
            manage_registrations()
        else:
            print("Invalid choice. Please select 0-4.")


if __name__ == "__main__":
    main()