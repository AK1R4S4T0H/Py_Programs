# Python Conky, PySide6
import platform
import psutil
from PySide6 import QtCore, QtGui, QtWidgets
import os
import datetime

os.environ['QT_QPA_PLATFORM'] = 'xcb'

class PonkyPy(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PONKY PY")

        self.layout = QtWidgets.QVBoxLayout(self)

        # User Info
        self.user_info = QtWidgets.QLabel()
        self.layout.addWidget(self.user_info)

        # System Uptime
        self.uptime_info = QtWidgets.QLabel()
        self.layout.addWidget(self.uptime_info)

        # SysInfo
        self.system_info = QtWidgets.QLabel()
        self.layout.addWidget(self.system_info)
        system_details = []
        system_details.append(f"OS: {platform.system()} {platform.release()}")
        system_details.append(f"Machine: {platform.machine()}")
        system_details.append(f"System Type: {platform.architecture()[0]}")
        system_details.append(f"Memory: {round(psutil.virtual_memory().total / (1024 ** 3))} GB")
        system_details.append(f"Hostname: {platform.node()}")
        system_details.append(f"Python Version: {platform.python_version()}")

        self.system_info.setText("\n".join(system_details))

        # CPU
        self.cpu_label = QtWidgets.QLabel("CPU Usage:")
        self.cpu_label.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.cpu_label)

        self.cpu_meter = QtWidgets.QProgressBar()
        self.cpu_meter.setRange(0, 100)
        self.cpu_meter.setTextVisible(False)
        self.layout.addWidget(self.cpu_meter)

        # RAM
        self.ram_label = QtWidgets.QLabel("RAM Usage:")
        self.ram_label.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.ram_label)

        self.ram_meter = QtWidgets.QProgressBar()
        self.ram_meter.setRange(0, 100)
        self.ram_meter.setTextVisible(False)
        self.layout.addWidget(self.ram_meter)

        # Disk
        self.disk_label = QtWidgets.QLabel("Disk Usage:")
        self.disk_label.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.disk_label)

        self.disk_meter = QtWidgets.QProgressBar()
        self.disk_meter.setRange(0, 100)
        self.disk_meter.setTextVisible(False)
        self.layout.addWidget(self.disk_meter)

        # Network
        self.network_label = QtWidgets.QLabel("Network Usage:")
        self.network_label.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.network_label)

        self.network_info = QtWidgets.QLabel()
        self.layout.addWidget(self.network_info)

        self.update_meter()

    def update_meter(self):
        # CPU
        cpu_percent = psutil.cpu_percent()
        self.cpu_meter.setValue(cpu_percent)
        self.cpu_meter.setFixedSize(200, 30)  # Set the minimum size of the CPU progress bar
        self.cpu_label.setText(f"CPU: {cpu_percent}%")

        # RAM
        ram_percent = psutil.virtual_memory().percent
        self.ram_meter.setValue(ram_percent)
        self.ram_meter.setFixedSize(200, 30)  # Set the minimum size of the RAM progress bar
        self.ram_label.setText(f"RAM: {ram_percent}%")

        # Disk
        disk_percent = psutil.disk_usage("/").percent
        self.disk_meter.setValue(disk_percent)
        self.disk_meter.setFixedSize(200, 30)  # Set the minimum size of the disk progress bar
        self.disk_label.setText(f"Disk: {disk_percent}%")

        # Network
        network_counters = psutil.net_io_counters()
        network_info = [
            f"Bytes Sent: {network_counters.bytes_sent}",
            f"Bytes Received: {network_counters.bytes_recv}",
            f"Packets Sent: {network_counters.packets_sent}",
            f"Packets Received: {network_counters.packets_recv}",
            f"Error in Sent: {network_counters.errout}",
            f"Error in Received: {network_counters.errin}",
            f"Drop in Sent: {network_counters.dropout}",
            f"Drop in Received: {network_counters.dropin}",
        ]
        self.network_info.setText("\n".join(network_info))

        # System Uptime
        uptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.uptime_info.setText(f"System Time: {uptime}")

        # User Info
        user_info = psutil.users()[0].name
        self.user_info.setText(f"User: {user_info}")

        QtCore.QTimer.singleShot(1000, self.update_meter)


    def run(self):

        system_details = []
        system_details.append(f"OS: {platform.system()} {platform.release()}")
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
