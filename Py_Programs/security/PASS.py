# -*- coding: utf-8 -*-
"""
Created on Wednesday March 16 2023

@author: AK1R4S4T0H
"""

# Password Generator GUI
import sys
import random
import string
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QLineEdit, QProgressBar, QWidget, QStyle
from PySide6.QtCore import QFile

class PasswordGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Generator")
        try:
            style_file = QFile("Py_Programs/style.qss")
            if style_file.open(QFile.ReadOnly | QFile.Text):
                style_sheet = style_file.readAll()
                style_file.close()
                style_sheet = str(style_sheet, encoding='utf-8')
                self.setStyleSheet(style_sheet)
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            style_file = QFile("style.qss")
            if style_file.open(QFile.ReadOnly | QFile.Text):
                style_sheet = style_file.readAll()
                style_file.close()
                style_sheet = str(style_sheet, encoding='utf-8')
                self.setStyleSheet(style_sheet)
            else:
                print("Failed to open style.qss")

        layout = QVBoxLayout()

        length_label = QLabel("Password Length:")
        layout.addWidget(length_label)

        self.length_entry = QLineEdit()
        layout.addWidget(self.length_entry)

        generate_button = QPushButton("Generate Password")
        generate_button.clicked.connect(self.generate_password)
        layout.addWidget(generate_button)

        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_entry)

        reveal_button = QPushButton("Reveal Password")
        reveal_button.clicked.connect(self.reveal_password)
        layout.addWidget(reveal_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


    def generate_password(self):
        length = int(self.length_entry.text())
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
        self.password_entry.setText(password)

    def reveal_password(self):
        self.password_entry.setEchoMode(QLineEdit.Normal)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec())
