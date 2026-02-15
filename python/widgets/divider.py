from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from PySide6.QtCore import Qt
from gui.themes import theme

class TacticalDivider(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # --- OVERRIDES ---
        self.primary_override = None
        self.line_thickness = 1.0
        self.diamond_size = 12.0
        
        self.setFixedHeight(20)
        theme.theme_signals.updated.connect(self.update)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pri = self.primary_override if self.primary_override else QColor(theme.ACTIVE["primary"])
        w, h = float(self.width()), float(self.height())

        p.setPen(QPen(pri, self.line_thickness))
        mid_y = h / 2
        mid_x = w / 2
        d = self.diamond_size / 2

        # Draw Lines with a gap in the center
        p.drawLine(0, mid_y, mid_x - d - 5, mid_y)
        p.drawLine(mid_x + d + 5, mid_y, w, mid_y)

        # Draw Center Diamond
        path = QPainterPath()
        path.moveTo(mid_x, mid_y - d) # Top
        path.lineTo(mid_x + d, mid_y) # Right
        path.lineTo(mid_x, mid_y + d) # Bottom
        path.lineTo(mid_x - d, mid_y) # Left
        path.closeSubpath()
        
        p.setBrush(pri)
        p.drawPath(path)
        p.end()