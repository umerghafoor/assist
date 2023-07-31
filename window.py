from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QInputDialog, QLineEdit, QMessageBox
from PyQt6.QtGui import QCursor
import sys
import json
import os
from comman import runCustomDialog


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

        # Add the buttons to the button layout
        button_layout.addWidget(self.hide_button)
        button_layout.addWidget(self.add_button_button)

        # Initialize an empty list to hold the dynamically created buttons
        self.dynamic_buttons = []
        self.dynamic_buttons_paths = []

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
        # Ask for the path of the app or folder
        button_type, new_button_name, path, ok = runCustomDialog()
        print(type(path), ",", path)
        if ok and path:
            # Check if the app or folder exists
            if not os.path.exists(path):
                QMessageBox.critical(
                    self, "Error", f"The {button_type.lower()} path does not exist.")
                return

            # Create a new button with a unique name
            new_button = QPushButton(new_button_name)

            # Increment the button counter for the next button
            self.button_counter += 1

            # Add the new button to the list and move it to a new position
            self.dynamic_buttons.append(new_button)
            self.dynamic_buttons_paths.append(path)
            x_pos = len(self.dynamic_buttons) * 50
            new_button.setGeometry(50 + x_pos, 50, 100, 30)

            # Add the new button to the layout that contains buttons and remove buttons
            # Get the layout at index 1 (where buttons and remove buttons are placed)
            buttons_remove_layout = self.layout().itemAt(1)
            buttons_remove_layout.addWidget(new_button)

            # Create a remove button for the new button
            remove_button = QPushButton("Remove")
            buttons_remove_layout.addWidget(remove_button)

            # Connect the remove button's clicked signal to the remove_button method
            remove_button.clicked.connect(
                lambda checked, btn=new_button, rmv=remove_button: self.remove_button(btn, rmv))

            # Save the button's data
            label = new_button.text()
            pos = (new_button.pos().x(), new_button.pos().y())
            # print(type(label))
            # print(type(path))
            # print(type(pos))
            self.save_buttons(label, pos, button_type, path)

            # Connect the new button's clicked signal to the corresponding function
            if button_type == "App":
                new_button.clicked.connect(lambda: self.open_app(path))
            elif button_type == "Folder":
                new_button.clicked.connect(lambda: self.open_folder(path))

    def open_app(self, path):
        os.startfile(path)

    def open_folder(self, path):
        os.startfile(path)

    def save_buttons(self, label, pos, button_type, path):
        # Check if the file exists and contains data
        try:
            with open("buttons.json", "r") as file:
                button_data = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, initialize the button_data list
            button_data = []

        # Append the new button data to the existing list
        button_data.append({"label": label, "pos": pos,
                           "path": path, "type": button_type})

        # Write the updated data back to the file
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

                        # Add the path information to the button as an attribute (for App and Folder buttons)
                        setattr(new_button, "path", data.get("path", ""))

                        # Add the type information to the button as an attribute
                        setattr(new_button, "type", data.get("type", ""))

                        self.dynamic_buttons.append(new_button)

                        # Add the new button to the layout that contains buttons and remove buttons
                        # Get the layout at index 1 (where buttons and remove buttons are placed)
                        buttons_remove_layout = self.layout().itemAt(1)
                        buttons_remove_layout.addWidget(new_button)

                        # Create a remove button for the new button
                        remove_button = QPushButton("Remove")
                        buttons_remove_layout.addWidget(remove_button)

                        # Connect the remove button's clicked signal to the remove_button method
                        remove_button.clicked.connect(
                            lambda checked, btn=new_button, rmv=remove_button: self.remove_button(btn, rmv))

                        # Connect the new button's clicked signal to the corresponding function
                        if new_button.type == "App":
                            new_button.clicked.connect(
                                lambda: self.open_app(new_button.path))
                        elif new_button.type == "Folder":
                            new_button.clicked.connect(
                                lambda: self.open_folder(new_button.path))
        except FileNotFoundError:
            pass

    def button_exists(self, label):
        return any(button.text() == label for button in self.dynamic_buttons)

    def remove_button(self, button, remove_button):
        if button in self.dynamic_buttons:
            self.dynamic_buttons.remove(button)
            button.deleteLater()
            remove_button.deleteLater()


def runApp2(testing):
    if testing:
        app = QApplication(sys.argv)
        print("Two is runing")

        window = MyWindow()
        window.load_buttons()
        window.show_window()

        app.exec()


# runApp2(1)
