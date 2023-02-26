from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QPushButton, QToolButton
from PyQt6.uic import loadUi


class HomeWindow(QWidget):

    def __int__(self, parent):
        super(HomeWindow, self).__init__(parent)
        loadUi("./ui/main.ui", self)

        self.searchButton.setIconSize(QSize(50,50))
        self.searchButton.setIcon(QIcon("../resource/icon/search.png"))
        self.searchButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)




