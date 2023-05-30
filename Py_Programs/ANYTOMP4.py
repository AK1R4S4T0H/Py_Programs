# for converting any video format to mp4
# doesnt work right
#
""" Created by: AK1R4S4T0H
"""
import sys
import subprocess
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QFile


class VideoConv(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        try:
            style_file = QFile("Py_Programs/style.qss")
            if style_file.open(QFile.ReadOnly | QFile.Text):
                style_sheet = style_file.readAll()
                style_file.close()
                style_sheet = str(style_sheet, encoding='utf-8')
                self.setStyleSheet(style_sheet)
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            style_file = QFile("style.qss")
            if style_file.open(QFile.ReadOnly | QFile.Text):
                style_sheet = style_file.readAll()
                style_file.close()
                style_sheet = str(style_sheet, encoding='utf-8')
                self.setStyleSheet(style_sheet)
            else:
                print("Failed to open style.qss")

        self.setWindowTitle("Video Converter")
        self.label_input = QtWidgets.QLabel("Input Video:")
        self.entry_input = QtWidgets.QLineEdit()
        self.button_browse = QtWidgets.QPushButton("Browse")
        self.button_browse.clicked.connect(self.select_file)

        self.button_output = QtWidgets.QPushButton("Choose Output File")
        self.button_output.clicked.connect(self.select_output_file)

        self.button_convert = QtWidgets.QPushButton("Convert")
        self.button_convert.clicked.connect(self.convert_video)

        self.status_label = QtWidgets.QLabel("")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label_input)
        layout.addWidget(self.entry_input)
        layout.addWidget(self.button_browse)
        layout.addWidget(self.button_output)
        layout.addWidget(self.button_convert)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def select_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilters(["Video files (*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.ogv *.ogg)", "All files (*.*)"])
        file_dialog.selectNameFilter("Video files (*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.ogv *.ogg)")

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            self.entry_input.setText(file_path)

    def select_output_file(self):
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix("mp4")
        file_dialog.setNameFilter("MP4 files (*.mp4)")
        
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            self.button_output.setText(file_path)

    def convert_video(self):
        input_file = self.entry_input.text()
        output_file = self.button_output.text()

        if input_file and output_file:
            command = f"ffmpeg -i {input_file} -codec:v libx264 {output_file}"
            try:
                subprocess.run(command, check=True, shell=True)
                self.status_label.setText('Conversion complete!')
            except subprocess.CalledProcessError:
                self.status_label.setText('Conversion failed!')
        else:
            self.status_label.setText('Please select input and output files.')


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = VideoConv()
    window.show()

    sys.exit(app.exec())
