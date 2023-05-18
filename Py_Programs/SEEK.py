import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image

def extract_data():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*")])
    if not file_path:
        return

    image = Image.open(file_path)

    binary_data = ""

    pixels = image.load()

    for row in range(image.height):
        for col in range(image.width):
            r, g, b = pixels[col, row]

            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    secret_data = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        secret_data += chr(int(byte, 2))

    messagebox.showinfo("Extracted Message", secret_data)

window = tk.Tk()
window.title("Extract Secrets from Images")

style = ttk.Style()
style.theme_use('clam')
style.configure('.', foreground='white', background='#300a24')
style.configure('TLabel', foreground='white', background='#300a24', font=('Arial', 12))
style.configure('TButton', foreground='white', background='#9c27b0', font=('Arial', 12))
style.configure('TEntry', foreground='black', background='white', font=('Arial', 12))

label = ttk.Label(window, text="Select an image to extract the hidden message:")
label.pack()

button_extract = ttk.Button(window, text="Extract Data", command=extract_data)
button_extract.pack()

window.mainloop()
