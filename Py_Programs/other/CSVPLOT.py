# Genreate a matplotlib graph based on whatever CSV file you
# Open with it
#
""" Created by: AK1R4S4T0H
"""
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt


def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        data = pd.read_csv(file_path)
        return data
    return None


def plot_scatter():
    selected_x = x_variable.get()
    selected_y = y_variable.get()
    title = title_entry.get()
    x_label = x_label_entry.get()
    y_label = y_label_entry.get()
    marker_color = color_entry.get()
    marker_size = int(size_entry.get())

    data = load_data()
    if data is not None:
        plt.scatter(data[selected_x], data[selected_y], color=marker_color, s=marker_size)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()


window = tk.Tk()
window.title("Data Science Plot GUI")

load_button = tk.Button(window, text="Load Data", command=load_data)
load_button.pack(pady=10)

x_variable = tk.StringVar(window)
y_variable = tk.StringVar(window)

x_label = tk.Label(window, text="X-Axis")
x_label.pack()

x_dropdown = tk.OptionMenu(window, x_variable, "")
x_dropdown.pack()

y_label = tk.Label(window, text="Y-Axis")
y_label.pack()

y_dropdown = tk.OptionMenu(window, y_variable, "")
y_dropdown.pack()

title_label = tk.Label(window, text="Title")
title_label.pack()

title_entry = tk.Entry(window)
title_entry.pack()

x_label_label = tk.Label(window, text="X-Axis Label")
x_label_label.pack()

x_label_entry = tk.Entry(window)
x_label_entry.pack()

y_label_label = tk.Label(window, text="Y-Axis Label")
y_label_label.pack()

y_label_entry = tk.Entry(window)
y_label_entry.pack()

color_label = tk.Label(window, text="Marker Color")
color_label.pack()

color_entry = tk.Entry(window)
color_entry.pack()

size_label = tk.Label(window, text="Marker Size")
size_label.pack()

size_entry = tk.Entry(window)
size_entry.pack()

plot_button = tk.Button(window, text="Plot", command=plot_scatter)
plot_button.pack(pady=10)

# Update dropdowns with column names once data is loaded
data = load_data()
if data is not None:
    columns = list(data.columns)
    x_variable.set(columns[0])
    y_variable.set(columns[1])
    x_dropdown["menu"].delete(0, "end")
    y_dropdown["menu"].delete(0, "end")
    for column in columns:
        x_dropdown["menu"].add_command(label=column, command=lambda value=column: x_variable.set(value))
        y_dropdown["menu"].add_command(label=column, command=lambda value=column: y_variable.set(value))

# Run the GUI main loop
window.mainloop()
