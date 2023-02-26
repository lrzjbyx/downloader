from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QToolButton,QLabel
from PyQt5.uic import loadUi


class DownloadWindow(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("./view/ui/download.ui", self)
