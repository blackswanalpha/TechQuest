from PyQt6.QtWidgets import QWidget, QVBoxLayout

class ProgressTrackingTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
