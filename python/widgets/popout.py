import os
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtCore import Qt, QUrl

class TacticalPopout(QWidget):
    _instance = None

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 1. Force a visible size for the container
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 1024, 600)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.view = QQuickWidget()
        
        # Path Logic
        current_dir = os.path.dirname(os.path.abspath(__file__))
        qml_path = os.path.join(current_dir, "qml", "popout.qml")
        
        # 2. DEBUG: Print status if it fails
        self.view.statusChanged.connect(self.check_status)
        
        self.view.setSource(QUrl.fromLocalFile(qml_path))
        self.view.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.view.setClearColor(Qt.transparent)
        
        layout.addWidget(self.view)

    def check_status(self, status):
        """Prints QML errors to your terminal if the file doesn't load."""
        if status == QQuickWidget.Status.Error:
            print("\n[QML ERROR DETECTED]")
            for error in self.view.errors():
                print(f"  - Line {error.line()}: {error.description()}")
        elif status == QQuickWidget.Status.Ready:
            print("[QML STATUS] Popout Ready and Visible.")
            # Connect signal only after Ready
            root_obj = self.view.rootObject()
            if root_obj:
                root_obj.closeRequested.connect(self.destroy_me)

    def destroy_me(self):
        TacticalPopout._instance = None
        self.close()
        self.deleteLater()

    @classmethod
    def launch(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance.show()
            # Force the window to the front
            cls._instance.raise_()
            cls._instance.activateWindow()
        return cls._instance