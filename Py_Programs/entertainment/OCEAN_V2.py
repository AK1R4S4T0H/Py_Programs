import sys
import numpy as np
import sounddevice as sd
import pygame
import pygame.locals as pg_locals
from PySide6.QtCore import Qt, QThread, Signal, QPointF, QObject
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QPainter, QColor, QPen, QPaintEvent, QImage, QPixmap, QResizeEvent


class Waves(QObject):
    class WaveformWidget(QWidget):
        # Audio settings
        CHANNELS = 7
        SAMPLE_RATE = 44100
        BLOCK_SIZE = 512

        # Visualization settings
        BACKGROUND_COLOR = (0, 0, 0)
        NUM_WAVEFORMS = 7
        WAVEFORM_COLORS = [(255, 120, 0), (255, 200, 0), (0, 255, 100), (0, 150, 255), (0, 0, 255), (255, 0, 255),
                           (255, 255, 255)]
        LINE_WIDTH = 2

        # Frequencies
        LOW_FREQ = 60
        HIGH_FREQ = 3000
        NUM_FREQ_BINS = 1700

        freq_bins = np.logspace(np.log10(LOW_FREQ), np.log10(HIGH_FREQ), NUM_FREQ_BINS)

        waveform_freq_ranges = np.linspace(LOW_FREQ, HIGH_FREQ, NUM_WAVEFORMS + 10)
        waveform_freq_ranges = list(zip(waveform_freq_ranges[:-1], waveform_freq_ranges[1:]))

        def __init__(self, parent=None):
            super().__init__(parent)

            self.setMinimumSize(220, 200)

            self.stream = sd.InputStream(callback=self.audio_capture_callback, channels=self.CHANNELS,
                                         samplerate=self.SAMPLE_RATE, blocksize=self.BLOCK_SIZE, device="pulse")
            self.stream.start()

            self.init_pygame()

            self.image = None
            self.surface = None

            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        def init_pygame(self):
            pygame.init()
            self.clock = pygame.time.Clock()
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pg_locals.RESIZABLE)
            pygame.display.set_caption("Waveform Visualization")


        def audio_capture_callback(self, indata, frames, time, status):
            audio_data = indata.mean(axis=1)
            audio_data = np.interp(np.linspace(0, len(audio_data) + 1 / 1, self.width()),
                                   np.arange(len(audio_data)), audio_data)
            scaled_data = audio_data * (self.height() / 1) + (self.height() / 20)

            waveforms = [scaled_data * (i + 1) / self.NUM_WAVEFORMS for i in range(self.NUM_WAVEFORMS)]

            self.waveforms = waveforms  # Store the waveforms as an instance variable

            self.update()

        def resizeEvent(self, event: QResizeEvent):
            width = event.size().width()
            height = event.size().height()

            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            self.image = QImage(width, height, QImage.Format_RGB32)
            self.surface = pygame.surfarray.make_surface(self.image)

        def paintEvent(self, event: QPaintEvent):
            painter = QPainter(self)

            # Handle Pygame events
            self.handle_events()

            # Convert the Pygame surface to a QPixmap
            if self.surface is not None:
                qimage = QImage(self.surface.get_buffer(), self.surface.get_width(), self.surface.get_height(),
                                QImage.Format_RGB32)
                pixmap = QPixmap.fromImage(qimage)
                painter.drawPixmap(0, 0, pixmap)

        def update_pygame_surface(self):
            if self.surface is None or self.surface.get_size() != (self.SCREEN_WIDTH, self.SCREEN_HEIGHT):
                self.image = QImage(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, QImage.Format_RGB32)
                self.surface = pygame.surfarray.make_surface(self.image)

            self.surface.fill(self.BACKGROUND_COLOR)

            # Draw the waveforms
            waveform_height = self.SCREEN_HEIGHT / self.NUM_WAVEFORMS
            for i, waveform in enumerate(self.waveforms):
                color = self.WAVEFORM_COLORS[i % len(self.WAVEFORM_COLORS)]
                pygame.draw.lines(self.surface, color, False, list(enumerate(waveform)))

            self.update()


        def handle_events(self):
            for event in pygame.event.get():
                if event.type == pg_locals.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pg_locals.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pg_locals.RESIZABLE)
                    self.image = QImage(event.w, event.h, QImage.Format_RGB32)
                    self.surface = pygame.surfarray.make_surface(self.image)


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
