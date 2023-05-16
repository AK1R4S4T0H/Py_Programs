import os
import tkinter as tk
from tkinter import ttk

class Master:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My Programs")
        self.root.geometry("400x550")

        style = ttk.Style()
        style.theme_use('clam')
        bg_color = "#1c1c1c"  
        fg_color = "white"    
        btn_color = "#5c335c" 
        hover_color = "#7e489a" 

        style.configure(".", background=bg_color, foreground=fg_color)
        style.configure("TNotebook", tabposition="n", background=bg_color)
        style.configure("TNotebook.Tab",font=("Helvetica", 15), background=bg_color, foreground=fg_color, padding=[10, 10], width=20)
        style.map("TNotebook.Tab", background=[("selected", btn_color)],padding=[("selected", 7)])
        style.configure("Custom.TButton",
                        background=btn_color,
                        foreground=fg_color,
                        font=("Helvetica", 10),
                        padding=1,
                        width=15)
        style.map("Custom.TButton",
                  foreground=[("hover", "white")],
                  background=[("hover", hover_color)])

        ###### CONFIGURATION ######

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # Home tab
        home_tab = ttk.Frame(self.notebook)
        self.notebook.add(home_tab, text="Home")
        home_label = ttk.Label(home_tab, text="Welcome to Py_Programs! \n   Collection of Various \n   Python Programs!!", font=("Helvetica", 20))
        home_label.grid(row=0, column=0, sticky="nsew")
        
        # Program tab
        programs_tab = ttk.Frame(self.notebook)
        self.notebook.add(programs_tab, text="Programs")

        programs_frame = ttk.Frame(programs_tab)
        programs_frame.grid(row=0, column=0, sticky="nsew")
        
        programs = [
            ("ABC's.py", "Py_Programs", "ABC Flashcards"),
            ("ANYTOMP4.py", "Py_Programs", "Any to Mp4"),
            ("AUDIO.py", "Py_Programs", "Audio Player"),
            ("Calculator.py", "Py_Programs", "Calculator"),
            ("CSVPLOT.py", "Py_Programs", "CSV Plot"),
            ("DODGE.py", "Py_Programs", "Dodge the Dots"),
            ("IMAGE.py", "Py_Programs", "Image Viewer"),
            ("installer.py", "Py_Programs", "Fake Install"),
            ("JAP.py", "Py_Programs", "Japanese Flash"),
            ("MIDIPLAYER.py", "Py_Programs", "Midi Player"),
            ("Notepad.py", "Py_Programs", "Notepad"),
            ("PATTERN_GEN.py", "Py_Programs", "Pattern Generator"),
            ("PYTOEXE.py", "Py_Programs", "Py to EXE"),
            ("STAR.py", "Py_Programs", "Turtle Star"),
            ("VIDEO.py", "Py_Programs", "Video Player")
        ]

        # Create a grid for the buttons
        num_columns = 3
        for i, program in enumerate(programs):
            button = ttk.Button(programs_frame, text=program[2], command=lambda p=program, b=None: self.open_program(p, b))
            button.grid(row=i // num_columns, column=i % num_columns, padx=10, pady=5, sticky="nsew")
            style.configure("Custom.TButton", background=btn_color, foreground=fg_color)
            button.configure(style="Custom.TButton")

        # About tab
        about_tab = ttk.Frame(self.notebook)
        self.notebook.add(about_tab, text="About")
        about_label = ttk.Label(about_tab, text=" Py_Programs is a collection of small \n Python programs. They were made for \n Fun, and Practice, \n Feel Free to use them for \n the same and edit them to your \n liking, but Remember,\n With Great Power \n Comes Great Responsibility \n Free Software should always be Free.\n \n Thank you,\n \n AK1R4", font=("Helvetica", 16))
        about_label.grid(row=0, column=0, sticky="nsew")
            # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        programs_tab.grid_rowconfigure(0, weight=1)
        programs_tab.grid_columnconfigure(0, weight=1)

def open_program(self, program, button):
    initial_directory = os.getcwd() 
    os.chdir(program[1])
    self.root.update()
    os.system("python " + program[0])
    os.chdir(initial_directory)  

if __name__ == "__main__":
    program_launcher = Master()
    program_launcher.root.mainloop()