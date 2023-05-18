import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image
from PIL.ExifTags import TAGS


def show_image_metadata():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*")])
    if not file_path:
        return

    image = Image.open(file_path)
    metadata = image._getexif()

    metadata_text.delete("1.0", tk.END)

    if metadata:
        for tag_id, value in metadata.items():
            tag_name = TAGS.get(tag_id, tag_id)

            if isinstance(value, bytes):
                try:
                    value = value.decode("utf-8")
                except UnicodeDecodeError:
                    value = repr(value)
            metadata_text.insert(tk.END, f"{tag_name}: {value}\n")
    else:
        metadata_text.insert(tk.END, "No metadata found.")


window = tk.Tk()
window.title("Image Metadata Viewer")

style = ttk.Style()
style.theme_use('clam')
style.configure(".", foreground="white", background="#300a24")
style.configure("TLabel", foreground="white", background="#300a24", font=("Arial", 12))
style.configure("TButton", foreground="white", background="#9c27b0", font=("Arial", 12))
style.configure("TText", foreground="white", background="black", font=("Courier New", 11))

button_select_image = ttk.Button(window, text="Select Image", command=show_image_metadata)
button_select_image.pack(pady=10)

metadata_text = tk.Text(window, height=20, width=80)
metadata_text.pack()

window.mainloop()
