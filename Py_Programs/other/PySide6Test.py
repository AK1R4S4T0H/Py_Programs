import sys
import os
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QFile
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QRadioButton, QStyleFactory, QMenu,
    QFrame, QPushButton, QPlainTextEdit, QStyle, QMenuBar, QStatusBar,
    QMessageBox, QProgressBar
)


os.environ['QT_QPA_PLATFORM'] = 'xcb'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Test Page")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon("icon.png"))
        style_file = QFile("Py_Programs/style.qss")
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_sheet = style_file.readAll()
            style_file.close()
            style_sheet = str(style_sheet, encoding='utf-8')
            self.setStyleSheet(style_sheet)
        else:
            print("Failed to open style.qss")

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Input area
        input_frame = QFrame()
        input_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        layout.addWidget(input_frame)
        input_layout = QHBoxLayout(input_frame)
        input_layout.addWidget(QLabel("Name:"))
        self.name_entry = QLineEdit()
        input_layout.addWidget(self.name_entry)

        # Text display area
        text_frame = QFrame()
        text_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        layout.addWidget(text_frame)
        text_layout = QVBoxLayout(text_frame)
        self.output_label = QLabel("Output:")
        text_layout.addWidget(self.output_label)
        self.output_text = QPlainTextEdit()
        self.output_text.setReadOnly(True)
        text_layout.addWidget(self.output_text)

        # Buttons
        button_frame = QFrame()
        button_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        layout.addWidget(button_frame)
        button_layout = QHBoxLayout(button_frame)
        self.show_button = QPushButton("Show")
        self.clear_button = QPushButton("Clear")
        self.progress_button = QPushButton("Start Progress")
        self.animate_button = QPushButton("Animate")
        button_layout.addWidget(self.show_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.progress_button)
        button_layout.addWidget(self.animate_button)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Menu bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.file_menu = self.menu_bar.addMenu("File")
        self.edit_menu = self.menu_bar.addMenu("Edit")

        # Status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Connect signals to slots
        self.show_button.clicked.connect(self.show_output)
        self.clear_button.clicked.connect(self.clear_output)
        self.progress_button.clicked.connect(self.start_progress)
        self.animate_button.clicked.connect(self.start_animation)

    def show_output(self):
        name = self.name_entry.text()
        self.output_text.setPlainText(f"Hello, {name}!")

    def clear_output(self):
        self.name_entry.clear()
        self.output_text.clear()

    def start_progress(self):
        self.progress_bar.setValue(0)
        for i in range(101):
            self.progress_bar.setValue(i)
            QApplication.processEvents()

    def start_animation(self):
        animation = QPropertyAnimation(self.animate_button, b"geometry")
        animation.setDuration(1000)
        animation.setStartValue(self.animate_button.geometry())
        animation.setEndValue(QRect(200, 200, 100, 50))
        animation.start(QPropertyAnimation.DeleteWhenStopped)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle(QStyleFactory.create("Fusion"))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
