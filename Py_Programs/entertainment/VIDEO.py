# mp4 video player using PySide6
#
""" Created by: AK1R4S4T0H
"""
import sys
import os
import cv2
from PySide6 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets

os.environ['QT_QPA_PLATFORM'] = 'xcb'

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.video_path = ""
        self.cap = None
        self.media_player = None

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
        self.video_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.root, "Open Video", "", "Video Files (*.mp4);;All Files (*)"
        )
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            self.initialize_media_player()
            self.play_video()

    def initialize_media_player(self):
        self.media_player = QtMultimedia.QMediaPlayer(self.root)
        video_widget = QtMultimediaWidgets.QVideoWidget()
        self.media_player.setVideoOutput(video_widget)

        self.canvas.setRenderHint(QtGui.QPainter.Antialiasing)
        self.canvas.setScene(QtWidgets.QGraphicsScene(self.canvas))
        self.canvas.scene().addWidget(video_widget)

    def play_video(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                # Resize the frame to fit the canvas size
                canvas_size = self.canvas.size()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
                frame = frame.scaled(canvas_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                pixmap = QtGui.QPixmap.fromImage(frame)
                scene = QtWidgets.QGraphicsScene()
                scene.addPixmap(pixmap)
                self.canvas.setScene(scene)

                # Play the video using QMediaPlayer
                if self.media_player is not None:
                    self.media_player.setMedia(QtMultimedia.QMediaContent())
                    self.media_player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(self.video_path)))
                    self.media_player.play()

        # Schedule next frame
        QtCore.QTimer.singleShot(33, self.play_video)


    def pause_video(self):
        if self.media_player is not None:
            if self.media_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
                self.media_player.pause()

    def stop_video(self):
        if self.media_player is not None:
            if self.media_player.state() != QtMultimedia.QMediaPlayer.StoppedState:
                self.media_player.stop()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    player = VideoPlayer(window)
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())