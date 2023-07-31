import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QPushButton
import os

class FileListWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('File List Window')

        self.button_layout = QVBoxLayout()

        self.open_button = QPushButton('Open Directory', self)
        self.open_button.clicked.connect(self.open_directory)

        self.refresh_button = QPushButton('Refresh', self)
        self.refresh_button.clicked.connect(self.refresh_files)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.open_button)
        main_layout.addWidget(self.refresh_button)
        main_layout.addLayout(self.button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.directory="C:/Users/Hp/temp_folder"
        self.display_files(self.directory)


    def open_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Open Directory', '')
        if directory:
            self.display_files(directory)
            print(directory)

    def display_files(self, directory):
        self.clear_buttons()
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    if entry.is_file():
                        self.create_button(entry.name)
        except OSError as e:
            print(f"Error: {e}")

    def create_button(self, filename):
        button_layout = QVBoxLayout()

        file_button = QPushButton(filename, self)
        file_button.clicked.connect(lambda checked, name=filename: self.on_button_clicked(name))
        button_layout.addWidget(file_button)

        delete_button = QPushButton('Delete', self)
        delete_button.clicked.connect(lambda checked, name=filename: self.on_delete_button_clicked(name))
        button_layout.addWidget(delete_button)

        self.button_layout.addLayout(button_layout)

    def clear_buttons(self):
        while self.button_layout.count() > 0:
            item = self.button_layout.takeAt(0)
            widget = item.layout()
            if widget:
                while widget.count() > 0:
                    widget_item = widget.takeAt(0)
                    widget_widget = widget_item.widget()
                    if widget_widget:
                        widget_widget.deleteLater()

    def on_button_clicked(self, filename):
        print(f"Selected file: {filename}")

    def on_delete_button_clicked(self, filename):
        try:
            # Construct the full path to the file
            full_path = os.path.join(self.directory, filename)
            
            # Check if the file exists before attempting to delete it
            if os.path.exists(full_path):
                os.remove(full_path)
                print(f"Deleted file: {filename}")
            else:
                print(f"File not found: {filename}")
        except OSError as e:
            print(f"Error deleting file: {e}")

    def refresh_files(self):
        self.clear_buttons()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileListWindow()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())
