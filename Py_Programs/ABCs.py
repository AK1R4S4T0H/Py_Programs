""" Created by: AK1R4S4T0H
"""
import random
import tkinter as tk

phrases = {'A','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w', 'x','y','z',
'B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V', 'W','X','Y','Z',
'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17','18', '19', '20'}

root = tk.Tk()
root.title("ABC's")
root.geometry("400x400")

label = tk.Label(root, font=("Sans", 150), bg="black", fg="white")

def display_phrase():
    phrase = random.choice(list(phrases))
    label.config(text=f"{phrase}")
    
    root.after(10000, display_phrase)

button = tk.Button(root, text="Show me a phrase!", command=display_phrase)

label.pack(expand=True, fill='both')
button.pack()

root.mainloop()