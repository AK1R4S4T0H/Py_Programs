# mp4 video player using cv2 and tkinter
#
""" Created by: AK1R4S4T0H
"""
import tkinter as tk
from tkinter import ttk, filedialog
import cv2
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.video_path = ""
        self.cap = None

        self.style = ttk.Style()
        self.style.configure("TButton", background="#555555", foreground="white")
        self.style.map('TButton', foreground=[("hover", "white")], background=[("hover", "#660066")])

        self.canvas = tk.Canvas(root, bg='#220022', borderwidth=15, width=700, height=700)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        self.btn_open = ttk.Button(root, text="Open Video", command=self.open_video, style="TButton")
        self.btn_open.pack(side="top", fill="both", expand=True)

        self.btn_play = ttk.Button(root, text="Play", command=self.play_video, style="TButton")
        self.btn_play.pack(side="right", fill="both", expand=True)

        self.btn_pause = ttk.Button(root, text="Pause", command=self.pause_video, style="TButton")
        self.btn_pause.pack(side="left", fill="both", expand=True)

        self.btn_stop = ttk.Button(root, text="Stop", command=self.stop_video, style="TButton")
        self.btn_stop.pack(side="bottom", fill="both", expand=True)

    def open_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=(("Video Files", "*.mp4"), ("All Files", "*.*")))
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            self.play_video()

    def play_video(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                # Resize the frame to fit the canvas size
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = image.resize((canvas_width, canvas_height), Image.ANTIALIAS)
                image = ImageTk.PhotoImage(image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
                self.canvas.image = image
        self.root.after(30, self.play_video)  # Delay between frames

    def on_canvas_resize(self, event):
        self.play_video()

    def pause_video(self):
        # pause the video by simply not calling play_video
        pass

    def stop_video(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root)
    root.mainloop()
