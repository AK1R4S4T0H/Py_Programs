import os
import sys
import qrcode
from PIL import Image, ImageQt
from PySide6.QtCore import Qt, QFile
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog, QMessageBox, QFrame
)
os.environ['QT_QPA_PLATFORM'] = 'xcb'

QR_CODE_SIZE = 600


class QRCodeGeneratorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Generator")
        self.setGeometry(100, 100, 800, 800)
        style_file = QFile("style.qss")
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_sheet = style_file.readAll()
            style_file.close()
            style_sheet = str(style_sheet, encoding='utf-8')
            self.setStyleSheet(style_sheet)
        else:
            print("Failed to open style.qss")

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)

        canvas_frame = QFrame()
        main_layout.addWidget(canvas_frame)
        canvas_layout = QVBoxLayout(canvas_frame)

        self.canvas = QLabel()
        self.canvas.setAlignment(Qt.AlignCenter)
        self.canvas.setMinimumSize(QR_CODE_SIZE, QR_CODE_SIZE)
        canvas_layout.addWidget(self.canvas)

        file_frame = QFrame()
        main_layout.addWidget(file_frame)
        file_layout = QHBoxLayout(file_frame)

        self.file_entry = QLineEdit()
        file_layout.addWidget(self.file_entry)

        file_button = QPushButton("Select File")
        file_button.clicked.connect(self.select_file)
        file_layout.addWidget(file_button)

        data_frame = QFrame()
        main_layout.addWidget(data_frame)
        data_layout = QHBoxLayout(data_frame)

        data_label = QLabel("Data:")
        data_layout.addWidget(data_label)

        self.data_entry = QLineEdit()
        data_layout.addWidget(self.data_entry)

        draw_button = QPushButton("Draw QR Code")
        draw_button.clicked.connect(self.generate_and_draw)
        main_layout.addWidget(draw_button)

        save_button = QPushButton("Save QR Code")
        save_button.clicked.connect(self.save_image)
        main_layout.addWidget(save_button)

    def generate_and_draw(self):
        data = self.data_entry.text()
        filename = self.file_entry.text()

        if not data and not filename:
            return

        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)

        if data:
            qr.add_data(data)

        if filename:
            with open(filename, 'rb') as file:
                qr.add_data(file.read())

        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Resize the image
        img = img.resize((QR_CODE_SIZE, QR_CODE_SIZE), Image.LANCZOS)

        # Convert the QRCode image to QImage
        qimage = ImageQt.ImageQt(img)
        pixmap = QPixmap.fromImage(qimage)

        self.canvas.setPixmap(pixmap)

    def select_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select File")
        if filename:
            self.file_entry.setText(filename)

    def save_image(self):
        pixmap = self.canvas.pixmap()
        if pixmap:
            filename, _ = QFileDialog.getSaveFileName(self, "Save QR Code", "", "PNG Image (*.png);;JPEG Image (*.jpg)")
            if filename:
                pixmap.save(filename)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QRCodeGeneratorWindow()
    window.show()

    sys.exit(app.exec())
