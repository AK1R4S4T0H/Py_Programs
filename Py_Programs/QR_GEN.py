import tkinter as tk
from tkinter import filedialog
import qrcode
from PIL import Image, ImageTk

QR_CODE_SIZE = 600

def generate_and_draw(canvas, data_entry, file_entry):
    data = data_entry.get()
    filename = file_entry.get()

    if not data and not filename:
        return

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)

    if data:
        qr.add_data(data)

    if filename:
        with open(filename, 'rb') as file:
            qr.add_data(file.read())

    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Resize the image
    img = img.resize((QR_CODE_SIZE, QR_CODE_SIZE), Image.ANTIALIAS)

    # Convert the QRCode image to PhotoImage
    img_pil = img.convert("RGB")
    img_tk = ImageTk.PhotoImage(img_pil)

    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.image = img_tk

def select_file(file_entry):
    filename = filedialog.askopenfilename()
    if filename:
        file_entry.delete(0, tk.END)
        file_entry.insert(tk.END, filename)

def save_image(canvas):
    image = canvas.image
    if image:
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")])
        if filename:
            image.save(filename)

def main():
    root = tk.Tk()
    root.title("QR Code Generator")
    root.geometry("800x800")

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame, width=QR_CODE_SIZE, height=QR_CODE_SIZE)
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    file_frame = tk.Frame(main_frame)
    file_frame.pack(pady=10)

    file_entry = tk.Entry(file_frame, width=50)
    file_entry.pack(side=tk.LEFT)

    file_button = tk.Button(file_frame, text="Select File", command=lambda: select_file(file_entry))
    file_button.pack(side=tk.LEFT, padx=5)

    data_frame = tk.Frame(main_frame)
    data_frame.pack(pady=10)

    data_label = tk.Label(data_frame, text="Data:")
    data_label.pack(side=tk.LEFT)

    data_entry = tk.Entry(data_frame, width=50)
    data_entry.pack(side=tk.LEFT)

    draw_button = tk.Button(main_frame, text="Draw QR Code", command=lambda: generate_and_draw(canvas, data_entry, file_entry))
    draw_button.pack(pady=10)

    save_button = tk.Button(main_frame, text="Save QR Code", command=lambda: save_image(canvas))
    save_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()