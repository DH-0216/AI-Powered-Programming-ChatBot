import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt
from chat import ChatBotGUI


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout(self) 
        self.set_background_image()

        # Navigation bar
        nav_bar = QHBoxLayout()
        nav_bar.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(nav_bar)


        # Try it now button
        try_button = QPushButton("TRY IT NOW")
        try_button.setObjectName("tryButton") 
        main_layout.addWidget(try_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set main layout
        self.setWindowTitle("Home Page")
        self.setGeometry(100, 100, 600, 600)

        
        try_button.clicked.connect(self.open_chat_window) 
        
        stylesheet_path = os.path.join(os.path.dirname(__file__), "assets", "styles.qss")
        self.load_stylesheet(stylesheet_path)

    def set_background_image(self):
        image_path = os.path.join(os.path.dirname(__file__), "assets", "Untitled-1.png")
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print(f"Error: Could not load background image from '{image_path}'")
        else:
            palette = QPalette()
            palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio))) 
            self.setPalette(palette)

    def load_stylesheet(self, filename):

        if os.path.exists(filename):
            with open(filename, "r") as f:
                stylesheet = f.read()
                self.setStyleSheet(stylesheet)
        else:
            print(f"Warning: Stylesheet file '{filename}' not found.")

    def open_chat_window(self):
       
        self.chat_window = ChatBotGUI()
        self.chat_window.show() 

    def resizeEvent(self, event):

        super().resizeEvent(event)
        self.set_background_image()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    home_page = HomePage()
    home_page.showMaximized()
    sys.exit(app.exec())
