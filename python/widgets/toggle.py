from PySide6.QtWidgets import QCheckBox
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtCore import Qt, QRectF
from gui.themes import theme

class TacticalToggle(QCheckBox):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        # --- OVERRIDES ---
        self.primary_override = None
        self.track_width = 40.0
        self.font_size = 10
        
        self.setMinimumHeight(30)
        theme.theme_signals.updated.connect(self.update)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pri = self.primary_override if self.primary_override else QColor(theme.ACTIVE["primary"])
        state_col = pri if self.isChecked() else QColor(100, 100, 100)
        
        # 1. Draw Background Track
        track_rect = QRectF(0, 5, self.track_width, 20)
        p.setPen(QPen(state_col, 1.5))
        p.setBrush(QColor(0, 0, 0, 150))
        p.drawRect(track_rect)

        # 2. Draw Sliding Block
        block_x = (self.track_width - 15) if self.isChecked() else 3
        p.setBrush(state_col)
        p.drawRect(block_x, 8, 12, 14)

        # 3. Draw Text
        p.setPen(Qt.white)
        p.setFont(QFont("Consolas", self.font_size, QFont.Weight.Bold))
        p.drawText(self.track_width + 10, 20, self.text())
        p.end()