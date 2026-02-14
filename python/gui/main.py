from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QCursor
from PySide6.QtCore import Qt
from gui.dashboard import Dashboard  # import the visual GUI stuff

class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RC Ground Control")

        # Set the visual dashboard as central widget
        self.setCentralWidget(Dashboard())

        # Full screen + no cursor
        self.showFullScreen()
        QApplication.instance().setOverrideCursor(QCursor(Qt.BlankCursor))

        # ESC to exit
        self.setFocusPolicy(Qt.StrongFocus)

    def start(self):
        """Main GUI logic entry - can add signals, timers, connections here later"""
        print("Main GUI logic started")  # example - add more logic as needed

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        super().keyPressEvent(event)

    def closeEvent(self, event):
        QApplication.instance().restoreOverrideCursor()
        super().closeEvent(event)