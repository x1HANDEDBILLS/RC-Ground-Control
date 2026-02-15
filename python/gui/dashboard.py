from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QPushButton, QFrame
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from gui.themes import theme
from widgets.label import TacticalLabel
from widgets.popout import TacticalPopout
# Note: ColorEngineBox import can be removed if only used by the popout now

class TacticalPanel(QFrame):
    def __init__(self, title="PANEL_ID", parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 25, 15, 15)
        self.header = TacticalLabel(title, size=9, bold=True)
        self.layout.addWidget(self.header, alignment=Qt.AlignTop)
        theme.theme_signals.updated.connect(self.update_style)
        self.update_style()

    def update_style(self):
        pri = theme.ACTIVE["hex"]
        self.setStyleSheet(f"TacticalPanel {{ border: 1px solid {pri}; background: rgba(0,0,0,150); margin-top: 10px; }}")

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1024, 600)
        self.layout = QGridLayout(self)

        # Main Controls
        self.ctrl_panel = TacticalPanel("SYSTEM_RESOURCES")
        self.btn_theme = QPushButton("OPEN COLOR ENGINE")
        self.btn_theme.setMinimumHeight(50)
        self.btn_theme.clicked.connect(self.open_theme_popout)
        self.ctrl_panel.layout.addWidget(self.btn_theme)
        self.ctrl_panel.layout.addStretch()

        # Telemetry View
        self.view_panel = TacticalPanel("MAIN_VIEWPORT")
        self.view_panel.layout.addWidget(TacticalLabel("ACTIVE TELEMETRY FEED...", size=14))
        self.view_panel.layout.addStretch()

        self.layout.addWidget(self.ctrl_panel, 0, 0)
        self.layout.addWidget(self.view_panel, 0, 1)

        theme.theme_signals.updated.connect(self.sync_ui)
        self.sync_ui()

    def open_theme_popout(self):
        """
        NEW QML LAUNCHER: 
        We no longer pass widgets or text here. 
        The QML file handles the visual content.
        """
        TacticalPopout.launch()

    def sync_ui(self):
        pri = theme.ACTIVE["hex"]
        self.setStyleSheet(f"""
            QPushButton {{ 
                border: 1px solid {pri}; 
                color: {pri}; 
                font-family: 'Consolas'; 
                padding: 10px; 
            }}
            QPushButton:hover {{ background: {pri}; color: black; }}
        """)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.drawPixmap(0, 0, theme.get_numpy_gradient(self.width(), self.height()))