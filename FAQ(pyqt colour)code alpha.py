import sys
import spacy
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QWidget, QLabel
from PyQt5.QtGui import QFont, QIcon, QColor, QTextCursor
from PyQt5.QtCore import Qt

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define a more extensive FAQ data structure with AI-related questions
faq_data = {
    "what is artificial intelligence": "Artificial Intelligence (AI) is the simulation of human intelligence in machines that are programmed to think and learn.",
    "what are the types of machine learning": "The main types of machine learning are supervised learning, unsupervised learning, and reinforcement learning.",
    "how does natural language processing work": "Natural Language Processing (NLP) involves analyzing and understanding human language using algorithms, often involving tokenization, parsing, and semantic analysis.",
    "what is deep learning": "Deep Learning is a subset of machine learning that uses neural networks with many layers to model complex patterns in large amounts of data.",
    "what are neural networks": "Neural networks are computational models inspired by the human brain, consisting of layers of interconnected nodes (neurons) that process data.",
    "what is a chatbot": "A chatbot is an AI program designed to simulate conversation with human users, often used in customer service to answer questions and provide assistance.",
    "how do you train a machine learning model": "Training a machine learning model involves providing it with data, allowing it to learn patterns from the data, and then evaluating its performance to make predictions or decisions.",
    "what is the difference between AI and machine learning": "AI is a broad field that encompasses any technique enabling machines to mimic human behavior, while machine learning is a specific approach within AI that uses data to train models to make predictions or decisions.",
    "what is supervised learning": "Supervised learning is a type of machine learning where the model is trained on labeled data, meaning each training example is paired with an output label.",
    "what is unsupervised learning": "Unsupervised learning involves training a model on data without labeled responses, aiming to find hidden patterns or structures in the data."
}

# Function to handle the chatbot response
def get_response(user_input):
    user_input = user_input.lower()
    doc = nlp(user_input)
    for question, answer in faq_data.items():
        if question in user_input:
            return answer
    return "Sorry, I don't understand your question. Please try again."

# Main GUI application class
class ChatbotApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI FAQ Chatbot")
        self.setGeometry(100, 100, 400, 500)
        self.setWindowIcon(QIcon('chatbot_icon.png'))

        # Main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Title label
        self.title_label = QLabel("AI FAQ Chatbot", self)
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("background-color: #091833; color: white; padding: 10px; border-radius: 5px;")
        self.layout.addWidget(self.title_label)

        # Chat display
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: #d1f7ff; color: #000000; border: 1px solid #cccccc;")
        self.layout.addWidget(self.chat_display)

        # User input field
        self.user_input = QLineEdit(self)
        self.user_input.setFont(QFont("Arial", 12))
        self.user_input.setPlaceholderText("Type your AI-related question here...")
        self.user_input.setStyleSheet("background-color: #ffffff; color: #000000; border: 1px solid #cccccc; padding: 5px; border-radius: 5px;")
        self.layout.addWidget(self.user_input)

        # Send button
        self.send_button = QPushButton("Send", self)
        self.send_button.setFont(QFont("Arial", 12))
        self.send_button.setStyleSheet("background-color: #091833; color: white; border: none; padding: 10px; border-radius: 5px;")
        self.send_button.clicked.connect(self.handle_send)
        self.layout.addWidget(self.send_button)

    def handle_send(self):
        user_text = self.user_input.text().strip()
        if user_text:
            self.chat_display.append(f'<b style="color: #007bff;">You:</b> {user_text}')
            response = get_response(user_text)
            self.chat_display.append(f'<b style="color: #28a745;">Bot:</b> {response}')
            self.user_input.clear()

# Main execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    chatbot_app = ChatbotApp()
    chatbot_app.show()
    sys.exit(app.exec_())
