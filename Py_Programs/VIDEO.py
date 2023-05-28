# mp4 video player using cv2 and PySide6
#
""" Created by: AK1R4S4T0H
"""
import sys
import os
from PySide6 import QtCore, QtGui, QtWidgets
import cv2
from PIL import Image, ImageTk

os.environ['QT_QPA_PLATFORM'] = 'xcb'
class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.video_path = ""
        self.cap = None
        try:
            style_file = QtCore.QFile("Py_Programs/style.qss")
            if style_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                style_sheet = style_file.readAll()
                style_file.close()
                style_sheet = str(style_sheet, encoding='utf-8')
                self.root.setStyleSheet(style_sheet)
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            style_file = QtCore.QFile("style.qss")
            if style_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                style_sheet = style_file.readAll()
                style_file.close()
                style_sheet = str(style_sheet, encoding='utf-8')
                self.root.setStyleSheet(style_sheet)
            else:
                print("Failed to open style.qss")

        self.canvas = QtWidgets.QGraphicsView(root)
        self.canvas.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("#220022")))
        self.canvas.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)

        self.btn_open = QtWidgets.QPushButton("Open Video", clicked=self.open_video)
        self.btn_play = QtWidgets.QPushButton("Play", clicked=self.play_video)
        self.btn_pause = QtWidgets.QPushButton("Pause", clicked=self.pause_video)
        self.btn_stop = QtWidgets.QPushButton("Stop", clicked=self.stop_video)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.btn_open)
        layout.addWidget(self.btn_play)
        layout.addWidget(self.btn_pause)
        layout.addWidget(self.btn_stop)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        root.setCentralWidget(central_widget)

    def open_video(self):
        self.video_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.root, "Open Video",
                                                                   "", "Video Files (*.mp4);;All Files (*)")
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            self.play_video()

    def play_video(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                # Resize the frame to fit the canvas size
                canvas_size = self.canvas.size()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                frame = frame.resize((canvas_size.width(), canvas_size.height()), Image.ANTIALIAS)
                frame = ImageTk.PhotoImage(frame)
                self.canvas.setScene(QtGui.QGraphicsScene())
                self.canvas.scene().addPixmap(QtGui.QPixmap.fromImage(frame))
        QtCore.QTimer.singleShot(30, self.play_video)  # Delay between frames

    def pause_video(self):
        # Pause the video by simply not calling play_video
        pass

    def stop_video(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            self.canvas.setScene(QtGui.QGraphicsScene())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    root = QtWidgets.QMainWindow()
    player = VideoPlayer(root)
    root.show()
    sys.exit(app.exec())
