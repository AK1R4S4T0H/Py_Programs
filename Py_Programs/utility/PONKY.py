""" Created by: AK1R4S4T0H
"""
# Python Conky like program
import psutil
import platform
import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkinter import font as tkfont


import psutil
import platform
import tkinter as tk
from tkinter import ttk


class PonkyPy:
    def __init__(self):
        self.BACKGROUND_COLOR = "#492a44"
        self.LABEL_COLOR = "#d1d1e0"
        self.METER_COLOR = "#daaaff"
        self.root = tk.Tk()
        self.root.title("PONKY PY")
        self.root.configure(bg=self.BACKGROUND_COLOR)
        self.style = ttk.Style()
        self.style.configure("Custom.Horizontal.TProgressbar", troughcolor=self.BACKGROUND_COLOR, background=self.METER_COLOR)

        # CPU
        self.cpu_label = ttk.Label(self.root, text="CPU Usage:", foreground=self.LABEL_COLOR, background=self.BACKGROUND_COLOR)
        self.cpu_label.pack()

        self.cpu_meter = ttk.Progressbar(self.root, mode="determinate", length=200, style="Custom.Horizontal.TProgressbar", value=0)
        self.cpu_meter.pack()

        # RAM
        self.ram_label = ttk.Label(self.root, text="RAM Usage:", foreground=self.LABEL_COLOR, background=self.BACKGROUND_COLOR)
        self.ram_label.pack()

        self.ram_meter = ttk.Progressbar(self.root, mode="determinate", length=200, style="Custom.Horizontal.TProgressbar", value=0)
        self.ram_meter.pack()

        # SysInfo
        self.system_label = ttk.Label(self.root, text="System Information:", foreground=self.LABEL_COLOR, background=self.BACKGROUND_COLOR, font=("Arial", 12, "bold"))
        self.system_label.pack(pady=10)

        self.system_info = ttk.Label(self.root, text="", foreground=self.LABEL_COLOR, background=self.BACKGROUND_COLOR, justify="left")
        self.system_info.pack()

        self.update_meter()

    def update_meter(self):
        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent

        self.cpu_meter["value"] = cpu_percent
        self.ram_meter["value"] = ram_percent

        self.cpu_label.config(text=f"CPU Usage: {cpu_percent}%")
        self.ram_label.config(text=f"RAM Usage: {ram_percent}%")

        self.root.after(1000, self.update_meter)

    def run(self):
        # Retrieve SysInfo
        system_details = []
        system_details.append(f"OS: {platform.system()} {platform.release()}")
        system_details.append(f"Processor: {platform.processor()}")
        system_details.append(f"Machine: {platform.machine()}")
        system_details.append(f"System Type: {platform.architecture()[0]}")
        system_details.append(f"Memory: {round(psutil.virtual_memory().total / (1024 ** 3))} GB")
        system_details.append(f"Hostname: {platform.node()}")
        system_details.append(f"Python Version: {platform.python_version()}")

        self.system_info.config(text="\n".join(system_details))

        self.root.mainloop()


if __name__ == "__main__":
    ponky = PonkyPy()
    ponky.run()
