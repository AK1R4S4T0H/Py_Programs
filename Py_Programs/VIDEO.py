# mp4 video player using cv2 and tkinter
import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.title("Video Player")
        self.video_path = ""
        self.cap = None

        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        self.btn_open = tk.Button(root, text="Open Video", command=self.open_video)
        self.btn_open.pack()

        self.btn_play = tk.Button(root, text="Play", command=self.play_video)
        self.btn_play.pack()

        self.btn_pause = tk.Button(root, text="Pause", command=self.pause_video)
        self.btn_pause.pack()

        self.btn_stop = tk.Button(root, text="Stop", command=self.stop_video)
        self.btn_stop.pack()

    def open_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=(("Video Files", "*.mp4"), ("All Files", "*.*")))
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            self.play_video()

    def play_video(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
                self.canvas.image = image
                self.root.after(30, self.play_video)  # Delay between frames

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
