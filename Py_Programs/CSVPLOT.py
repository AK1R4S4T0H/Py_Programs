# Genreate a matplotlib graph based on whatever CSV file you
# Open with it
#
""" Created by: AK1R4S4T0H
"""
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import pandas as pd

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if file_path:
        data = pd.read_csv(file_path)
        generate_graph(data)

def generate_graph(data):
    plt.figure(figsize=(8, 6))

    column_names = list(data.columns)

    x_column = column_names[0]
    y_columns = column_names[1:]

    for y_column in y_columns:
        plt.plot(data[x_column], data[y_column], label=y_column)

    plt.xlabel(x_column)
    plt.ylabel(y_columns)
    plt.title('CSV Data Graph')
    plt.grid(True)
    plt.legend()
    plt.show()


root = tk.Tk()
root.title('CSV Graph')

open_button = tk.Button(root, text='Open CSV', command=open_file)
open_button.pack(pady=10)

root.mainloop()