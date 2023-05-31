# Python Conky, PySide6
import platform
import psutil
from PySide6 import QtCore, QtGui, QtWidgets
import os
import datetime

os.environ['QT_QPA_PLATFORM'] = 'xcb'

class CircularProgressBar(QtWidgets.QProgressBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('QProgressBar {border: none;}')
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFormat("%p%")
        self.setFixedSize(75, 75)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        radius = min(self.width(), self.height()) / 1
        pen_width = 10
        progress = 360 * self.value() / (self.maximum() - self.minimum())
        start_angle = 90 * 16  # 90 degrees
        end_angle = (90 - progress) * 16  # 90 - progress degrees

        # background circles
        painter.setPen(QtGui.QPen(QtGui.QColor(100, 100, 100), pen_width))
        painter.drawArc(pen_width / 2, pen_width / 2, radius - pen_width, radius - pen_width, 0, 360 * 16)
        
        # progress arc
        painter.setPen(QtGui.QPen(QtGui.QColor('#165753'), pen_width))
        path = QtGui.QPainterPath()
        path.arcMoveTo(pen_width / 2, pen_width / 2, radius - pen_width, radius - pen_width, start_angle)
        path.arcTo(pen_width / 2, pen_width / 2, radius - pen_width, radius - pen_width, start_angle, -progress)
        painter.drawPath(path)

        # text in the center
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
        painter.drawText(self.rect(), QtCore.Qt.AlignCenter, f"{self.value()}%")

class PonkyPy(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PONKY PY")
        self.setStyleSheet('QLabel {border: none;background: transparent;}')

        self.layout = QtWidgets.QVBoxLayout(self)

        # CPU
        self.cpu_label = QtWidgets.QLabel("CPU")
        self.cpu_label.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.cpu_label)

        self.cpu_meter = CircularProgressBar()
        self.cpu_meter.setRange(0, 100)
        self.cpu_meter.setTextVisible(False)
        self.layout.addWidget(self.cpu_meter)

        # RAM
        self.ram_label = QtWidgets.QLabel("RAM")
        self.ram_label.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.ram_label)

        self.ram_meter = CircularProgressBar()
        self.ram_meter.setRange(0, 100)
        self.ram_meter.setTextVisible(False)
        self.layout.addWidget(self.ram_meter)

        # Disk
        self.disk_label = QtWidgets.QLabel("Disk")
        self.disk_label.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.disk_label)

        self.disk_meter = CircularProgressBar()
        self.disk_meter.setRange(0, 100)
        self.disk_meter.setTextVisible(False)
        self.layout.addWidget(self.disk_meter)

        self.update_meter()

    def update_meter(self):
        # CPU
        cpu_percent = psutil.cpu_percent()
        self.cpu_meter.setValue(cpu_percent)
        self.cpu_label.setText(f"CPU:")

        # RAM
        ram_percent = psutil.virtual_memory().percent
        self.ram_meter.setValue(ram_percent)
        self.ram_label.setText(f"RAM:")

        # Disk
        disk_percent = psutil.disk_usage("/").percent
        self.disk_meter.setValue(disk_percent)
        self.disk_label.setText(f"Disk:")

        QtCore.QTimer.singleShot(1000, self.update_meter)

    def run(self):
        try:
            style_file = QtCore.QFile("Py_Programs/style.qss")
            if style_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                style_sheet = style_file.readAll()
                style_file.close()
                style_sheet = str(style_sheet, encoding='utf-8')
                self.setStyleSheet(style_sheet)
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            style_file = QtCore.QFile("style.qss")
            if style_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                style_sheet = style_file.readAll()
                style_file.close()
                style_sheet = str(style_sheet, encoding='utf-8')
                self.setStyleSheet(style_sheet)
            else:
                print("Failed to open style.qss")

        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ponky = PonkyPy()
    ponky.run()
    app.exec()
