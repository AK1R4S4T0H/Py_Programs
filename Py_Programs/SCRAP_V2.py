import os
import subprocess
import csv
import requests
from bs4 import BeautifulSoup
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QRadioButton, QStyleFactory, QMenu, QFileDialog,
    QFrame, QPushButton, QPlainTextEdit, QStyle, QMenuBar, QStatusBar, QMessageBox
)
from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QAction
import os

os.environ['QT_QPA_PLATFORM'] = 'xcb'

class Scrap(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Scraper")
        self.setGeometry(100, 100, 600, 600)
        style_file = QtCore.QFile("Py_Programs/style.qss")
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

        self.text_title = QPlainTextEdit()
        self.text_title.setReadOnly(True)
        self.text_title.setPlaceholderText("Title")
        self.text_paragraphs = QPlainTextEdit()
        self.text_paragraphs.setReadOnly(True)
        self.text_paragraphs.setPlaceholderText("Paragraphs")
        self.text_links = QPlainTextEdit()
        self.text_links.setReadOnly(True)
        self.text_links.setPlaceholderText("Links")

        display_layout = QVBoxLayout(self.frame_display)
        display_layout.addWidget(self.text_title)
        display_layout.addWidget(self.text_paragraphs)
        display_layout.addWidget(self.text_links)

        self.frame_theme = QFrame()
        self.frame_theme.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.frame_theme.setLineWidth(1)
        self.layout.addWidget(self.frame_theme)

        self.label_theme = QLabel("Theme:")
        self.radio_default = QRadioButton("Light")
        self.radio_dark = QRadioButton("Dark")
        self.radio_default.setChecked(True)

        theme_layout = QHBoxLayout(self.frame_theme)
        theme_layout.addWidget(self.label_theme)
        theme_layout.addWidget(self.radio_default)
        theme_layout.addWidget(self.radio_dark)

        self.theme_group = QtWidgets.QButtonGroup()
        self.theme_group.addButton(self.radio_default)
        self.theme_group.addButton(self.radio_dark)

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
        title = soup.title.string if soup.title else ""
        paragraphs = soup.find_all("p")
        links = soup.find_all("a")

        self.text_title.setPlainText(title)
        self.text_paragraphs.setPlainText("\n".join([p.text for p in paragraphs]))
        self.text_links.setPlainText("\n".join([link.get("href") for link in links]))

        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a URL.")

            
    def clear_button_clicked(self):
        self.entry_url.clear()
        self.text_title.clear()
        self.text_paragraphs.clear()
        self.text_links.clear()

    def open_notepad(self):
        subprocess.Popen(["notepad.exe"])

    def ipynb(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setFilter(QDir.Files)

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            subprocess.Popen(["jupyter", "notebook", file_path])

    def contextMenuEvent(self, event):
        self.popup_menu.exec_(self.mapToGlobal(event.pos()))


app = QApplication([])
window = Scrap()
window.show()
app.exec()