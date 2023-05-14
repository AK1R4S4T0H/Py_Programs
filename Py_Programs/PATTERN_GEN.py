# Python Programs that generates a random Pattern
# made up of small squares
#
import tkinter as tk
import random

WIDTH = 500
HEIGHT = 500

def generate_pattern():
    pattern = []
    for i in range(10):
        row = []
        for j in range(10):
            if random.random() < 0.5:
                row.append(0)
            else:
                row.append(1)
        pattern.append(row)
    return pattern

def draw_pattern(canvas, pattern):
    cell_width = WIDTH // len(pattern[0])
    cell_height = HEIGHT // len(pattern)
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            x1 = j * cell_width
            y1 = i * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            if pattern[i][j] == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill="black")
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill="white")

def main():
    root = tk.Tk()
    root.title("Pattern Generator")
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()
    pattern = generate_pattern()
    button = tk.Button(root, width=40, height=3, text='Another', command=generate_pattern())
    button.pack()
    button1 = tk.Button(root, width=20, height=3, text="draw", command=draw_pattern(canvas, pattern))
    button1.pack()
    draw_pattern(canvas, pattern)
    root.mainloop()



if __name__ == "__main__":
    main()
