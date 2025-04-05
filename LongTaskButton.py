
"""
A button class whose function is to spawn a potentially long-running task in the background.
It will spawn off a seperate thread, so that the UI can get updated normally while the task is running.
If the button is pressed during a run, it will signal the task to stop early.
"""

import threading
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QThread

class LongTaskButton(QPushButton):
    def __init__(self, text_normal, text_running, callback, parent=None):
        """
        :param text_normal: The initial text of the button.
        :param text_running: The text displayed while the task is running.
        :param callback: The function to run in a separate thread.
                         It must accept a threading.Event as its single argument.
        """
        super().__init__(text_normal, parent)
        self._text_normal = text_normal
        self._text_running = text_running
        self._callback = callback
        self._thread = None
        self._stop_event = None

        # Connect the clicked signal to our handler.
        self.clicked.connect(self._handle_click)

    def _handle_click(self):
        # If no thread is running, start the long task.
        if self._thread is None or not self._thread.isRunning():
            # Create an event to signal early termination.
            self._stop_event = threading.Event()
            # Create and start a QThread to run the callback.
            self._thread = TaskThread(self._callback, self._stop_event)
            self._thread.finished.connect(self._task_finished)
            self.setText(self._text_running)
            self._thread.start()
        else:
            # If the thread is running, signal it to stop.
            if self._stop_event:
                self._stop_event.set()

    def _task_finished(self):
        # Reset button text when the task is complete.
        self.setText(self._text_normal)
        # Optionally, clean up the thread reference.
        self._thread = None
        self._stop_event = None
    def __del__(self):
        # When the button is destroyed, signal the running thread (if any) to stop.
        if self._stop_event and not self._stop_event.is_set():
            self._stop_event.set()
        if self._thread and self._thread.isRunning():
            # Wait for the thread to finish.
            self._thread.wait()

# QThread subclass that runs the callback function for LongTaskButton.
class TaskThread(QThread):
    def __init__(self, callback, stop_event, parent=None):
        super().__init__(parent)
        self.callback = callback
        self.stop_event = stop_event

    def run(self):
        # Run the callback, passing the stop event so it can check for early termination
        self.callback(self.stop_event)


