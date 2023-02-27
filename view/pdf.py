from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QToolButton,QLabel
from PyQt5.uic import loadUi


class PdfWindow(QWidget):

    def __init__(self,home):
        super().__init__()
        self.home = home
        loadUi("./view/ui/pdf.ui", self)
