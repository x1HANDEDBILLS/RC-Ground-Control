from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath, QFont
from PySide6.QtCore import Qt
from gui.themes import theme

class TacticalInput(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.primary_override = None
        self.bevel_size = 6.0
        self.border_width = 1.0
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(35)
        theme.theme_signals.updated.connect(self.update)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        pri = self.primary_override if self.primary_override else QColor(theme.ACTIVE["primary"])
        w, h, n = float(self.width()), float(self.height()), self.bevel_size

        path = QPainterPath()
        path.moveTo(n, 0); path.lineTo(w-n, 0); path.lineTo(w, n); path.lineTo(w, h-n); path.lineTo(w-n, h); path.lineTo(n, h); path.lineTo(0, h-n); path.lineTo(0, n); path.closeSubpath()

        p.fillPath(path, QColor(10, 10, 10, 200))
        p.setPen(QPen(pri, self.border_width + (1.0 if self.hasFocus() else 0.0)))
        p.drawPath(path)

        p.setPen(Qt.white); p.setFont(QFont("Consolas", 10))
        if not self.text(): p.setOpacity(0.5)
        p.drawText(self.rect().adjusted(10,0,-10,0), Qt.AlignVCenter, self.text() or self.placeholderText())