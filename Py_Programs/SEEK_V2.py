import sys
from PySide6.QtCore import QFile, QPropertyAnimation, QPoint
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QTextEdit, QWidget, QLineEdit
from PIL import Image
import os
import random

os.environ['QT_QPA_PLATFORM'] = 'xcb'


class ExtractSecretsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        style_file = QFile("Py_Programs/style.qss")
        if style_file.open(QFile.ReadOnly | QFile.Text):
            style_sheet = style_file.readAll()
            style_file.close()
            style_sheet = str(style_sheet, encoding='utf-8')
            self.setStyleSheet(style_sheet)
        else:
            print("Failed to open style.qss")
        self.setWindowTitle("Extract Secrets from Images")
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        label_key = QLabel("Enter XOR encryption key:")
        layout.addWidget(label_key)
        
        self.entry_key = QLineEdit()
        layout.addWidget(self.entry_key)
        
        button_extract = QPushButton("Extract Data")
        button_extract.clicked.connect(self.decrypt_data)
        layout.addWidget(button_extract)
      
        central_widget.setLayout(layout)
    
    def decrypt_data(self):
        encryption_key = int(self.entry_key.text())

        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Image Files (*.png *.jpg *.jpeg);;All Files (*)")
        if not file_path:
            return

        image = Image.open(file_path)

        binary_data = ""

        pixels = image.load()

        for row in range(image.height):
            for col in range(image.width):
                r, g, b = pixels[col, row]

                binary_data += str(r & 1)
                binary_data += str(g & 1)
                binary_data += str(b & 1)

        secret_data = ""
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i + 8]
            secret_data += chr(int(byte, 2) ^ encryption_key)

        if secret_data.startswith("FILE:"):
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Hidden File", "", "All Files (*)")
            if save_path:
                with open(save_path, 'wb') as file:
                    file.write(secret_data.encode())
                QMessageBox.information(self, "File Saved", "Hidden file saved successfully!")
        else:
            popup = QMessageBox(self)
            popup.setWindowTitle("Extracted Message")

            width = 500  # Set the desired width of the popup window
            height = 300  # Set the desired height of the popup window
            popup.setGeometry(50, 50, width, height)

            text_edit = QTextEdit(popup)
            text_edit.setReadOnly(True)
            text_edit.setPlainText(secret_data)
            text_edit.setFixedSize(width, height) 
            popup.layout().addWidget(text_edit)

            save_button = QPushButton("Save Text")
            save_button.clicked.connect(lambda: self.save_text(secret_data))
            popup.addButton(save_button, QMessageBox.ActionRole)

            popup.exec()

    def save_text(self, text):
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Text", "", "Text Files (*.txt);;All Files (*)")
        if save_path:
            with open(save_path, 'w') as file:
                file.write(text)
            QMessageBox.information(self, "Text Saved", "Text saved successfully!")

app = QApplication(sys.argv)
window = ExtractSecretsWindow()
window.show()
sys.exit(app.exec())
