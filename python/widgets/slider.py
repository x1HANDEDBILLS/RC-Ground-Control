from PySide6.QtWidgets import QSlider
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from PySide6.QtCore import Qt, QRectF
from gui.themes import theme

class TacticalSlider(QSlider):
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        # --- OVERRIDES ---
        self.primary_override = None
        self.track_thickness = 2.0
        self.handle_size = 16.0
        self.alpha_multiplier = 1.0
        
        self.setMinimumHeight(30)
        theme.theme_signals.updated.connect(self.update)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pri = self.primary_override if self.primary_override else QColor(theme.ACTIVE["primary"])
        w, h = float(self.width()), float(self.height())
        
        # 1. Draw Track (The Rail)
        p.setPen(QPen(pri.darker(200), self.track_thickness))
        p.drawLine(10, h/2, w-10, h/2)

        # 2. Calculate Handle Position
        range_val = self.maximum() - self.minimum()
        pos_pct = (self.value() - self.minimum()) / range_val if range_val != 0 else 0
        handle_x = 10 + (pos_pct * (w - 20))
        
        # 3. Draw Tactical Diamond Handle
        p.setBrush(pri)
        p.setPen(QPen(Qt.white, 1.0) if self.underMouse() else Qt.NoPen)
        
        s = self.handle_size / 2
        path = QPainterPath()
        path.moveTo(handle_x, h/2 - s)  # Top
        path.lineTo(handle_x + s, h/2)  # Right
        path.lineTo(handle_x, h/2 + s)  # Bottom
        path.lineTo(handle_x - s, h/2)  # Left
        path.closeSubpath()
        p.drawPath(path)
        p.end()