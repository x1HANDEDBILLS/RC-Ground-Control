import sys
from PySide6.QtWidgets import QApplication
from gui.main import MainGUI  # import the main GUI logic

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_gui = MainGUI()
    main_gui.start()  # call to start the GUI logic

    sys.exit(app.exec())