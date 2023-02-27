from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QToolButton, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.uic import loadUi

from view.detail import DetailWindow
from view.download import DownloadWindow
from view.pdf import PdfWindow
from view.play import PlayWindow
from view.search import SearchWindow
from view.set import SetWindow
# from api.bilibili_downloader import BilibiliVideoDownloader
from api.bilibili import Bilibili

class HomeWindow(QMainWindow):
    searchSignal = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        loadUi("./view/ui/home.ui", self)
        self.setWindowTitle("downloader")
        #
        # QToolButton().resize(QSize(80,80))
        # QLabel().setPixmap(QIcon("../resource/icon/search.png"))
        self.loginPic.setPixmap(QPixmap("./resource/icon/user.png"))
        self.loginPic.setScaledContents(True)


        self.searchButton.setIconSize(QSize(50,50))
        self.searchButton.setFixedSize(QSize(80,80))
        self.searchButton.setIcon(QIcon("./resource/icon/search.png"))
        self.searchButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.searchButton.clicked.connect(self.switchSearchWindow)


        self.detailButton.setIconSize(QSize(50,50))
        self.detailButton.setFixedSize(QSize(80,80))
        self.detailButton.setIcon(QIcon("./resource/icon/detail.png"))
        self.detailButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.detailButton.clicked.connect(self.switchDetailWindow)


        self.downloadButton.setIconSize(QSize(50,50))
        self.downloadButton.setFixedSize(QSize(80,80))
        self.downloadButton.setIcon(QIcon("./resource/icon/download.png"))
        self.downloadButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.downloadButton.clicked.connect(self.switchDownloadWindow)


        self.playButton.setIconSize(QSize(50,50))
        self.playButton.setFixedSize(QSize(80,80))
        self.playButton.setIcon(QIcon("./resource/icon/play.png"))
        self.playButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.playButton.clicked.connect(self.switchPlayWindow)

        self.pdfButton.setIconSize(QSize(50,50))
        self.pdfButton.setFixedSize(QSize(80,80))
        self.pdfButton.setIcon(QIcon("./resource/icon/pdf.png"))
        self.pdfButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.pdfButton.clicked.connect(self.switchPdfWindow)


        self.setButton.setIconSize(QSize(50,50))
        self.setButton.setFixedSize(QSize(80,80))
        self.setButton.setIcon(QIcon("./resource/icon/set.png"))
        self.setButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setButton.clicked.connect(self.switchSetWindow)


        # 搜索窗口
        self.searchWindow = SearchWindow(self)
        # 详情窗口
        self.detailWindow = DetailWindow(self)
        # 下载窗口
        self.downloadWindow = DownloadWindow(self)
        # pdf窗口
        self.pdfWindow = PdfWindow(self)
        # play窗口
        self.playWindow = PlayWindow(self)
        # 设置窗口
        self.setWindow = SetWindow(self)
        # 窗口开关
        self.switchWindow = [True,False,False,False,False,True]



        # 下载器
        self.downloader = Bilibili()

        # frame布局
        self.frameLayout = QVBoxLayout()
        self.frameLayout.setContentsMargins(0, 0, 0, 0)
        self.frameLayout.addWidget(self.searchWindow)
        self.frame.setLayout(self.frameLayout)

        # 搜索信号
        self.searchSignal.connect(self.searchProcessHandle)
        # 搜索结果
        self.searchResult = None


    def searchProcessHandle(self,data):
        self.searchResult  =  data
        self.detailWindow.addSignal.emit(data)


    def removeAllWidgetInLayout(self):
        self.frameLayout.takeAt(0).widget().setParent(None)


    def switchSearchWindow(self):
        if self.switchWindow[0]:
            self.removeAllWidgetInLayout()
            self.frameLayout.addWidget(self.searchWindow)

    def switchDetailWindow(self):
        if  self.switchWindow[1]:
            self.removeAllWidgetInLayout()
            self.frameLayout.addWidget(self.detailWindow)


    def switchDownloadWindow(self):
        if  self.switchWindow[2]:
            self.removeAllWidgetInLayout()
            self.frameLayout.addWidget(self.downloadWindow)

    def switchPlayWindow(self):
        if  self.switchWindow[3]:
            self.removeAllWidgetInLayout()
            self.frameLayout.addWidget(self.playWindow)


    def switchPdfWindow(self):
        if  self.switchWindow[4]:
            self.removeAllWidgetInLayout()
            self.frameLayout.addWidget(self.pdfWindow)


    def switchSetWindow(self):
        if  self.switchWindow[5]:
            self.removeAllWidgetInLayout()
            self.frameLayout.addWidget(self.setWindow)

