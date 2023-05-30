import os
import subprocess
import csv
import requests
from bs4 import BeautifulSoup
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QRadioButton, QStyleFactory, QMenu, QFileDialog,
    QFrame, QPushButton, QPlainTextEdit, QStyle, QMenuBar, QStatusBar,
    QMessageBox, QGridLayout, QCheckBox, QVBoxLayout
)
from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QAction


os.environ['QT_QPA_PLATFORM'] = 'xcb'


class Scrap(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Scraper")
        self.setGeometry(100, 100, 600, 600)
        self.setMaximumHeight(600)
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

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        self.frame_input = QFrame()
        self.frame_input.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.frame_input.setLineWidth(1)
        self.layout.addWidget(self.frame_input)

        self.entry_url = QLineEdit()
        self.button_scrape = QPushButton("Scrape")
        self.button_clear = QPushButton("Clear")

        input_layout = QHBoxLayout(self.frame_input)
        input_layout.addWidget(self.entry_url)
        input_layout.addWidget(self.button_scrape)
        input_layout.addWidget(self.button_clear)

        self.frame_display = QFrame()
        self.frame_display.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.frame_display.setLineWidth(1)
        self.layout.addWidget(self.frame_display)

        self.grid_layout = QGridLayout(self.frame_display)
        self.grid_layout.setAlignment(Qt.AlignTop)


        self.frame_theme = QFrame()
        self.frame_theme.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.frame_theme.setLineWidth(0.2)
        self.layout.addWidget(self.frame_theme)

        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.menu1 = self.menu_bar.addMenu("File")
        self.action_open_notepad = QAction("Open Notepad", self)
        self.menu1.addAction(self.action_open_notepad)
        self.menu1.addAction("Open .ipynb", self.ipynb)

        self.menu2 = self.menu_bar.addMenu("Edit")
        self.menu2.addAction("Clear", self.clear_button_clicked)

        self.popup_menu = QMenu(self)
        self.popup_menu.addAction("Open Notepad", self.open_notepad)

        self.button_scrape.clicked.connect(self.scrape_button_clicked)
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.action_open_notepad.triggered.connect(self.open_notepad)

        self.checkboxes = []
        self.textboxes = []
        self.target_elements = {
                        'title': False,
                        'p': False,
                        'a': False,
                        'h1': False,
                        'h2': False,
                        'h3': False,
                        'h4': False,
                        'h5': False,
                        'h6': False,
                        'div': False,
                        'span': False,
                        'header': False,
                        'footer': False,
                        'nav': False,
                        'main': False,
                        'article': False,
                        'section': False,
                        'aside': False,
                        'ul': False,
                        'ol': False,
                        'li': False,
                        'dl': False,
                        'dt': False,
                        'dd': False,
                        'table': False,
                        'tt': False,
                        'tr': False,
                        'td': False,
                        'th': False,
                        'caption': False,
                        'thead': False,
                        'tbody': False,
                        'tfoot': False,
                        'form': False,
                        'input': False,
                        'button': False,
                        'select': False,
                        'option': False,
                        'textarea': False,
                        'label': False,
                        'script': False,
                        'style': False,
                        'head': False,
                        'body': False,
                        'html': False
                    }

        self.create_checkboxes()

    def create_checkboxes(self):
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)

        num_rows = len(self.target_elements)
        num_columns = 4

        for index, (element, checked) in enumerate(self.target_elements.items()):
            checkbox = QCheckBox(element)
            checkbox.setChecked(checked)
            checkbox.stateChanged.connect(self.checkbox_state_changed)
            self.checkboxes.append(checkbox)

            textbox = QPlainTextEdit()
            textbox.setReadOnly(True)
            textbox.setPlaceholderText(f"{element} Text")
            self.textboxes.append(textbox)

            row = index // num_columns
            column = index % num_columns * 2

            grid_layout.addWidget(checkbox, row, column)
            grid_layout.addWidget(textbox, row, column + 1)
            checkbox.setStyleSheet("QCheckBox::indicator { width: 30px; height: 30px;}"
                                    "QCheckBox { font-size: 17px; padding: 2px; }")
            checkbox.setFixedHeight(50)
            textbox.setFixedWidth(230)
            textbox.setFixedHeight(50)

        self.layout.addWidget(grid_widget)




    def checkbox_state_changed(self, state):
        checkbox = self.sender()
        element = checkbox.text()
        checked = state == Qt.Checked
        self.target_elements[element] = True

    def scrape_button_clicked(self):
        url = self.entry_url.text()

        # Check URL for http:// or https://
        if not url.startswith('http://') and not url.startswith('https://'):
            # Try with https://
            url_with_https = f'https://{url}'
            try:
                response = requests.get(url_with_https)
                response.raise_for_status()  # Check request errors
            except requests.RequestException:
                # Try http://
                url_with_http = f'http://{url}'
                try:
                    response = requests.get(url_with_http)
                    response.raise_for_status()
                except requests.RequestException as e:
                    self.display_error_message(f"Request Error: {str(e)}")
                    return
                except Exception as e:
                    self.display_error_message(f"An error occurred: {str(e)}")
                    return
        else:
            # URL includes http:// https://
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.RequestException as e:
                self.display_error_message(f"Request Error: {str(e)}")
                return
            except Exception as e:
                self.display_error_message(f"An error occurred: {str(e)}")
                return

        soup = BeautifulSoup(response.text, "html.parser")

        for index, (element, checked) in enumerate(self.target_elements.items()):
            if checked:
                elements = soup.find_all(element)
                textbox = self.textboxes[index]
                if element == 'a':
                    textbox.setPlainText("\n".join([ele['href'] for ele in elements]))
                else:
                    textbox.setPlainText("\n".join([ele.text for ele in elements]))

        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a URL.")

        directory = "scrap"
        filename = "scrap.csv"
        os.makedirs(directory, exist_ok=True)  # Create "scrap" dir if it doesn't exist

        file_path = os.path.join(directory, filename)

        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            for index, (element, checked) in enumerate(self.target_elements.items()):
                if checked:
                    elements = soup.find_all(element)
                    writer.writerow([element])
                    if element == 'a':
                        writer.writerow([ele['href'] for ele in elements])
                    else:
                        writer.writerow([ele.text for ele in elements])

    def clear_button_clicked(self):
        self.entry_url.clear()

        for checkbox in self.checkboxes:
            checkbox.setChecked(False)

        for textbox in self.textboxes:
            textbox.clear()

    def open_notepad(self):
        program = ("Notepad.py", "Py_Programs")
        directory = os.getcwd()
        os.chdir(directory + "/" + program[1])
        subprocess.run(["python3", program[0]])
        os.chdir(directory)

    def display_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

    def ipynb(self):
        path = QFileDialog.getOpenFileName(self, "Open file", "", "Jupyter Notebook Files (*.ipynb)")
        subprocess.run(["jupyter", "notebook", path[0]])

if __name__ == "__main__":
    app = QApplication([])
    window = Scrap()
    window.show()
    app.exec()
