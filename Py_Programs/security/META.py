# -*- coding: utf-8 -*-
"""
Created on Wednesday March 17 2023

@author: AK1R4S4T0H
"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QTextEdit, QWidget, QFileDialog, QLabel
from PySide6.QtGui import QFont, QColor, QPixmap
from PySide6.QtCore import QFile
from PIL import Image
from PIL.ExifTags import TAGS
import os

os.environ['QT_QPA_PLATFORM'] = 'xcb'

class ImageMetadataViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Metadata Viewer")
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

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.button_select_image = QPushButton("Select Image", self)
        self.button_select_image.clicked.connect(self.show_image_metadata)
        layout.addWidget(self.button_select_image)

        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)

        self.metadata_text = QTextEdit(self)
        self.metadata_text.setReadOnly(True)
        layout.addWidget(self.metadata_text)

    def show_image_metadata(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg);;All Files (*)")
        if not file_path:
            return

        image = Image.open(file_path)
        metadata = image._getexif()

        self.metadata_text.clear()

        if metadata:
            for tag_id, value in metadata.items():
                tag_name = TAGS.get(tag_id, tag_id)

                if isinstance(value, bytes):
                    try:
                        value = value.decode("utf-8")
                    except UnicodeDecodeError:
                        value = repr(value)
                self.metadata_text.append(f"{tag_name}: {value}")
        else:
            self.metadata_text.append("No metadata found.")

        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap.scaledToWidth(800))  # Adjust the width as needed


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageMetadataViewer()
    window.show()
    sys.exit(app.exec())
