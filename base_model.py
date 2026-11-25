# base_model.py
from abc import ABC, abstractmethod
from db_connection import DatabaseConnection

class BaseModel(ABC):
    """Абстрактный базовый класс для всех моделей."""

    def __init__(self):
        self.db = DatabaseConnection()

    def _execute_query(self, query, params=None):
        """
        Выполняет SQL запрос и возвращает результат.
        """
        cursor = self.db.get_cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Для SELECT запросов получаем результаты
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                return results if results else []
            else:
                # Для INSERT/UPDATE/DELETE подтверждаем транзакцию
                self.db.connection.commit()
                return True
        except Exception as e:
            self.db.connection.rollback()
            raise Exception(f"Query failed: {e}")
        finally:
            cursor.close()

    def _call_procedure(self, proc_name, params=None):
        """
        Совместимость с старым кодом.
        Перенаправляет вызовы к обработчикам в подклассах.
        """
        raise NotImplementedError(f"Procedure {proc_name} must be implemented in subclass")

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def get_by_id(self, id_val):
        pass

    @classmethod
    @abstractmethod
    def get_all(cls):
        pass