import sys
import numpy as np
from PySide6.QtGui import QColor, QImage, QPixmap
from PySide6.QtCore import Qt, QObject, Signal

class ThemeSignals(QObject):
    updated = Signal()

theme_signals = ThemeSignals() 
ACTIVE = {}

THEMES = {
    "RED":     {"p": (255, 0, 0),     "s": (200, 100, 100), "bg_l": (45, 5, 5),    "bg_d": (15, 2, 2),   "hex": "#FF0000", "font": "Consolas"},
    "GREEN":   {"p": (0, 255, 0),     "s": (100, 200, 100), "bg_l": (5, 45, 5),    "bg_d": (2, 15, 2),   "hex": "#00FF00", "font": "Consolas"},
    "BLUE":    {"p": (0, 0, 255),     "s": (100, 100, 200), "bg_l": (5, 5, 45),    "bg_d": (2, 2, 15),   "hex": "#0000FF", "font": "Consolas"},
    "CYAN":    {"p": (0, 255, 255),   "s": (150, 200, 200), "bg_l": (5, 35, 45),   "bg_d": (2, 5, 15),   "hex": "#00FFFF", "font": "Consolas"},
    "MAGENTA": {"p": (255, 0, 255),   "s": (200, 150, 200), "bg_l": (40, 5, 40),   "bg_d": (15, 2, 15),  "hex": "#FF00FF", "font": "Consolas"},
    "YELLOW":  {"p": (255, 255, 0),   "s": (200, 200, 150), "bg_l": (45, 45, 5),   "bg_d": (15, 15, 2),  "hex": "#FFFF00", "font": "Consolas"},
    "GREY":    {"p": (160, 160, 160), "s": (120, 120, 120), "bg_l": (40, 40, 40),  "bg_d": (20, 20, 20), "hex": "#A0A0A0", "font": "Consolas"},
    "DARK_GREY": {"p": (80, 80, 80),  "s": (140, 140, 140), "bg_l": (25, 25, 25),  "bg_d": (10, 10, 10), "hex": "#505050", "font": "Consolas"}
}

def set_active_theme(name):
    global ACTIVE
    name = name.upper()
    data = THEMES.get(name, THEMES["RED"])
    
    if ACTIVE.get("name") != name:
        print(f"[THEME] Loading {name}")
    
    ACTIVE = {
        "primary": QColor(*data["p"]),
        "secondary": QColor(*data["s"]),
        "bg_light": data["bg_l"],
        "bg_dark": data["bg_d"],
        "hex": data["hex"],
        "font": data["font"],
        "name": name
    }
    theme_signals.updated.emit()

def set_custom_color(qcolor):
    global ACTIVE
    r, g, b = qcolor.red(), qcolor.green(), qcolor.blue()
    bg_l = (int(r * 0.15), int(g * 0.15), int(b * 0.15))
    bg_d = (int(r * 0.05), int(g * 0.05), int(b * 0.05))

    ACTIVE = {
        "primary": qcolor,
        "secondary": qcolor.lighter(130),
        "bg_light": bg_l,
        "bg_dark": bg_d,
        "hex": qcolor.name().upper(),
        "font": "Consolas",
        "name": "CUSTOM"
    }
    theme_signals.updated.emit()

def get_qss():
    font = ACTIVE.get("font", "Consolas")
    return f"QWidget {{ background-color: transparent; color: white; font-family: '{font}'; }}"

if not ACTIVE:
    set_active_theme("RED")

def get_numpy_gradient(w, h):
    w, h = max(1, int(w)), max(1, int(h))
    x, y = np.linspace(0, 1, w), np.linspace(0, 1, h)
    xv, yv = np.meshgrid(x, y)
    ratio = (xv + yv) / 2.0 
    c_l, c_d = ACTIVE["bg_light"], ACTIVE["bg_dark"]
    noise = np.random.normal(0, 1.5, (h, w))
    r = np.clip((c_l[0] + (c_d[0]-c_l[0])*ratio) + noise, 0, 255)
    g = np.clip((c_l[1] + (c_d[1]-c_l[1])*ratio) + noise, 0, 255)
    b = np.clip((c_l[2] + (c_d[2]-c_l[2])*ratio) + noise, 0, 255)
    arr = np.dstack((r, g, b)).astype(np.uint8)
    return QPixmap.fromImage(QImage(arr.data, w, h, w*3, QImage.Format.Format_RGB888))

# --- CRITICAL FIX FOR YOUR MAIN.PY IMPORT STYLE ---
theme = sys.modules[__name__]