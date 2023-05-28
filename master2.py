""" Created by: AK1R4S4T0H
"""

# master launcher for the Py_Programs
import os
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QLabel, QWidget, QPushButton, QGridLayout
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import Slot, QFile
import sys

os.environ['QT_QPA_PLATFORM'] = 'xcb'
class Master:
    def __init__(self):
        self.app = QApplication([])
        self.window = QMainWindow()
        self.window.setWindowTitle("My Programs")
        self.window.setGeometry(100, 100, 400, 550)
        style_file = QFile("Py_Programs/style.qss")
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

        # Home tab
        home_tab = QWidget()
        tab_widget.addTab(home_tab, "Home")
        home_layout = QVBoxLayout(home_tab)
        home_label = QLabel("""\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2
\2\2 Welcome to Py_Programs! \2\2
\2\2\2\2\2 Collection of Various \2\2\2
\2\2\2\2\2\2 Python Programs \2\2\2
\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2\2
\2\2\2\2\2\2         /.:lodxxc,'',;..\\                    
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

        # Programs tab
        programs_tab = QWidget()
        tab_widget.addTab(programs_tab, "Programs")
        programs_layout = QGridLayout(programs_tab)

        programs = [
            ("ABCs.py", "Py_Programs", "ABC Flashcards"),
            ("ANYTOMP4.py", "Py_Programs", "Any to Mp4"),
            ("AUDIO.py", "Py_Programs", "TTK Audio Player"),
            ("AUDIO_V2.py", "Py_Programs", "PyQt Audio"),
            ("BROWSE.py", "Py_Programs", "Web Browser"),
            ("Calculator.py", "Py_Programs", "Calculator"),
            ("CSVPLOT.py", "Py_Programs", "CSV Plot"),
            ("DODGE.py", "Py_Programs", "Dodge the Dots"),
            ("form.py", "Py_Programs", "Register Form"),
            ("IMAGE.py", "Py_Programs", "Image Viewer"),
            ("installer.py", "Py_Programs", "Fake Install"),
            ("JAP.py", "Py_Programs", "Japanese Flash"),
            ("MIDIPLAYER.py", "Py_Programs", "Midi Player"),
            ("MILES.py", "Py_Programs", "Miles to Kilos"),
            ("Notepad.py", "Py_Programs", "Notepad"),
            ("PATTERN_GEN.py", "Py_Programs", "Pattern Generator"),
            ("PASS.py", "Py_Programs", "Pass Generator"),
            ("PONKY.py", "Py_Programs", "Ponky"),
            ("popup.py", "Py_Programs", "Popup Test"),
            ("PYTOEXE.py", "Py_Programs", "Py to EXE"),
            ("scan.py", "Py_Programs", "Nmap GUI"),
            ("STAR.py", "Py_Programs", "Turtle Star"),
            ("LOGS.py", "Py_Programs", "Key-Logger"),
            ("test.py", "Py_Programs", "Ttk Test"),
            ("test2.py", "Py_Programs", "Ttk Test 2"),
            ("PySide6Test.py", "Py_Programs", "PySide6 Test"),
            ("test3.py", "Py_Programs", "Print TTK"),
            ("VIDEO.py", "Py_Programs", "Video Player"),
            ("HIDE.py", "Py_Programs", "Steg Hide"),
            ("SEEK.py", "Py_Programs", "Steg Seek"),
            ("HIDE_V2.py", "Py_Programs", "Steg Hide V2"),
            ("SEEK_V2.py", "Py_Programs", "Steg Seek V2"),
            ("META.py", "Py_Programs", "Image Metadata"),
            ("PORT.py", "Py_Programs", "Py_PortScanner"),
            ("SCRap.py", "Py_Programs", "Web Scraper"),
            ("SCRAP_V2.py", "Py_Programs", "Web ScrapV2"),
            ("QR_GEN.py", "Py_Programs", "QR Code Gen"),
            ("KEYS.py", "Py_Programs", "Music Visual"),
            ("WAVES.py", "Py_Programs", "Visualizer")
        ]

        num_columns = 3
        for i, program in enumerate(programs):
            button = QPushButton(program[2])
            button.clicked.connect(lambda _=program, p=program: self.open_program(p))
            row = i // num_columns
            col = i % num_columns
            programs_layout.addWidget(button, row, col, 1, 1)

        # About tab
        about_tab = QWidget()
        tab_widget.addTab(about_tab, "About")
        about_layout = QVBoxLayout(about_tab)
        about_label = QLabel(" Py_Programs is a collection of small \n Python programs. They were made for \n Fun, and Practice, \n Feel Free to use them for \n the same and edit them to your \n liking, but Remember,\n With Great Power \n Comes Great Responsibility \n Free Software should always be Free.\n \n Thank you,\n \n AK1R4S4T0H")
        about_label.setStyleSheet("font-size: 16px;")
        about_layout.addWidget(about_label)

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

if __name__ == "__main__":
    program_launcher = Master()
    sys.exit(program_launcher.app.exec())

