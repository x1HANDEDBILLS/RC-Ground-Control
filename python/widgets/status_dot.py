from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QRadialGradient
from PySide6.QtCore import Qt

class StatusDot(QWidget):
    def __init__(self, size=15, parent=None):
        super().__init__(parent)
        # --- OVERRIDES ---
        self.color_override = QColor("#555555") # State color
        self.glow_intensity = 0.6
        
        self.setFixedSize(size, size)

    def set_status(self, color_name):
        self.color_override = QColor(color_name)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 1. Draw Outer Glow
        grad = QRadialGradient(self.width()/2, self.height()/2, self.width()/2)
        glow_col = QColor(self.color_override)
        glow_col.setAlpha(int(255 * self.glow_intensity))
        grad.setColorAt(0, glow_col)
        grad.setColorAt(1, Qt.transparent)
        
        p.setBrush(grad)
        p.setPen(Qt.NoPen)
        p.drawEllipse(0, 0, self.width(), self.height())
        
        # 2. Draw Core Dot
        p.setBrush(self.color_override)
        p.drawEllipse(self.width()*0.25, self.height()*0.25, self.width()*0.5, self.height()*0.5)