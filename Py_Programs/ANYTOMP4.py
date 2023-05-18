# for converting any video format to mp4
# doesnt work right
#
""" Created by: AK1R4S4T0H
"""
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip

def convert_to_mp4(input_file, output_file):
    clip = VideoFileClip(input_file)
    clip.write_videofile(output_file, codec='libx264')

def select_file():
    filetypes = (
        ('Video files', '*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.ogv *.ogg'),
        ('All files', '*.*')
    )
    filepath = filedialog.askopenfilename(filetypes=filetypes)
    if filepath:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, filepath)

def convert_video():
    input_file = entry_input.get()
    output_file = entry_output.get()
    if input_file and output_file:
        convert_to_mp4(input_file, output_file)
        status_label.config(text='Conversion complete!')
    else:
        status_label.config(text='Please select input and output files.')

window = tk.Tk()
window.title("Video Converter")

label_input = tk.Label(window, text="Input Video:")
label_input.pack()
entry_input = tk.Entry(window, width=50)
entry_input.pack()
button_browse = tk.Button(window, text="Browse", command=select_file)
button_browse.pack()

label_output = tk.Label(window, text="Output File:")
label_output.pack()
entry_output = tk.Entry(window, width=50)
entry_output.pack()

button_convert = tk.Button(window, text="Convert", command=convert_video)
button_convert.pack()

status_label = tk.Label(window, text="")
status_label.pack()


window.mainloop()
