# uses tkhtmlview to make a basic window for a html file
# could be handy for about pages, or readmes for programs
# easy enough to make a popup
""" Created by: AK1R4S4T0H
"""
import tkinter as tk
from tkinter import ttk, filedialog
from tkhtmlview import HTMLLabel


class HTMLViewGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML View")
        self.root.geometry("800x600")
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.root.config(background="#a2a6d6")
        self.style.configure("TFrame", background="#a2a6d6")
        self.style.configure("TLabel", background="#ffffff", foreground="black")
        self.style.configure("TButton", background="#a2a6d6", foreground="black")
        

        def open_html():
            file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
            with open(file_path, "r") as file:
                html_content = file.read()
                html_label.set_html(html_content)


        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        html_label = HTMLLabel(main_frame)
        html_label.pack(fill=tk.BOTH, expand=True)

        html_load = ttk.Button(main_frame, text="load HTML", command=lambda: open_html())
        html_load.pack(fill=tk.BOTH, padx=5, pady=10)



if __name__ == "__main__":
    root = tk.Tk()
    html_view = HTMLViewGUI(root)
    root.mainloop()

