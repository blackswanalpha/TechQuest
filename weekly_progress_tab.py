from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView


class WeeklyProgressTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Week", "Total Possible Points", "Points Earned", "Completion Percentage"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        self.load_progress()

    def load_progress(self):
        weeks = [
            {"Week": "Week 1", "Total Possible Points": 360},
            {"Week": "Week 2", "Total Possible Points": 360},
            {"Week": "Week 3", "Total Possible Points": 360},
            {"Week": "Week 4", "Total Possible Points": 360},
            {"Week": "Week 5", "Total Possible Points": 240}
        ]

        self.table.setRowCount(len(weeks))

        for row, week in enumerate(weeks):
            self.table.setItem(row, 0, QTableWidgetItem(week["Week"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(week["Total Possible Points"])))
            self.table.setItem(row, 2, QTableWidgetItem(""))
            self.table.setItem(row, 3, QTableWidgetItem(""))

        self.update_completion_percentage()

    def update_completion_percentage(self):
        for row in range(self.table.rowCount()):
            total_possible_points = float(self.table.item(row, 1).text())
            points_earned = self.table.item(row, 2).text()

            if points_earned:
                points_earned = float(points_earned)
                completion_percentage = (points_earned / total_possible_points) * 100
                self.table.setItem(row, 3, QTableWidgetItem(f"{completion_percentage:.2f}%"))
            else:
                self.table.setItem(row, 3, QTableWidgetItem("0.00%"))
