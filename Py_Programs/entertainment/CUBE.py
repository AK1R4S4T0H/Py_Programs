import sys
import pyaudio
import numpy as np
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QVector3D, QColor, QKeyEvent
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *


class AudioVisualizerWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.audio_input_device = None
        self.audio_data = None

        self.rotation = 0.0
        self.scaling = 1.0
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.camera_z = -5.0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_visualizer)
        self.timer.start(50)

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-width/2, width/2, -height/2, height/2, -10.0, 10.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.camera_x, self.camera_y, self.camera_z,
                  self.camera_x, self.camera_y, self.camera_z + 1.0,
                  0.0, 1.0, 0.0)

        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(self.rotation, 1.0, 1.0, 1.0)

        # Cube
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.0, 0.0)  # Red color
        glVertex3f(1.0 * self.scaling, 1.0 * self.scaling, -1.0 * self.scaling)
        glVertex3f(-1.0 * self.scaling, 1.0 * self.scaling, -1.0 * self.scaling)
        glVertex3f(-1.0 * self.scaling, 1.0 * self.scaling, 1.0 * self.scaling)
        glVertex3f(1.0 * self.scaling, 1.0 * self.scaling, 1.0 * self.scaling)
        glEnd()

    def start_audio_stream(self):
        self.audio_input_device = pyaudio.PyAudio().open(format=pyaudio.paFloat32, channels=1, rate=44100,
                                                        input=True, frames_per_buffer=1024,
                                                        stream_callback=self.audio_callback)
        self.audio_input_device.start_stream()

    def stop_audio_stream(self):
        self.audio_input_device.stop_stream()
        self.audio_input_device.close()

    def audio_callback(self, in_data, frame_count, time_info, status):
        audio_samples = np.frombuffer(in_data, dtype=np.float32)
        self.audio_data = audio_samples
        return None, pyaudio.paContinue

    def update_visualizer(self):
        self.rotation += 0.5
        self.scaling = np.mean(np.abs(self.audio_data)) if self.audio_data is not None else 1.0
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.camera_x -= 0.1
        elif event.key() == Qt.Key_Right:
            self.camera_x += 0.1
        elif event.key() == Qt.Key_Up:
            self.camera_y += 0.1
        elif event.key() == Qt.Key_Down:
            self.camera_y -= 0.1

        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Visualizer")
        self.setGeometry(100, 100, 800, 600)

        self.visualizer_widget = AudioVisualizerWidget(self)
        self.setCentralWidget(self.visualizer_widget)

        self.start_audio_stream()

    def start_audio_stream(self):
        self.visualizer_widget.start_audio_stream()

    def closeEvent(self, event):
        self.visualizer_widget.stop_audio_stream()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
