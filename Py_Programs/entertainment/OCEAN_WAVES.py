""" Created by: AK1R4S4T0H
"""
import os
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog, QDockWidget, QLabel, QSpinBox, QPushButton, QVBoxLayout, QApplication, QMainWindow, QWidget
from OCEAN import Waves
import numpy as np

os.environ['QT_QPA_PLATFORM'] = 'xcb'
class SettingsDialog(QDialog):
    settingsChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")

        self.channels_spinbox = QSpinBox()
        self.channels_spinbox.setRange(1, 10)
        self.channels_spinbox.setValue(Waves.WaveformWidget.CHANNELS)

        self.sample_rate_spinbox = QSpinBox()
        self.sample_rate_spinbox.setRange(1, 100000)
        self.sample_rate_spinbox.setValue(Waves.WaveformWidget.SAMPLE_RATE)

        # self.block_size_spinbox = QSpinBox()
        # self.block_size_spinbox.setRange(1, 4096)
        # self.block_size_spinbox.setValue(Waves.WaveformWidget.BLOCK_SIZE)

        self.num_waveforms_spinbox = QSpinBox()
        self.num_waveforms_spinbox.setRange(1, 20)
        self.num_waveforms_spinbox.setValue(Waves.WaveformWidget.NUM_WAVEFORMS)

        self.line_width_spinbox = QSpinBox()
        self.line_width_spinbox.setRange(1, 10)
        self.line_width_spinbox.setValue(Waves.WaveformWidget.LINE_WIDTH)

        self.low_freq_spinbox = QSpinBox()
        self.low_freq_spinbox.setRange(1, 10000)
        self.low_freq_spinbox.setValue(Waves.WaveformWidget.LOW_FREQ)

        self.high_freq_spinbox = QSpinBox()
        self.high_freq_spinbox.setRange(1, 10000)
        self.high_freq_spinbox.setValue(Waves.WaveformWidget.HIGH_FREQ)

        self.num_freq_bins_spinbox = QSpinBox()
        self.num_freq_bins_spinbox.setRange(1, 10000)
        self.num_freq_bins_spinbox.setValue(Waves.WaveformWidget.NUM_FREQ_BINS)

        self.save_button = QPushButton("Update")
        self.save_button.clicked.connect(self.save_settings)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Channels:"))
        layout.addWidget(self.channels_spinbox)
        layout.addWidget(QLabel("Sample Rate:"))
        layout.addWidget(self.sample_rate_spinbox)
        # layout.addWidget(QLabel("Block Size:"))
        # layout.addWidget(self.block_size_spinbox)
        layout.addWidget(QLabel("Number of Waveforms:"))
        layout.addWidget(self.num_waveforms_spinbox)
        layout.addWidget(QLabel("Line Width:"))
        layout.addWidget(self.line_width_spinbox)
        layout.addWidget(QLabel("Low Frequency:"))
        layout.addWidget(self.low_freq_spinbox)
        layout.addWidget(QLabel("High Frequency:"))
        layout.addWidget(self.high_freq_spinbox)
        layout.addWidget(QLabel("Frequency Bins:"))
        layout.addWidget(self.num_freq_bins_spinbox)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_settings(self):
        channels = self.channels_spinbox.value()
        sample_rate = self.sample_rate_spinbox.value()
        # block_size = self.block_size_spinbox.value()
        num_waveforms = self.num_waveforms_spinbox.value()
        line_width = self.line_width_spinbox.value()
        low_freq = self.low_freq_spinbox.value()
        high_freq = self.high_freq_spinbox.value()
        num_freq_bins = self.num_freq_bins_spinbox.value()

        Waves.WaveformWidget.CHANNELS = channels
        Waves.WaveformWidget.SAMPLE_RATE = sample_rate
        # Waves.WaveformWidget.BLOCK_SIZE = block_size
        Waves.WaveformWidget.NUM_WAVEFORMS = num_waveforms
        Waves.WaveformWidget.LINE_WIDTH = line_width
        Waves.WaveformWidget.LOW_FREQ = low_freq
        Waves.WaveformWidget.HIGH_FREQ = high_freq
        Waves.WaveformWidget.NUM_FREQ_BINS = num_freq_bins

        self.settingsChanged.emit()


class SettingsDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidget(SettingsDialog())

        self.setWindowTitle("Settings")
        self.setAllowedAreas(Qt.LeftDockWidgetArea)

        self.setFeatures(self.features() & QDockWidget.DockWidgetClosable)

    def closeEvent(self, event):
        event.ignore()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.addWidget(Waves.WaveformWidget())

        settings_dock = SettingsDockWidget()
        self.addDockWidget(Qt.LeftDockWidgetArea, settings_dock)

        settings_dock.widget().settingsChanged.connect(self.update_settings)

        self.setWindowTitle("OCEAN.Waves")
        self.setGeometry(100, 100, 770, 500)

    def update_settings(self):
        print("Settings Updated!")
        print("")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()