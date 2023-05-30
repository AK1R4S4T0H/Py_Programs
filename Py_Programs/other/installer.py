# Fake Installer, why not
""" Created by: AK1R4S4T0H
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def install():
    install_button.config(state=tk.DISABLED)
    progress_bar.start(10)

    for i in range(21):
        progress_bar.step(1)
        progress_label.config(text=f'Installing {i*1}%...')
        root.update_idletasks()
        root.after(1000)

    progress_label.config(text='Installation complete!')
    install_button.config(text='Exit', command=confirm_exit, state=tk.NORMAL)
    progress_bar.stop()

def confirm_exit():
    result = messagebox.askquestion("Confirm Exit", "Are you sure you want to exit?")
    if result == 'yes':
        root.destroy()

root = tk.Tk()
root.title('Fake Installer')

# Configure styles
style = ttk.Style()
style.configure('TFrame', background='#f1f1f1')
style.configure('TLabel', background='#f1f1f1', font=('Helvetica', 16, 'bold'))
style.configure('Custom.Horizontal.TProgressbar', troughcolor='#c4c4c4', background='#007acc',
                lightcolor='green', darkcolor='green')
style.configure('TButton', background='#007acc', foreground='white', font=('Helvetica', 12), padx=10, pady=5)
style.map('TButton', background=[('active', '#004c80')])

# Main frame
main_frame = ttk.Frame(root, padding='20', style='TFrame')
main_frame.pack()
title_label = ttk.Label(main_frame, text='Installation Wizard', style='TLabel')
title_label.pack(pady=(0, 20))
progress_bar = ttk.Progressbar(main_frame, length=300, mode='determinate',
                              style='Custom.Horizontal.TProgressbar')
progress_bar.pack()
progress_label = ttk.Label(main_frame, text='Installing...', style='TLabel')
progress_label.pack(pady=(20, 10))
install_button = ttk.Button(main_frame, text='Install', command=install, style='TButton')
install_button.pack(pady=(10, 0))

root.protocol("WM_DELETE_WINDOW", confirm_exit)  # Handle window close button

root.mainloop()
