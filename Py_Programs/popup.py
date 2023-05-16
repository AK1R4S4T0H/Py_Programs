import tkinter as tk
from tkinter import ttk

def show_popup():
    popup = tk.Toplevel()
    popup.title("Popup")
    popup.geometry("300x200")
    popup.resizable(False, False)
    popup.configure(bg='black')

    label = ttk.Label(popup, text="Welcome to the Popup!!!!!", foreground='white', background='black', font=('Courier', 18, 'bold'))
    label.pack(pady=50)

    button = ttk.Button(popup, text="Close", command=popup.destroy)
    button.pack(pady=20, padx=50)

    popup.focus_set()
    popup.grab_set()
    popup.transient(root)
    popup.wait_window(popup)

root = tk.Tk()
root.title("Pop-up")
root.geometry("400x300")
root.configure(bg='black')

button = ttk.Button(root, text="Show Popup", command=show_popup)
button.pack(pady=100)

root.mainloop()
