import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import random

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*")])
    if file_path:
        button_save.config(state=tk.NORMAL)
        button_hide.config(state=tk.NORMAL)
        label_selected_image.config(text="Selected Image: " + file_path)
        window.image_path = file_path

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        window.file_path = file_path
        label_selected_file.config(text="Selected File: " + file_path)

def hide_data():
    file_path = window.image_path
    if not file_path:
        messagebox.showwarning("Error", "Please select an image file.")
        return

    image = Image.open(file_path)

    secret_data = ""
    if hasattr(window, 'file_path'):
        with open(window.file_path, 'r') as file:
            secret_data = file.read()

    if not secret_data:
        messagebox.showwarning("Error", "Please select a file to hide.")
        return

    # XOR encryption key
    encryption_key = random.randint(1, 255)

    # Perform XOR encryption on the secret data
    encrypted_data = "".join(chr(ord(char) ^ encryption_key) for char in secret_data)

    binary_data = ''.join(format(ord(char), '08b') for char in encrypted_data)

    num_pixels = image.width * image.height
    max_data_size = num_pixels * 3 // 8
    if len(binary_data) > max_data_size:
        messagebox.showwarning("Error", "The selected image is too small to hold the file.")
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

        # Provide the encryption key to the user
        messagebox.showinfo("Encryption Key", "Encryption key: {}".format(encryption_key))

window = tk.Tk()
window.title("Hide Secrets in Images")

style = ttk.Style()
style.theme_use('clam')
style.configure('.', foreground='white', background='#300a24')
style.configure('TLabel', foreground='white', background='#300a24', font=('Arial', 12))
style.configure('TButton', foreground='white', background='#9c27b0', font=('Arial', 12))
style.configure('TEntry', foreground='black', background='white', font=('Arial', 12))

label = ttk.Label(window, text="Enter the secret message or select a file:")
label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

text_entry = tk.Text(window, height=4)
text_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

button_select_image = ttk.Button(window, text="Select Image", command=select_image)
button_select_image.grid(row=2, column=0, padx=10, pady=10)

button_select_file = ttk.Button(window, text="Select File", command=select_file)
button_select_file.grid(row=2, column=1, padx=10, pady=10)

button_hide = ttk.Button(window, text="Hide Data", command=hide_data, state=tk.DISABLED)
button_hide.grid(row=3, column=0, padx=10, pady=10)

button_save = ttk.Button(window, text="Save Image", state=tk.DISABLED)
button_save.grid(row=3, column=1, padx=10, pady=10)

label_selected_image = ttk.Label(window, text="Selected Image: ")
label_selected_image.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

label_selected_file = ttk.Label(window, text="Selected File: ")
label_selected_file.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

window.mainloop()

