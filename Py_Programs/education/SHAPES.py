import random
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy
from PySide6.QtGui import QColor, QPainter, QPolygonF
from PySide6.QtCore import Qt, QTimer, QPoint
import os

os.environ['QT_QPA_PLATFORM'] = 'xcb'


class ShapeLearningApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.shapes = ['Triangle', 'Square', 'Circle', 'Pentagon', 'Hexagon', 'Octagon', 'Diamond', 'Star']
        self.colors = [QColor('red'), QColor('green'), QColor('blue'), QColor('yellow'), QColor('orange'),
                       QColor('purple'), QColor('pink'), QColor('cyan'), QColor('magenta')]

        self.setWindowTitle("Shape Learning App")
        self.setGeometry(100, 100, 400, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.main_label = QLabel(self)
        self.main_label.setStyleSheet("font-size: 90px;")
        self.main_label.setAlignment(Qt.AlignCenter)

        self.word_label = QLabel(self)
        self.word_label.setStyleSheet("font-size: 30px;")
        self.word_label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton("Show me a shape!", self)
        self.button.setStyleSheet("color: #FFFFFF;background-color: #165753;font-size: 12px;padding: 5px")
        self.button.clicked.connect(self.display_shape)

        layout.addWidget(self.main_label)
        spacer_item = QSpacerItem(20, 60, QSizePolicy.Expanding)
        layout.addItem(spacer_item)
        layout.addWidget(self.word_label)
        layout.addWidget(self.button)

        self.current_shape = None
        self.current_color = None

    def display_shape(self):
        index = random.randint(0, len(self.shapes) - 1)
        self.current_shape = self.shapes[index]
        self.current_color = self.colors[index]
        QTimer.singleShot(7000, self.display_shape)

        self.main_label.setText(self.current_shape)
        self.main_label.setStyleSheet(
            f"color: white;font-size: 70px;")

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.current_shape is not None and self.current_color is not None:
            painter.setBrush(self.current_color)

            if self.current_shape == 'Triangle':
                points = [QPoint(200, 100), QPoint(100, 300), QPoint(300, 300)]
                painter.drawPolygon(QPolygonF(points))
            elif self.current_shape == 'Square':
                painter.drawRect(100, 100, 200, 200)
            elif self.current_shape == 'Circle':
                painter.drawEllipse(100, 100, 200, 200)
            elif self.current_shape == 'Pentagon':
                points = [QPoint(200, 100), QPoint(100, 200), QPoint(120, 300),
                          QPoint(280, 300), QPoint(300, 200)]
                painter.drawPolygon(QPolygonF(points))
            elif self.current_shape == 'Hexagon':
                points = [QPoint(150, 100), QPoint(250, 100), QPoint(300, 200),
                          QPoint(250, 300), QPoint(150, 300), QPoint(100, 200)]
                painter.drawPolygon(QPolygonF(points))
            elif self.current_shape == 'Octagon':
                points = [QPoint(150, 100), QPoint(250, 100), QPoint(300, 150),
                          QPoint(300, 250), QPoint(250, 300), QPoint(150, 300),
                          QPoint(100, 250), QPoint(100, 150)]
                painter.drawPolygon(QPolygonF(points))
            elif self.current_shape == 'Diamond':
                points = [QPoint(200, 100), QPoint(300, 200), QPoint(200, 300), QPoint(100, 200)]
                painter.drawPolygon(QPolygonF(points))
            elif self.current_shape == 'Star':
                outer_points = [QPoint(200, 100), QPoint(230, 200), QPoint(330, 220), QPoint(250, 270),
                                QPoint(270, 370), QPoint(200, 320), QPoint(130, 370), QPoint(150, 270),
                                QPoint(70, 220), QPoint(170, 200)]
                inner_points = [QPoint(200, 160), QPoint(230, 220), QPoint(200, 250), QPoint(170, 220)]
                painter.drawPolygon(QPolygonF(outer_points))
                painter.drawPolygon(QPolygonF(inner_points))


if __name__ == "__main__":
    app = QApplication([])
    shape_app = ShapeLearningApp()
    shape_app.show()
    app.exec()
