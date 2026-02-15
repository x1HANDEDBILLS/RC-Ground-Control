import sys
import os
import signal
from PySide6.QtWidgets import QApplication

# Ensure imports work from the 'python' root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main import MainGUI
from gui.themes import theme

# Allow Ctrl+C to kill the app instantly
signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Global theme initialization
    theme.set_active_theme("RED") # Change to "RED", "AMBER", etc.
    app.setStyleSheet(theme.get_qss())

    main_gui = MainGUI()
    main_gui.start()

    sys.exit(app.exec())