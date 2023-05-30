# Python Audio Player using pygame, Work in progress
# Track slider doesnt work, YET
# Skip Buttons in progress, MADE BUT NO FUNCTION
#
""" Created by: AK1R4S4T0H
"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pygame

class Audio:
    def __init__(self, master):
        self.master = master
        master.title("Music")
        master.resizable(True, True)
        master.config(bg='#7733EE')
        master.attributes('-alpha', 0.75)
        master.geometry('333x230')
        master.winfo_toplevel()

        style = ttk.Style()
        style.configure('TButton', border=('#FFFFFF', 5) ,font=('Helvetica', 11, 'bold'), foreground='#FFFFFF', background='#7777EE')
        style.map('TButton', foreground=[("hover", "white")], background=[("hover", "#DD33DD")])
        style.configure('TLabel', font=('Helvetica', 15, 'bold'), foreground='#FFFFFF', background='#7733EE')
        style.configure('TScale', foreground='#FFFFFF', background='#7777EE', troughcolor='#9955EE')
        
        # Labels and buttons
        self.file_label = ttk.Label(master, text="Please choose a song:")
        self.file_label.grid(row=0, columnspan=1, pady=5, sticky="w")

        self.file_button = ttk.Button(master, text="Browse", command=self.choose_file)
        self.file_button.grid(row=1, columnspan=1, pady=2, sticky="w")

        self.play_button = ttk.Button(master, text="Play", command=self.play)
        self.play_button.grid(row=2, column=0, pady=2, sticky="w")

        self.stop_button = ttk.Button(master, text="Stop", command=self.stop)
        self.stop_button.grid(row=3, column=0, pady=5, sticky='w')

        # self.skip_button = ttk.Button(master, text="Skip", command=self.skip)
        # self.skip_button.grid(row=4, column=0, pady=5, sticky='w')

        # self.track_label = ttk.Label(master, text='Track:')
        # self.track_label.grid(row=3, column=3, pady=2, sticky='w')

        # self.track_slider = ttk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, command=self.track)
        # self.track_slider.grid(row=4, column=3, pady=2, sticky='w')

        self.volume_label = ttk.Label(master, text='Volume:')
        self.volume_label.grid(row=5, column=0, pady=2, sticky='w')

        self.volume_slider = ttk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.grid(row=6, column=0, pady=2, sticky='w')

        # Variables
        self.file_path = None
        self.freq = None
        self.time = None

        # Init pygame mixer
        pygame.mixer.init()

    def choose_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3")])
        name = self.file_path[15-0:]  # avoid enlarging the window
        self.file_label.config(text="Song: " + name)

    def track(self, value):
        # track functionality
        pass

    def play(self):
        pygame.mixer.music.load(self.file_path)
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def set_volume(self, value):
        pygame.mixer.music.set_volume(float(value) / 100)

    def skip(self):
        # skip functionality
        pass

if __name__ == '__main__':
    root = tk.Tk()
    app = Audio(root)
    root.mainloop()
