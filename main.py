from PyQt5.QtWidgets import QApplication

from view.home import HomeWindow

if __name__ == '__main__':
    app = QApplication([])
    win = HomeWindow()
    win.show()
    app.exec_()