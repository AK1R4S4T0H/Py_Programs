import sys
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QTextEdit, QWidget, QLineEdit
from PIL import Image
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import os
import subprocess

os.environ['QT_QPA_PLATFORM'] = 'xcb'

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return encrypted_data


class HideSecretsWindow(QMainWindow):
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
        self.setWindowTitle("Hide Secrets in Images")
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        label = QLabel("Enter the secret message or select a file:")
        layout.addWidget(label)
        
        self.text_entry = QTextEdit()
        layout.addWidget(self.text_entry)
        
        button_select_image = QPushButton("Select Image")
        button_select_image.clicked.connect(self.select_image)
        layout.addWidget(button_select_image)
        
        button_select_file = QPushButton("Select File")
        button_select_file.clicked.connect(self.select_file)
        layout.addWidget(button_select_file)
        
        self.button_hide = QPushButton("Hide Data")
        self.button_hide.clicked.connect(self.hide_data)
        self.button_hide.setEnabled(False)
        layout.addWidget(self.button_hide)
        
        self.button_save = QPushButton("Save Image")
        self.button_save.setEnabled(False)
        layout.addWidget(self.button_save)
        
        self.label_selected_image = QLabel("Selected Image: ")
        layout.addWidget(self.label_selected_image)
        
        self.label_selected_file = QLabel("Selected File: ")
        layout.addWidget(self.label_selected_file)
        
        central_widget.setLayout(layout)
        
        self.image_path = None
        self.file_path = None
    
    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg);;All Files (*)")
        if file_path:
            self.button_hide.setEnabled(True)
            self.button_save.setEnabled(True)
            self.label_selected_image.setText("Selected Image: " + file_path)
            self.image_path = file_path
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.file_path = file_path
            self.label_selected_file.setText("Selected File: " + file_path)
    
    def hide_data(self):
        file_path = self.image_path
        if not file_path:
            QMessageBox.warning(self, "Error", "Please select an image file.")
            return

        image = Image.open(file_path)

        secret_data = ""
        if self.file_path:
            with open(self.file_path, 'rb') as file:
                secret_data = file.read()

        if not secret_data:
            QMessageBox.warning(self, "Error", "Please select a file to hide.")
            return

        # Generate a random encryption key
        encryption_key = get_random_bytes(16)

        # Perform AES encryption on the secret data
        encrypted_data = encrypt_data(secret_data, encryption_key)

        binary_data = ''.join(format(byte, '08b') for byte in encrypted_data)

        num_pixels = image.width * image.height
        max_data_size = num_pixels * 3 // 8
        if len(binary_data) > max_data_size:
            QMessageBox.warning(self, "Error", "The selected image is too small to hold the file.")
            return

        pixels = image.load()
        data_index = 0

        for row in range(image.height):
            for col in range(image.width):
                r, g, b = pixels[col, row]

                if data_index < len(binary_data):
                    r = (r & 0xFE) | int(binary_data[data_index])
                    data_index += 1

                if data_index < len(binary_data):
                    g = (g & 0xFE) | int(binary_data[data_index])
                    data_index += 1

                if data_index < len(binary_data):
                    b = (b & 0xFE) | int(binary_data[data_index])
                    data_index += 1

                pixels[col, row] = (r, g, b)

                if data_index >= len(binary_data):
                    break

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image Files (*.png);;All Files (*)")
        if save_path:
            image.save(save_path)
            QMessageBox.information(self, "Success", "Image saved successfully!")

            # encryption key
            encryption_key_hex = encryption_key.hex()
            QMessageBox.information(self, "Encryption Key", "Encryption key: {}".format(encryption_key_hex))
            self.copy_encryption_key(encryption_key_hex)

            # Execute the hidden file when the image is viewed
            command = 'python3 {}'.format(save_path)  # Replace 'python3' with the appropriate command for your executable file type
            subprocess.Popen(command, shell=True)

    def copy_encryption_key(self, encryption_key_hex):
        clipboard = QApplication.clipboard()
        clipboard.setText(encryption_key_hex)
        QMessageBox.information(self, "Copy Key", "Encryption key copied to clipboard.")


app = QApplication(sys.argv)
window = HideSecretsWindow()
window.show()
sys.exit(app.exec())
