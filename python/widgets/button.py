from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from PySide6.QtCore import Qt
from gui.themes import theme

class TacticalButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        
        # --- PHYSICAL DESIGN OVERRIDES ---
        self.bevel_size = 8.0
        self.border_width = 1.5
        self.clip_corners = True
        self.font_size = 10
        self.is_bold = True
        
        # --- COLOR & LIGHTING OVERRIDES ---
        self.primary_override = None      # Main Glow/Text color
        self.secondary_override = None    # Border color
        self.alpha_multiplier = 1.0       # 0.0 to 1.0 (Master Transparency)
        self.use_texture = True           # Toggle NumPy grit
        self.show_text = True
        
        self.setMinimumHeight(40)
        self._bg_cache = None
        self._pressed = False
        theme.theme_signals.updated.connect(self.refresh_widget)

    def refresh_widget(self):
        self._bg_cache = None
        self.update()

    def mousePressEvent(self, event):
        self._pressed = True; self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._pressed = False; self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # RESOLVE VARIABLES
        pri = self.primary_override if self.primary_override else QColor(theme.ACTIVE["primary"])
        sec = self.secondary_override if self.secondary_override else QColor(theme.ACTIVE["secondary"])
        w, h = float(self.width()), float(self.height())
        n = self.bevel_size if self.clip_corners else 0.0

        # DRAW SHAPE
        path = QPainterPath()
        path.moveTo(n, 0); path.lineTo(w-n, 0); path.lineTo(w, n); path.lineTo(w, h-n)
        path.lineTo(w-n, h); path.lineTo(n, h); path.lineTo(0, h-n); path.lineTo(0, n); path.closeSubpath()

        # LAYER 1: TEXTURE
        if self.use_texture:
            if self._bg_cache is None or self._bg_cache.size() != self.size():
                self._bg_cache = theme.get_numpy_gradient(int(w), int(h))
            p.setClipPath(path)
            p.drawPixmap(0, 0, self._bg_cache)
            p.setClipping(False)

        # LAYER 2: TINT
        overlay = QColor(pri)
        # Dynamic interaction logic
        alpha = 180 if self._pressed else (80 if self.underMouse() else 35)
        if self.primary_override: alpha = pri.alpha() # Respect custom alpha if provided
        overlay.setAlpha(int(alpha * self.alpha_multiplier))
        p.fillPath(path, overlay)

        # LAYER 3: BORDER
        p.setPen(QPen(pri if self.underMouse() else sec, self.border_width))
        p.drawPath(path)

        # LAYER 4: TEXT
        if self.show_text:
            p.setPen(Qt.white if (self.underMouse() or self.primary_override) else sec)
            p.setFont(QFont("Consolas", self.font_size, QFont.Weight.Bold if self.is_bold else QFont.Weight.Normal))
            p.drawText(self.rect(), Qt.AlignCenter, self.text())
        p.end()