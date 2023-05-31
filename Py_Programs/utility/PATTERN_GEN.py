# Python Programs that generates a random Pattern
# made up of small squares
# Updated to Ttk, and made buttons work
""" Created by: AK1R4S4T0H
"""
import tkinter as tk
import tkinter.ttk as ttk
import random

WIDTH = 200
HEIGHT = 150

def generate_and_draw(canvas):
    pattern = []
    for i in range(10):
        row = []
        for j in range(10):
            if random.random() < 0.5:
                row.append(0)
            else:
                row.append(1)
        pattern.append(row)
    draw_pattern(canvas, pattern)

def draw_pattern(canvas, pattern):
    canvas.delete("all")  # Clear the canvas
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
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', background='#5c335c', foreground='white', width=25, borderwidth=1, focusthickness=3.5, focuscolor='none')
    style.map('TButton', background=[('active', '#7c007c')])
    style.configure('TFrame', background='#5c335c', foreground='white', width=25, borderwidth=1, relief='flat', focusthickness=2.5, focuscolor='none')
    style.map('TFrame', background=[('active', '#7c007c')])
    style.configure('TCanvas', background='#5c335c', foreground='white', width=25, borderwidth=1, relief='flat', focusthickness=3.5, focuscolor='white')
    style.map('TCanvas')
    
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    canvas = tk.Canvas(main_frame, width=WIDTH, height=HEIGHT)
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    draw_button = ttk.Button(main_frame, text="Draw", command=lambda: generate_and_draw(canvas))
    draw_button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()