from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QGroupBox, QProgressBar, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from datetime import datetime, timedelta
import logging
import traceback


class HomeTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='development_tracker.log'
        )
        self.logger = logging.getLogger(__name__)

        # Initialize UI
        self._setup_ui()

        # Load initial data
        self.update_home_stats()

    def _setup_ui(self):
        """Set up the user interface components."""
        self.layout = QVBoxLayout()

        # Welcome Section with dynamic date
        self._create_welcome_section()

        # Quick Stats Section
        self._create_quick_stats_section()

        # Progress Overview
        self._create_skill_progress_section()

        self.setLayout(self.layout)

    def _create_welcome_section(self):
        """Create the welcome label with current date."""
        welcome_label = QLabel(
            f"Welcome to Development Tracker - {datetime.now().strftime('%B %d, %Y')}"
        )
        welcome_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #2c3e50;"
        )
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(welcome_label)

    def _create_quick_stats_section(self):
        """Create the quick stats group box."""
        quick_stats_group = QGroupBox("Quick Stats")
        quick_stats_layout = QGridLayout()

        # Define stat labels with initial values
        stat_configs = [
            ("Total Tasks", "total_tasks"),
            ("Completed Tasks", "completed_tasks"),
            ("Total Points", "total_points"),
            ("Avg Task Duration", "avg_duration")
        ]

        for i, (label_text, attr_name) in enumerate(stat_configs):
            row, col = divmod(i, 2)
            label = QLabel(f"{label_text}: 0")
            label.setStyleSheet("font-weight: bold;")
            setattr(self, f"{attr_name}_label", label)
            quick_stats_layout.addWidget(label, row, col)

        quick_stats_group.setLayout(quick_stats_layout)
        self.layout.addWidget(quick_stats_group)

    def _create_skill_progress_section(self):
        """Create skill progress bars with predefined categories."""
        progress_group = QGroupBox("Skill Progress")
        progress_layout = QVBoxLayout()

        # Predefined skill categories with default max points
        self.skill_categories = {
            "DevOps": 100,
            "Next.js": 100,
            "Microservices": 100,
            "CI/CD": 100,
            "Kubernetes": 100,
            "Project Management": 100
        }

        self.skill_progress_bars = {}

        for category, max_points in self.skill_categories.items():
            category_layout = QHBoxLayout()
            label = QLabel(f"{category}:")

            progress_bar = QProgressBar()
            progress_bar.setMaximum(100)
            progress_bar.setTextVisible(True)
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 2px solid grey;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #4CAF50;
                    width: 10px;
                    margin: 0.5px;
                }
            """)

            category_layout.addWidget(label)
            category_layout.addWidget(progress_bar)
            progress_layout.addLayout(category_layout)

            self.skill_progress_bars[category] = progress_bar

        progress_group.setLayout(progress_layout)
        self.layout.addWidget(progress_group)

    def update_home_stats(self):
        """
        Update home statistics from database with comprehensive error handling.

        Uses a try-except block to handle potential database connection or query errors.
        Logs errors and provides user feedback via message boxes.
        """
        try:
            # Validate database connection
            if not hasattr(self.parent, 'cursor'):
                raise AttributeError("Database cursor not found. Ensure database connection is established.")

            # Calculate current week's date range
            today = datetime.today()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            # Fetch weekly task statistics
            self.parent.cursor.execute('''
                SELECT 
                    COUNT(*) as total_tasks,
                    COUNT(CASE WHEN status = 'Completed' THEN 1 END) as completed_tasks,
                    COALESCE(SUM(points_earned), 0) as total_points,
                    COALESCE(AVG(actual_duration), 0) as avg_duration
                FROM daily_tasks 
                WHERE date BETWEEN ? AND ?
            ''', (start_of_week.strftime('%Y-%m-%d'), end_of_week.strftime('%Y-%m-%d')))

            task_stats = self.parent.cursor.fetchone()

            # Update task statistics labels
            self.total_tasks_label.setText(f"Total Tasks: {task_stats[0]}")
            self.completed_tasks_label.setText(f"Completed Tasks: {task_stats[1]}")
            self.total_points_label.setText(f"Total Points: {task_stats[2]:.2f}")
            self.avg_duration_label.setText(f"Avg Task Duration: {task_stats[3]:.2f} hrs")

            # Fetch skill mastery data
            self.parent.cursor.execute("""
                SELECT category, max_points, points_earned 
                FROM skill_mastery 
                WHERE category IN ({})
            """.format(','.join(f'"{cat}"' for cat in self.skill_categories.keys())))

            skill_data = self.parent.cursor.fetchall()

            # Update skill progress bars
            for category, max_points, points_earned in skill_data:
                if category in self.skill_progress_bars:
                    progress_percentage = min(
                        (points_earned / max_points) * 100 if max_points > 0 else 0,
                        100
                    )
                    self.skill_progress_bars[category].setValue(int(progress_percentage))
                    self.logger.info(f"Updated {category} progress: {progress_percentage:.2f}%")

        except Exception as e:
            error_msg = f"Error updating home stats: {str(e)}\n{traceback.format_exc()}"
            self.logger.error(error_msg)

            # Display error to user
            QMessageBox.warning(
                self,
                "Data Update Error",
                "Unable to retrieve statistics. Please check your database connection.",
                QMessageBox.StandardButton.Ok
            )