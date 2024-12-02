from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class ProgressTrackingTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.layout = QVBoxLayout()

        self.progress_label = QLabel("Progress Tracking")
        self.layout.addWidget(self.progress_label)

        # Total task points label
        self.total_task_points_label = QLabel("Total Task Points: 0")
        self.layout.addWidget(self.total_task_points_label)

        self.setLayout(self.layout)

        self.load_progress()

    def load_progress(self):
        # Calculate total task points
        self.parent.cursor.execute('SELECT SUM(points_earned) FROM daily_tasks')
        total_points = self.parent.cursor.fetchone()[0]

        if total_points is None:
            total_points = 0

        self.total_task_points_label.setText(f"Total Task Points: {total_points}")
