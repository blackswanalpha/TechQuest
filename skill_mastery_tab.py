from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem


class SkillMasteryTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        layout = QVBoxLayout()

        # Skill Mastery Table
        self.skill_table = QTableWidget()
        self.skill_table.setColumnCount(5)
        self.skill_table.setHorizontalHeaderLabels([
            "Skill Area", "Max Points",
            "Points Earned", "Proficiency", "Progress"
        ])

        # Initialize default skills
        default_skills = [
            ("DevOps", 500),
            ("Next.js", 500),
            ("Microservices", 500),
            ("CI/CD", 500),
            ("Kubernetes", 500),
            ("Project Management", 500)
        ]

        for skill, max_points in default_skills:
            self.parent.cursor.execute('''
            INSERT OR IGNORE INTO skill_mastery (skill_area, max_points, points_earned, proficiency_level)
            VALUES (?, ?, 0, 'Beginner')
            ''', (skill, max_points))

        self.parent.conn.commit()

        self.load_skills()

        layout.addWidget(self.skill_table)
        self.setLayout(layout)

    def load_skills(self):
        """Load skills from the database into the table"""
        self.skill_table.setRowCount(0)
        self.parent.cursor.execute("SELECT * FROM skill_mastery")
        skills = self.parent.cursor.fetchall()

        for row_number, row_data in enumerate(skills):
            self.skill_table.insertRow(row_number)
            for column_number, data in enumerate(row_data[1:]):
                self.skill_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
