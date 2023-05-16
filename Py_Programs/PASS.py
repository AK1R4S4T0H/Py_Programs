# Ttk Password Generator GUI
import tkinter as tk
from tkinter import ttk
import random
import string

def generate_password():
    length = int(length_entry.get())
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
    password_entry.delete(0, tk.END)
    password_entry.insert(tk.END, password)
    update_progress_bar(password)

def reveal_password():
    password_entry.config(show="")

def update_progress_bar(password):
    length = len(password)
    strength = 0

    has_lowercase = any(char.islower() for char in password)
    has_uppercase = any(char.isupper() for char in password)
    has_digits = any(char.isdigit() for char in password)
    has_special_chars = any(char in string.punctuation for char in password)

    if has_lowercase:
        strength += 1
    if has_uppercase:
        strength += 1
    if has_digits:
        strength += 1
    if has_special_chars:
        strength += 1

    if strength == 0:
        progress_bar["value"] = 0
        progress_bar["style"] = "red.Horizontal.TProgressbar"
    elif strength == 1:
        progress_bar["value"] = 25
        progress_bar["style"] = "orange.Horizontal.TProgressbar"
    elif strength == 2:
        progress_bar["value"] = 50
        progress_bar["style"] = "yellow.Horizontal.TProgressbar"
    elif strength == 3:
        progress_bar["value"] = 75
        progress_bar["style"] = "green.Horizontal.TProgressbar"
    else:
        progress_bar["value"] = 100
        progress_bar["style"] = "blue.Horizontal.TProgressbar"


root = tk.Tk()
root.title("Password Generator")

length_label = ttk.Label(root, text="Password Length:")
length_label.pack()
length_entry = ttk.Entry(root)
length_entry.pack()

generate_button = ttk.Button(root, text="Generate Password", command=generate_password)
generate_button.pack()

password_entry = ttk.Entry(root, show="*")
password_entry.pack()

reveal_button = ttk.Button(root, text="Reveal Password", command=reveal_password)
reveal_button.pack()

progress_style = ttk.Style()
progress_style.theme_use("default")
progress_style.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
progress_style.configure("orange.Horizontal.TProgressbar", foreground='orange', background='orange')
progress_style.configure("yellow.Horizontal.TProgressbar", foreground='yellow', background='yellow')
progress_style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
progress_style.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue')

progress_bar = ttk.Progressbar(root, mode="determinate", length=200)
progress_bar.pack()

root.mainloop()
