import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from OCEAN import Waves
from AUDIO_V3 import Audio

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BREEZE.Music")

        # Create the central widget and set its layout
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        waves = Waves.WaveformWidget()
        central_layout.addWidget(waves)

        audio = Audio()
        audio.setMaximumHeight(300)
        audio.setMinimumWidth(220)
        central_layout.addWidget(audio)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
