from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from PySide6.QtCore import Qt
from gui.themes import theme

class TacticalPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # --- OVERRIDES ---
        self.primary_override = None
        self.bevel_size = 15.0
        self.border_width = 1.0
        self.bg_alpha = 25              # Internal fill opacity
        self.alpha_multiplier = 1.0     # Master opacity
        self.use_texture = True
        
        self.container_layout = QVBoxLayout(self)
        self.container_layout.setContentsMargins(15, 15, 15, 15)
        self._bg_cache = None
        theme.theme_signals.updated.connect(self.refresh_ui)

    def refresh_ui(self):
        self._bg_cache = None; self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pri = self.primary_override if self.primary_override else QColor(theme.ACTIVE["primary"])
        w, h, n = float(self.width()), float(self.height()), self.bevel_size
        
        path = QPainterPath()
        path.moveTo(n, 0); path.lineTo(w-n, 0); path.lineTo(w, n); path.lineTo(w, h-n)
        path.lineTo(w-n, h); path.lineTo(n, h); path.lineTo(0, h-n); path.lineTo(0, n); path.closeSubpath()

        if self.use_texture:
            if self._bg_cache is None: self._bg_cache = theme.get_numpy_gradient(int(w), int(h))
            p.setClipPath(path); p.drawPixmap(0, 0, self._bg_cache); p.setClipping(False)

        bg = QColor(pri)
        bg.setAlpha(int(self.bg_alpha * self.alpha_multiplier))
        p.fillPath(path, bg)
        
        p.setPen(QPen(pri, self.border_width))
        p.drawPath(path)