import os
import sys
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QIcon, QColor, QPalette, QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QStyleFactory, QSlider,
    QMessageBox, QGridLayout, QLineEdit, QListWidget, QListWidgetItem
)
import pygame

os.environ['QT_QPA_PLATFORM'] = 'xcb'

class Audio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music")
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowOpacity(0.75)
        self.setGeometry(100, 100, 500, 230)
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

        layout = QGridLayout(central_widget)
        layout.setContentsMargins(10, 5, 5, 10)

        font = QFont("Helvetica", 13, QFont.Bold)

        self.file_label = QLabel("Please choose a song:", self)
        self.file_label.setFont(font)

        self.file_button = QPushButton("Browse", self)
        self.file_button.clicked.connect(self.browse_folder)
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

        self.forward_button = QPushButton("➡️", self)
        self.forward_button.clicked.connect(self.forward)
        self.forward_button.setFont(font)
        self.forward_button.setStyleSheet("""
            QPushButton:hover {
                background-color: #888888;
            }
        """)

        self.back_button = QPushButton("⬅️", self)
        self.back_button.clicked.connect(self.back)
        self.back_button.setFont(font)
        self.back_button.setStyleSheet("""
            QPushButton:hover {
                background-color: #888888;
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

        self.song_picker = QLineEdit(self)
        self.song_picker.setReadOnly(True)

        self.song_list_widget = QListWidget(self)
        self.song_list_widget.itemClicked.connect(self.select_song)

        layout.addWidget(self.file_label, 0, 0, 1, 3)
        layout.addWidget(self.file_button, 1, 0, 1, 3)
        layout.addWidget(self.song_picker, 2, 0, 1, 3)
        layout.addWidget(self.song_list_widget, 3, 0, 1, 3)
        layout.addWidget(self.play_button, 4, 0)
        layout.addWidget(self.pause_button, 4, 1)
        layout.addWidget(self.stop_button, 4, 2)
        layout.addWidget(self.back_button, 5, 1)
        layout.addWidget(self.forward_button, 5, 2)
        layout.addWidget(self.volume_label, 5, 0)
        layout.addWidget(self.volume_slider, 6, 0, 2, 3)

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

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.song_picker.setText(folder_path)
            self.load_songs(folder_path)

    def load_songs(self, folder_path):
        self.song_list_widget.clear()
        files = QDir(folder_path).entryList(["*.mp3"], QDir.Files)
        for file in files:
            song_path = os.path.join(folder_path, file)
            name = song_path.split("/")[-1]
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, song_path)
            self.song_list_widget.addItem(item)

    def select_song(self, item):
        self.file_path = item.data(Qt.UserRole)
        self.file_label.setText("Song: " + item.text())

    def play(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            if self.file_path:
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

    def forward(self):
        if pygame.mixer.music.get_busy() and not self.paused:
            current_index = self.song_list_widget.currentRow()
            next_index = current_index + 1
            if next_index < self.song_list_widget.count():
                next_item = self.song_list_widget.item(next_index)
                self.song_list_widget.setCurrentItem(next_item)
                self.file_path = next_item.data(Qt.UserRole)
                self.file_label.setText("Song: " + next_item.text())
                pygame.mixer.music.load(self.file_path)
                pygame.mixer.music.play()

    def back(self):
        if pygame.mixer.music.get_busy() and not self.paused:
            current_index = self.song_list_widget.currentRow()
            prev_index = current_index - 1
            if prev_index >= 0:
                prev_item = self.song_list_widget.item(prev_index)
                self.song_list_widget.setCurrentItem(prev_item)
                self.file_path = prev_item.data(Qt.UserRole)
                self.file_label.setText("Song: " + prev_item.text())
                pygame.mixer.music.load(self.file_path)
                pygame.mixer.music.play()
    def set_volume(self, value):
        pygame.mixer.music.set_volume(value / 100)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
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
