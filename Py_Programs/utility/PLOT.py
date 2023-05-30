""" Created by: AK1R4S4T0H
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit
import pandas as pd
import matplotlib.pyplot as plt
from PySide6.QtCore import QFile
import os

os.environ['QT_QPA_PLATFORM'] = 'xcb'

class PlotGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Plot")
        self.setGeometry(100, 100, 200, 200)
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

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.data_label = QLabel("CSV Plot")
        self.data_input_label = QLabel("Input Data:")
        self.data_input_textedit = QTextEdit()

        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_data)

        self.load_csv_button = QPushButton("Load CSV")
        self.load_csv_button.clicked.connect(self.load_csv_data)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.plot_button)
        button_layout.addWidget(self.load_csv_button)

        layout.addWidget(self.data_label)
        layout.addWidget(self.data_input_label)
        layout.addWidget(self.data_input_textedit)
        layout.addLayout(button_layout)

    def plot_data(self):
        data = self.data_input_textedit.toPlainText()
        if data:
            data = data.strip()
            lines = data.split("\n")
            rows = [line.split(",") for line in lines]
            df = pd.DataFrame(rows)
            try:
                df = df.astype(float)
                plt.plot(df[0], df[1])
                plt.xlabel("X")
                plt.ylabel("Y")
                plt.title("Data Plot")
                plt.show()
            except ValueError:
                print("Invalid data format. Please enter numeric values.")
        else:
            print("No data entered.")

    def load_csv_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                df = pd.read_csv(file_path)
                plt.plot(df.iloc[:, 0], df.iloc[:, 1])
                plt.xlabel("X")
                plt.ylabel("Y")
                plt.title("Data Plot")
                plt.show()
            except pd.errors.EmptyDataError:
                print("Empty CSV file.")
            except pd.errors.ParserError:
                print("Invalid CSV file format.")
        else:
            print("No file selected.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotGUI()
    window.show()
    sys.exit(app.exec())
