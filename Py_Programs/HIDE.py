import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image

def hide_data():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*")])
    if not file_path:
        return

    image = Image.open(file_path)

    secret_data = text_entry.get("1.0", tk.END).strip()

    if not secret_data:
        messagebox.showwarning("Error", "Please enter a secret message or select a file.")
        return

    binary_data = ''.join(format(ord(char), '08b') for char in secret_data)

    num_pixels = image.width * image.height
    max_data_size = num_pixels * 3 // 8
    if len(binary_data) > max_data_size:
        messagebox.showwarning("Error", "The selected image is too small to hold the secret data.")
        return

    pixels = image.load()
    data_index = 0

    for row in range(image.height):
        for col in range(image.width):
            r, g, b = pixels[col, row]

            if data_index < len(binary_data):
                r = (r & 0xFE) | int(binary_data[data_index])
                data_index += 1

            if data_index < len(binary_data):
                g = (g & 0xFE) | int(binary_data[data_index])
                data_index += 1

            if data_index < len(binary_data):
                b = (b & 0xFE) | int(binary_data[data_index])
                data_index += 1

            pixels[col, row] = (r, g, b)

            if data_index >= len(binary_data):
                break

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image Files", "*.png"), ("All Files", "*.*")])
    if save_path:
        image.save(save_path)
        messagebox.showinfo("Success", "Image saved successfully!")

window = tk.Tk()
window.title("Hide Secrets in Images")

style = ttk.Style()
style.theme_use('clam')
style.configure('.', foreground='white', background='#300a24')
style.configure('TLabel', foreground='white', background='#300a24', font=('Arial', 12))
style.configure('TButton', foreground='white', background='#9c27b0', font=('Arial', 12))
style.configure('TEntry', foreground='black', background='white', font=('Arial', 12))

label = ttk.Label(window, text="Enter the secret message or select a file:")
label.pack()

text_entry = tk.Text(window, height=4)
text_entry.pack()

button_hide = ttk.Button(window, text="Hide Data", command=hide_data)
button_hide.pack()

button_save = ttk.Button(window, text="Save Image")
button_save.pack()

window.mainloop()


button = ttk.Button(window, text="Select Image", command=hide_data)
button.pack()

window.mainloop()
