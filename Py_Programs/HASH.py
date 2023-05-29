import hashlib
import itertools
import multiprocessing
import os
import time
import math
from PySide6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QProgressBar, QCheckBox, QGridLayout, QFileDialog
from PySide6.QtCore import Qt, QThread, Signal, QTimer, QFile

HASH_ALGORITHMS = {
    "MD5": hashlib.md5,
    "SHA1": hashlib.sha1,
    "SHA224": hashlib.sha224,
    "SHA256": hashlib.sha256,
    "SHA384": hashlib.sha384,
    "SHA512": hashlib.sha512,
    "SHA3-224": hashlib.sha3_224,
    "SHA3-256": hashlib.sha3_256,
    "SHA3-384": hashlib.sha3_384,
    "SHA3-512": hashlib.sha3_512,
    "SHAKE128": hashlib.shake_128,
    "SHAKE256": hashlib.shake_256,
    "BLAKE2s": hashlib.blake2s,
    "BLAKE2b": hashlib.blake2b,
}


CHARACTER_SET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # Character set for brute force

class RainbowTable:
    def __init__(self, hash_algorithm, chain_length):
        self.hash_algorithm = hash_algorithm
        self.chain_length = chain_length
        self.rainbow_table = {}

    def build_table(self, password_range):
        for password in password_range:
            hashed_password = self.hash_password(password)
            reduced_password = self.reduce_password(hashed_password)

            for _ in range(self.chain_length):
                hashed_password = self.hash_password(reduced_password)
                reduced_password = self.reduce_password(hashed_password)

            self.rainbow_table[reduced_password] = password

    def crack_password(self, target_hash):
        reduced_password = self.reduce_password(target_hash)

        for _ in range(self.chain_length):
            hashed_password = self.hash_password(reduced_password)
            reduced_password = self.reduce_password(hashed_password)

            if reduced_password in self.rainbow_table:
                return self.rainbow_table[reduced_password]

        return None

    def hash_password(self, password):
        return self.hash_algorithm(password.encode()).hexdigest()

    def reduce_password(self, hashed_password):
        return hashed_password[:8]  # modify the reduction logic as needed


class HashCrackerThread(QThread):
    progress_updated = Signal(int)  # Signal emitted when progress is updated
    crack_finished = Signal(str)  # Signal emitted when hash cracking is finished

    def __init__(self, hash_value, selected_approaches, selected_algorithms, dictionary_file):
        super().__init__()
        self.hash_value = hash_value
        self.selected_approaches = selected_approaches
        self.selected_algorithms = selected_algorithms
        self.dictionary_file = dictionary_file
        self.timer = QTimer()
        self.timer.setSingleShot(True)

    def run(self):
        cracked_password = None
        total_passwords = self.get_total_passwords()

        for approach in self.selected_approaches:
            if approach == "Brute Force":
                for algorithm in self.selected_algorithms:
                    hash_algorithm = HASH_ALGORITHMS[algorithm]
                    for password_index, password in enumerate(self.generate_passwords()):
                        hashed_password = hash_algorithm(password.encode()).hexdigest()
                        if hashed_password == self.hash_value:
                            cracked_password = password
                            break
                        progress = (password_index + 1) / total_passwords * 100
                        self.progress_updated.emit(progress)
                    if cracked_password:
                        break
            elif approach == "Dictionary Attack":
                with open(self.dictionary_file, "r") as file:
                    passwords = file.read().splitlines()
                    for password_index, password in enumerate(passwords):
                        for algorithm in self.selected_algorithms:
                            hash_algorithm = HASH_ALGORITHMS[algorithm]
                            hashed_password = hash_algorithm(password.encode()).hexdigest()
                            if hashed_password == self.hash_value:
                                cracked_password = password
                                break
                        if cracked_password:
                            break
                        progress = (password_index + 1) / len(passwords) * 100
                        self.progress_updated.emit(progress)
            elif approach == "Rainbow Table":
                cracked_password = self.crack_with_rainbow_table()
                if cracked_password:
                    break
            elif approach == "Hybrid Attack":
                cracked_password = self.crack_with_hybrid_attack()
                if cracked_password:
                    break

            if cracked_password:
                break

        self.timer.stop()
        self.crack_finished.emit(cracked_password)

    def get_total_passwords(self):
        total_passwords = 0
        for approach in self.selected_approaches:
            if approach == "Brute Force":
                password_length = 1
                while True:
                    total_passwords += len(CHARACTER_SET) ** password_length
                    password_length += 1
                    if total_passwords >= 1e6:
                        break
            elif approach == "Dictionary Attack":
                with open(self.dictionary_file, "r") as file:
                    total_passwords += len(file.readlines())
        return total_passwords

    def generate_passwords(self):
        password_length = 1
        while True:
            for password in itertools.product(CHARACTER_SET, repeat=password_length):
                yield "".join(password)
            password_length += 1

    def crack_with_rainbow_table(self):
        rainbow_table = RainbowTable(HASH_ALGORITHMS["SHA256"], chain_length=1000)
        rainbow_table.build_table(self.generate_passwords())

        cracked_password = rainbow_table.crack_password(self.hash_value)
        return cracked_password

    def crack_with_hybrid_attack(self):
        dictionary_words = []
        with open(self.dictionary_file, "r") as file:
            dictionary_words = file.read().splitlines()

        for password in self.generate_passwords():
            for dictionary_word in dictionary_words:
                combined_password = password + dictionary_word
                for algorithm in self.selected_algorithms:
                    hash_algorithm = HASH_ALGORITHMS[algorithm]
                    hashed_password = hash_algorithm(combined_password.encode()).hexdigest()
                    if hashed_password == self.hash_value:
                        return combined_password

        return None

class HashCrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hash Cracker")
        self.setGeometry(100, 100, 400, 400)
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

        self.label = QLabel("Enter the hash:")
        self.hash_input = QLineEdit()
        self.algorithm_label = QLabel("Select the hash algorithm(s):")
        self.algorithm_checkboxes = {}

        self.approach_label = QLabel("Select the crack approach(es):")
        self.approach_checkboxes = {}

        self.dictionary_label = QLabel("Select a dictionary file:")
        self.dictionary_input = QLineEdit()
        self.dictionary_button = QPushButton("Browse...")

        self.crack_button = QPushButton("Crack Hash")
        self.result_label = QLabel()
        self.progress_bar = QProgressBar()
        self.timer_label = QLabel()

        layout.addWidget(self.label)
        layout.addWidget(self.hash_input)
        layout.addWidget(self.algorithm_label)

        algorithm_grid = QGridLayout()
        column_count = math.ceil(len(HASH_ALGORITHMS) / 2)  # Number of columns in the grid

        row = 0
        column = 0

        for index, algorithm in enumerate(HASH_ALGORITHMS):
            checkbox = QCheckBox(algorithm)
            self.algorithm_checkboxes[algorithm] = checkbox
            algorithm_grid.addWidget(checkbox, row, column)

            # Move to the next row/column
            column += 1
            if column >= column_count:
                column = 0
                row += 1

        # Set the grid layout as the layout for the central widget
        layout.addLayout(algorithm_grid)

        layout.addWidget(self.approach_label)
        self.brute_force_checkbox = QCheckBox("Brute Force")
        self.approach_checkboxes["Brute Force"] = self.brute_force_checkbox
        layout.addWidget(self.brute_force_checkbox)

        self.dictionary_attack_checkbox = QCheckBox("Dictionary Attack")
        self.approach_checkboxes["Dictionary Attack"] = self.dictionary_attack_checkbox
        layout.addWidget(self.dictionary_attack_checkbox)

        self.rainbow_table_checkbox = QCheckBox("Rainbow Table")
        self.approach_checkboxes["Rainbow Table"] = self.rainbow_table_checkbox
        layout.addWidget(self.rainbow_table_checkbox)

        self.hybrid_attack_checkbox = QCheckBox("Hybrid Attack")
        self.approach_checkboxes["Hybrid Attack"] = self.hybrid_attack_checkbox
        layout.addWidget(self.hybrid_attack_checkbox)

        layout.addWidget(self.dictionary_label)
        dictionary_layout = QHBoxLayout()
        dictionary_layout.addWidget(self.dictionary_input)
        dictionary_layout.addWidget(self.dictionary_button)
        layout.addLayout(dictionary_layout)

        layout.addWidget(self.crack_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.timer_label)

        self.crack_button.clicked.connect(self.crack_hash)
        self.dictionary_button.clicked.connect(self.browse_dictionary)

    def browse_dictionary(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                file_path = file_paths[0]
                self.dictionary_input.setText(file_path)

    def crack_hash(self):
        hash_value = self.hash_input.text()
        selected_algorithms = []

        for algorithm, checkbox in self.algorithm_checkboxes.items():
            if checkbox.isChecked():
                selected_algorithms.append(algorithm)

        selected_approaches = []

        for approach, checkbox in self.approach_checkboxes.items():
            if checkbox.isChecked():
                selected_approaches.append(approach)

        if not selected_algorithms:
            self.result_label.setText("Select at least one algorithm")
            return

        if not selected_approaches:
            self.result_label.setText("Select at least one crack approach")
            return

        if "Dictionary Attack" in selected_approaches and not self.dictionary_input.text():
            self.result_label.setText("Select a dictionary file")
            return

        dictionary_file = self.dictionary_input.text() if "Dictionary Attack" in selected_approaches else None

        self.result_label.setText("Cracking in progress...")
        self.crack_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.timer_label.setText("Time remaining: Calculating...")

        self.cracker_thread = HashCrackerThread(hash_value, selected_approaches, selected_algorithms, dictionary_file)
        self.cracker_thread.crack_finished.connect(self.display_result)
        self.cracker_thread.progress_updated.connect(self.update_progress)
        self.cracker_thread.timer.timeout.connect(self.update_timer)

        self.timer_start_time = None

        self.cracker_thread.start()
        self.timer_start_time = self.cracker_thread.timer.remainingTime()
        self.cracker_thread.timer.start(1000)

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def update_timer(self):
        if self.timer_start_time:
            elapsed_time = self.cracker_thread.timer.remainingTime()
            time_remaining = self.timer_start_time - elapsed_time
            if time_remaining > 0:
                self.timer_label.setText(f"Time remaining: {time_remaining/1000:.1f} seconds")
            else:
                self.timer_label.setText("Time remaining: Calculating...")

    def display_result(self, result):
        self.cracker_thread.timer.stop()
        if result:
            self.result_label.setText(f"Password found: {result}")
        else:
            self.result_label.setText("Password not found")
        self.crack_button.setEnabled(True)
        self.timer_label.setText("Time remaining: N/A")


if __name__ == "__main__":
    app = QApplication([])
    hash_cracker_app = HashCrackerApp()
    hash_cracker_app.show()
    app.exec()