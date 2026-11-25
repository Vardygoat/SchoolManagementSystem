# models/teacher.py
from base_model import BaseModel

class Teacher(BaseModel):
    def __init__(self, teacher_id=None, first_name=None, last_name=None,
                 hire_date=None, email=None, phone=None, department=None):
        super().__init__()
        self.teacher_id = teacher_id
        self.first_name = first_name
        self.last_name = last_name
        self.hire_date = hire_date
        self.email = email
        self.phone = phone
        self.department = department

    def add(self):
        if not self.first_name or not self.last_name or not self.email:
            raise ValueError("First name, last name and email are required")
        
        query = """INSERT INTO Teachers (first_name, last_name, hire_date, email, phone, department)
                   VALUES (?, ?, ?, ?, ?, ?)"""
        self._execute_query(query, (
            self.first_name, self.last_name, self.hire_date,
            self.email, self.phone, self.department
        ))
        return True

    def update(self):
        if not self.teacher_id:
            raise ValueError("Teacher ID required for update")
        
        query = """UPDATE Teachers SET first_name = ?, last_name = ?, hire_date = ?,
                   email = ?, phone = ?, department = ? WHERE teacher_id = ?"""
        self._execute_query(query, (
            self.first_name, self.last_name, self.hire_date,
            self.email, self.phone, self.department, self.teacher_id
        ))
        return True

    def delete(self, teacher_id=None):
        if teacher_id:
            self.teacher_id = teacher_id
        if not self.teacher_id:
            raise ValueError("Teacher ID required for deletion")
        
        query = "DELETE FROM Teachers WHERE teacher_id = ?"
        self._execute_query(query, (self.teacher_id,))
        return True

    def get_by_id(self, teacher_id):
        query = "SELECT * FROM Teachers WHERE teacher_id = ?"
        result = self._execute_query(query, (teacher_id,))
        
        if result:
            data = dict(result[0])
            self.teacher_id = data['teacher_id']
            self.first_name = data['first_name']
            self.last_name = data['last_name']
            self.hire_date = data['hire_date']
            self.email = data['email']
            self.phone = data['phone']
            self.department = data['department']
            return self
        return None

    @classmethod
    def get_all(cls):
        instance = cls()
        query = "SELECT * FROM Teachers ORDER BY last_name, first_name"
        results = instance._execute_query(query)
        
        teachers = []
        for row in results:
            data = dict(row)
            teachers.append(cls(
                teacher_id=data['teacher_id'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                hire_date=data['hire_date'],
                email=data['email'],
                phone=data['phone'],
                department=data['department']
            ))
        return teachers

    @classmethod
    def search_by_name(cls, search_term):
        instance = cls()
        query = """SELECT * FROM Teachers 
                   WHERE first_name LIKE ? OR last_name LIKE ?
                   ORDER BY last_name, first_name"""
        search_pattern = f"%{search_term}%"
        results = instance._execute_query(query, (search_pattern, search_pattern))
        
        teachers = []
        for row in results:
            data = dict(row)
            teachers.append(cls(
                teacher_id=data['teacher_id'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                department=data['department']
            ))
        return teachers

    def __str__(self):
        return f"{self.teacher_id}: {self.first_name} {self.last_name} ({self.department})"