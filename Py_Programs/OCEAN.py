import os
import sys
import numpy as np
import sounddevice as sd
import pygame
from PySide6.QtCore import Qt, QThread, Signal, QPointF, QObject
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QPen, QPaintEvent

os.environ['QT_QPA_PLATFORM'] = 'xcb'
class Waves(QObject):
    class WaveformWidget(QWidget):
        # Audio settings
        CHANNELS = 7
        SAMPLE_RATE = 44100
        BLOCK_SIZE = 512

        # Visualization settings
        SCREEN_WIDTH = 220
        SCREEN_HEIGHT = 200
        BACKGROUND_COLOR = (0, 0, 0)
        NUM_WAVEFORMS = 7
        WAVEFORM_COLORS = [(255, 120, 0), (255, 200, 0), (0, 255, 100), (0, 150, 255), (0, 0, 255), (255, 0, 255),
                           (255, 255, 255)]
        LINE_WIDTH = 2

        # Frequencies
        FREQUENCIES = [[60, 261.63], [262, 493.66], [494, 929.63], [930, 1449.23], [1450, 2292.00], [2293, 2640.00],
                       [2641, 3193.88]]

        # Frequency settings
        LOW_FREQ = 60
        HIGH_FREQ = 3000
        NUM_FREQ_BINS = 1700

        freq_bins = np.logspace(np.log10(LOW_FREQ), np.log10(HIGH_FREQ), NUM_FREQ_BINS)

        waveform_freq_ranges = np.linspace(LOW_FREQ, HIGH_FREQ, NUM_WAVEFORMS + 10)
        waveform_freq_ranges = list(zip(waveform_freq_ranges[:-1], waveform_freq_ranges[1:]))

        pygame.init()

        def __init__(self, parent=None):
            super().__init__(parent)

            self.setMinimumSize(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

            self.stream = sd.InputStream(callback=self.audio_capture_callback, channels=self.CHANNELS,
                                         samplerate=self.SAMPLE_RATE,
                                         blocksize=self.BLOCK_SIZE, device="pulse")
            self.stream.start()

        def audio_capture_callback(self, indata, frames, time, status):
            audio_data = indata.mean(axis=1)
            audio_data = np.interp(np.linspace(0, len(audio_data) + 1 / 1, self.SCREEN_WIDTH),
                                   np.arange(len(audio_data)), audio_data)
            scaled_data = audio_data * (self.SCREEN_HEIGHT / 1) + (self.SCREEN_HEIGHT / 20)

            waveforms = [scaled_data * (i + 1) / self.NUM_WAVEFORMS for i in range(self.NUM_WAVEFORMS)]

            waveform_height = self.SCREEN_HEIGHT / self.NUM_WAVEFORMS

            self.waveforms = waveforms  # Store the waveforms as an instance variable

            self.update()

        def paintEvent(self, event: QPaintEvent):
            painter = QPainter(self)
            painter.setPen(QPen(QColor(255, 255, 255), self.LINE_WIDTH))

            # Fill the background
            painter.fillRect(event.rect(), QColor(*self.BACKGROUND_COLOR))

            waveform_height = self.SCREEN_HEIGHT / self.NUM_WAVEFORMS

            for i, waveform in enumerate(self.waveforms):

                color = QColor(*self.WAVEFORM_COLORS[i % len(self.WAVEFORM_COLORS)])
                painter.setPen(QPen(color, self.LINE_WIDTH))

                y_offset = int(i * waveform_height + waveform_height // 300000)
                scaled_waveform = waveform * (i + 15) / self.NUM_WAVEFORMS  # Adjust the scaling factor

                waveform_points = [QPointF(x, y + y_offset) for x, y in enumerate(scaled_waveform)]
                painter.drawPolyline(waveform_points)

                y_offset = int(i * waveform_height / 300 + waveform_height // 300000)
                scaled_waveform = waveform * (i + 15) / self.NUM_WAVEFORMS
                freq_range = list(self.waveform_freq_ranges)[i]

                waveform_points = [QPointF(x, y + y_offset) for x, y in enumerate(scaled_waveform)]
                painter.drawPolyline(waveform_points)

                y_offset = int(i * waveform_height / 300 + waveform_height // 300000)
                scaled_waveform = waveform * (i + 45) / self.NUM_WAVEFORMS
                freq_range = list(self.waveform_freq_ranges)[i]

                waveform_points = [QPointF(x, y + y_offset) for x, y in enumerate(scaled_waveform)]
                painter.drawPolyline(waveform_points)

                y_offset = int(i * waveform_height / 300 + waveform_height // 300000)
                scaled_waveform = waveform * (i + 75) / self.NUM_WAVEFORMS
                freq_range = list(self.waveform_freq_ranges)[i]

                waveform_points = [QPointF(x, y + y_offset) for x, y in enumerate(scaled_waveform)]
                painter.drawPolyline(waveform_points)

                y_offset = int(i * waveform_height / 300 + waveform_height // 300000)
                scaled_waveform = waveform * (i + 95) / self.NUM_WAVEFORMS
                freq_range = list(self.waveform_freq_ranges)[i]

                waveform_points = [QPointF(x, y + y_offset) for x, y in enumerate(scaled_waveform)]
                painter.drawPolyline(waveform_points)

                y_offset = int(i * waveform_height + waveform_height // 300000)
                scaled_waveform = waveform * (i + 25) / self.NUM_WAVEFORMS  # Adjust the scaling factor

                waveform_points = [QPointF(x, y + y_offset) for x, y in enumerate(scaled_waveform)]
                painter.drawPolyline(waveform_points)


        def closeEvent(self, event):
            self.stream.stop()
            self.stream.close()
            pygame.quit()

    class AudioCaptureThread(QThread):
        capture_started = Signal()
        capture_stopped = Signal()

        def run(self):
            app = QApplication([])

            self.capture_started.emit()

            sys.exit(app.exec())

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("Waveform Visualization")

            self.waveform_widget = Waves.WaveformWidget()
            layout = QVBoxLayout()
            layout.addWidget(self.waveform_widget)

            central_widget = QWidget()
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

            self.audio_capture_thread = Waves.AudioCaptureThread()
            self.audio_capture_thread.capture_started.connect(self.capture_started)
            self.audio_capture_thread.capture_stopped.connect(self.capture_stopped)
            self.audio_capture_thread.start()

        def capture_started(self):
            print("Audio capture started.")

        def capture_stopped(self):
            print("Audio capture stopped.")

        def closeEvent(self, event):
            self.audio_capture_thread.quit()
            self.audio_capture_thread.wait()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Waves.MainWindow()
    window.show()
    sys.exit(app.exec())
