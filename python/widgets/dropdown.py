from PySide6.QtWidgets import QComboBox, QStyledItemDelegate
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from PySide6.QtCore import Qt
from gui.themes import theme

class TacticalDropdown(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # --- OVERRIDES ---
        self.primary_override = None
        self.bevel_size = 8.0
        self.border_width = 1.5
        self.font_size = 10
        self.alpha_multiplier = 1.0
        
        self.setMinimumHeight(40)
        self.view().verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")
        self.setItemDelegate(QStyledItemDelegate())
        theme.theme_signals.updated.connect(self.update)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pri = self.primary_override if self.primary_override else QColor(theme.ACTIVE["primary"])
        w, h, n = float(self.width()), float(self.height()), self.bevel_size
        
        path = QPainterPath()
        path.moveTo(n, 0); path.lineTo(w-n, 0); path.lineTo(w, n); path.lineTo(w, h-n); path.lineTo(w-n, h); path.lineTo(n, h); path.lineTo(0, h-n); path.lineTo(0, n); path.closeSubpath()

        # Background Tint
        overlay = QColor(pri)
        overlay.setAlpha(int((60 if self.underMouse() else 30) * self.alpha_multiplier))
        p.fillPath(path, overlay)
        p.setPen(QPen(pri, self.border_width))
        p.drawPath(path)

        # Arrow
        p.setBrush(pri); p.setPen(Qt.NoPen)
        tri = QPainterPath()
        tri.moveTo(w-20, h/2-3); tri.lineTo(w-10, h/2-3); tri.lineTo(w-15, h/2+4); p.drawPath(tri)

        # Text
        p.setPen(Qt.white); p.setFont(QFont("Consolas", self.font_size, QFont.Weight.Bold))
        p.drawText(self.rect().adjusted(10, 0, -30, 0), Qt.AlignVCenter, self.currentText())