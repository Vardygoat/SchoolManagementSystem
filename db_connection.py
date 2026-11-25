# db_connection.py
import sqlite3
from db_config import DB_PATH

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(DB_PATH)
                self.connection.row_factory = sqlite3.Row  # Return rows as dictionaries
                self.connection.execute("PRAGMA foreign_keys = ON")  # Enable foreign keys
            except Exception as e:
                raise Exception(f"Database connection failed: {e}")
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_cursor(self):
        conn = self.connect()
        return conn.cursor()