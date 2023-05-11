# Creates an EXE from a .py file
import tkinter as tk
import tkinter.filedialog as fd
import subprocess

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.file_path = tk.StringVar()
        self.file_label = tk.Label(self, textvariable=self.file_path)
        self.file_label.pack(side="top")

        self.choose_file_button = tk.Button(self, text="Choose file", command=self.choose_file)
        self.choose_file_button.pack(side="top")

        self.convert_button = tk.Button(self, text="Convert to .exe", command=self.convert_to_exe)
        self.convert_button.pack(side="bottom")

    def choose_file(self):
        filetypes = (("Python files", "*.py"), ("All files", "*.*"))
        file_path = fd.askopenfilename(title="Choose a file", filetypes=filetypes)
        self.file_path.set(file_path)

    def convert_to_exe(self):
        file_path = self.file_path.get()
        subprocess.call(["pyinstaller", "--onefile", file_path])
        self.file_path.set("")

root = tk.Tk()
app = App(master=root)
app.mainloop()
