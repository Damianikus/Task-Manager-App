import sys
from dataclasses import dataclass
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem, QDialog, QComboBox
)
from PyQt6.QtGui import QFont, QIcon

@dataclass
class Task:
    description: str
    category: str
    due_date: datetime
    priority: str

class Category:
    description: str
    imagePath: str

    def __init__(self, description, imagePath):
        self.description = description
        self.imagePath = imagePath


class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setWindowIcon(QIcon("data/random/ToDoIcon.png"))
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Aufgabenliste
        self.task_list = QListWidget(self)
        layout.addWidget(self.task_list)

        self.setLayout(layout)

        self.categories = [
            Category(description="Arbeit", imagePath="data/category/buroklammer.png"),
            Category(description="Freizeit", imagePath="data/category/gruppe.png"),
            Category(description="Uni", imagePath="data/category/study.png"),
            Category(description="Sonstige", imagePath="data/category/zufallig.png")
        ]

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
        dialog = TaskDialog(self.categories)
        if dialog.exec():  # Wenn auf "Speichern" geklickt wurde
            task_text = dialog.get_task_text()
            if task_text:
                self.task_list.addItem(QListWidgetItem(task_text))

# --- Dialog für neue Aufgabe ---
class TaskDialog(QDialog):
    def __init__(self, categories: list[Category]):
        super().__init__()
        self.setWindowTitle("Neuen Task hinzufügen")
        self.setWindowIcon(QIcon("data/random/task.png"))
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        self.task_input = QLineEdit()
        layout.addWidget(self.task_input)

        self.save_button = QPushButton("Speichern")
        self.save_button.clicked.connect(self.accept)  # Schließt Dialog mit .exec()
        layout.addWidget(self.save_button)

        self.category_box = QComboBox()
        for category in categories:  # übergeben vom Hauptfenster
            icon = QIcon(category.imagePath)
            self.category_box.addItem(icon, category.description)
        layout.addWidget(self.category_box)

        self.setLayout(layout)

    def get_task_text(self):
        return self.task_input.text().strip()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenster = TaskManager()
    fenster.showMaximized()
    sys.exit(app.exec())
