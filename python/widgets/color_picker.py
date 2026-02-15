from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QMouseEvent, QPen
from PySide6.QtCore import Qt, QRect
from gui.themes import theme

class TacticalColorPicker(QWidget):
    """The Spectrum Slider with built-in pixel-grab override."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(50)
        self.draw_border = True
        self.border_color = "#888888"

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 1. Gradient Spectrum
        grad = QLinearGradient(0, 0, self.width(), 0)
        # Science-based stops for a perfect spectrum
        colors = [QColor(255,0,0), QColor(255,255,0), QColor(0,255,0), 
                  QColor(0,255,255), QColor(0,0,255), QColor(255,0,255), QColor(255,0,0)]
        for i, col in enumerate(colors):
            grad.setColorAt(i/6, col)
            
        p.setBrush(grad)
        p.setPen(Qt.NoPen)
        p.drawRect(self.rect())

        # 2. Border Override Logic (Matches Label style)
        if self.draw_border:
            p.setPen(QPen(QColor(self.border_color), 1, Qt.DashLine))
            p.drawRect(0, 0, self.width()-1, self.height()-1)

    def mousePressEvent(self, event): self.handle_click(event)
    def mouseMoveEvent(self, event): 
        if event.buttons() & Qt.LeftButton: self.handle_click(event)

    def handle_click(self, event):
        # The ultimate override: Grabs the exact pixel and forces theme update
        pix = self.grab(QRect(event.position().x(), event.position().y(), 1, 1))
        color = pix.toImage().pixelColor(0, 0)
        if color.isValid():
            theme.set_custom_color(color)

class ColorEngineBox(QFrame):
    """The full unit containing the spectrum and sorted scientific presets."""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Fixed Box logic: Ensuring the control unit has a consistent footprint
        self.setFixedWidth(350) 
        self.setStyleSheet("QFrame { border: 1px solid #444; background: #0A0A0A; padding: 15px; }")
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        
        # 1. Spectrum Slider
        self.spectrum = TacticalColorPicker()
        main_layout.addWidget(self.spectrum)
        
        # 2. Sorted Quick-Select Defaults
        # We sort them: Primaries (R,G,B) -> Secondaries (C,M,Y) -> Neutrals
        sort_order = ["RED", "GREEN", "BLUE", "CYAN", "MAGENTA", "YELLOW", "WHITE", "GREY"]
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        for name in sort_order:
            if name in theme.THEMES:
                data = theme.THEMES[name]
                btn = QPushButton()
                btn.setFixedSize(28, 28)
                # Apply the hex from theme.py to the button background
                btn.setStyleSheet(f"""
                    QPushButton {{ 
                        background-color: {data['hex']}; 
                        border: 1px solid #666; 
                        border-radius: 4px; 
                    }}
                    QPushButton:hover {{ border: 2px solid white; }}
                """)
                # Link click to the theme-switch override
                btn.clicked.connect(lambda _, n=name: theme.set_active_theme(n))
                btn_layout.addWidget(btn)
            
        main_layout.addLayout(btn_layout)