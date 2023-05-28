# Hex color picker and Color Picker with dropper
import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QColorDialog
from PyQt5.QtGui import QColor, QPalette, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QFile
import os

os.environ['QT_QPA_PLATFORM'] = 'xcb'
class ColorViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HEX")
        self.setGeometry(200, 200, 300, 200)
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

        self.color_label = QLabel()
        self.color_label.setAlignment(Qt.AlignCenter)
        self.color_label.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")

        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText("Enter color in hex")

        self.random_button = QPushButton("Random Color")
        self.random_button.clicked.connect(self.generate_random_color)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.show_color)

        self.pick_color_button = QPushButton("Pick Color")
        self.pick_color_button.clicked.connect(self.pick_color)

        layout = QVBoxLayout()
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.random_button)
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.pick_color_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # background color-changing
        self.background_timer = QTimer(self)
        self.background_timer.timeout.connect(self.change_background_color)
        self.background_timer.start(1500)  # 1.5 seconds

    def change_background_color(self):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)

        # Set background
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(red, green, blue))
        self.setPalette(palette)


    def generate_random_color(self):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)

        self.set_color(red, green, blue)

    def show_color(self):
        color_hex = self.color_input.text()
        if not color_hex.startswith("#"):
            color_hex = "#" + color_hex

        color = QColor(color_hex)
        if color.isValid():
            self.set_color(color.red(), color.green(), color.blue())
        else:
            self.set_color(0, 0, 0) 

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.set_color(color.red(), color.green(), color.blue())

    def set_color(self, red, green, blue):
        hex_color = "#{:02X}{:02X}{:02X}".format(red, green, blue)
        self.color_label.setText(hex_color)
        self.color_label.setStyleSheet("font-size: 24px; font-weight: bold; color: {};".format(hex_color))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ColorViewer()
    window.show()

    sys.exit(app.exec())