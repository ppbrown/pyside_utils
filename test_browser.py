
# This exists solely to demo the DirectoryBrowser class

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QSplitter,
    QMainWindow, QLabel
)
from PySide6.QtCore import Qt

from DirectoryBrowser import DirectoryBrowser


class MainDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 400)
        self.label = QLabel("I am the main display", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_label(self, text):
        self.label.setText(text)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        splitter = QSplitter(Qt.Horizontal)
        # Create the main display first.
        self.main_display = MainDisplay()
        # Provide the callback function to update the main display when a file is clicked.
        self.directory_browser = DirectoryBrowser(file_clicked_callback=self.on_file_clicked)

        splitter.addWidget(self.directory_browser)
        splitter.addWidget(self.main_display)
        splitter.setSizes([250, 400])
        self.setCentralWidget(splitter)
        self.setWindowTitle("Directory Browser with Main Display")

    def on_file_clicked(self, directory, file_name):
        # Update the main display label with the directory and file name.
        self.main_display.update_label(f"Directory: {directory}\nFile: {file_name}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

