from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtGui import QPainter, QColor, QPainterPath, QPen
from PySide6.QtCore import Qt
from gui.themes import theme
from widgets.label import TacticalLabel

class StatusHeader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.primary_override = None
        self.height_override = 55
        self.setFixedHeight(self.height_override)
        
        # Layout with extra padding to prevent text hitting the edges
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(40, 0, 40, 15)
        
        self.title_label = TacticalLabel("SYSTEM STATUS: NOMINAL", size=12)
        self.title_label.setMinimumWidth(350) # Prevent compression
        self.layout.addWidget(self.title_label)
        
        self.layout.addStretch()
        
        self.ver_label = TacticalLabel("OS v2.0.4-LNK", size=9)
        self.ver_label.alpha_multiplier = 0.7
        self.layout.addWidget(self.ver_label)
        
        theme.theme_signals.updated.connect(self.update)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        pri = self.primary_override if self.primary_override else QColor(theme.ACTIVE["primary"])
        w, h = float(self.width()), float(self.height())

        path = QPainterPath()
        path.moveTo(0, 0); path.lineTo(w, 0); path.lineTo(w, h - 15)
        path.lineTo(w - 30, h); path.lineTo(30, h); path.lineTo(0, h - 15)
        path.closeSubpath()

        p.setBrush(QColor(10, 10, 10, 230)) # Slightly translucent black
        p.setPen(QPen(pri, 2.0))
        p.drawPath(path)
        p.end()