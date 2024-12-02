from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout, \
    QDialog, QTableWidget, QTableWidgetItem


class SkillMasteryTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()

        # Skill mastery inputs
        self.skill_area_input = QLineEdit()
        self.max_points_input = QLineEdit()
        self.points_earned_input = QLineEdit()
        self.proficiency_level_input = QLineEdit()

        # Add inputs to form layout
        self.form_layout.addRow("Skill Area:", self.skill_area_input)
        self.form_layout.addRow("Max Points:", self.max_points_input)
        self.form_layout.addRow("Points Earned:", self.points_earned_input)
        self.form_layout.addRow("Proficiency Level:", self.proficiency_level_input)

        # Add skill button
        self.add_skill_btn = QPushButton("Add Skill")
        self.add_skill_btn.clicked.connect(self.add_skill)
        self.form_layout.addRow(self.add_skill_btn)

        self.layout.addLayout(self.form_layout)

        # Skill mastery table
        self.skill_table = QTableWidget()
        self.layout.addWidget(self.skill_table)

        # Reload button
        self.reload_btn = QPushButton("Reload")
        self.reload_btn.clicked.connect(self.load_skills)
        self.layout.addWidget(self.reload_btn)

        self.setLayout(self.layout)

        self.load_skills()

    def add_skill(self):
        # Form validation
        if not all([self.skill_area_input.text(), self.max_points_input.text(), self.points_earned_input.text(),
                    self.proficiency_level_input.text()]):
            QMessageBox.warning(self, "Validation Error", "All fields are required.")
            return

        try:
            max_points = float(self.max_points_input.text())
            points_earned = float(self.points_earned_input.text())
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Points fields must be numeric.")
            return

        # Insert into database
        self.parent.cursor.execute('''
        INSERT INTO skill_mastery (skill_area, max_points, points_earned, proficiency_level)
        VALUES (?, ?, ?, ?)
        ''', (
            self.skill_area_input.text(), max_points, points_earned,
            self.proficiency_level_input.text()
        ))

        self.parent.conn.commit()

        self.load_skills()
        QMessageBox.information(self, "Success", "Skill added successfully!")

    def load_skills(self):
        # Load skills from database and display them in table
        self.parent.cursor.execute('SELECT * FROM skill_mastery')
        skills = self.parent.cursor.fetchall()

        self.skill_table.setRowCount(len(skills))
        self.skill_table.setColumnCount(5)
        self.skill_table.setHorizontalHeaderLabels(
            ["ID", "Skill Area", "Max Points", "Points Earned", "Proficiency Level"])

        for row, skill in enumerate(skills):
            for col, data in enumerate(skill):
                self.skill_table.setItem(row, col, QTableWidgetItem(str(data)))

            edit_button = QPushButton("Edit")
            edit_button.setStyleSheet("background-color: green;")
            edit_button.clicked.connect(lambda ch, skill=skill: self.edit_skill_dialog(skill))

            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("background-color: red;")
            delete_button.clicked.connect(lambda ch, skill_id=skill[0]: self.delete_skill(skill_id))

            self.skill_table.setCellWidget(row, 5, edit_button)
            self.skill_table.setCellWidget(row, 6, delete_button)

    def edit_skill_dialog(self, skill):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Skill")

        form_layout = QFormLayout()

        skill_area_input = QLineEdit(skill[1])
        max_points_input = QLineEdit(str(skill[2]))
        points_earned_input = QLineEdit(str(skill[3]))
        proficiency_level_input = QLineEdit(skill[4])

        form_layout.addRow("Skill Area:", skill_area_input)
        form_layout.addRow("Max Points:", max_points_input)
        form_layout.addRow("Points Earned:", points_earned_input)
        form_layout.addRow("Proficiency Level:", proficiency_level_input)

        save_button = QPushButton("Save")
        save_button.clicked.connect(
            lambda: self.save_skill(skill[0], skill_area_input, max_points_input, points_earned_input,
                                    proficiency_level_input, dialog))

        form_layout.addRow(save_button)

        dialog.setLayout(form_layout)
        dialog.exec()

    def save_skill(self, skill_id, skill_area_input, max_points_input, points_earned_input, proficiency_level_input,
                   dialog):
        # Validate form inputs
        if not all([skill_area_input.text(), max_points_input.text(), points_earned_input.text(),
                    proficiency_level_input.text()]):
            QMessageBox.warning(self, "Validation Error", "All fields are required.")
            return

        try:
            max_points = float(max_points_input.text())
            points_earned = float(points_earned_input.text())
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Points fields must be numeric.")
            return

        # Update skill in database
        self.parent.cursor.execute('''
        UPDATE skill_mastery
        SET skill_area = ?, max_points = ?, points_earned = ?, proficiency_level = ?
        WHERE id = ?
        ''', (
            skill_area_input.text(), max_points, points_earned,
            proficiency_level_input.text(), skill_id
        ))

        self.parent.conn.commit()

        dialog.accept()
        self.load_skills()
        QMessageBox.information(self, "Success", "Skill updated successfully!")

    def delete_skill(self, skill_id):
        self.parent.cursor.execute('DELETE FROM skill_mastery WHERE id = ?', (skill_id,))
        self.parent.conn.commit()
        self.load_skills()
        QMessageBox.information(self, "Success", "Skill deleted successfully!")
