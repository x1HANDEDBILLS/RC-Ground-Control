from PySide6.QtWidgets import QProgressBar
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt
from gui.themes import theme

class TacticalProgress(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        # --- OVERRIDES ---
        self.primary_override = None
        self.segments = 12
        self.segment_gap = 3
        
        self.setFixedHeight(18)
        self.setTextVisible(False)
        theme.theme_signals.updated.connect(self.update)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pri = self.primary_override if self.primary_override else QColor(theme.ACTIVE["primary"])
        w, h = float(self.width()), float(self.height())
        
        # Background Border
        p.setPen(QPen(pri, 1))
        p.drawRect(0, 0, w-1, h-1)

        # Draw Segments
        val_pct = (self.value() - self.minimum()) / (self.maximum() - self.minimum())
        
        seg_w = (w - (self.segments + 1) * self.segment_gap) / self.segments
        
        for i in range(self.segments):
            if (i / self.segments) < val_pct:
                p.setBrush(pri)
                p.setPen(Qt.NoPen)
            else:
                p.setBrush(QColor(pri).darker(400))
                p.setOpacity(0.2)
                
            x_pos = self.segment_gap + (i * (seg_w + self.segment_gap))
            p.drawRect(x_pos, 3, seg_w, h-6)
            p.setOpacity(1.0)
        p.end()