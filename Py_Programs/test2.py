# more ttk attributes
# on the house
import tkinter as tk
from tkinter import ttk

def button_clicked():
    label.configure(text="Button clicked!")
    messagebox.showinfo("Info", "Button clicked!")

def menu_selected(event):
    selected_item = combobox.get()
    label.configure(text=f"Selected: {selected_item}")

root = tk.Tk()
root.title("Additional TTK GUI Example")

# Creating a Notebook with Tabs
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Tab 1: LabelFrame
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='LabelFrame')

label_frame = ttk.LabelFrame(tab1, text="LabelFrame")
label_frame.pack(padx=20, pady=20)

label = ttk.Label(label_frame, text="Hello, TTK!")
label.pack(padx=10, pady=10)

button = ttk.Button(label_frame, text="Click Me!", command=button_clicked)
button.pack(padx=10, pady=10)

# Tab 2: Scale and Separator
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='Scale & Separator')

scale = ttk.Scale(tab2, from_=0, to=100, length=200, orient=tk.HORIZONTAL)
scale.pack(padx=20, pady=20)

separator = ttk.Separator(tab2, orient=tk.HORIZONTAL)
separator.pack(fill=tk.X, padx=20, pady=20)

# Tab 3: Progressbar and Scrollbar
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text='Progressbar & Scrollbar')

progressbar = ttk.Progressbar(tab3, length=200, mode='determinate')
progressbar.pack(padx=20, pady=20)

scrollbar = ttk.Scrollbar(tab3, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)

listbox = tk.Listbox(tab3, yscrollcommand=scrollbar.set)
for i in range(1, 21):
    listbox.insert(tk.END, f"Item {i}")
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
scrollbar.config(command=listbox.yview)

# Tab 4: OptionMenu
tab4 = ttk.Frame(notebook)
notebook.add(tab4, text='OptionMenu')

options = ['Option 1', 'Option 2', 'Option 3']
selected_option = tk.StringVar()
selected_option.set(options[0])

optionmenu = ttk.OptionMenu(tab4, selected_option, *options)
optionmenu.pack(padx=20, pady=20)

# Tab 5: Notebook Styling
tab5 = ttk.Frame(notebook)
notebook.add(tab5, text='Notebook Styling')

style = ttk.Style()
style.configure("Custom.TNotebook.Tab", background="lightblue", padding=[10, 5])
notebook.configure(style="Custom.TNotebook")

# Running the GUI
root.mainloop()
