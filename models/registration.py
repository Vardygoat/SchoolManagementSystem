# models/registration.py
from base_model import BaseModel

#Registration model
class Registration(BaseModel):
    def __init__(self, registration_id=None, student_id=None, course_id=None,
                 registration_date=None, grade=None, student_name=None, course_name=None):
        super().__init__()
        self.registration_id = registration_id
        self.student_id = student_id
        self.course_id = course_id
        self.registration_date = registration_date
        self.grade = grade
        self.student_name = student_name
        self.course_name = course_name

    #register a student to a course
    def register(self):
        if not self.student_id or not self.course_id:
            raise ValueError("Student ID and Course ID are required")
        
        query = """INSERT INTO Registrations (student_id, course_id)
                   VALUES (?, ?)"""
        self._execute_query(query, (self.student_id, self.course_id))
        return True

    def add(self):
        #add the registration
        return self.register()

    #update the grade for the registration
    def update_grade(self, registration_id, grade):
        if grade is not None and (grade < 0 or grade > 100):
            raise ValueError("Grade must be between 0 and 100")
        
        query = "UPDATE Registrations SET grade = ? WHERE registration_id = ?"
        self._execute_query(query, (grade, registration_id))
        return True

    #update the registration info (grade)
    def update(self):
        if not self.registration_id:
            raise ValueError("Registration ID required for update")
        
        if self.grade is not None and (self.grade < 0 or self.grade > 100):
            raise ValueError("Grade must be between 0 and 100")
        
        query = "UPDATE Registrations SET grade = ? WHERE registration_id = ?"
        self._execute_query(query, (self.grade, self.registration_id))
        return True

    #delete the registration (unenroll from course)
    def delete(self, registration_id=None):
        
        if registration_id:
            self.registration_id = registration_id
        if not self.registration_id:
            raise ValueError("Registration ID required for deletion")
        
        query = "DELETE FROM Registrations WHERE registration_id = ?"
        self._execute_query(query, (self.registration_id,))
        return True

        #get the registration by id
    def get_by_id(self, registration_id):
        query = """SELECT r.*, s.first_name || ' ' || s.last_name as student_name, c.course_name
                   FROM Registrations r
                   JOIN Students s ON r.student_id = s.student_id
                   JOIN Courses c ON r.course_id = c.course_id
                   WHERE r.registration_id = ?"""
        result = self._execute_query(query, (registration_id,))
        
        if result:
            data = dict(result[0])
            self.registration_id = data['registration_id']
            self.student_id = data['student_id']
            self.course_id = data['course_id']
            self.registration_date = data['registration_date']
            self.grade = data['grade']
            self.student_name = data['student_name']
            self.course_name = data['course_name']
            return self
        return None

    #get all registrations
    @classmethod
    def get_all(cls):
        instance = cls()
        query = """SELECT r.registration_id, r.student_id, r.course_id, r.registration_date, r.grade,
                          s.first_name || ' ' || s.last_name as student_name,
                          c.course_name, t.first_name || ' ' || t.last_name as teacher_name
                   FROM Registrations r
                   JOIN Students s ON r.student_id = s.student_id
                   JOIN Courses c ON r.course_id = c.course_id
                   LEFT JOIN Teachers t ON c.teacher_id = t.teacher_id
                   ORDER BY student_name, c.course_name"""
        results = instance._execute_query(query)
        
        registrations = []
        for row in results:
            data = dict(row)
            registrations.append(cls(
                registration_id=data['registration_id'],
                student_id=data['student_id'],
                course_id=data['course_id'],
                registration_date=data['registration_date'],
                grade=data['grade'],
                student_name=data['student_name'],
                course_name=data['course_name']
            ))
        return registrations

    #get all registrations for a student by id
    @classmethod
    def get_by_student(cls, student_id):
        """Получить все регистрации студента."""
        instance = cls()
        query = """SELECT r.registration_id, r.course_id, r.registration_date, r.grade,
                          c.course_name, t.first_name || ' ' || t.last_name as teacher_name
                   FROM Registrations r
                   JOIN Courses c ON r.course_id = c.course_id
                   LEFT JOIN Teachers t ON c.teacher_id = t.teacher_id
                   WHERE r.student_id = ?
                   ORDER BY r.registration_date"""
        results = instance._execute_query(query, (student_id,))
        
        registrations = []
        for row in results:
            data = dict(row)
            registrations.append(cls(
                registration_id=data['registration_id'],
                course_id=data['course_id'],
                registration_date=data['registration_date'],
                grade=data['grade'],
                course_name=data['course_name']
            ))
        return registrations

    #get all students registered for a course by id
    @classmethod
    def get_by_course(cls, course_id):
        instance = cls()
        query = """SELECT r.registration_id, r.student_id, r.registration_date, r.grade,
                          s.first_name || ' ' || s.last_name as student_name
                   FROM Registrations r
                   JOIN Students s ON r.student_id = s.student_id
                   WHERE r.course_id = ?
                   ORDER BY student_name"""
        results = instance._execute_query(query, (course_id,))
        
        registrations = []
        for row in results:
            data = dict(row)
            registrations.append(cls(
                registration_id=data['registration_id'],
                student_id=data['student_id'],
                registration_date=data['registration_date'],
                grade=data['grade'],
                student_name=data['student_name']
            ))
        return registrations

    #check if a student is registered for a course
    @classmethod
    def is_registered(cls, student_id, course_id):
        instance = cls()
        query = """SELECT COUNT(*) as count FROM Registrations
                   WHERE student_id = ? AND course_id = ?"""
        result = instance._execute_query(query, (student_id, course_id))
        
        if result:
            count = dict(result[0])['count']
            return count > 0
        return False