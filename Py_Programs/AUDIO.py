# Python Audio Player using pygame, Work in progress
# Track slider doesnt work, YET
# Skip Buttons in progress, MADE BUT NO FUNCTION
import tkinter as tk;from tkinter import filedialog
from tkinter import font as tkFont;import pygame

class Audio:
    def __init__(self, master):
        self.master = master;master.title("Music")
        master.resizable(True, True);master.config(bg='#7700EE')
        master.attributes('-alpha', 0.75);master.geometry('333x230')
        helv36 = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)
        helv = tkFont.Font(family='Helvetica', size=11, weight=tkFont.BOLD)

        # labels and buttons
        self.file_label = tk.Label(master, font=helv36, borderwidth=2, text="Please shoose a song:")
        self.file_label.grid(row=0, columnspan=1, pady=5, sticky="w")

        self.file_button = tk.Button(master, font=helv, borderwidth=2,  text="Browse:", command=self.choose_file)
        self.file_button.grid(row=1, columnspan=1, pady=2, sticky="w")

        self.play_button = tk.Button(master, font=helv, borderwidth=2, text="Play", command=self.play)
        self.play_button.grid(row=2, column=0, pady=2, sticky="w")

        self.stop_button = tk.Button(master, font=helv, borderwidth=2, text="Stop", command=self.stop)
        self.stop_button.grid(row=3, column=0, pady=5, sticky='w')

        # self.skip_button = tk.Button(master, font=helv, borderwidth=2, text="Skip")
        # self.skip_button.grid(row=4, column=0, pady=5, sticky='w')

        # self.track_label = tk.Label(master, font=helv, borderwidth=2, text='Track:')
        # self.track_label.grid(row=3, column=3, pady=2, sticky='w')

        # self.track_slider = tk.Scale(master, borderwidth=2, from_=0, to=100, orient=tk.HORIZONTAL, command=self.track)
        # self.track_slider.gri
        
        # volume sd(row=4, column=3, pady=2, sticky='w')
        # volume slider
        self.volume_label = tk.Label(master, font=helv, borderwidth=2, text='Volume:')
        self.volume_label.grid(row=1, column=3, pady=2, sticky='w')

        self.volume_slider = tk.Scale(master, borderwidth=2, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.grid(row=2, column=3, pady=2, sticky='w')

        # variables
        self.file_path = None;self.freq = None;self.time = None      
        # look into properly implementing time
        # Initialize pygame mixer, dont forget about this again
        pygame.mixer.init()

    def choose_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3")])
        name = self.file_path[15-0:] # so the name isnt too long and makes the window larger
        self.file_label.config(text=f"Song: " + name)

    def track(self, value):
        self.value = Audio.time;value.value = self.value
        return self.value

    def play(self):
        pygame.mixer.music.load(self.file_path)
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def set_volume(self, value):
        pygame.mixer.music.set_volume(float(value) / 100)

    def skip(self):
        pass

root = tk.Tk();app = Audio(root)
root.mainloop()