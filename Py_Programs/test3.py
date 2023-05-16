import tkinter as tk
from tkinter import ttk

root = tk.Tk()

style = ttk.Style()
style.theme_use('default')

style.configure('TButton',
                font=('Helvetica', 11, 'bold'),
                foreground='#FFFFFF',
                background='#7777EE')
style.map('TButton',
          foreground=[("hover", "white")],
          background=[("hover", "#DD33DD")])

style.configure('TLabel',
                font=('Helvetica', 15, 'bold'),
                foreground='#FFFFFF',
                background='#7733EE')

style.configure('TScale',
                foreground='#FFFFFF',
                background='#7777EE',
                troughcolor='#9955EE')


# Get all element names
element_names = style.element_names()

# Print all style options and maps
for element in element_names:
    options = style.element_options(element)
    maps = style.map(element)
    print(f"{element}: {options}")
    print(f"{element} map: {maps}")

root.mainloop()