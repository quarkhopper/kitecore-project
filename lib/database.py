from abc import ABC, abstractmethod

class Database(ABC):
    """Abstract base class for database interactions."""

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def execute_query(self, query, params=None):
        pass

    @abstractmethod
    def fetch_results(self, query, params=None):
        pass

import sqlite3

class SQLiteDatabase(Database):
    def __init__(self, db_path="kitecore_local.db"):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()

    def fetch_results(self, query, params=None):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
        
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class CloudDatabase(Database):
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

    def connect(self):
        self.session = self.Session()

    def close(self):
        if self.session:
            self.session.close()

    def execute_query(self, query, params=None):
        with self.session.begin():
            self.session.execute(query, params or {})

    def fetch_results(self, query, params=None):
        result = self.session.execute(query, params or {})
        return result.fetchall()

    def get_engine(self):
        return self.engine


import os

def get_database():
    db_mode = os.getenv("KITE_DB_MODE", "local")  # Default to local
    if db_mode == "cloud":
        return CloudDatabase(os.getenv("DATABASE_URL"))
    else:
        return SQLiteDatabase()
