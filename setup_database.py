#!/usr/bin/env python3
"""
Setup script for School Management System database.
This script creates a local SQLite database with all necessary tables.
"""

import sqlite3
import os
from db_config import DB_PATH

def create_database():
    """Create SQLite database and tables."""
    print("\n" + "="*60)
    print("  School Management System - Database Setup")
    print("="*60)
    
    # Check if database already exists
    db_exists = os.path.exists(DB_PATH)
    
    if db_exists:
        print(f"\n1. Database already exists: {DB_PATH}")
        response = input("   Do you want to reset it? (y/n): ").strip().lower()
        if response != 'y':
            print("  ✓ Using existing database")
            return True
        else:
            os.remove(DB_PATH)
            print("  ✓ Database reset")
    
    # Connect to database (creates if not exists)
    print(f"\n2. Creating database file...")
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.execute("PRAGMA foreign_keys = ON")
        print(f"  ✓ Database created: {DB_PATH}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    # Create tables
    print("\n3. Creating tables...")
    try:
        cursor = connection.cursor()
        
        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                date_of_birth DATE,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                address TEXT,
                town TEXT,
                post_code TEXT,
                enrollment_date DATE DEFAULT CURRENT_DATE
            )
        """)
        
        # Teachers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Teachers (
                teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                hire_date DATE,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                department TEXT
            )
        """)
        
        # Courses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                description TEXT,
                credits INTEGER NOT NULL CHECK(credits > 0 AND credits <= 10),
                teacher_id INTEGER,
                FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id) ON DELETE SET NULL
            )
        """)
        
        # Registrations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Registrations (
                registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                registration_date DATE DEFAULT CURRENT_DATE,
                grade REAL CHECK(grade >= 0 AND grade <= 100),
                FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE,
                UNIQUE(student_id, course_id)
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_name ON Students(first_name, last_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_email ON Students(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_teacher_name ON Teachers(first_name, last_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_course_name ON Courses(course_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_registration_student ON Registrations(student_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_registration_course ON Registrations(course_id)")
        
        connection.commit()
        print("  ✓ All tables created successfully")
        
    except Exception as e:
        print(f"  ✗ Error creating tables: {e}")
        connection.close()
        return False
    
    connection.close()
    
    print("\n" + "="*60)
    print("  ✓ Database setup completed successfully!")
    print("="*60)
    print(f"\nDatabase file: {os.path.abspath(DB_PATH)}")
    print("\nYou can now run: python main.py")
    return True


if __name__ == "__main__":
    import sys
    success = create_database()
    sys.exit(0 if success else 1)
