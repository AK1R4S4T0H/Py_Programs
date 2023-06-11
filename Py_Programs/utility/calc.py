import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout, QLineEdit, QPushButton
from PySide6.QtCore import QFile

class Calculator(QMainWindow):
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

        self.setWindowTitle("Calculator")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        self.result_display = QLineEdit()
        main_layout.addWidget(self.result_display)

        number_layout = QGridLayout()  
        main_layout.addLayout(number_layout)

        buttons = [
            '6', '7', '8', '9',
            '2', '3', '4', '5',
            '1', '0', '*', '-',
            '/', 'C', '=', '+'
        ]

        row = 0
        col = 0
        for button_text in buttons[:10]:
            button = QPushButton(button_text)
            button.clicked.connect(self.handle_button_click)
            number_layout.addWidget(button, row, col)

            col += 1
            if col > 3:
                col = 0
                row += 1

        operator_layout = QGridLayout()  
        main_layout.addLayout(operator_layout)

        for button_text in buttons[10:]:  
            button = QPushButton(button_text)
            button.clicked.connect(self.handle_button_click)
            operator_layout.addWidget(button)

    def handle_button_click(self):
        button = self.sender()
        button_text = button.text()

        if button_text == '=':
            expression = self.result_display.text()
            try:
                result = eval(expression)
                self.result_display.setText(str(result))
            except Exception as e:
                self.result_display.setText("Error")
        elif button_text == 'C':
            self.result_display.clear()
        else:
            current_text = self.result_display.text()
            new_text = current_text + button_text
            self.result_display.setText(new_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
