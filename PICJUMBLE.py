# Program for jumbling images for use in Machine Learning
# Add normal file dialog for image open
import random
from tkinter import *
from PIL import Image, ImageTk

original_image = Image.open(r"")

rows = 3
cols = 3

width = original_image.width // cols
height = original_image.height // rows

grid_pieces = []

for r in range(rows):
    for c in range(cols):
        x0 = c * width
        y0 = r * height
        x1 = x0 + width
        y1 = y0 + height
        grid_piece = original_image.crop((x0, y0, x1, y1))
        grid_pieces.append(grid_piece)

# rotate grid piece and shuffle
random.shuffle(grid_pieces)
for i in range(len(grid_pieces)):
    grid_pieces[i] = grid_pieces[i].rotate(90)

# pasting the grid pieces
new_image = Image.new("RGB", (original_image.width, original_image.height))
for r in range(rows):
    for c in range(cols):
        i = r * cols + c
        x0 = c * width
        y0 = r * height
        x1 = x0 + width
        y1 = y0 + height
        new_image.paste(grid_pieces[i], (x0, y0, x1, y1))


root = Tk()
root.title("Jumbled Image")

# convert to PhotoImage
photo = ImageTk.PhotoImage(new_image)

label = Label(root, image=photo)
label.pack()

def save_image():
    new_image.save("jumbled_image.jpg")


button = Button(root, text="Save", command=save_image)
button.pack()

root.mainloop()
