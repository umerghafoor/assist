from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox
from PyQt6.QtCore import pyqtSignal
import sys


class CustomDialog(QDialog):
    # Define signals with arguments corresponding to the returned values
    dialog_accepted = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()

        self.init_ui()
        self.selected_type = None
        self.name = None
        self.path = None

    def init_ui(self):
        # Create widgets
        type_label = QLabel("Select a type:")
        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Folder", "Path"])

        name_label = QLabel("Enter the name:")
        self.name_line_edit = QLineEdit()

        path_label = QLabel("Enter the path:")
        self.path_line_edit = QLineEdit()

        ok_button = QPushButton("OK")

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(type_label)
        layout.addWidget(self.type_dropdown)
        layout.addWidget(name_label)
        layout.addWidget(self.name_line_edit)
        layout.addWidget(path_label)
        layout.addWidget(self.path_line_edit)
        layout.addWidget(ok_button)

        # Set the layout for the dialog
        self.setLayout(layout)

        # Connect the button click signal to a slot (function)
        ok_button.clicked.connect(self.on_ok_button_clicked)

    def on_ok_button_clicked(self):
        # Retrieve the values from the widgets
        self.selected_type = self.type_dropdown.currentText()
        self.name = self.name_line_edit.text()
        self.path = self.path_line_edit.text()

        # Emit the dialog_accepted signal with the values
        self.dialog_accepted.emit(self.selected_type, self.name, self.path)

        # Close the dialog
        self.close()


def runCustomDialog():
    dialog = CustomDialog()
    dialog.exec()
    print("ran")
    if dialog.dialog_accepted:
        return dialog.selected_type, dialog.name, dialog.path, True


app = QApplication(sys.argv)
# Call the runCustomDialog function to execute the dialog

# runCustomDialog()
