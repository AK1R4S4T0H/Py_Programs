# uses tkhtmlview to make a basic window for a html file
# could be handy for about pages, or readmes for programs
# easy enough to make a popup
import tkinter as tk
from tkinter import ttk
from tkhtmlview import HTMLLabel

class HTMLViewGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML View")
        self.root.geometry("800x600")

        self.create_html_view()

    def create_html_view(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        html_label = HTMLLabel(main_frame)
        html_label.pack(fill=tk.BOTH, expand=True)

        # Load the HTML file
        with open("", "r") as file:
            html_content = file.read()
            html_label.set_html(html_content)

if __name__ == "__main__":
    root = tk.Tk()
    html_view = HTMLViewGUI(root)
    root.mainloop()

