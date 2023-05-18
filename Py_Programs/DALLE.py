# Tried to make a DALLE Image Generator tkinter GUI
""" Created by: AK1R4S4T0H
"""
import tkinter as tk
import pytorch as torch
from transformers import DALLEForImageGeneration, DALLETokenizer
from PIL import Image, ImageTk

# Load the DALLE model and tokenizer
model = DALLEForImageGeneration.from_pretrained('image_generation_model')
tokenizer = DALLETokenizer.from_pretrained('image_generation_model')

window = tk.Tk()
window.title("DALLE Image Generation")
window.geometry("800x600")

input_box = tk.Entry(window, width=50)
input_box.pack(pady=20)

def generate_image():
    input_text = input_box.get()
    encoded_input = tokenizer(input_text, return_tensors='pt', padding=True)
    with torch.no_grad():
        output = model.generate(**encoded_input)
    image = Image.fromarray(output[0].permute(1, 2, 0).numpy())
    image = image.resize((400, 400))
    image_tk = ImageTk.PhotoImage(image)
    image_label.configure(image=image_tk)
    image_label.image = image_tk

generate_button = tk.Button(window, text="Generate Image", command=generate_image)
generate_button.pack()

image_label = tk.Label(window)
image_label.pack(pady=20)

window.mainloop()
