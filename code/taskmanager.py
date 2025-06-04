import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem
)
from PyQt6.QtGui import QFont

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Eingabefeld
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Neuen Task eingeben...")
        layout.addWidget(self.task_input)

        # Aufgabenliste
        self.task_list = QListWidget(self)
        layout.addWidget(self.task_list)

        self.setLayout(layout)

        # Floating Action Button (FAB)
        self.fab = QPushButton("+", self)
        self.fab.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.fab.setFixedSize(60, 60)
        self.fab.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 30px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.fab.clicked.connect(self.task_hinzufuegen)

    def resizeEvent(self, event):
        # Positioniere den FAB unten rechts
        self.fab.move(self.width() - 80, self.height() - 80)

    def task_hinzufuegen(self):
        task_text = self.task_input.text().strip()
        if task_text:
            self.task_list.addItem(QListWidgetItem(task_text))
            self.task_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenster = TaskManager()
    fenster.showMaximized()
    sys.exit(app.exec())
