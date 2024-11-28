import sys
import sqlite3
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

from daily_tasks_tab import DailyTasksTab
from skill_mastery_tab import SkillMasteryTab
from progress_tracking_tab import ProgressTrackingTab
from project_certification_tab import ProjectCertificationTab


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

        # Add tabs to tab widget
        self.tab_widget.addTab(self.daily_tasks_tab, "Daily Tasks")
        self.tab_widget.addTab(self.skill_mastery_tab, "Skill Mastery")
        self.tab_widget.addTab(self.progress_tracking_tab, "Progress Tracking")
        self.tab_widget.addTab(self.project_certification_tab, "Projects & Certifications")

        main_layout.addWidget(self.tab_widget)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def init_database(self):
        """Initialize SQLite database for tracking"""
        self.conn = sqlite3.connect('development_tracker.db')
        self.cursor = self.conn.cursor()

        # Create tables
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


def main():
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    # Create and show the main window
    tracker = DevelopmentTracker()
    tracker.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
