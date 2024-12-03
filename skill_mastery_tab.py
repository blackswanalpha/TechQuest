from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFormLayout, QTableWidget,
    QTableWidgetItem, QDialog, QProgressBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class SkillMasteryTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Title
        title_label = QLabel("Skill Mastery Tracker")
        title_label.setFont(QFont('Arial', 16))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Input Layout
        input_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)

        # Input Fields
        input_fields = [
            ("Skill Area", "skill_area"),
            ("Max Points", "max_points"),
            ("Points Earned", "points_earned"),
            ("Proficiency Level", "proficiency_level")
        ]

        self.input_widgets = {}
        for label_text, field_name in input_fields:
            field_layout = QVBoxLayout()
            label = QLabel(label_text)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Enter {label_text.lower()}")

            field_layout.addWidget(label)
            field_layout.addWidget(line_edit)
            input_layout.addLayout(field_layout)

            self.input_widgets[field_name] = line_edit

        # Add Skill Button
        add_skill_btn = QPushButton("Add Skill")
        add_skill_btn.clicked.connect(self.add_skill)
        main_layout.addWidget(add_skill_btn)

        # Skills Table
        self.skills_table = QTableWidget()
        self.skills_table.setColumnCount(7)
        self.skills_table.setHorizontalHeaderLabels([
            "ID", "Skill Area", "Max Points", "Points Earned",
            "Progress", "Proficiency Level", "Actions"
        ])
        main_layout.addWidget(self.skills_table)

        # Load initial skills
        self.load_skills()

    def add_skill(self):
        # Gather input values
        inputs = {k: v.text().strip() for k, v in self.input_widgets.items()}

        # Validate inputs
        if not all(inputs.values()):
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        try:
            max_points = float(inputs['max_points'])
            points_earned = float(inputs['points_earned'])
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Points must be numeric!")
            return

        # Insert into database
        self.parent.cursor.execute('''
        INSERT INTO skill_mastery 
        (skill_area, max_points, points_earned, proficiency_level) 
        VALUES (?, ?, ?, ?)
        ''', (
            inputs['skill_area'], max_points, points_earned,
            inputs['proficiency_level']
        ))
        self.parent.conn.commit()

        # Clear input fields
        for field in self.input_widgets.values():
            field.clear()

        # Reload skills table
        self.load_skills()
        QMessageBox.information(self, "Success", "Skill added successfully!")

    def load_skills(self):
        # Clear existing table contents
        self.skills_table.setRowCount(0)

        # Fetch skills from database
        self.parent.cursor.execute('SELECT * FROM skill_mastery')
        skills = self.parent.cursor.fetchall()

        # Populate table
        for skill in skills:
            row_position = self.skills_table.rowCount()
            self.skills_table.insertRow(row_position)

            # Add skill details to table
            for col, value in enumerate(skill):
                self.skills_table.setItem(
                    row_position, col,
                    QTableWidgetItem(str(value))
                )

            # Progress Bar
            progress_widget = QWidget()
            progress_layout = QHBoxLayout(progress_widget)
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)

            # Calculate progress percentage
            progress_percentage = int((skill[3] / skill[2]) * 100) if skill[2] > 0 else 0
            progress_bar.setValue(progress_percentage)
            progress_label = QLabel(f"{progress_percentage}%")

            progress_layout.addWidget(progress_bar)
            progress_layout.addWidget(progress_label)
            progress_layout.setContentsMargins(0, 0, 0, 0)
            self.skills_table.setCellWidget(row_position, 4, progress_widget)

            # Action Buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)

            # Edit Button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, s=skill: self.edit_skill_dialog(s))

            # Delete Button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, skill_id=skill[0]: self.delete_skill(skill_id))

            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_layout.setContentsMargins(0, 0, 0, 0)
            self.skills_table.setCellWidget(row_position, 6, action_widget)

    def edit_skill_dialog(self, skill):
        # Create edit dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Skill")
        layout = QFormLayout()

        # Input fields pre-filled with current skill data
        skill_area = QLineEdit(str(skill[1]))
        max_points = QLineEdit(str(skill[2]))
        points_earned = QLineEdit(str(skill[3]))
        proficiency_level = QLineEdit(str(skill[4]))

        layout.addRow("Skill Area:", skill_area)
        layout.addRow("Max Points:", max_points)
        layout.addRow("Points Earned:", points_earned)
        layout.addRow("Proficiency Level:", proficiency_level)

        # Save button
        save_btn = QPushButton("Save Changes")
        save_btn.clicked.connect(lambda: self.save_skill(
            skill[0], skill_area, max_points, points_earned, proficiency_level, dialog
        ))
        layout.addRow(save_btn)

        dialog.setLayout(layout)
        dialog.exec()

    def save_skill(self, skill_id, skill_area, max_points, points_earned, proficiency_level, dialog):
        # Validate inputs
        if not all([skill_area.text(), max_points.text(),
                    points_earned.text(), proficiency_level.text()]):
            QMessageBox.warning(self, "Validation Error", "All fields are required.")
            return

        try:
            max_points_val = float(max_points.text())
            points_earned_val = float(points_earned.text())
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Points fields must be numeric.")
            return

        # Update in database
        self.parent.cursor.execute('''
        UPDATE skill_mastery
        SET skill_area = ?, max_points = ?, points_earned = ?, proficiency_level = ?
        WHERE id = ?
        ''', (
            skill_area.text(), max_points_val, points_earned_val,
            proficiency_level.text(), skill_id
        ))

        self.parent.conn.commit()

        # Close dialog and reload skills
        dialog.accept()
        self.load_skills()
        QMessageBox.information(self, "Success", "Skill updated successfully!")

    def delete_skill(self, skill_id):
        # Confirmation dialog
        reply = QMessageBox.question(
            self, 'Delete Skill',
            'Are you sure you want to delete this skill?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Delete from database
            self.parent.cursor.execute('DELETE FROM skill_mastery WHERE id = ?', (skill_id,))
            self.parent.conn.commit()

            # Reload skills
            self.load_skills()
            QMessageBox.information(self, "Success", "Skill deleted successfully!")