import random
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QTimer
import os

os.environ['QT_QPA_PLATFORM'] = 'xcb'
class ColorLearningApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.color_words = ['Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Purple', 'Pink']
        self.colors = [QColor('red'), QColor('green'), QColor('blue'), QColor('yellow'), QColor('orange'), QColor('purple'), QColor('pink')]

        self.setWindowTitle("Color Learning App")
        self.setGeometry(100, 100, 400, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.label = QLabel(self)
        self.label.setStyleSheet("font-size: 90px;")
        self.label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton("Show me a color!", self)
        self.button.setStyleSheet("color: #FFFFFF;background-color: #165753;font-size: 12px;padding: 5px")
        self.button.clicked.connect(self.display_color)

        layout.addWidget(self.label)
        layout.addWidget(self.button)

    def display_color(self):
        index = random.randint(0, len(self.color_words) - 1)
        color_word = self.color_words[index]
        color = self.colors[index]
        QTimer.singleShot(7000, self.display_color)

        self.label.setText(color_word)
        self.label.setStyleSheet(f"background-color: {color.name()}; color: white;font-size: 90px;")

if __name__ == "__main__":
    app = QApplication([])
    color_app = ColorLearningApp()
    color_app.show()
    app.exec()
