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
        self.root.geometry("400x450")
        self.root.configure(bg="#1c1c1c")

        # Create label for title
        title = tk.Label(self.root, text="Py_Programs", font=("Helvetica", 20), fg="#FFFFFF", bg="#1c1c1c")
        title.pack(pady=20)

        # Create button for each program
        programs = [
            ("AUDIO.py", "Py_Programs"),
            ("Calculator.py", "Py_Programs"),
            ("IMAGE.py", "Py_Programs"),
            ("JAP.py", "Py_Programs"),
            ("MIDIPLAYER.py", "Py_Programs"),
            ("Notepad.py", "Py_Programs"),
            ("PATTERN_GEN.py", "Py_Programs"),
            ("PYTOEXE.py", "Py_Programs"),
            ("STAR.py", "Py_Programs")
        ]
        for program in programs:
            button = ttk.Button(self.root, text=program[0], command=lambda p=program: self.open_program(p))
            button.pack(pady=5)

    def open_program(self, program):
        initial_directory = os.getcwd()  # Store the initial directory
        os.chdir(program[1])
        os.system("python " + program[0])
        os.chdir(initial_directory)  # Return back to the initial directory

if __name__ == "__main__":
    program_launcher = Master()
    program_launcher.root.mainloop()