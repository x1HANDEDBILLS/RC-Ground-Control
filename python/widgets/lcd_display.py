from PySide6.QtWidgets import QLCDNumber, QSizePolicy
from PySide6.QtGui import QPainter, QColor, QPalette
from PySide6.QtCore import Qt, QSize
from gui.themes import theme

class TacticalLCD(QLCDNumber):
    def __init__(self, digits=3, parent=None):
        super().__init__(digits, parent)
        # --- OVERRIDES ---
        self.primary_override = None
        self.scanline_opacity = 40 
        self.fixed_width = None  # Use this to bypass auto-scaling manually
        self.fixed_height = 45
        
        # Standard Tactical Styling
        self.setSegmentStyle(QLCDNumber.Flat)
        self.setFrameStyle(0)
        
        # TELL LAYOUT: "Listen to my sizeHint, don't stretch me"
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        theme.theme_signals.updated.connect(self.update)

    def sizeHint(self):
        """Calculates width based on digit count with a 3-digit minimum floor."""
        if self.fixed_width:
            return QSize(self.fixed_width, self.fixed_height)
        
        # Logic: Use the actual digit count, but don't let it look smaller than a 3-digit box
        # This keeps the 'Tactical' weight consistent
        effective_digits = max(3, self.digitCount())
        
        calc_width = (effective_digits * 25) + 10
        return QSize(calc_width, self.fixed_height)

    def paintEvent(self, event):
        # Resolve Dynamic Color from Theme
        pri = self.primary_override if self.primary_override else QColor(theme.ACTIVE["primary"])
        
        # Set the segment color
        pal = self.palette()
        pal.setColor(QPalette.WindowText, pri)
        self.setPalette(pal)
        
        # Draw the base numbers
        super().paintEvent(event) 
        
        # Draw Tactical Scanlines
        p = QPainter(self)
        p.setPen(QColor(0, 0, 0, self.scanline_opacity))
        for y in range(0, self.height(), 2):
            p.drawLine(0, y, self.width(), y)
        p.end()