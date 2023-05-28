import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFrame, QGridLayout, QTextEdit, QCheckBox, QStyle, QStyleFactory
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import Slot, QFile
import os

os.environ['QT_QPA_PLATFORM'] = 'xcb'
class Scan:
    def __init__(self):
        self.app = QApplication([])
        self.window = QMainWindow()
        self.window.setWindowTitle("Nmap GUI")
        self.window.setGeometry(100, 100, 400, 600)
        style_file = QFile("Py_Programs/style.qss")
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_sheet = style_file.readAll()
            style_file.close()
            style_sheet = str(style_sheet, encoding='utf-8')
            self.window.setStyleSheet(style_sheet)
        else:
            print("Failed to open style.qss")
        

        self.central_widget = QFrame(self.window)
        
        self.window.setCentralWidget(self.central_widget)

        self.layout = QGridLayout(self.central_widget)
        self.layout.setSpacing(10)

        self.ip_label = QLabel("Enter IP Address:")
        self.ip_entry = QTextEdit()
        self.ip_entry.setFixedHeight(30)
        self.options_frame = QFrame()
        self.options_layout = QGridLayout(self.options_frame)
        self.button_frame = QFrame()
        self.button_layout = QGridLayout(self.button_frame)
        self.output_text = QTextEdit()
        self.output_text.setFixedHeight(150)
        self.output_text.setReadOnly(True)

        self.layout.addWidget(self.ip_label, 0, 0)
        self.layout.addWidget(self.ip_entry, 1, 0)
        self.layout.addWidget(self.options_frame, 2, 0)
        self.layout.addWidget(self.button_frame, 3, 0)
        self.layout.addWidget(self.output_text, 4, 0)

        self.options = [
            ("-sS", "SYN scan"),
            ("-sT", "Connect scan"),
            ("-sU", "UDP scan"),
            ("-sA", "ACK scan"),
            ("-sW", "Window scan"),
            ("-sM", "Maimon scan"),
            ("-sN", "Null scan"),
            ("-sF", "FIN scan"),
            ("-sX", "Xmas scan"),
            ("-sY", "SCTP INIT scan"),
            ("-sZ", "SCTP COOKIE-ECHO scan"),
            ("-sO", "IP protocol scan"),
            ("-p-", "All ports"),
            ("-p1-65535", "Scan all 65535 ports"),
            ("-F", "Fast scan mode"),
            ("-r", "Scan ports consecutively"),
            ("-A", "Aggressive scan"),
            ("-O", "OS detection"),
            ("-T0", "Paranoid timing template"),
            ("-T1", "Sneaky timing template"),
            ("-T2", "Polite timing template"),
            ("-T3", "Normal timing template"),
            ("-T4", "Aggressive timing template"),
            ("-T5", "Insane timing template"),
            ("-d", "Enable debugging output"),
            ("-v", "Increase verbosity level"),
            ("-n", "Disable DNS resolution"),
            ("-Pn", "Treat all hosts as online"),
            ("-PE", "ICMP echo request ping"),
            ("-PP", "ICMP timestamp ping"),
            ("-PM", "ICMP netmask ping"),
            ("-PR", "ARP ping"),
            ("-sn", "Ping scan"),
            ("-PR", "ARP scan"),
            ("-PO", "IP protocol scan"),
            ("-PS", "TCP SYN scan"),
            ("-PA", "TCP ACK scan"),
            ("-PU", "UDP scan"),
            ("-PY", "SCTP INIT scan"),
            ("-PE", "ICMP echo request ping"),
            ("-PP", "ICMP timestamp ping"),
            ("-PM", "ICMP netmask ping"),
            ("-PR", "ARP ping"),
            ("-PE", "ICMP echo request ping"),
            ("-PA", "TCP ACK scan"),
            ("-PU", "UDP scan"),
            ("-PY", "SCTP INIT scan"),
            ("-g <portranges>", "Send packets to specified ports"),
            ("-p <portranges>", "Only scan specified ports"),
            ("-iL <inputfile>", "Input from list of hosts/networks"),
            ("-oN <file>", "Output normal format"),
            ("-oX <file>", "Output XML format"),
            ("-oS <file>", "Output  s|<rIpt kIddi3 0uTpuT"),
            ("-oG <file>", "Output Grepable format"),
            ("-v", "Increase verbosity level"),
            ("-d", "Enable debugging output"),
            ("-h", "Print this help summary page."),
        ]

        self.option_vars = []
        self.option_values = []

        self.num_columns = 4
        for i, (option, description) in enumerate(self.options):
            row = i // self.num_columns
            column = i % self.num_columns
            option_var = QCheckBox(description)
            
            self.options_layout.addWidget(option_var, row, column)
            self.option_vars.append(option_var)
            self.option_values.append(option)

        self.preview_button = QPushButton("Preview Command")
        self.preview_button.clicked.connect(self.preview_button_click)
        self.scan_button = QPushButton("Scan")
        self.scan_button.clicked.connect(self.scan_button_click)

        self.button_layout.addWidget(self.preview_button, 0, 0)
        self.button_layout.addWidget(self.scan_button, 0, 1)

        self.window.show()

    @Slot()
    def scan_button_click(self):
        target = self.ip_entry.toPlainText()
        selected_options = [option for option, var in zip(self.option_values, self.option_vars) if var.isChecked()]
        output, error = self.run_nmap(target, selected_options)
        self.output_text.clear()
        if output:
            self.output_text.insertPlainText(output)
        elif error:
            self.output_text.insertPlainText(f"Error: {error}")

    @Slot()
    def preview_button_click(self):
        target = self.ip_entry.toPlainText()
        selected_options = [option for option, var in zip(self.option_values, self.option_vars) if var.isChecked()]
        command = self.preview_command(target, selected_options)
        self.output_text.clear()
        self.output_text.insertPlainText(command)

    def run_nmap(self, target, options):
        command = ["sudo", "nmap"] + options + [target]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        return output.decode(), error.decode()

    def preview_command(self, target, options):
        command = "sudo nmap " + " ".join(options) + " " + target
        return command

if __name__ == "__main__":
    scan = Scan()
    scan.app.exec()