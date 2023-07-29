from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QInputDialog, QLineEdit, QMessageBox
from PyQt6.QtGui import QCursor
import sys
import json
import os


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

        # Initialize a counter for generating unique button names
        self.button_counter = 1

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Create a vertical layout to hold the dynamically created buttons and remove buttons
        buttons_remove_layout = QVBoxLayout()

        # Add the layout to the main layout
        main_layout.addLayout(buttons_remove_layout)

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
        # Ask the user for the type of button to add (regular, app, or folder)
        button_types = ["Regular", "App", "Folder"]
        button_type, ok = QInputDialog.getItem(self, "Add Button", "Choose button type:", button_types, 0, False)
        
        if ok and button_type:
            if button_type == "Regular":
                # Create a new regular button with a unique name
                new_button_name = f"Dynamic Button {self.button_counter}"
                new_button = QPushButton(new_button_name)

                # Increment the button counter for the next button
                self.button_counter += 1

                # Add the new button to the list and move it to a new position
                self.dynamic_buttons.append(new_button)
                x_pos = len(self.dynamic_buttons) * 50
                new_button.setGeometry(50 + x_pos, 50, 100, 30)

                # Add the new button to the layout that contains buttons and remove buttons
                buttons_remove_layout = self.layout().itemAt(1)  # Get the layout at index 1 (where buttons and remove buttons are placed)
                buttons_remove_layout.addWidget(new_button)

                # Create a remove button for the new button
                remove_button = QPushButton("Remove")
                buttons_remove_layout.addWidget(remove_button)

                # Connect the remove button's clicked signal to the remove_button method
                remove_button.clicked.connect(lambda checked, btn=new_button, rmv=remove_button: self.remove_button(btn, rmv))
            else:
                # Ask for the path of the app or folder
                path, ok = QInputDialog.getText(self, "Enter Path", f"Enter the {button_type} path:")
                if ok and path:
                    # Check if the app or folder exists
                    if not os.path.exists(path):
                        QMessageBox.critical(self, "Error", f"The {button_type.lower()} path does not exist.")
                        return

                    # Create a new button with a unique name
                    new_button_name = f"{button_type} Button {self.button_counter}"
                    new_button = QPushButton(new_button_name)

                    # Increment the button counter for the next button
                    self.button_counter += 1

                    # Add the new button to the list and move it to a new position
                    self.dynamic_buttons.append(new_button)
                    x_pos = len(self.dynamic_buttons) * 50
                    new_button.setGeometry(50 + x_pos, 50, 100, 30)

                    # Add the new button to the layout that contains buttons and remove buttons
                    buttons_remove_layout = self.layout().itemAt(1)  # Get the layout at index 1 (where buttons and remove buttons are placed)
                    buttons_remove_layout.addWidget(new_button)

                    # Create a remove button for the new button
                    remove_button = QPushButton("Remove")
                    buttons_remove_layout.addWidget(remove_button)

                    # Connect the remove button's clicked signal to the remove_button method
                    remove_button.clicked.connect(lambda checked, btn=new_button, rmv=remove_button: self.remove_button(btn, rmv))

                    # Connect the new button's clicked signal to the corresponding function
                    if button_type == "App":
                        new_button.clicked.connect(lambda: self.open_app(path))
                    elif button_type == "Folder":
                        new_button.clicked.connect(lambda: self.open_folder(path))

    def open_app(self, path):
        os.startfile(path)

    def open_folder(self, path):
        os.startfile(path)
        
    def save_buttons(self):
        button_data = [{"label": button.text(), "pos": (button.pos().x(), button.pos().y())} for button in self.dynamic_buttons]
        with open("buttons.json", "w") as file:
            json.dump(button_data, file)

    def load_buttons(self):
        try:
            with open("buttons.json", "r") as file:
                button_data = json.load(file)
                for data in button_data:
                    label = data["label"]
                    if not self.button_exists(label):
                        new_button = QPushButton(label, self)
                        new_button.move(data["pos"][0], data["pos"][1])
                        self.dynamic_buttons.append(new_button)

                        # Add the new button to the layout that contains buttons and remove buttons
                        buttons_remove_layout = self.layout().itemAt(1)  # Get the layout at index 1 (where buttons and remove buttons are placed)
                        buttons_remove_layout.addWidget(new_button)

                        # Create a remove button for the new button
                        remove_button = QPushButton("Remove")
                        buttons_remove_layout.addWidget(remove_button)

                        # Connect the remove button's clicked signal to the remove_button method
                        remove_button.clicked.connect(lambda checked, btn=new_button, rmv=remove_button: self.remove_button(btn, rmv))
        except FileNotFoundError:
            pass
    
    def button_exists(self, label):
        return any(button.text() == label for button in self.dynamic_buttons)

    def remove_button(self, button, remove_button):
        if button in self.dynamic_buttons:
            self.dynamic_buttons.remove(button)
            button.deleteLater()
            remove_button.deleteLater()

def runApp():
    app = QApplication(sys.argv)

    window = MyWindow()
    window.load_buttons()
    window.show_window()

    app.exec()

runApp()
