from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QPainter, QColor, QFont, QFontMetrics, QPen
from PySide6.QtCore import Qt, QSize
from gui.themes import theme

class TacticalLabel(QLabel):
    def __init__(self, text="", parent=None, size=10, bold=True):
        super().__init__(text, parent)
        
        # --- PROPERTIES ---
        self.color_override = None      
        self.bg_override = Qt.transparent
        self.alpha_multiplier = 1.0     
        self.font_size = size           
        self.is_bold = bold             
        
        # Debug Border (Keep this true one last time to confirm)
        self.draw_border = True         
        self.border_color = "#888888"   
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Back to Fixed, because now our math will be correct
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        theme.theme_signals.updated.connect(self.update)
        # Initial sizing
        self.update_geometry()

    def get_target_font(self):
        """Helper to ensure we use the EXACT same font for math and drawing."""
        return QFont("Consolas", self.font_size, 
                     QFont.Weight.Bold if self.is_bold else QFont.Weight.Normal)

    def update_geometry(self):
        """
        THE FIX: We create the Consolas font HERE to measure it.
        Previously, we were measuring the default system font (Arial/Sans),
        which is narrower than Consolas, causing the box to be too small.
        """
        target_font = self.get_target_font()
        metrics = QFontMetrics(target_font)
        
        # Measure the text using the CORRECT font
        text_w = metrics.horizontalAdvance(self.text())
        text_h = metrics.height()
        
        # Add a consistent, comfortable padding
        # 30px total (15px left, 15px right) is plenty if the measurement is accurate.
        pad_h = 30
        pad_v = 10
        
        self.setFixedSize(text_w + pad_h, text_h + pad_v)

    def setText(self, text):
        super().setText(text)
        self.update_geometry()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        
        # 1. Visual Debug Border
        if self.draw_border:
            pen = QPen(QColor(self.border_color), 1, Qt.DashLine)
            p.setPen(pen)
            p.drawRect(0, 0, self.width() - 1, self.height() - 1)
            
        # 2. Background
        if self.bg_override != Qt.transparent:
            p.fillRect(self.rect(), self.bg_override)
            
        # 3. Text Setup
        col = QColor(self.color_override) if self.color_override else QColor(theme.ACTIVE["secondary"])
        col.setAlpha(int(255 * self.alpha_multiplier))
        
        # USE THE HELPER to ensure paint uses the exact font we measured
        p.setFont(self.get_target_font())
        p.setPen(col)
        
        # 4. Drawing
        # Now that the box is guaranteed to be 30px wider than the text,
        # Center alignment will look perfect.
        p.drawText(self.rect(), Qt.AlignCenter, self.text())
        p.end()