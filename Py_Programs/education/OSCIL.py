""" Created by: AK1R4S4T0H
"""
import sys
import numpy as np
import pygame
from pygame.locals import *
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QSlider, QDockWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random


class OscilloscopeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.vertical_slider = QSlider(Qt.Vertical)
        self.vertical_slider.setRange(0, 100)
        self.vertical_slider.setValue(50)
        self.vertical_slider.valueChanged.connect(self.update_oscilloscope)

        self.horizontal_slider = QSlider(Qt.Horizontal)
        self.horizontal_slider.setRange(0, 100)
        self.horizontal_slider.setValue(50)
        self.horizontal_slider.valueChanged.connect(self.update_oscilloscope)

        self.knob1 = QSlider(Qt.Horizontal)
        self.knob1.setRange(0, 100)
        self.knob1.setValue(50)
        self.knob1.valueChanged.connect(self.update_oscilloscope)

        self.knob2 = QSlider(Qt.Horizontal)
        self.knob2.setRange(0, 100)
        self.knob2.setValue(50)
        self.knob2.valueChanged.connect(self.update_oscilloscope)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        knob_layout = QVBoxLayout()
        knob_layout.addWidget(QLabel("Amplitude"))
        knob_layout.addWidget(self.vertical_slider)
        knob_layout.addWidget(QLabel("Frequency"))
        knob_layout.addWidget(self.horizontal_slider)
        knob_layout.addWidget(QLabel("Knob 1"))
        knob_layout.addWidget(self.knob1)
        knob_layout.addWidget(QLabel("Knob 2"))
        knob_layout.addWidget(self.knob2)

        layout.addLayout(knob_layout)
        self.setLayout(layout)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))
        self.is_running = True

    def update_oscilloscope(self):
        vertical_value = self.vertical_slider.value() / 100
        horizontal_value = self.horizontal_slider.value() / 100
        knob1_value = self.knob1.value() / 100
        knob2_value = self.knob2.value() / 100

        x = np.linspace(0, 1, 1000)
        y = np.sin(2 * np.pi * (x + horizontal_value)) * vertical_value * knob1_value + random.uniform(-0.1, 0.1) * knob2_value

        self.ax.clear()
        self.ax.plot(x, y, 'r')
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(-1, 1)
        self.canvas.draw()

        self.screen.fill((0, 0, 0))
        waveform_height = int(self.screen.get_height() / 2)
        for i in range(1, len(x)):
            pygame.draw.line(self.screen, (255, 255, 255),
                             (int(x[i - 1] * self.screen.get_width()), waveform_height + int(y[i - 1] * waveform_height)),
                             (int(x[i] * self.screen.get_width()), waveform_height + int(y[i] * waveform_height)), 1)

        pygame.display.flip()

    def closeEvent(self, event):
        self.is_running = False
        pygame.quit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Oscilloscope")

        oscilloscope_widget = OscilloscopeWidget(self)

        dock_widget = QDockWidget("Knobs", self)
        dock_widget.setWidget(oscilloscope_widget)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock_widget)

    def closeEvent(self, event):
        self.centralWidget().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
