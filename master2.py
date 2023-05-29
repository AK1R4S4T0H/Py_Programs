""" Created by: AK1R4S4T0H
"""
# master launcher for the Py_Programs PySide6 Version
import os
import sys
import platform
import psutil
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QPushButton, QGridLayout, QStyle, QStyleFactory, QDockWidget, QSizePolicy
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import Slot, QFile, QProcess, Qt
from Py_Programs.PONKYDOCK import PonkyPy
from Py_Programs.PYPAD import Notes
from Py_Programs.AUDIO_V2 import Audio
from Py_Programs.HEX import ColorViewer as CoVi
from Py_Programs.PLOT import PlotGUI
from Py_Programs.PASS import PasswordGenerator

os.environ['QT_QPA_PLATFORM'] = 'xcb'

class Master:
    def __init__(self):
        self.app = QApplication([])
        self.recursion_limit = 1000
        self.window = QMainWindow()
        self.window.setWindowTitle("My Programs")
        self.window.setGeometry(100, 200, 300, 650)
        
        try:
            style_file = QFile("Py_Programs/style.qss")
            if style_file.open(QFile.ReadOnly | QFile.Text):
                style_sheet = style_file.readAll()
                style_file.close()
                style_sheet = str(style_sheet, encoding='utf-8')
                self.window.setStyleSheet(style_sheet)
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            style_file = QFile("style.qss")
            if style_file.open(QFile.ReadOnly | QFile.Text):
                style_sheet = style_file.readAll()
                style_file.close()
                style_sheet = str(style_sheet, encoding='utf-8')
                self.window.setStyleSheet(style_sheet)
            else:
                print("Failed to open style.qss")

        central_widget = QWidget(self.window)
        self.window.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # Home ------------------------------------------------------------|
        home_tab = QWidget()
        tab_widget.addTab(home_tab, "Home")
        home_layout = QVBoxLayout(home_tab)
        home_label = QLabel("""\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2
    \2\2\2\2 Welcome to Py_Programs! \2\2\2\2\2\2\2\2\2\2\2\2\2
      \2\2\2\2\2\2 Collection of Various \2\2\2\2\2\2\2\2\2\2\2\2\2
        \2\2\2\2\2\2 Python Programs \2\2\2\2\2\2\2\2\2\2\2
         \2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2
           \2\2\2\2\2\2\2         /.:lodxxc,'',;..\\                    
            \2\2\2\2\2         /.':loddxl,''........\\          
              \2\2......;;:;:coxxdoc:'.      ..... \\             
               \2\2\2     ..:'     .c.        'xNOkox'              
                  \2\2    (      .X.         '\033\033\033\033\033\033\033           
                   \2\2    :     'WO.    .xN00Kd,          
                      \2    ::lOUlKOXXO0NNk,          
                        \2|:::;:::oNWWN0NKK             
                             ':..;dxkOkOXK0d'             
                            .''..;lok0kkdcdk.            
                          ..:  ,coOK00x;;kXO .'.         
                        '.  .;;..;:clc:d0Oo,    ''. .  .    
                    .'.      ,:\u0399\u03A0c\u0398g\u03A0\u0399\u03A4\u0398DdXo ..   .',....

        
        """)
        home_label.setStyleSheet("font-size: 20px;")
        home_layout.addWidget(home_label)


        # Programs -------------------------------------------------------|
        programs = [
            # START CATEGORIES ------------------------------------------|
            # Entertainment ---------------------------------------------|
            ("DODGE.py", "Py_Programs", "Dodge the Dots", "Entertainment"),
            ("MIDIPLAYER.py", "Py_Programs", "Midi Player", "Entertainment"),
            ("AUDIO.py", "Py_Programs", "TTK Audio Player", "Entertainment"),
            ("BROWSE.py", "Py_Programs", "Web Browser", "Entertainment"),
            ("STAR.py", "Py_Programs", "Turtle Star", "Entertainment"),
            ("VIDEO.py", "Py_Programs", "Video Player", "Entertainment"),
            ("KEYS.py", "Py_Programs", "Music Visual", "Entertainment"),
            ("WAVES.py", "Py_Programs", "Visualizer", "Entertainment"),
            # Education -------------------------------------------|
            ("JAP.py", "Py_Programs", "Japanese Flash", "Education"),
            ("ABCs.py", "Py_Programs", "ABC Flashcards", "Education"),
            ("COLORS.py", "Py_Programs", "Color Learn", "Education"),
            ("HEX.py", "Py_Programs", "Color/HEX View", "Education"),
            ("scan.py", "Py_Programs", "Nmap GUI", "Education"),
            ("test3.py", "Py_Programs", "Print TTK", "Education"),
            # Utility ---------------------------------------------|
            ("AUDIO_V2.py", "Py_Programs", "PyQt Audio", "Utility"),
            ("Calculator.py", "Py_Programs", "Calculator", "Utility"),
            ("PONKY.py", "Py_Programs", "Ponky", "Utility"),
            ("PONKY2.py", "Py_Programs", "Ponky V2", "Utility"),
            ("PLOT.py", "Py_Programs", "Plot", "Utility"),
            ("ANYTOMP4.py", "Py_Programs", "Any to Mp4", "Utility"),
            ("IMAGE.py", "Py_Programs", "Image Viewer", "Utility"),
            ("form.py", "Py_Programs", "Register Form", "Other"),
            ("MILES.py", "Py_Programs", "Miles to Kilos", "Utility"),
            ("Notepad.py", "Py_Programs", "Notepad", "Utility"),
            ("PYPAD.py", "Py_Programs", "PyPad", "Utility"),
            ("PATTERN_GEN.py", "Py_Programs", "Pattern Generator", "Utility"),
            ("PYTOEXE.py", "Py_Programs", "Py to EXE", "Utility"),
            ("SCRap.py", "Py_Programs", "Web Scraper", "Utility"),
            ("SCRAP_V2.py", "Py_Programs", "Web ScrapV2", "Utility"),
            ("SCRAP.py", "Py_Programs", "Web ScrapV3", "Utility"),
            ("QR_GEN.py", "Py_Programs", "QR Code Gen", "Utility"),
            # Security -----------------------------------------|
            ("HIDE.py", "Py_Programs", "Steg Hide", "Security"),
            ("SEEK.py", "Py_Programs", "Steg Seek", "Security"),
            ("HIDE_V2.py", "Py_Programs", "Steg Hide V2", "Security"),
            ("SEEK_V2.py", "Py_Programs", "Steg Seek V2", "Security"),
            ("META.py", "Py_Programs", "Image Metadata", "Security"),
            ("PORT.py", "Py_Programs", "Py_PortScanner", "Security"),
            ("PASS.py", "Py_Programs", "Pass Generator", "Security"),
            ("scan_V2.py", "Py_Programs", "Qt Nmap GUI", "Security"),
            ("LOGS.py", "Py_Programs", "Key-Logger", "Security"),
            ("LOGS_V2.py", "Py_Programs", "Key-Log V2", "Security"),
            # Other ------------------------------------------------|
            ("installer.py", "Py_Programs", "Fake Install", "Other"),
            ("CSVPLOT.py", "Py_Programs", "CSV Plot", "Other"),
            ("popup.py", "Py_Programs", "Popup Test", "Other"),
            ("test.py", "Py_Programs", "Ttk Test", "Other"),
            ("test2.py", "Py_Programs", "Ttk Test 2", "Other"),
            ("PySide6Test.py", "Py_Programs", "PySide6 Test", "Other")
            # END CATEGORIES --------------------------------------|
        ]

        categories = set([program[3] for program in programs])

        for category in categories:
            category_tab = QWidget()
            tab_widget.addTab(category_tab, category)
            category_layout = QGridLayout(category_tab)

            # Filter by category
            category_programs = [program for program in programs if program[3] == category]

            num_columns = 5
            for i, program in enumerate(category_programs):
                button = QPushButton(program[2])
                button.clicked.connect(lambda _=program, p=program: self.open_program(p))
                row = i // num_columns
                col = i % num_columns
                category_layout.addWidget(button, row, col)

            category_layout.setHorizontalSpacing(4)
            category_layout.setVerticalSpacing(4)
            category_layout.setRowStretch(row + 2, 1)
            category_layout.setColumnStretch(col + 2, 1)


        # About -----------------------------------------------------------------|
        
        about_tab = QWidget()
        tab_widget.addTab(about_tab, "About")
        about_layout = QVBoxLayout(about_tab)
        about_label = QLabel(" Py_Programs is a collection of small \n Python programs. They were made for \n Fun, and Practice, \n Feel Free to use them for \n the same and edit them to your \n liking, but Remember,\n With Great Power \n Comes Great Responsibility \n Free Software should always be Free.\n \n Thank you,\n \n AK1R4S4T0H")
        about_label.setStyleSheet("font-size: 16px;")
        about_layout.addWidget(about_label)

        # PONKY2-0 ------------------------------------------------------------|

        left_widget = QDockWidget("System Information", self.window)
        left_widget.setFeatures(QDockWidget.DockWidgetVerticalTitleBar)
        left_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        ponky = PonkyPy()
        ponky.setMaximumHeight(640)
        ponky.setMinimumHeight(640)
        left_widget.setWidget(ponky)

        self.window.addDockWidget(Qt.LeftDockWidgetArea, left_widget)

        # Custom Dock Right ---------------------------------------------------|

        dock_widget = QDockWidget("Notes", self.window)
        dock_widget.setFeatures(QDockWidget.DockWidgetFloatable)

        custom_widget = QWidget(dock_widget)
        layout = QVBoxLayout(custom_widget)

        # |---------- Dock Widgets ----------| #

        pypad = Notes()
        pypad.setMinimumHeight(300)
        
        pypad.setMinimumWidth(200)
        layout.addWidget(pypad)

        dock_label = QLabel("Music Player", self.window)
        layout.addWidget(dock_label)

        
        audio = Audio()
        audio.setMinimumWidth(200)
        layout.addWidget(audio)

        # Set custom widget to the dock
        dock_widget.setWidget(custom_widget)

        self.window.addDockWidget(Qt.RightDockWidgetArea, dock_widget)

        # Custom Dock Bottom ---------------------------------------------------|

        bot_dock_widget = QDockWidget("Other", self.window)
        bot_dock_widget.setFeatures(QDockWidget.DockWidgetFloatable)

        bot_widget = QWidget(bot_dock_widget)
        bot_layout = QHBoxLayout(bot_widget)

        # |---------- Dock Widgets ----------| #

        Hex = CoVi()
        Hex.setMinimumWidth(200)
        Hex.setMaximumHeight(150)
        Hex.setMaximumWidth(200)
        bot_layout.addWidget(Hex)

        Plot = PlotGUI()
        Plot.setMinimumWidth(200)
        Plot.setMaximumHeight(150)
        Plot.setMaximumWidth(200)
        bot_layout.addWidget(Plot)

        Pass = PasswordGenerator()
        Pass.setMinimumWidth(200)
        Pass.setMaximumHeight(150)
        Pass.setMaximumWidth(200)
        bot_layout.addWidget(Pass)

        bot_dock_widget.setWidget(bot_widget)

        self.window.addDockWidget(Qt.BottomDockWidgetArea, bot_dock_widget)

        # END TABS ----------------------------------------------------------|
        
        self.window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.window.show()
        self.app.aboutToQuit.connect(self.close_application)
        self.app.exec()

    def open_program(self, program):
        initial_directory = os.getcwd()
        os.chdir(program[1])
        self.app.processEvents()
        subprocess.Popen(["python3", program[0]])
        os.chdir(initial_directory)

    def close_application(self):
        self.app.quit()

    def run(self):
        sys.setrecursionlimit(self.recursion_limit)
        try:
            program_launcher = Master()
            sys.exit(program_launcher.app.exec())
        except RecursionError:
            print("RecursionError occurred. Closing the application.")
            sys.exit(1)

if __name__ == "__main__":
    
    program_launcher = Master()
    program_launcher.show()
    sys.exit(app.exec())