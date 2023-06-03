""" Created by: AK1R4S4T0H
"""
# master launcher for the Py_Programs PySide6 Version
# Py_Programs and all Works related are Licensed under the GNU 3.0 license 
import os
import sys
import platform
import psutil
import subprocess
import functools
from PySide6.QtWidgets import QApplication,QMessageBox, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QPushButton, QGridLayout, QStyle, QStyleFactory, QDockWidget, QSizePolicy
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import Slot, QFile, QProcess, Qt
# ---------------------------------------|
# My Py_Programs Imports for the Docks
from Py_Programs import *
from Py_Programs.PONKYDOCK import PonkyPy
from Py_Programs.PYPAD import Notes
from Py_Programs.AUDIO_V3 import Audio
from Py_Programs.HEX import ColorViewer as CoVi
from Py_Programs.utility.PLOT import PlotGUI
from Py_Programs.security.PASS import PasswordGenerator
from Py_Programs.utility.ANYTOMP4 import VideoConv
from Py_Programs.OCEAN import Waves
# ----------------------------------------|


os.environ['QT_QPA_PLATFORM'] = 'xcb'

class Master:
    def __init__(self):
        self.app = QApplication([])
        self.recursion_limit = 1000
        self.window = QMainWindow()
        self.window.setWindowTitle("My Programs")
        self.window.setGeometry(100, 200, 300, 450)
        
        
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
        central_widget.setMaximumHeight(500)
        central_widget.setMaximumWidth(520)

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
            ("DODGE.py", "Py_Programs/entertainment", "Dodge the Dots", "Entertainment"),
            ("MIDIPLAYER.py", "Py_Programs/entertainment", "Midi Player", "Entertainment"),
            ("AUDIO.py", "Py_Programs/entertainment", "TTK Audio Player", "Entertainment"),
            ("BROWSE.py", "Py_Programs/entertainment", "Web Browser", "Entertainment"),
            ("STAR.py", "Py_Programs/entertainment", "Turtle Star", "Entertainment"),
            ("VIDEO.py", "Py_Programs/entertainment", "Video Player", "Entertainment"),
            ("KEYS.py", "Py_Programs/entertainment", "Music Visual", "Entertainment"),
            ("WAVES.py", "Py_Programs/entertainment", "Visualizer", "Entertainment"),
            ("AUDIO_V4.py", "Py_Programs/entertainment", "Audio & Visual", "Entertainment"),
            ("AUDIO_V5.py", "Py_Programs/entertainment", "Audio V5", "Entertainment"),
            # Education -------------------------------------------|
            ("JAP.py", "Py_Programs/education", "Japanese Flash", "Education"),
            ("ABCs.py", "Py_Programs/education", "ABC Flashcards", "Education"),
            ("COLORS.py", "Py_Programs/education", "Color Learn", "Education"),
            ("SHAPES.py", "Py_Programs/education", "Shapes Learn", "Education"),
            ("OSCIL.py", "Py_Programs/education", "Oscilloscope", "Education"),
            ("HEX.py", "Py_Programs", "Color/HEX View", "Education"),
            ("scan.py", "Py_Programs/education", "Nmap GUI", "Education"),
            ("test3.py", "Py_Programs/education", "Print TTK", "Education"),
            # Utility ---------------------------------------------|
            ("AUDIO_V2.py", "Py_Programs/utility", "PyQt Audio", "Utility"),
            ("Calculator.py", "Py_Programs/utility", "Calculator", "Utility"),
            ("PONKY.py", "Py_Programs/utility", "Ponky", "Utility"),
            ("PONKY2.py", "Py_Programs/utility", "Ponky V2", "Utility"),
            ("PLOT.py", "Py_Programs/utility", "Plot", "Utility"),
            ("ANYTOMP4.py", "Py_Programs/utility", "Any to Mp4", "Utility"),
            ("IMAGE.py", "Py_Programs/utility", "Image Viewer", "Utility"),
            ("form.py", "Py_Programs/utility", "Register Form", "Other"),
            ("MILES.py", "Py_Programs/utility", "Miles to Kilos", "Utility"),
            ("Notepad.py", "Py_Programs/utility", "Notepad", "Utility"),
            ("PYPAD.py", "Py_Programs", "PyPad", "Utility"),
            ("PATTERN_GEN.py", "Py_Programs/utility", "Pattern Generator", "Utility"),
            ("PYTOEXE.py", "Py_Programs/utility", "Py to EXE", "Utility"),
            ("SCRap.py", "Py_Programs/utility", "Web Scraper", "Utility"),
            ("SCRAP_V2.py", "Py_Programs/utility", "Web ScrapV2", "Utility"),
            ("SCRAPE3.py", "Py_Programs/utility", "Web ScrapV3", "Utility"),
            ("web.py", "Py_Programs/utility", "Simple HTML View", "Utility"),
            ("QR_GEN.py", "Py_Programs/utility", "QR Code Gen", "Utility"),
            # Security -----------------------------------------|
            ("HIDE.py", "Py_Programs/security", "Steg Hide", "Security"),
            ("SEEK.py", "Py_Programs/security", "Steg Seek", "Security"),
            ("HASH.py", "Py_Programs/security", "Hash Cracker", "Security"),
            ("HIDE_V2.py", "Py_Programs/security", "Steg Hide V2", "Security"),
            ("SEEK_V2.py", "Py_Programs/security", "Steg Seek V2", "Security"),
            ("META.py", "Py_Programs/security", "Image Metadata", "Security"),
            ("PORT.py", "Py_Programs/security", "Py_PortScanner", "Security"),
            ("PASS.py", "Py_Programs/security", "Pass Generator", "Security"),
            ("scan_V2.py", "Py_Programs/security", "Qt Nmap GUI", "Security"),
            ("LOGS.py", "Py_Programs/security", "Key-Logger", "Security"),
            ("LOGS_V2.py", "Py_Programs/security", "Key-Log V2", "Security"),
            # Other ------------------------------------------------|
            ("installer.py", "Py_Programs/other", "Fake Install", "Other"),
            ("CSVMERGE.py", "Py_Programs/other", "Merge CSVs", "Other"),
            ("CSVPLOT.py", "Py_Programs/other", "CSV Plot", "Other"),
            ("popup.py", "Py_Programs/other", "Popup Test", "Other"),
            ("test.py", "Py_Programs/other", "Ttk Test", "Other"),
            ("test2.py", "Py_Programs/other", "Ttk Test 2", "Other"),
            ("PySide6Test.py", "Py_Programs/other", "PySide6 Test", "Other"),
            ("pyside6test2.py", "Py_Programs/other", "Print PySide6", "Other")
            # END CATEGORIES --------------------------------------|
        ]

        categories = set([program[3] for program in programs])

        for category in categories:
            category_tab = QWidget()
            tab_widget.addTab(category_tab, category)
            category_layout = QGridLayout(category_tab)

            # Filter by category ---------------------------------------|
            category_programs = [program for program in programs if program[3] == category]

            num_columns = 5
            for i, program in enumerate(category_programs):
                button = QPushButton(program[2])
                button.clicked.connect(functools.partial(self.open_program, program))
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
        left_widget.setFeatures(QDockWidget.DockWidgetVerticalTitleBar | QDockWidget.DockWidgetFloatable)
        left_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        custom_left_widget = QWidget(left_widget)
        left_layout = QVBoxLayout(custom_left_widget)
        pypad = Notes()
        pypad.setMinimumHeight(200)
        pypad.setMaximumHeight(200)
        pypad.setMinimumWidth(150)
        left_layout.addWidget(pypad)

        ponky = PonkyPy()
        ponky.setMaximumHeight(330)
        ponky.setMinimumWidth(150)
        ponky.setMinimumHeight(300)
        left_layout.addWidget(ponky)

        

        left_widget.setWidget(custom_left_widget)

        self.window.addDockWidget(Qt.LeftDockWidgetArea, left_widget)

        # Custom Dock Right ---------------------------------------------------|

        dock_widget = QDockWidget("Visualizer", self.window)
        dock_widget.setFeatures(QDockWidget.DockWidgetFloatable)
        dock_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        custom_widget = QWidget(dock_widget)
        layout = QVBoxLayout(custom_widget)

        # |---------- Dock Widgets ----------| #

        waves = Waves.WaveformWidget()
        layout.addWidget(waves)

        audio = Audio()
        audio.setMaximumHeight(300)
        audio.setMinimumWidth(220)
        layout.addWidget(audio)

        

        # Set custom widget to the dock ------------------------------|
        dock_widget.setWidget(custom_widget)

        self.window.addDockWidget(Qt.RightDockWidgetArea, dock_widget)

        # Custom Dock Bottom ---------------------------------------------------|

        bot_dock_widget = QDockWidget("Other", self.window)
        bot_dock_widget.setFeatures(QDockWidget.DockWidgetFloatable)
        bot_dock_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        bot_widget = QWidget(bot_dock_widget)
        bot_layout = QHBoxLayout(bot_widget)

        # |---------- Dock Widgets ----------| #

        Hex = CoVi()
        Hex.setMinimumWidth(200)
        Hex.setMaximumHeight(170)
        Hex.setMaximumWidth(200)
        bot_layout.addWidget(Hex)

        Plot = PlotGUI()
        Plot.setMinimumWidth(200)
        Plot.setMaximumHeight(170)
        Plot.setMaximumWidth(200)
        bot_layout.addWidget(Plot)

        Pass = PasswordGenerator()
        Pass.setMinimumWidth(200)
        Pass.setMaximumHeight(170)
        Pass.setMaximumWidth(200)
        bot_layout.addWidget(Pass)

        Conv = VideoConv()
        Conv.setMinimumWidth(200)
        Conv.setMaximumHeight(170)
        Conv.setMaximumWidth(200)
        bot_layout.addWidget(Conv)

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
        reply = QMessageBox.question(
            self.window,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.No:
            self.app.quit()
        else:
            pass
        
        

    def run(self):
        sys.setrecursionlimit(self.recursion_limit)
        try:
            program_launcher = Master()
            sys.exit(program_launcher.app.exec())
        except RecursionError:
            print("RecursionError: Closing the application.")
            sys.exit(1)

if __name__ == "__main__":
    
    program_launcher = Master()
    sys.exit(program_launcher)