""" Created by: AK1R4S4T0H
"""
import random
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import QTimer, Qt
import os

os.environ['QT_QPA_PLATFORM'] = 'xcb'
phrases = {'A','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w', 'x','y','z',
        'B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V', 'W','X','Y','Z',
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17','18', '19', '20'}
class ABC(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ABC's")
        self.setGeometry(100, 100, 400, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.label = QLabel(self)
        self.label.setFont("Sans")
        self.label.setStyleSheet("background-color: black; color: white;font-size: 180px;")
        self.label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton("Show me a phrase!", self)
        self.button.setStyleSheet("color: #FFFFFF;background-color: #165753;font-size: 12px;padding: 5px")
        self.button.clicked.connect(self.display_phrase)

        layout.addWidget(self.label)
        layout.addWidget(self.button)

    def display_phrase(self):
        phrase = random.choice(list(phrases))
        self.label.setText(phrase)

        QTimer.singleShot(10000, self.display_phrase)

if __name__ == "__main__":
    app = QApplication([])
    abc = ABC()
    abc.show()
    app.exec()
