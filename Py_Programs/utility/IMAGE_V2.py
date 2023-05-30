# Image viewer in python

""" Created by: AK1R4S4T0H
"""
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
import os

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("background-color: #110011;")

        self.images = []
        self.current_image = 0

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.canvas = QLabel(self)
        self.canvas.setStyleSheet("background-color: #220022;")
        self.layout.addWidget(self.canvas)

        self.previous_button = QPushButton("Previous", self)
        self.previous_button.setStyleSheet("background-color: #555555; color: white;")
        self.layout.addWidget(self.previous_button)
        self.previous_button.clicked.connect(self.show_previous_image)

        self.next_button = QPushButton("Next", self)
        self.next_button.setStyleSheet("background-color: #555555; color: white;")
        self.layout.addWidget(self.next_button)
        self.next_button.clicked.connect(self.show_next_image)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.setStyleSheet("background-color: #555555; color: white;")
        self.layout.addWidget(self.browse_button)
        self.browse_button.clicked.connect(self.browse_directory)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.load_images(directory)
            self.show_image()

    def load_images(self, directory):
        self.images.clear()
        for file in os.listdir(directory):
            if file.endswith(".jpg") or file.endswith(".png"):
                image_path = os.path.join(directory, file)
                image = QImage(image_path)
                image = self.resize_image(image)
                self.images.append(QPixmap.fromImage(image))

    def resize_image(self, image):
        canvas_width = self.canvas.width()
        canvas_height = self.canvas.height()
        image_width = image.width()
        image_height = image.height()

        width_ratio = canvas_width / image_width
        height_ratio = canvas_height / image_height

        ratio = min(width_ratio, height_ratio)

        new_width = int(image_width * ratio)
        new_height = int(image_height * ratio)
        return image.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation)

    def show_image(self):
        if self.images:
            pixmap = self.images[self.current_image]
            self.canvas.setPixmap(pixmap)

    def show_next_image(self):
        if self.current_image == len(self.images) - 1:
            self.current_image = 0
        else:
            self.current_image += 1
        self.show_image()

    def show_previous_image(self):
        if self.current_image == 0:
            self.current_image = len(self.images) - 1
        else:
            self.current_image -= 1
        self.show_image()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec())
