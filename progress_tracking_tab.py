from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar,
    QTableWidget, QTableWidgetItem, QGroupBox, QPushButton
)
from PyQt6.QtCore import Qt
from datetime import datetime


class ProgressTrackingTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout()

        # Overall Progress Section
        overall_progress_group = QGroupBox("Overall Progress")
        overall_progress_layout = QVBoxLayout()

        # Total Points
        self.total_points_label = QLabel("Total Points: 0")
        overall_progress_layout.addWidget(self.total_points_label)

        # Progress Bars for Different Categories
        self.progress_bars = {}
        categories = ["DevOps", "Next.js", "Microservices", "CI/CD", "Kubernetes", "Project Management"]

        for category in categories:
            category_layout = QHBoxLayout()
            label = QLabel(f"{category}:")
            progress_bar = QProgressBar()
            progress_bar.setMaximum(100)
            progress_bar.setTextVisible(True)

            category_layout.addWidget(label)
            category_layout.addWidget(progress_bar)

            overall_progress_layout.addLayout(category_layout)
            self.progress_bars[category] = progress_bar

        overall_progress_group.setLayout(overall_progress_layout)
        self.layout.addWidget(overall_progress_group)

        # Detailed Progress Table
        progress_table_group = QGroupBox("Detailed Progress")
        progress_table_layout = QVBoxLayout()

        self.progress_table = QTableWidget()
        self.progress_table.setColumnCount(5)
        self.progress_table.setHorizontalHeaderLabels(
            ["Category", "Points Earned", "Max Points", "Progress", "Proficiency"])
        progress_table_layout.addWidget(self.progress_table)

        progress_table_group.setLayout(progress_table_layout)
        self.layout.addWidget(progress_table_group)

        # Progress Report Button
        report_btn = QPushButton("Generate Progress Report")
        report_btn.clicked.connect(self.generate_progress_report)
        self.layout.addWidget(report_btn)

        self.setLayout(self.layout)

        self.load_progress()

    def load_progress(self):
        # Fetch skill mastery data
        self.parent.cursor.execute("SELECT * FROM skill_mastery")
        skill_data = self.parent.cursor.fetchall()

        # Calculate total points
        total_points = 0
        self.progress_table.setRowCount(len(skill_data))

        for row, skill in enumerate(skill_data):
            category, max_points, points_earned, proficiency = skill[1:]
            total_points += points_earned

            # Update progress table
            self.progress_table.setItem(row, 0, QTableWidgetItem(category))
            self.progress_table.setItem(row, 1, QTableWidgetItem(str(points_earned)))
            self.progress_table.setItem(row, 2, QTableWidgetItem(str(max_points)))

            progress_percentage = (points_earned / max_points) * 100 if max_points > 0 else 0
            self.progress_table.setItem(row, 3, QTableWidgetItem(f"{progress_percentage:.2f}%"))
            self.progress_table.setItem(row, 4, QTableWidgetItem(proficiency))

            # Update progress bars
            if category in self.progress_bars:
                self.progress_bars[category].setValue(int(progress_percentage))

        self.total_points_label.setText(f"Total Points: {total_points:.2f}")

    def generate_progress_report(self):
        report_dialog = QDialog(self)
        report_dialog.setWindowTitle("Progress Report")
        report_layout = QVBoxLayout()

        # Basic report details
        report_text = QTextEdit()
        report_text.setReadOnly(True)

        report_content = f"Progress Report Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        self.parent.cursor.execute("SELECT * FROM skill_mastery")
        skill_data = self.parent.cursor.fetchall()

        report_content += "Skill Mastery Breakdown:\n"
        for skill in skill_data:
            category, max_points, points_earned, proficiency = skill[1:]
            progress_percentage = (points_earned / max_points) * 100 if max_points > 0 else 0

            report_content += (f"{category}:\n"
                               f"  Points Earned: {points_earned:.2f}\n"
                               f"  Max Points: {max_points}\n"
                               f"  Progress: {progress_percentage:.2f}%\n"
                               f"  Proficiency Level: {proficiency}\n\n")

        report_text.setText(report_content)
        report_layout.addWidget(report_text)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(report_dialog.close)
        report_layout.addWidget(close_btn)

        report_dialog.setLayout(report_layout)
        report_dialog.resize(500, 600)
        report_dialog.exec()