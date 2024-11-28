import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('development_tracker.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_tasks (
            id INTEGER PRIMARY KEY,
            date TEXT,
            task_category TEXT,
            task_description TEXT,
            planned_duration REAL,
            actual_duration REAL,
            status TEXT,
            complexity INTEGER,
            points_earned REAL,
            notes TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS skill_mastery (
            id INTEGER PRIMARY KEY,
            skill_area TEXT,
            max_points REAL,
            points_earned REAL,
            proficiency_level TEXT
        )
        ''')

        self.conn.commit()

    def fetch_all_tasks(self):
        self.cursor.execute("SELECT * FROM daily_tasks")
        return self.cursor.fetchall()

    def insert_task(self, date, category, task, duration, complexity, status, points_earned, notes):
        self.cursor.execute('''
        INSERT INTO daily_tasks 
        (date, task_category, task_description, planned_duration, 
        actual_duration, complexity, status, points_earned, notes)
        VALUES (?, ?, ?, ?, 0, ?, ?, ?, ?)
        ''', (date, category, task, duration, complexity, status, points_earned, notes))
        self.conn.commit()
