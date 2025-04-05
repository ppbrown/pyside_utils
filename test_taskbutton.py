import sys
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
# Import the custom button class (assumes it is defined in a module named long_task_button.py)
from LongTaskButton import LongTaskButton

def long_running_task(stop_event):
    """A dummy long task that checks for early termination every second."""
    for i in range(10):
        if stop_event.is_set():
            print(f"Task cancelled early at iteration {i + 1}.")
            return
        print(f"Working... iteration {i + 1}/10")
        time.sleep(1)
    print("Task completed successfully.")

def main():
    app = QApplication(sys.argv)
    
    # Create a main window with a vertical layout.
    window = QMainWindow()
    window.setWindowTitle("Long Task Button Test Harness")
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    
    # Create our custom button with normal and running texts.
    btn = LongTaskButton("Start Task", "Task Running - Click to Cancel", long_running_task)
    layout.addWidget(btn)
    
    window.setCentralWidget(central_widget)
    window.resize(300, 100)
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
