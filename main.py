import sys

from PyQt6.QtWidgets import QApplication
from view.home import HomeWindow


if __name__ == '__main__':
    app = QApplication([])
    win = HomeWindow()
    win.show()
    sys.exit(app.exec())
    # app.exec_()

