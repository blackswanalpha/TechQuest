from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QComboBox, QGroupBox, QCalendarWidget
)
from PyQt6.QtCore import QDate
from datetime import datetime, timedelta

class WeeklyProgressTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout()

        # Date Selection Section
        date_selection_group = QGroupBox("Date Range")
        date_selection_layout = QHBoxLayout()

        self.start_date_calendar = QCalendarWidget()
        self.end_date_calendar = QCalendarWidget()

        date_selection_layout.addWidget(QLabel("Start Date:"))
        date_selection_layout.addWidget(self.start_date_calendar)
        date_selection_layout.addWidget(QLabel("End Date:"))
        date_selection_layout.addWidget(self.end_date_calendar)

        date_selection_group.setLayout(date_selection_layout)
        self.layout.addWidget(date_selection_group)

        # Category Filter
        filter_layout = QHBoxLayout()
        category_label = QLabel("Filter by Category:")
        self.category_filter = QComboBox()
        self.category_filter.addItems([
            "All", "DevOps", "Next.js", "Microservices",
            "CI/CD", "Kubernetes", "Project Management"
        ])
        self.category_filter.currentTextChanged.connect(self.load_weekly_progress)

        filter_layout.addWidget(category_label)
        filter_layout.addWidget(self.category_filter)
        self.layout.addLayout(filter_layout)

        # Weekly Progress Table
        self.weekly_progress_table = QTableWidget()
        self.weekly_progress_table.setColumnCount(6)
        self.weekly_progress_table.setHorizontalHeaderLabels([
            "Date", "Category", "Task", "Planned Duration", "Actual Duration", "Points Earned"
        ])
        self.layout.addWidget(self.weekly_progress_table)

        # Summary Section
        summary_group = QGroupBox("Weekly Summary")
        summary_layout = QHBoxLayout()

        self.total_tasks_label = QLabel("Total Tasks: 0")
        self.total_points_label = QLabel("Total Points: 0")
        self.avg_duration_label = QLabel("Avg Duration: 0 hrs")

        summary_layout.addWidget(self.total_tasks_label)
        summary_layout.addWidget(self.total_points_label)
        summary_layout.addWidget(self.avg_duration_label)

        summary_group.setLayout(summary_layout)
        self.layout.addWidget(summary_group)

        self.setLayout(self.layout)

        # Initialize with current week
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        self.start_date_calendar.setSelectedDate(QDate(start_of_week.year, start_of_week.month, start_of_week.day))
        self.end_date_calendar.setSelectedDate(QDate(end_of_week.year, end_of_week.month, end_of_week.day))

        self.load_weekly_progress()

    def load_weekly_progress(self):
        start_date = self.start_date_calendar.selectedDate().toString("yyyy-MM-dd")
        end_date = self.end_date_calendar.selectedDate().toString("yyyy-MM-dd")
        category_filter = self.category_filter.currentText()

        query = '''
        SELECT date, task_category, task_description, 
               planned_duration, actual_duration, points_earned 
        FROM daily_tasks 
        WHERE date BETWEEN ? AND ?
        '''
        params = [start_date, end_date]

        if category_filter != "All":
            query += " AND task_category = ?"
            params.append(category_filter)

        self.parent.cursor.execute(query, params)
        weekly_tasks = self.parent.cursor.fetchall()

        self.weekly_progress_table.setRowCount(len(weekly_tasks))

        total_tasks = 0
        total_points = 0
        total_duration = 0

        for row, task in enumerate(weekly_tasks):
            for col, data in enumerate(task):
                self.weekly_progress_table.setItem(row, col, QTableWidgetItem(str(data)))

            total_tasks += 1
            total_points += task[5]
            total_duration += task[4]

        avg_duration = total_duration / total_tasks if total_tasks > 0 else 0

        self.total_tasks_label.setText(f"Total Tasks: {total_tasks}")
        self.total_points_label.setText(f"Total Points: {total_points:.2f}")
        self.avg_duration_label.setText(f"Avg Duration: {avg_duration:.2f} hrs")