from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class HomeTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        welcome_label = QLabel("Welcome to the Development Tracker!")
        instructions_label = QLabel(
            "Navigate through the tabs to manage your daily tasks, track skill mastery, and monitor your progress.")

        layout.addWidget(welcome_label)
        layout.addWidget(instructions_label)

        self.setLayout(layout)
