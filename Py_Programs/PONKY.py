import psutil
import platform
import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkinter import font as tkfont

BACKGROUND_COLOR = "#292a44"
LABEL_COLOR = "#d1d1e0"
METER_COLOR = "#8a85ff"

def update_meter():
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent

    cpu_meter["value"] = cpu_percent
    ram_meter["value"] = ram_percent

    cpu_label.config(text=f"CPU Usage: {cpu_percent}%")
    ram_label.config(text=f"RAM Usage: {ram_percent}%")

    root.after(1000, update_meter)

root = tk.Tk()
root.title("PONKY PY")
root.configure(bg=BACKGROUND_COLOR)
style = ttk.Style()
style.configure("Custom.Horizontal.TProgressbar", troughcolor=BACKGROUND_COLOR, background=METER_COLOR)

# CPU
cpu_label = ttk.Label(root, text="CPU Usage:", foreground=LABEL_COLOR, background=BACKGROUND_COLOR)
cpu_label.pack()

cpu_meter = ttk.Progressbar(root, mode="determinate", length=200, style="Custom.Horizontal.TProgressbar", value=0)
cpu_meter.pack()

# RAM
ram_label = ttk.Label(root, text="RAM Usage:", foreground=LABEL_COLOR, background=BACKGROUND_COLOR)
ram_label.pack()

ram_meter = ttk.Progressbar(root, mode="determinate", length=200, style="Custom.Horizontal.TProgressbar", value=0)
ram_meter.pack()

# SysInfo
system_label = ttk.Label(root, text="System Information:", foreground=LABEL_COLOR, background=BACKGROUND_COLOR, font=("Arial", 12, "bold"))
system_label.pack(pady=10)

system_info = ttk.Label(root, text="", foreground=LABEL_COLOR, background=BACKGROUND_COLOR, justify="left")
system_info.pack()

# Retrieve SysInfo
system_details = []
system_details.append(f"OS: {platform.system()} {platform.release()}")
system_details.append(f"Processor: {platform.processor()}")
system_details.append(f"Machine: {platform.machine()}")
system_details.append(f"System Type: {platform.architecture()[0]}")
system_details.append(f"Memory: {round(psutil.virtual_memory().total / (1024 ** 3))} GB")
system_details.append(f"Hostname: {platform.node()}")
system_details.append(f"Python Version: {platform.python_version()}")

system_info.config(text="\n".join(system_details))

update_meter()

root.mainloop()

