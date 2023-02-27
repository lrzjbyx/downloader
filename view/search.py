import threading
from urllib.request import urlopen

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QToolButton, QLabel, QLineEdit
from PyQt5.uic import loadUi


class SearchWindow(QWidget):

    def __init__(self,home):
        super().__init__()
        loadUi("./view/ui/search.ui", self)
        self.label.setPixmap(QPixmap("./resource/icon/log.png"))
        self.home = home
        self.pushButton.clicked.connect(self.search)
        self.lineEdit.setText("https://www.bilibili.com/video/BV1224y1n7qh/?spm_id_from=333.1007.tianma.1-2-2.click")
        QLineEdit().text().isascii()

    def search(self):
        if self.lineEdit.text().isascii():
            # 多线程
            x = threading.Thread(target=self.searchThreadHandle)
            x.start()


    def searchThreadHandle(self):
        self.home.downloader.set(self.lineEdit.text())
        search_result = self.home.downloader.require_input_link_video()
        self.home.searchSignal.emit(search_result)