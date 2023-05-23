import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextBrowser
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Browser")
        self.resize(800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        url_layout = QHBoxLayout()
        self.url_entry = QLineEdit()
        url_layout.addWidget(self.url_entry)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_website)
        url_layout.addWidget(self.browse_button)

        main_layout.addLayout(url_layout)

        self.response_text = QTextBrowser()
        main_layout.addWidget(self.response_text)

        self.network_manager = QNetworkAccessManager(self)

    @Slot()
    def browse_website(self):
        url = self.url_entry.text()
        request = QNetworkRequest()
        request.setUrl(url)

        self.network_manager.finished.connect(self.handle_network_reply)
        self.network_manager.get(request)

    @Slot()
    def handle_network_reply(self, reply):
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            html = str(data, 'utf-8')
            self.response_text.setHtml(html)
        else:
            self.response_text.setPlainText(f"An error occurred: {reply.errorString()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebBrowser()
    window.show()
    sys.exit(app.exec())
