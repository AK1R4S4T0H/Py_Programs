# very bad chatbot
# 
""" Created by: AK1R4S4T0H
"""
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
)

model_name = "EleutherAI/gpt-neo-1.3B"
tokenizer_name = "EleutherAI/gpt-neo-1.3B"

tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

class ChatbotGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)

        self.input_field = QLineEdit()

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.generate_output)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.chat_history)
        main_layout.addLayout(input_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Chatbot")
        self.setStyleSheet("background-color: #A569BD; color: white;")

    def generate_output(self):
        input_text = self.input_field.text().strip()
        self.input_field.clear()

        if not input_text:
            return

        input_ids = tokenizer.encode(input_text, return_tensors="pt")
        output = model.generate(input_ids)

        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        self.chat_history.append(f"<b>You:</b> {input_text}")
        self.chat_history.append(f"<b>Chatbot:</b> {generated_text}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chatbot_gui = ChatbotGUI()
    chatbot_gui.show()
    sys.exit(app.exec_())
