from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt
from gui.themes import theme

class TacticalMeter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # --- OVERRIDES ---
        self.primary_override = None
        self.border_width = 1.0
        self.pip_count = 10
        self.pip_gap = 2
        self.value = 0.0  # 0.0 to 1.0
        
        self.setFixedWidth(35)
        self.setMinimumHeight(120) # Ensure enough vertical space
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        theme.theme_signals.updated.connect(self.update)

    def set_value(self, val):
        """Update the level from 0.0 to 1.0 and trigger a redraw"""
        self.value = max(0.0, min(1.0, val))
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pri = self.primary_override if self.primary_override else QColor(theme.ACTIVE["primary"])
        w, h = float(self.width()), float(self.height())

        # 1. Outer Frame (Tactical Container)
        p.setPen(QPen(pri, self.border_width))
        p.drawRect(5, 5, w-10, h-10)

        # 2. Pip Drawing Logic
        usable_h = h - 14
        pip_h = (usable_h / self.pip_count) - self.pip_gap
        
        for i in range(self.pip_count):
            # Calculate from bottom up (0 is bottom, pip_count-1 is top)
            threshold = i / self.pip_count
            is_lit = self.value > threshold
            
            y_pos = (h - 7) - ((i + 1) * (pip_h + self.pip_gap))
            
            if is_lit:
                p.setBrush(pri)
                p.setOpacity(1.0)
            else:
                # Dim pips for the background "ghost" look
                p.setBrush(pri.darker(300))
                p.setOpacity(0.15)
                
            p.setPen(Qt.NoPen)
            p.drawRect(8, y_pos, w-16, pip_h)
        p.end()