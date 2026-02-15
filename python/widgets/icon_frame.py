from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt
from gui.themes import theme

class IconFrame(QWidget):
    def __init__(self, size=40, parent=None):
        super().__init__(parent)
        
        # --- OVERRIDES ---
        self.primary_override = None
        self.border_width = 1.5
        self.corner_length = 8.0     # How far the "L" shape extends
        self.alpha_multiplier = 1.0
        
        self.setFixedSize(size, size)
        
        # Internal layout to hold an actual icon or text
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(4, 4, 4, 4)
        
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("background: transparent; color: white;")
        self.layout.addWidget(self.icon_label)
        
        theme.theme_signals.updated.connect(self.update)

    def set_icon_text(self, text):
        """Quick way to put a character or symbol in the frame"""
        self.icon_label.setText(text)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pri = self.primary_override if self.primary_override else QColor(theme.ACTIVE["primary"])
        w, h = float(self.width()), float(self.height())
        l = self.corner_length
        
        pen = QPen(pri, self.border_width)
        p.setPen(pen)
        p.setOpacity(self.alpha_multiplier)
        
        # DRAW TACTICAL BRACKETS (The 4 'L' shapes)
        
        # Top-Left
        p.drawLine(0, 0, l, 0)
        p.drawLine(0, 0, 0, l)
        
        # Top-Right
        p.drawLine(w, 0, w - l, 0)
        p.drawLine(w, 0, w, l)
        
        # Bottom-Left
        p.drawLine(0, h, l, h)
        p.drawLine(0, h, 0, h - l)
        
        # Bottom-Right
        p.drawLine(w, h, w - l, h)
        p.drawLine(w, h, w, h - l)
        
        p.end()