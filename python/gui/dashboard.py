from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt

class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #101010;")  # blank dark grey screen

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Blank - add visuals (widgets, labels, etc.) here later
        # Example placeholder (comment out if you want fully blank)
        # label = QLabel("Blank Dark Grey Dashboard")
        # label.setAlignment(Qt.AlignCenter)
        # label.setStyleSheet("color: #FF1E1E; font-size: 32px;")
        # layout.addWidget(label, stretch=1)