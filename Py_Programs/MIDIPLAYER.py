# MIDI Player, Needs work
import mido
import rtmidi
import pyaudio
import tkinter as tk
from tkinter import filedialog

class MidiPlayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('MIDI Player')
        self.root.geometry('300x100')

        self.file_path = ''
        self.midi_file = None
        self.playing = False

        self.file_label = tk.Label(self.root, text='No file selected')
        self.file_label.pack()

        self.open_button = tk.Button(self.root, text='Open', command=self.open_file)
        self.open_button.pack()

        self.play_button = tk.Button(self.root, text='Play', command=self.play)
        self.play_button.pack()

        self.stop_button = tk.Button(self.root, text='Stop', command=self.stop)
        self.stop_button.pack()

        self.root.mainloop()

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[('MIDI Files', '*.mid')])
        if self.file_path:
            self.file_label.config(text=self.file_path)
            self.midi_file = mido.MidiFile(self.file_path)

    def play(self):
        if self.midi_file and not self.playing:
            self.playing = True
            with mido.open_output() as port:
                for msg in self.midi_file.play():
                    port.send(msg)
                    if not self.playing:
                        break
            self.playing = False

    def stop(self):
        quit()

MidiPlayer()
