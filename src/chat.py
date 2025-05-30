import os
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer
from ui.chatbot_ui import Ui_Form
import google.generativeai as genai
from predefined_responses import predefined_responses
from fuzzywuzzy import process
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

chat = model.start_chat(history=[])

class ChatBotGUI(QWidget, Ui_Form): 
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
       
        self.setWindowTitle("AI-Powered Programming ChatBot")
        self.setGeometry(100, 100, 500, 600)
        self.textEdit.setReadOnly(True)
        
        self.pushButton.clicked.connect(self.get_response)
        self.lineEdit.returnPressed.connect(self.get_response) 

       
        self.load_stylesheet("./assets/chat.qss")
        greeting = "Hello! I'm your AI programming assistant. How can I help you today? 😊"
        self.append_message(greeting, "left")
    
    def show_typing_indicator(self):  
        self.append_message("typing ...", "left")
        self.typing_index = self.textEdit.document().lineCount() - 1

    def remove_typing_indicator(self):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.select(cursor.SelectionType.LineUnderCursor)
        cursor.removeSelectedText()
        cursor.deletePreviousChar()
        
    # This function is triggered when the user presses the send button or hits Enter.
    def get_response(self):
        user_message = self.lineEdit.text().strip() 
        if user_message:
            self.append_message(user_message, "right")
            self.lineEdit.clear()
            self.pushButton.setEnabled(False)
            self.lineEdit.setEnabled(False)
            self.show_typing_indicator()
            
            # Use QTimer to delay processing and allow UI to update
            QTimer.singleShot(1000, lambda: self.process_response(user_message))

    def process_response(self, user_message):
        # Try to get a predefined response first
        bot_response = self.get_predefined_response(user_message)
        
        # If no predefined response, use Gemini AI
        if not bot_response:
            bot_response = self.process_message(user_message)
        
        self.handle_bot_reply(bot_response)
        
        
    def handle_bot_reply(self, bot_reply):
        self.remove_typing_indicator()
        self.append_message(bot_reply, "left")
        self.pushButton.setEnabled(True)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setFocus()        
            
            
    # This function appends messages to the textEdit widget with appropriate formatting.
    def append_message(self, message, align):
        """Formats messages for left/right alignment using HTML and CSS classes."""
        if align == "right":
            user_class = "user-message"
            sender = "You"
            formatted_message = f'<p class="{user_class}"><b>{sender}:</b> {message}</p>'
        else:
            user_class = "bot-message"
            sender = "Bot"
            formatted_message = f'<p class="{user_class}" style="color: rgb(52, 11, 236);"><b>{sender}:</b> {message}</p>'
        
        self.textEdit.append(formatted_message)
        self.textEdit.ensureCursorVisible()
        self.lineEdit.setFocus()
     
    # This function checks if the message is a predefined response.    
    def get_predefined_response(self, message):
        message = message.lower()

        if message.startswith("what is"):
            key_term = message.replace("what is", "").strip()
            return self.get_fuzzy_response(key_term)
        
        if len(message.split()) == 1:
            return self.get_fuzzy_response(message)

        return None
    
    
    

    # This function uses fuzzy matching to find the best predefined response.
    def get_fuzzy_response(self, key_term): 
        best_match, score = process.extractOne(key_term, predefined_responses.keys())

        if score > 70:
            return predefined_responses[best_match]

        return None
    
    
    
    # This function processes the message using OpenAI's GPT-4 API.
    def process_message(self, message):
   
        try:
            response = chat.send_message(message)
            return response.text.strip()
        except Exception as e:
            return f"Error: {str(e)}" 
        
        
        
    def load_stylesheet(self, filename):
        """Loads QSS file and applies styles.""" 
        try:
            abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
            with open(abs_path, "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Error: {filename} not found!")
