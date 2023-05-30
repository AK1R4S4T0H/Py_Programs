import os
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QColor, QPalette, QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QStyleFactory, QSlider,
    QMessageBox
)
import pygame

os.environ['QT_QPA_PLATFORM'] = 'xcb'

class Audio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music")
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowOpacity(0.75)
        self.setGeometry(100, 100, 333, 230)
        self.setStyleSheet("""
            QPushButton {
                background-color: #165753;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #DD33DD;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(40, 20, 20, 40)


        font = QFont("Helvetica", 13, QFont.Bold)

        self.file_label = QLabel("Please choose a song:", self)
        self.file_label.setFont(font)

        self.file_button = QPushButton("Browse", self)
        self.file_button.clicked.connect(self.choose_file)
        self.file_button.setFont(font)

        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play)
        self.play_button.setFont(font)
        self.play_button.setStyleSheet("""
            QPushButton:hover {
                background-color:  #00DDAA;
            }
        """)

        self.pause_button = QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.pause)
        self.pause_button.setFont(font)
        self.pause_button.setStyleSheet("""
            QPushButton:hover {
                background-color: #BBDD00;
            }
        """)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setFont(font)
        self.stop_button.setStyleSheet("""
            QPushButton:hover {
                background-color: #EE1100;
            }
        """)

        self.volume_label = QLabel("Volume:", self)
        self.volume_label.setFont(font)

        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setTickInterval(1)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)
        self.volume_slider.valueChanged.connect(self.set_volume)
        layout.addWidget(self.volume_slider)

        # Variables
        self.file_path = None
        self.paused = False
        self.paused_pos = 0

        # Init pygame mixer
        pygame.mixer.init()

        # Set colors
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#7733EE"))
        palette.setColor(QPalette.Button, QColor("#7777EE"))
        palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))
        palette.setColor(QPalette.Highlight, QColor("#DD33DD"))
        palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
        self.setPalette(palette)

        layout.addWidget(self.file_label)
        layout.addWidget(self.file_button)
        layout.addWidget(self.play_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.stop_button)
        layout.addStretch(1)  # Add stretchable space
        layout.addWidget(self.volume_label)
        layout.addWidget(self.volume_slider)

    def choose_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Choose a song", "", "Audio files (*.mp3)")
        if filename:
            self.file_path = filename
            name = self.file_path.split("/")[-1]
            self.file_label.setText("Song: " + name)

    def play(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.load(self.file_path)
            pygame.mixer.music.play()

    def pause(self):
        if pygame.mixer.music.get_busy() and not self.paused:
            self.paused_pos = pygame.mixer.music.get_pos()
            pygame.mixer.music.pause()
            self.paused = True

    def stop(self):
        pygame.mixer.music.stop()
        self.paused = False

    def set_volume(self, value):
        pygame.mixer.music.set_volume(value / 100)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Exit", "Are you sure /n YOU WANT EXIT?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))

    window = Audio()
    window.show()

    sys.exit(app.exec())
