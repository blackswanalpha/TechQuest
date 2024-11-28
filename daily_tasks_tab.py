from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QDialog, QFormLayout,
    QLineEdit, QComboBox, QLabel, QMessageBox, QTextEdit, QHBoxLayout, QFrame, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class DailyTasksTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.layout = QVBoxLayout()

        # Add Task Button
        add_task_btn = QPushButton("Add New Task")
        add_task_btn.clicked.connect(self.open_add_task_dialog)

        # Scroll Area to hold the cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout()
        self.cards_container.setLayout(self.cards_layout)

        self.scroll_area.setWidget(self.cards_container)

        self.layout.addWidget(add_task_btn)
        self.layout.addWidget(self.scroll_area)

        self.setLayout(self.layout)

        # Load tasks from the database
        self.load_tasks()

    def load_tasks(self):
        # Clear current cards
        for i in reversed(range(self.cards_layout.count())):
            self.cards_layout.itemAt(i).widget().setParent(None)

        self.parent.cursor.execute("SELECT * FROM daily_tasks")
        tasks = self.parent.cursor.fetchall()

        for task in tasks:
            card = self.create_task_card(task)
            self.cards_layout.addWidget(card)

    def create_task_card(self, task):
        card = QFrame()
        card.setFrameShape(QFrame.Shape.Box)
        card.setLineWidth(2)

        layout = QGridLayout()

        date_label = QLabel(f"Date: {task[1]}")
        category_label = QLabel(f"Category: {task[2]}")
        task_label = QLabel(f"Task: {task[3]}")
        planned_duration_label = QLabel(f"Planned Duration: {task[4]}")
        actual_duration_label = QLabel(f"Actual Duration: {task[5]}")
        status_label = QLabel(f"Status: {task[6]}")
        complexity_label = QLabel(f"Complexity: {task[7]}")
        points_earned_label = QLabel(f"Points Earned: {task[8]}")
        notes_label = QLabel(f"Notes: {task[9]}")

        layout.addWidget(date_label, 0, 0)
        layout.addWidget(category_label, 0, 1)
        layout.addWidget(task_label, 1, 0, 1, 2)
        layout.addWidget(planned_duration_label, 2, 0)
        layout.addWidget(actual_duration_label, 2, 1)
        layout.addWidget(status_label, 3, 0)
        layout.addWidget(complexity_label, 3, 1)
        layout.addWidget(points_earned_label, 4, 0)
        layout.addWidget(notes_label, 4, 1, 1, 2)

        # Action buttons
        action_layout = QHBoxLayout()
        edit_btn = QPushButton("Edit")
        edit_btn.setStyleSheet("background-color: green; color: white;")
        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("background-color: red; color: white;")

        edit_btn.clicked.connect(lambda _, t=task: self.open_edit_task_dialog(t))
        delete_btn.clicked.connect(lambda _, t=task: self.open_delete_task_dialog(t))

        action_layout.addWidget(edit_btn)
        action_layout.addWidget(delete_btn)

        layout.addLayout(action_layout, 5, 0, 1, 2)

        card.setLayout(layout)
        return card

    def open_add_task_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Task")

        layout = QFormLayout()

        # Input fields
        date_input = QLineEdit(datetime.now().strftime("%Y-%m-%d"))
        category_input = QComboBox()
        category_input.addItems([
            "DevOps", "Next.js", "Microservices",
            "CI/CD", "Kubernetes", "Project Management"
        ])

        task_input = QLineEdit()
        planned_duration_input = QLineEdit()
        actual_duration_input = QLineEdit()

        complexity_input = QComboBox()
        complexity_input.addItems([str(i) for i in range(1, 6)])

        status_input = QComboBox()
        status_input.addItems([
            "Not Started", "In Progress",
            "Partially Completed", "Completed"
        ])

        notes_input = QTextEdit()

        # Add inputs to layout
        layout.addRow("Date:", date_input)
        layout.addRow("Category:", category_input)
        layout.addRow("Task:", task_input)
        layout.addRow("Planned Duration (hours):", planned_duration_input)
        layout.addRow("Actual Duration (hours):", actual_duration_input)
        layout.addRow("Complexity:", complexity_input)
        layout.addRow("Status:", status_input)
        layout.addRow("Notes:", notes_input)

        # Save button
        save_btn = QPushButton("Save Task")
        save_btn.clicked.connect(lambda: self.save_task(
            dialog, date_input.text(), category_input.currentText(), task_input.text(),
            planned_duration_input.text(), actual_duration_input.text(), complexity_input.currentText(),
            status_input.currentText(), notes_input.toPlainText()
        ))

        layout.addRow(save_btn)

        dialog.setLayout(layout)
        dialog.exec()

    def save_task(self, dialog, date, category, task, planned_duration, actual_duration, complexity, status, notes):
        # Form validation
        if not all([date, category, task, planned_duration, complexity, status]):
            QMessageBox.warning(self, "Validation Error",
                                "All fields except 'Notes' and 'Actual Duration' are required.")
            return

        try:
            planned_duration = float(planned_duration)
            actual_duration = float(actual_duration) if actual_duration else 0
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Duration fields must be numeric.")
            return

        # Calculate points based on status and complexity
        points_calculation = {
            "Not Started": 0,
            "Partially Completed": int(complexity) * 0.5,
            "In Progress": int(complexity) * 0.75,
            "Completed": int(complexity) * 1.0
        }

        points_earned = points_calculation.get(status, 0)

        # Save to database
        self.parent.cursor.execute('''
        INSERT INTO daily_tasks 
        (date, task_category, task_description, planned_duration, actual_duration, 
        complexity, status, points_earned, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            date, category, task, planned_duration, actual_duration,
            complexity, status, points_earned, notes
        ))

        self.parent.conn.commit()

        # Refresh cards
        self.load_tasks()
        dialog.accept()
        QMessageBox.information(self, "Success", "Task added successfully!")

    def open_edit_task_dialog(self, task):
        task_id = task[0]

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Task")

        layout = QFormLayout()

        # Input fields
        date_input = QLineEdit(task[1])
        category_input = QComboBox()
        category_input.addItems([
            "DevOps", "Next.js", "Microservices",
            "CI/CD", "Kubernetes", "Project Management"
        ])
        category_input.setCurrentText(task[2])

        task_input = QLineEdit(task[3])
        planned_duration_input = QLineEdit(str(task[4]))
        actual_duration_input = QLineEdit(str(task[5]))

        complexity_input = QComboBox()
        complexity_input.addItems([str(i) for i in range(1, 6)])
        complexity_input.setCurrentText(str(task[7]))

        status_input = QComboBox()
        status_input.addItems([
            "Not Started", "In Progress",
            "Partially Completed", "Completed"
        ])
        status_input.setCurrentText(task[6])

        notes_input = QTextEdit(task[9])

        # Add inputs to layout
        layout.addRow("Date:", date_input)
        layout.addRow("Category:", category_input)
        layout.addRow("Task:", task_input)
        layout.addRow("Planned Duration (hours):", planned_duration_input)
        layout.addRow("Actual Duration (hours):", actual_duration_input)
        layout.addRow("Complexity:", complexity_input)
        layout.addRow("Status:", status_input)
        layout.addRow("Notes:", notes_input)

        # Save button
        save_btn = QPushButton("Save Task")
        save_btn.clicked.connect(lambda: self.update_task(
            dialog, task_id, date_input.text(), category_input.currentText(), task_input.text(),
            planned_duration_input.text(), actual_duration_input.text(), complexity_input.currentText(),
            status_input.currentText(), notes_input.toPlainText()
        ))

        layout.addRow(save_btn)

        dialog.setLayout(layout)
        dialog.exec()

    def update_task(self, dialog, task_id, date, category, task, planned_duration, actual_duration, complexity, status,
                    notes):
        # Form validation
        if not all([date, category, task, planned_duration, complexity, status]):
            QMessageBox.warning(self, "Validation Error",
                                "All fields except 'Notes' and 'Actual Duration' are required.")
            return

        try:
            planned_duration = float(planned_duration)
            actual_duration = float(actual_duration) if actual_duration else 0
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Duration fields must be numeric.")
            return

        # Calculate points based on status and complexity
        points_calculation = {
            "Not Started": 0,
            "Partially Completed": int(complexity) * 0.5,
            "In Progress": int(complexity) * 0.75,
            "Completed": int(complexity) * 1.0
        }

        points_earned = points_calculation.get(status, 0)

        # Update in database
        self.parent.cursor.execute('''
        UPDATE daily_tasks
        SET date=?, task_category=?, task_description=?, planned_duration=?, actual_duration=?, 
            complexity=?, status=?, points_earned=?, notes=?
        WHERE id=?
        ''', (
            date, category, task, planned_duration, actual_duration,
            complexity, status, points_earned, notes, task_id
        ))

        self.parent.conn.commit()

        # Refresh cards
        self.load_tasks()
        dialog.accept()
        QMessageBox.information(self, "Success", "Task updated successfully!")

    def open_delete_task_dialog(self, task):
        task_id = task[0]

        reply = QMessageBox.question(
            self, "Delete Task", "Are you sure you want to delete this task?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.parent.cursor.execute("DELETE FROM daily_tasks WHERE id=?", (task_id,))
            self.parent.conn.commit()

            # Refresh cards
            self.load_tasks()
            QMessageBox.information(self, "Success", "Task deleted successfully!")
