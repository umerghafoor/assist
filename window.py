from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QCursor
import sys
import json

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window properties
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle("Qt6 Window")

        # Create the main vertical layout for the window
        main_layout = QVBoxLayout(self)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Create a button and connect its clicked signal to the hide_window method
        self.hide_button = QPushButton("Hide Window")
        self.hide_button.clicked.connect(self.hide_window)

        # Create a button and connect its clicked signal to the add_button method
        self.add_button_button = QPushButton("Add Button")
        self.add_button_button.clicked.connect(self.add_button)

        # Create a button and connect its clicked signal to the save_buttons method
        self.save_button = QPushButton("Save Buttons")
        self.save_button.clicked.connect(self.save_buttons)

        # Create a button and connect its clicked signal to the load_buttons method
        self.load_button = QPushButton("Load Buttons")
        self.load_button.clicked.connect(self.load_buttons)

        # Add the buttons to the button layout
        button_layout.addWidget(self.hide_button)
        button_layout.addWidget(self.add_button_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)

        # Initialize an empty list to hold the dynamically created buttons
        self.dynamic_buttons = []

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Set the main layout as the window's layout
        self.setLayout(main_layout)

    def show_window(self):
        cursor_pos = QCursor.pos()
        cursor_pos.setX(cursor_pos.x() - 150)
        self.move(cursor_pos)
        self.show()

    def hide_window(self):
        self.save_buttons()
        self.close()

    def add_button(self):
        # Create a new button
        new_button = QPushButton("Dynamic Button")

        # Add the new button to the list and move it to a new position
        self.dynamic_buttons.append(new_button)
        x_pos = len(self.dynamic_buttons) * 50
        new_button.setGeometry(50 + x_pos, 50, 100, 30)

        # Add the new button to the button layout
        self.layout().addWidget(new_button)

        # Connect the button's clicked signal to the remove_button method
        new_button.clicked.connect(lambda: self.remove_button(new_button))

    def save_buttons(self):
        button_data = [{"label": button.text(), "pos": (button.pos().x(), button.pos().y())} for button in self.dynamic_buttons]
        with open("buttons.json", "w") as file:
            json.dump(button_data, file)

    def load_buttons(self):
        try:
            with open("buttons.json", "r") as file:
                button_data = json.load(file)
                for data in button_data:
                    new_button = QPushButton(data["label"], self)
                    new_button.move(data["pos"][0], data["pos"][1])
                    self.dynamic_buttons.append(new_button)
                    self.layout().addWidget(new_button)
                    new_button.clicked.connect(lambda: self.remove_button(new_button))
        except FileNotFoundError:
            pass

    def remove_button(self, button):
        if button in self.dynamic_buttons:
            self.dynamic_buttons.remove(button)
            button.deleteLater()

def runApp():
    app = QApplication(sys.argv)

    window = MyWindow()
    window.load_buttons()
    window.show_window()

    app.exec()

runApp()
