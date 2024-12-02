from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt


class SkillMasteryTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Skill Area", "Max Points", "Points Earned", "Proficiency Level"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        self.load_skills()

    def load_skills(self):
        self.parent.cursor.execute("SELECT * FROM skill_mastery")
        skills = self.parent.cursor.fetchall()

        self.table.setRowCount(len(skills))

        for row, skill in enumerate(skills):
            for col, value in enumerate(skill[1:]):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        self.update_proficiency_levels()

    def update_proficiency_levels(self):
        for row in range(self.table.rowCount()):
            points_earned = float(self.table.item(row, 2).text())
            max_points = float(self.table.item(row, 1).text())
            proficiency_level = self.calculate_proficiency_level(points_earned, max_points)
            self.table.setItem(row, 3, QTableWidgetItem(proficiency_level))

    def calculate_proficiency_level(self, points_earned, max_points):
        percentage = (points_earned / max_points) * 100

        if percentage >= 90:
            return "Expert"
        elif percentage >= 75:
            return "Advanced"
        elif percentage >= 50:
            return "Intermediate"
        else:
            return "Beginner"
