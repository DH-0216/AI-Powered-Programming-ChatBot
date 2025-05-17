import os
from PyQt6.QtWidgets import QWidget
from ui.chatbot_ui import Ui_Form
import openai
from predefined_responses import predefined_responses
from fuzzywuzzy import process
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAIKEY')

class ChatBotGUI(QWidget, Ui_Form): 
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
       
        self.setWindowTitle("AI-Powered Programming ChatBot")
        self.setGeometry(100, 100, 500, 600)

        
        self.pushButton.clicked.connect(self.get_response)
        self.lineEdit.returnPressed.connect(self.get_response) 

       
        self.load_stylesheet("./assets/chat.qss")

    
    # This function is triggered when the user presses the send button or hits Enter.
    def get_response(self):
        user_message = self.lineEdit.text().strip() 
        if user_message:
            self.append_message(user_message, "right")
            
            # Try to get a predefined response first
            bot_response = self.get_predefined_response(user_message)
            
            # If no predefined response, process the message with OpenAI GPT
            if not bot_response:
                bot_response = self.process_message(user_message)
            
            # Display the bot's response in the UI
            self.append_message(bot_response, "left")
            self.lineEdit.clear() 
            
            
            
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
        """Process the message with OpenAI's GPT-4 API."""
        try:
            response = openai.completions.create(
                model="gpt-4o",  
                prompt=message,
                max_tokens=150
            )
            return response.choices[0].text.strip() 
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
