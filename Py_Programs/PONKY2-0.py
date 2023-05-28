# Python Conky, PySide6
import platform
import psutil
from PySide6 import QtCore, QtGui, QtWidgets
import os

os.environ['QT_QPA_PLATFORM'] = 'xcb'

class PonkyPy(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PONKY PY")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # CPU
        self.cpu_label = QtWidgets.QLabel("CPU Usage:")
        self.layout.addWidget(self.cpu_label)

        self.cpu_meter = QtWidgets.QProgressBar()
        self.cpu_meter.setRange(0, 100)
        self.cpu_meter.setTextVisible(False)
        self.layout.addWidget(self.cpu_meter)

        # RAM
        self.ram_label = QtWidgets.QLabel("RAM Usage:")
        self.layout.addWidget(self.ram_label)

        self.ram_meter = QtWidgets.QProgressBar()
        self.ram_meter.setRange(0, 100)
        self.ram_meter.setTextVisible(False)
        self.layout.addWidget(self.ram_meter)

        # SysInfo
        self.system_label = QtWidgets.QLabel("System Information:")
        self.layout.addWidget(self.system_label)

        self.system_info = QtWidgets.QLabel()
        self.layout.addWidget(self.system_info)

        self.update_meter()

    def update_meter(self):
        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent

        self.cpu_meter.setValue(cpu_percent)
        self.ram_meter.setValue(ram_percent)

        self.cpu_label.setText(f"CPU Usage: {cpu_percent}%")
        self.ram_label.setText(f"RAM Usage: {ram_percent}%")

        QtCore.QTimer.singleShot(1000, self.update_meter)

    def run(self):
        # Retrieve SysInfo
        system_details = []
        system_details.append(f"OS: {platform.system()} {platform.release()}")
        system_details.append(f"Processor: {platform.processor()}")
        system_details.append(f"Machine: {platform.machine()}")
        system_details.append(f"System Type: {platform.architecture()[0]}")
        system_details.append(f"Memory: {round(psutil.virtual_memory().total / (1024 ** 3))} GB")
        system_details.append(f"Hostname: {platform.node()}")
        system_details.append(f"Python Version: {platform.python_version()}")

        self.system_info.setText("\n".join(system_details))

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
