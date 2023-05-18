# ttk attributes
""" Created by: AK1R4S4T0H
"""
import tkinter as tk
from tkinter import ttk

def button_clicked():
    label.configure(text="Button clicked!")

root = tk.Tk()
root.title("TTK GUI Example")

# Creating a Frame
frame = ttk.Frame(root, padding="20 20 20 20")
frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

# Creating a Label
label = ttk.Label(frame, text="Hello, TTK!")
label.grid(column=0, row=0, padx=5, pady=5)

# Creating a Button
button = ttk.Button(frame, text="Click Me!", command=button_clicked)
button.grid(column=0, row=1, padx=5, pady=5)

# Creating an Entry
entry = ttk.Entry(frame)
entry.grid(column=0, row=2, padx=5, pady=5)

# Creating a Checkbutton
checkbutton_var = tk.StringVar()
checkbutton = ttk.Checkbutton(frame, text="Check me!", variable=checkbutton_var, onvalue="On", offvalue="Off")
checkbutton.grid(column=0, row=3, padx=5, pady=5)

# Creating a Combobox
combobox_var = tk.StringVar()
combobox = ttk.Combobox(frame, textvariable=combobox_var)
combobox['values'] = ('Option 1', 'Option 2', 'Option 3')
combobox.grid(column=0, row=4, padx=5, pady=5)

# Creating a Progressbar
progressbar = ttk.Progressbar(frame, length=200, mode='indeterminate')
progressbar.grid(column=0, row=5, padx=5, pady=5)
progressbar.start()

# Creating a Notebook with Tabs
notebook = ttk.Notebook(frame)
notebook.grid(column=1, row=0, rowspan=6, padx=5, pady=5)

# Adding tabs to the Notebook
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='Tab 1')

tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='Tab 2')

# Creating a Treeview
treeview = ttk.Treeview(tab1)
treeview.grid(column=0, row=0, padx=5, pady=5)
treeview.insert('', '0', 'item1', text='Item 1')
treeview.insert('', '1', 'item2', text='Item 2')

# Running the GUI
root.mainloop()
