from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QToolButton,QLabel
from PyQt5.uic import loadUi


class SetWindow(QWidget):

    def __init__(self):
        super().__init__()
        loadUi("./view/ui/set.ui", self)
