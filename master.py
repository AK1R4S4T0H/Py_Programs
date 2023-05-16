# master program for launching others
# isnt perfect, but better than the other one
import os
import tkinter as tk
from tkinter import ttk
import PIL





class Master:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My Programs")
        self.root.geometry("400x550")
        self.root.configure(bg="#1c1c1c")
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('TButton', background = '#5c335c', foreground = 'white', width = 25, borderwidth=1, relief='flat', focusthickness=3.5, focuscolor='white')
        style.map('TButton', background=[('active','#7c007c')])
        title = tk.Label(self.root, text="Py_Programs", font=("Helvetica", 35), fg="#FFFFFF", bg="#1c1c1c")
        title.pack(pady=20)

        # button for each program
        programs = [
            ("AUDIO.py", "Py_Programs","Audio Player"),
            ("Calculator.py", "Py_Programs","Calculator"),
            ("DODGE.py", "Py_Programs","Dodge the Dots"),
            ("IMAGE.py", "Py_Programs","Image Viewer"),
            ("JAP.py", "Py_Programs", "Japanese Flash Cards"),
            ("MIDIPLAYER.py", "Py_Programs","Midi Player"),
            ("Notepad.py", "Py_Programs","Notepad"),
            ("PATTERN_GEN.py", "Py_Programs","Pattern Generator"),
            ("PYTOEXE.py", "Py_Programs", "Py to EXE"),
            ("STAR.py", "Py_Programs", "Turtle Star"),
            ("VIDEO.py", "Py_Programs", "Video Player")
        ]
        for program in programs:
            button = ttk.Button(self.root,  text=program[2], command=lambda p=program: self.open_program(p))
            button.pack(pady=5)


    def open_program(self, program):
        initial_directory = os.getcwd()  # Store the initial directory
        os.chdir(program[1])
        os.system("python " + program[0])
        os.chdir(initial_directory)  # Return back to the initial directory

if __name__ == "__main__":
    program_launcher = Master()
    program_launcher.root.mainloop()