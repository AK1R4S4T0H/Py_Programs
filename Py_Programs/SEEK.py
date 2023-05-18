import random
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image

def decrypt_data():
    encryption_key = int(entry_key.get())

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
        byte = binary_data[i:i + 8]
        secret_data += chr(int(byte, 2) ^ encryption_key)

    if secret_data.startswith("FILE:"):
        save_path = filedialog.asksaveasfilename(defaultextension=".*", filetypes=[("All Files", "*.*")])
        if save_path:
            with open(save_path, 'wb') as file:
                file.write(secret_data.encode())
            messagebox.showinfo("File Saved", "Hidden file saved successfully!")
    else:
        popup = tk.Toplevel(window)
        popup.title("Extracted Message")

        text = tk.Text(popup, height=20, width=50)
        text.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(popup, command=text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text.config(yscrollcommand=scrollbar.set)
        text.insert(tk.END, secret_data)

        save_button = ttk.Button(popup, text="Save Text", command=lambda: save_text(secret_data))
        save_button.pack(pady=10)

def save_text(text):
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if save_path:
        with open(save_path, 'w') as file:
            file.write(text)
        messagebox.showinfo("Text Saved", "Text saved successfully!")

window = tk.Tk()
window.title("Extract Secrets from Images")

style = ttk.Style()
style.theme_use('clam')
style.configure('.', foreground='white', background='#300a24')
style.configure('TLabel', foreground='white', background='#300a24', font=('Arial', 12))
style.configure('TButton', foreground='white', background='#9c27b0', font=('Arial', 12))
style.configure('TEntry', foreground='black', background='white', font=('Arial', 12))

label_key = ttk.Label(window, text="Enter XOR encryption key:")
label_key.pack()

entry_key = ttk.Entry(window)
entry_key.pack()

button_extract = ttk.Button(window, text="Extract Data", command=decrypt_data)
button_extract.pack()

window.mainloop()
