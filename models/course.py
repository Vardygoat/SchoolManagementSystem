# models/course.py
from base_model import BaseModel

#Course model
class Course(BaseModel):
    def __init__(self, course_id=None, course_name=None, description=None,
                 credits=None, teacher_id=None, teacher_name=None):
        super().__init__()
        self.course_id = course_id
        self.course_name = course_name
        self.description = description
        self.credits = credits
        self.teacher_id = teacher_id
        self.teacher_name = teacher_name


    #adding a course
    def add(self):
        if not self.course_name or not self.credits:
            raise ValueError("Course name and credits are required")
        
        query = """INSERT INTO Courses (course_name, description, credits, teacher_id)
                   VALUES (?, ?, ?, ?)"""
        self._execute_query(query, (
            self.course_name, self.description, self.credits, self.teacher_id
        ))
        return True


    #update the course info
    def update(self):
        if not self.course_id:
            raise ValueError("Course ID required for update")
        
        query = """UPDATE Courses SET course_name = ?, description = ?, credits = ?, teacher_id = ?
                   WHERE course_id = ?"""
        self._execute_query(query, (
            self.course_name, self.description, self.credits, self.teacher_id, self.course_id
        ))
        return True


    #delete a course
    def delete(self, course_id=None):
        if course_id:
            self.course_id = course_id
        if not self.course_id:
            raise ValueError("Course ID required for deletion")
        
        query = "DELETE FROM Courses WHERE course_id = ?"
        self._execute_query(query, (self.course_id,))
        return True


    #get the course by id
    def get_by_id(self, course_id):
        query = "SELECT * FROM Courses WHERE course_id = ?"
        result = self._execute_query(query, (course_id,))
        
        if result:
            data = dict(result[0])
            self.course_id = data['course_id']
            self.course_name = data['course_name']
            self.description = data['description']
            self.credits = data['credits']
            self.teacher_id = data['teacher_id']
            return self
        return None

    #get all courses
    @classmethod
    def get_all(cls):
        instance = cls()
        query = """SELECT c.*, COALESCE(t.first_name || ' ' || t.last_name, 'Not assigned') as teacher_name
                   FROM Courses c
                   LEFT JOIN Teachers t ON c.teacher_id = t.teacher_id
                   ORDER BY c.course_name"""
        results = instance._execute_query(query)
        
        courses = []
        for row in results:
            data = dict(row)
            courses.append(cls(
                course_id=data['course_id'],
                course_name=data['course_name'],
                description=data['description'],
                credits=data['credits'],
                teacher_id=data['teacher_id'],
                teacher_name=data.get('teacher_name')
            ))
        return courses

    #search courses by name
    @classmethod
    def search_by_name(cls, search_term):
        instance = cls()
        query = """SELECT c.*, COALESCE(t.first_name || ' ' || t.last_name, 'Not assigned') as teacher_name
                   FROM Courses c
                   LEFT JOIN Teachers t ON c.teacher_id = t.teacher_id
                   WHERE c.course_name LIKE ?
                   ORDER BY c.course_name"""
        search_pattern = f"%{search_term}%"
        results = instance._execute_query(query, (search_pattern,))
        
        courses = []
        for row in results:
            data = dict(row)
            courses.append(cls(
                course_id=data['course_id'],
                course_name=data['course_name'],
                description=data['description'],
                credits=data['credits'],
                teacher_name=data.get('teacher_name')
            ))
        return courses
    

#string representation of the course
    def __str__(self):
        return f"{self.course_id}: {self.course_name} (credits: {self.credits})"
