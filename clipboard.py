import sys
import os
import shutil
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPixmap, QIcon, QDrag, QCursor
from PyQt6.QtCore import Qt, QMimeData


class FileDropWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.temp_location = os.path.join(
            os.path.expanduser('~'), 'temp_folder')
        if not os.path.exists(self.temp_location):
            os.mkdir(self.temp_location)
        print(os.path.join(
            os.path.expanduser('~'), 'temp_folder'))
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if os.path.isfile(file_path):
                    # Copy the file to the temporary location
                    shutil.copy(file_path, os.path.join(
                        self.temp_location, os.path.basename(file_path)))

            event.acceptProposedAction()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("File Drop Window")
    window.setGeometry(100, 100, 400, 300)

    central_widget = FileDropWidget()
    window.setCentralWidget(central_widget)

    window.show()
    sys.exit(app.exec())
