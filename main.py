import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget
from daily_tasks_tab import DailyTasksTab
from skill_mastery_tab import SkillMasteryTab
from progress_tracking_tab import ProgressTrackingTab
from project_certification_tab import ProjectCertificationTab
from weekly_progress_tab import WeeklyProgressTab


class DevelopmentTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Development Tracking System")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize database
        self.init_database()

        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Create tab widget
        self.tab_widget = QTabWidget()

        # Create tabs
        self.daily_tasks_tab = DailyTasksTab(self)
        self.skill_mastery_tab = SkillMasteryTab(self)
        self.progress_tracking_tab = ProgressTrackingTab(self)
        self.project_certification_tab = ProjectCertificationTab(self)
        self.weekly_progress_tab = WeeklyProgressTab(self)

        # Add tabs to tab widget
        self.tab_widget.addTab(self.daily_tasks_tab, "Daily Tasks")
        self.tab_widget.addTab(self.skill_mastery_tab, "Skill Mastery")
        self.tab_widget.addTab(self.progress_tracking_tab, "Progress Tracking")
        self.tab_widget.addTab(self.project_certification_tab, "Project Certification")
        self.tab_widget.addTab(self.weekly_progress_tab, "Weekly Progress")

        # Add tab widget to main layout
        main_layout.addWidget(self.tab_widget)

        # Set main widget layout
        main_widget.setLayout(main_layout)

        # Set central widget of main window
        self.setCentralWidget(main_widget)

    def init_database(self):
        self.conn = sqlite3.connect('development_tracker.db')
        self.cursor = self.conn.cursor()

        # Create tables if they don't exist
        self.cursor.execute('''
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


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DevelopmentTracker()
    window.show()
    sys.exit(app.exec())
