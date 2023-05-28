import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QFontDialog, QColorDialog
from PySide6.QtGui import QFont, QColor, QAction
from PySide6.QtCore import QFile
import os

os.environ['QT_QPA_PLATFORM'] = 'xcb'

class Notes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyPad")
        self.setGeometry(100, 100, 600, 400)
        self.current_file = None
        self.bold_on = False
        self.italic_on = False
        self.underline_on = False
        self.font_family = QFont()
        self.font_size = 15
        self.font_color = QColor()
        self.create_widgets()
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

    def create_widgets(self):
        self.text_area = QTextEdit()
        self.setCentralWidget(self.text_area)

        self.create_actions()
        self.create_menus()

        self.status_bar = self.statusBar()

        self.text_area.textChanged.connect(self.update_status_bar)

        self.update_title()

    def create_actions(self):
        self.new_action = QAction("New", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(self.new_file)

        self.open_action = QAction("Open", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction("Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_file)

        self.save_as_action = QAction("Save As", self)
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        self.save_as_action.triggered.connect(self.save_file_as)

        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.close)

        self.cut_action = QAction("Cut", self)
        self.cut_action.setShortcut("Ctrl+X")
        self.cut_action.triggered.connect(self.cut)

        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut("Ctrl+C")
        self.copy_action.triggered.connect(self.copy)

        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut("Ctrl+V")
        self.paste_action.triggered.connect(self.paste)

        self.bold_action = QAction("Bold", self)
        self.bold_action.setShortcut("Ctrl+B")
        self.bold_action.triggered.connect(self.toggle_bold)

        self.italic_action = QAction("Italic", self)
        self.italic_action.setShortcut("Ctrl+I")
        self.italic_action.triggered.connect(self.toggle_italic)

        self.underline_action = QAction("Underline", self)
        self.underline_action.setShortcut("Ctrl+U")
        self.underline_action.triggered.connect(self.toggle_underline)

        self.font_family_action = QAction("Font Family", self)
        self.font_family_action.triggered.connect(self.change_font_family)

        self.font_size_action = QAction("Font Size", self)
        self.font_size_action.triggered.connect(self.change_font_size)

        self.font_color_action = QAction("Font Color", self)
        self.font_color_action.triggered.connect(self.change_font_color)

    def create_menus(self):
        self.menu_bar = self.menuBar()

        self.file_menu = self.menu_bar.addMenu("File")
        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        self.edit_menu = self.menu_bar.addMenu("Edit")
        self.edit_menu.addAction(self.cut_action)
        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)
        self.edit_menu.addAction(self.bold_action)
        self.edit_menu.addAction(self.italic_action)
        self.edit_menu.addAction(self.underline_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.font_family_action)
        self.edit_menu.addAction(self.font_size_action)
        self.edit_menu.addAction(self.font_color_action)

    def new_file(self):
        self.text_area.clear()
        self.current_file = None
        self.update_title()

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Text Files (*.txt);;All Files (*)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            with open(file_path, "r") as file:
                self.text_area.setText(file.read())
            self.current_file = file_path
            self.update_title()

    def save_file(self):
        if self.current_file:
            text = self.text_area.toPlainText()
            with open(self.current_file, "w") as file:
                file.write(text)
        else:
            self.save_file_as()

    def save_file_as(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter("Text Files (*.txt)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.current_file = file_path
            self.save_file()
            self.update_title()

    def cut(self):
        self.text_area.cut()

    def copy(self):
        self.text_area.copy()

    def paste(self):
        self.text_area.paste()

    def toggle_bold(self):
        self.bold_on = not self.bold_on
        font = self.text_area.currentFont()
        font.setBold(self.bold_on)
        self.text_area.setCurrentFont(font)

    def toggle_italic(self):
        self.italic_on = not self.italic_on
        font = self.text_area.currentFont()
        font.setItalic(self.italic_on)
        self.text_area.setCurrentFont(font)

    def toggle_underline(self):
        self.underline_on = not self.underline_on
        font = self.text_area.currentFont()
        font.setUnderline(self.underline_on)
        self.text_area.setCurrentFont(font)

    def change_font_family(self):
        font, ok = QFontDialog.getFont(self.font_family, self)
        if ok:
            self.font_family = font
            self.text_area.setCurrentFont(self.font_family)

    def change_font_size(self):
        size, ok = QFontDialog.getInt(self, "Font Size", "Enter the font size:", self.font_size)
        if ok:
            self.font_size = size
            self.font_family.setPointSize(self.font_size)
            self.text_area.setCurrentFont(self.font_family)

    def change_font_color(self):
        color = QColorDialog.getColor(self.font_color, self)
        if color.isValid():
            self.font_color = color
            self.text_area.setTextColor(self.font_color)

    def update_status_bar(self):
        text = self.text_area.toPlainText()
        word_count = len(text.split())
        self.status_bar.showMessage(f"Word Count: {word_count}")

    def update_title(self):
        title = "PyPad"
        if self.current_file:
            title += f" - {self.current_file}"
        self.setWindowTitle(title)


    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    notes = Notes()
    notes.show()
    sys.exit(app.exec())
