# Image viewer in python

""" Created by: AK1R4S4T0H
"""
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os

class ImageViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Viewer")
        self.master.geometry("600x600")
        self.master.config(bg='#110011')
        self.images = []
        self.current_image = 0

        self.style = ttk.Style()
        self.style.configure("TButton", background="#555555", foreground="white")
        self.style.map('TButton', foreground=[("hover", "white")], background=[("hover", "#660066")])
        self.style.configure("TLabel", background="#220022", foreground="white")

        self.canvas = tk.Canvas(self.master, bg='#220022', borderwidth=15, width=400, height=400)
        self.canvas.pack(side="top", fill="both", expand=True)

        self.previous_button = ttk.Button(self.master, style="TButton", text="Previous", command=self.show_previous_image)
        self.previous_button.pack(side="left", padx=10, pady=10)

        self.next_button = ttk.Button(self.master, style="TButton", text="Next", command=self.show_next_image)
        self.next_button.pack(side="right", padx=10, pady=10)

        self.browse_button = ttk.Button(self.master,style="TButton", text="Browse", command=self.browse_directory)
        self.browse_button.pack(side="bottom", ipadx=25, pady=10)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.load_images(directory)
            self.show_image()

    def load_images(self, directory):
        self.images.clear()
        for file in os.listdir(directory):
            if file.endswith(".jpg") or file.endswith(".png"):
                image = Image.open(os.path.join(directory, file))
                image = self.resize_image(image)
                self.images.append(ImageTk.PhotoImage(image))

    def resize_image(self, image):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        image_width, image_height = image.size

        width_ratio = canvas_width / image_width
        height_ratio = canvas_height / image_height

        ratio = min(width_ratio, height_ratio)

        new_width = int(image_width * ratio)
        new_height = int(image_height * ratio)
        return image.resize((new_width, new_height), Image.ANTIALIAS)

    def show_image(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.images[self.current_image], anchor="nw")

    def show_next_image(self):
        if self.current_image == len(self.images) - 1:
            self.current_image = 0
        else:
            self.current_image += 1
        self.show_image()

    def show_previous_image(self):
        if self.current_image == 0:
            self.current_image = len(self.images) - 1
        else:
            self.current_image -= 1
        self.show_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()