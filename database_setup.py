import sqlite3


def setup_database():
    conn = sqlite3.connect('development_tracker.db')
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_tasks (
        id INTEGER PRIMARY KEY,
        date TEXT,
        task_category TEXT,
        task_description TEXT,
        planned_duration REAL,
        actual_duration REAL,
        complexity INTEGER,
        status TEXT,
        points_earned REAL,
        notes TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS skill_mastery (
        id INTEGER PRIMARY KEY,
        skill_area TEXT,
        max_points REAL,
        points_earned REAL,
        proficiency_level TEXT
    )
    ''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    setup_database()
