# models/student.py
from base_model import BaseModel
from datetime import date

class Student(BaseModel):
    def __init__(self, student_id=None, first_name=None, last_name=None,
                 date_of_birth=None, email=None, phone=None,
                 address=None, town=None, post_code=None):
        super().__init__()
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email = email
        self.phone = phone
        self.address = address
        self.town = town
        self.post_code = post_code

    def add(self):
        #Student addition
        if not self.first_name or not self.last_name or not self.email:
            raise ValueError("First name, last name and email are required")
        
        query = """INSERT INTO Students (first_name, last_name, date_of_birth, email, phone, address, town, post_code)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        self._execute_query(query, (
            self.first_name, self.last_name, self.date_of_birth,
            self.email, self.phone, self.address, self.town, self.post_code
        ))
        return True

    def update(self):
        #Student update info
        if not self.student_id:
            raise ValueError("Student ID is required for update")
        
        query = """UPDATE Students SET first_name = ?, last_name = ?, date_of_birth = ?, 
                   email = ?, phone = ?, address = ?, town = ?, post_code = ?
                   WHERE student_id = ?"""
        self._execute_query(query, (
            self.first_name, self.last_name, self.date_of_birth,
            self.email, self.phone, self.address, self.town, self.post_code,
            self.student_id
        ))
        return True

    def delete(self, student_id=None):
        #delete student
        if student_id:
            self.student_id = student_id
        if not self.student_id:
            raise ValueError("Student ID is required for deletion")
        
        query = "DELETE FROM Students WHERE student_id = ?"
        self._execute_query(query, (self.student_id,))
        return True

    def get_by_id(self, student_id):
        #get the student by id
        query = "SELECT * FROM Students WHERE student_id = ?"
        result = self._execute_query(query, (student_id,))
        
        if result:
            data = dict(result[0])
            self.student_id = data['student_id']
            self.first_name = data['first_name']
            self.last_name = data['last_name']
            self.date_of_birth = data['date_of_birth']
            self.email = data['email']
            self.phone = data['phone']
            self.address = data['address']
            self.town = data['town']
            self.post_code = data['post_code']
            return self
        return None

    @classmethod
    def get_all(cls):
        #get all students
        instance = cls()
        query = "SELECT * FROM Students ORDER BY last_name, first_name"
        results = instance._execute_query(query)
        
        students = []
        for row in results:
            data = dict(row)
            students.append(cls(
                student_id=data['student_id'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                date_of_birth=data['date_of_birth'],
                email=data['email'],
                phone=data['phone'],
                address=data['address'],
                town=data['town'],
                post_code=data['post_code']
            ))
        return students

    @classmethod
    def search_by_name(cls, search_term):
        #search students by name and surname
        instance = cls()
        query = """SELECT * FROM Students 
                   WHERE first_name LIKE ? OR last_name LIKE ?
                   ORDER BY last_name, first_name"""
        search_pattern = f"%{search_term}%"
        results = instance._execute_query(query, (search_pattern, search_pattern))
        
        students = []
        for row in results:
            data = dict(row)
            students.append(cls(
                student_id=data['student_id'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                phone=data['phone']
            ))
        return students

    def __str__(self):
        return f"{self.student_id}: {self.first_name} {self.last_name} ({self.email})"