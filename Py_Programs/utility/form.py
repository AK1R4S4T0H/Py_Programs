""" Created by: AK1R4S4T0H
"""
import tkinter as tk
from tkinter import ttk
import csv

def submit_form():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        result_label.config(text="Form submitted successfully!")
        with open('form.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password])
    else:
        result_label.config(text="Please fill in all fields.")

root = tk.Tk()
root.title("User Registration Form")

notebook = ttk.Notebook(root)
notebook.pack()
# tab 1
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Registration Form")
form_frame = ttk.Frame(tab1, padding=20)
form_frame.pack()

username_label = ttk.Label(form_frame, text="Username:")
username_label.grid(row=0, column=0, sticky=tk.W)

username_entry = ttk.Entry(form_frame, width=30)
username_entry.grid(row=0, column=1)

password_label = ttk.Label(form_frame, text="Password:")
password_label.grid(row=1, column=0, sticky=tk.W)

password_entry = ttk.Entry(form_frame, width=30, show="*")
password_entry.grid(row=1, column=1)

submit_button = ttk.Button(form_frame, text="Submit", command=submit_form)
submit_button.grid(row=2, columnspan=2)
# tab 2
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Results")

result_label = ttk.Label(tab2, text="")
result_label.pack()

root.mainloop()
