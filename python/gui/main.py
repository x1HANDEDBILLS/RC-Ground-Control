from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QCursor
from PySide6.QtCore import Qt
from gui.dashboard import Dashboard 

class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RC Ground Control")
        self.setCentralWidget(Dashboard())

        # Full screen + hidden cursor for DietPi hardware
        self.showFullScreen()
        QApplication.instance().setOverrideCursor(QCursor(Qt.BlankCursor))

    def start(self):
        print("Tactical GUI Online.")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        super().keyPressEvent(event)

    def closeEvent(self, event):
        # SAFE SHUTDOWN: Restore cursor so the Pi is usable
        QApplication.instance().restoreOverrideCursor()
        print("Safe Shutdown Successful.")
        super().closeEvent(event)