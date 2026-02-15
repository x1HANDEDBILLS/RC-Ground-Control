from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont, QPen
from PySide6.QtCore import Qt
from gui.themes import theme

class TacticalCoords(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # --- OVERRIDES ---
        self.primary_override = None
        self.show_crosshair = True
        self.font_size = 9
        
        self.lat = "00.0000"
        self.lon = "00.0000"
        self.setFixedSize(160, 50)
        theme.theme_signals.updated.connect(self.update)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pri = self.primary_override if self.primary_override else QColor(theme.ACTIVE["primary"])
        
        # Draw Border
        p.setPen(QPen(pri, 1))
        p.drawRect(0, 0, self.width()-1, self.height()-1)
        
        # Technical Crosshair
        if self.show_crosshair:
            p.setOpacity(0.2)
            p.drawLine(self.width()/2, 0, self.width()/2, self.height())
            p.drawLine(0, self.height()/2, self.width(), self.height()/2)
            p.setOpacity(1.0)
        
        # Data Labels
        p.setPen(Qt.white)
        p.setFont(QFont("Consolas", self.font_size, QFont.Weight.Bold))
        p.drawText(self.rect().adjusted(5, 5, 0, 0), Qt.AlignTop | Qt.AlignLeft, f"LAT {self.lat}")
        p.drawText(self.rect().adjusted(5, 0, -5, -5), Qt.AlignBottom | Qt.AlignLeft, f"LON {self.lon}")
        p.end()