import os
import sys
import pygame
from PySide6.QtCore import Qt, QDir, QUrl
from PySide6.QtGui import QIcon, QColor, QPalette, QPen, QPainter
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLabel, QSlider, QMessageBox
)
from pydub import AudioSegment

os.environ['QT_QPA_PLATFORM'] = 'xcb'


class Sampler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sampler")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Waveform visualization
        self.waveform_widget = WaveformWidget()
        layout.addWidget(self.waveform_widget)

        # Playback controls
        control_layout = QHBoxLayout()
        layout.addLayout(control_layout)

        self.load_button = QPushButton("Load Sample")
        self.load_button.clicked.connect(self.load_sample)
        control_layout.addWidget(self.load_button)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play)
        control_layout.addWidget(self.play_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop)
        control_layout.addWidget(self.stop_button)

        # Volume control
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setTickInterval(1)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)
        control_layout.addWidget(self.volume_slider)

        # Status label
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        # Audio setup
        pygame.mixer.init()

    def load_sample(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Audio File", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if file_path:
            self.current_sample = AudioSegment.from_file(file_path)
            self.waveform_widget.set_waveform(self.current_sample)
            self.status_label.setText("Sample loaded")

    def play(self):
        if hasattr(self, 'current_sample'):
            sample_array = self.current_sample.get_array_of_samples()
            if len(sample_array.shape) == 1:
                sample_array = sample_array.reshape(-1, 2)  # Reshape to 2D array for stereo mixing
            sound = pygame.sndarray.make_sound(sample_array)
            sound.set_volume(self.volume_slider.value() / 100)
            sound.play()
            self.status_label.setText("Playing")

    def stop(self):
        pygame.mixer.stop()
        self.status_label.setText("Stopped")


class WaveformWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 200)
        self.waveform = None

    def set_waveform(self, audio_segment):
        self.waveform = audio_segment
        self.update()

    def paintEvent(self, event):
        if self.waveform:
            painter = QPainter(self)
            painter.setPen(QPen(QColor(255, 255, 255)))
            width = self.width()
            height = self.height()
            for i in range(0, width, 2):
                x = i
                y = height - self.waveform[i * len(self.waveform) // width] / (2 ** 16) * height
                painter.drawLine(x, height, x, y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Sampler()
    window.show()
    sys.exit(app.exec())
