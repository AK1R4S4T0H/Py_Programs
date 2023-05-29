import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QAbstractSpinBox, QCalendarWidget,
    QCheckBox, QComboBox, QCommandLinkButton, QDateEdit, QDateTimeEdit, QDockWidget, QDoubleSpinBox,
    QFocusFrame, QGroupBox, QLCDNumber, QLabel, QLineEdit, QListView, QMenu, QMenuBar, QMessageBox,
    QProgressBar, QPushButton, QRadioButton, QSlider, QSpinBox, QSplitter, QStatusBar, QTabBar,
    QTabWidget, QTextEdit, QTimeEdit, QToolBar, QToolBox, QToolButton, QTreeView, QTreeWidgetItem,
    QWizard, QWizardPage
)
from PySide6.QtGui import (
    QPalette, QFont, QColor, QIcon, QCursor, QKeySequence, QMovie, QPixmap, QDrag, QTextCursor,
    QStandardItem, QStandardItemModel, QTextListFormat, QTextTableFormat, QClipboard, QDesktopServices,
    QTextDocument, QBrush, QTransform, QPainter, QPen, QPicture, QPolygon, QPolygonF, QRegion,
    QResizeEvent, QShortcut, QShowEvent, QHoverEvent, QPaintEvent, QTextDocumentFragment,
    QTextLength, QTextFormat, QTextBlockFormat, QTextCharFormat, QTextTableFormat, QTextImageFormat,
    QTextFrameFormat, QDragEnterEvent, QDragMoveEvent, QDropEvent, QDragLeaveEvent, QEnterEvent,
    QWheelEvent, QMouseEvent, QKeyEvent, QFocusEvent, QContextMenuEvent, QInputMethodEvent,
    QTextOption
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        self.setWindowTitle("PySide6 QSS Attributes Demo")
        self.setGeometry(100, 100, 400, 600)

        # Create a widget to hold the text box
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # Create a vertical layout for the widget
        layout = QVBoxLayout(widget)

        # Create a text box to display the QSS attributes
        self.text_box = QTextEdit(widget)
        layout.addWidget(self.text_box)

        # Get all available style properties from Qt documentation
        style_properties = [QPalette, QFont, QColor, QIcon, QCursor, QKeySequence, QMovie, QPixmap, QTextCursor,
                    QStandardItem, QStandardItemModel, QTextListFormat, QTextTableFormat, QClipboard, QDesktopServices,
                    QTextDocument, QBrush, QTransform, QPainter, QPen, QPicture, QPolygon, QPolygonF, QRegion,
                    QResizeEvent, QShortcut, QShowEvent, QHoverEvent, QPaintEvent, QTextDocumentFragment, QTextLength,
                    QTextFormat, QTextBlockFormat, QTextCharFormat, QTextTableFormat, QTextImageFormat, QTextFrameFormat,
                    QDrag, QTextOption, QAbstractSpinBox, QCalendarWidget, QCheckBox, QComboBox, QCommandLinkButton,
                    QDateEdit, QDateTimeEdit, QDockWidget, QDoubleSpinBox, QFocusFrame, QGroupBox, QLCDNumber, QLabel,
                    QLineEdit, QListView, QMenu, QMenuBar, QMessageBox, QProgressBar, QPushButton, QRadioButton, QSlider,
                    QSpinBox, QSplitter, QStatusBar, QTabBar, QTabWidget, QTextEdit, QTimeEdit, QToolBar, QToolBox,
                    QToolButton, QTreeView, QTreeWidgetItem, QWizard, QWizardPage]

        properties_string = ""

        for widget_type in style_properties:
            widget_attributes = [attr for attr in dir(widget_type) if not attr.startswith('_')]  # Filter out private attributes
            attributes_string = ", ".join(widget_attributes)  # Join attributes into a string
            properties_string += f"{widget_type.__name__}:\n--------------------------------------------------------------------------------------------\n{attributes_string}\n--------------------------------------------------------------------------------------------\n"

        # Set the style properties and attributes string as the text content of the text box
        self.text_box.setPlainText(properties_string)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

