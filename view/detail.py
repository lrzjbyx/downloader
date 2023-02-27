import json
import threading
from time import gmtime, strftime
from urllib.request import urlopen

from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QToolButton, QLabel, QPushButton, QHBoxLayout, \
    QTableWidgetItem, QComboBox, QTableWidget, QMessageBox
from PyQt5.uic import loadUi

from api.bilibili import Bilibili
from components.table import DetailedTableQWidget

class DetailWindow(QWidget):
    addSignal = pyqtSignal(dict)
    parseSignal = pyqtSignal(dict)
    def __init__(self,home):
        super().__init__()
        self.home = home
        loadUi("./view/ui/detail.ui", self)


        layout = QHBoxLayout()
        self.tableWidget = DetailedTableQWidget()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tableWidget)
        self.widget.setLayout(layout)

        self.addSignal.connect(self.addProcessHandle)

        # 复选框
        self.checkBox.stateChanged.connect(self.checkBoxChangeEventHandle)

        # 解析视频信号
        self.parseSignal.connect(self.parseVideoCodesHandle)
        # 解析视频
        self.pushButton.clicked.connect(self.parseVideoEventHandle)
        # 解析信息
        self.parseInfo = []
        # 视频信息
        self.videoInfo = {}
        #  视频正在解析
        self.videoParsing = False
        # 下载视频按钮
        self.pushButton_2.clicked.connect(self.downloadVideoEventHandle)


    def downloadVideoEventHandle(self):
        if self.videoParsing is None:
            QMessageBox.warning(self, "提醒", "尚未检索视频", QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.Yes)
            return

        if self.videoParsing:
            QMessageBox.warning(self, "提醒", "正在检索视频", QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.Yes)
            return

        if not self.checkBox.isChecked():
            index = self.tableWidget.currentIndex().row()
            if index == -1:
                print("未选中任何行")
                return

            box =  QMessageBox.question(self,'提示',"是否确认下载< {0} >".format(self.tableWidget.item(index, 1).text()),QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if box == QMessageBox.Yes:


                item = {}
                item["cid"] = self.videoInfo["pages"][index]["cid"]
                item["audio_quality"] = {v: k for k, v in Bilibili.audio_quality.items()}[
                    self.tableWidget.cellWidget(index, 3).currentText()]
                item["video_quality"] = {v: k for k, v in Bilibili.video_quality.items()}[
                    self.tableWidget.cellWidget(index, 4).currentText()]
                item["video_codecs"] = self.tableWidget.cellWidget(index, 5).currentText()
                item["title"] = self.tableWidget.item(index, 1).text()

                

        else:
            box = QMessageBox.question(self, '提示',
                                       "已选中全部视频，即将开始下载",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if box == QMessageBox.Yes:
                downloadLists = []
                for index in range(len(self.videoInfo["pages"])):
                    item = {}
                    item["cid"] = self.videoInfo["pages"][index]["cid"]
                    item["audio_quality"] = {v: k for k, v in Bilibili.audio_quality.items()}[
                        self.tableWidget.cellWidget(index, 3).currentText()]
                    item["video_quality"] = {v: k for k, v in Bilibili.video_quality.items()}[
                        self.tableWidget.cellWidget(index, 4).currentText()]
                    item["video_codecs"] = self.tableWidget.cellWidget(index, 5).currentText()
                    item["title"] = self.tableWidget.item(index, 1).text()
                    downloadLists.append(item)

                print(downloadLists)


    def parseVideoCodesHandle(self,data):
        index = data["index"]
        value = data["data"]
        audio_quality = value["audio_quality"]
        video_codes = value["video_quality_codes"]
        video_quality = value["video_quality"]

        self.parseInfo.append({
            "audio_quality":audio_quality,
            "video_quality":video_quality,
            "video_codes":video_codes
        })

        for a in audio_quality:
            self.tableWidget.cellWidget(index, 3).addItem(Bilibili.audio_quality[str(a)])

        for b in video_quality:
            self.tableWidget.cellWidget(index, 4).addItem(Bilibili.video_quality[str(b)])

        # for code in codes:
        codecs = video_codes[int(video_quality[0])]
        for c in codecs:
            self.tableWidget.cellWidget(index, 5).addItem(str(c))


    def insertTableItem(self,data):
        self.tableWidget.setRowCount(len(data))
        for i, item in enumerate(data):
            index = QTableWidgetItem(str(i))
            title = QTableWidgetItem(item["part"])
            if int(item["duration"]) < 60:
                duration = QTableWidgetItem(strftime("%S", gmtime(int(item["duration"]))))
            elif int(item["duration"]) < 60*60:
                duration = QTableWidgetItem(strftime("%M:%S", gmtime(int(item["duration"]))))
            else:
                duration = QTableWidgetItem(strftime("%H:%M:%S", gmtime(int(item["duration"]))))

            self.tableWidget.setItem(i, 0, index)
            self.tableWidget.setItem(i, 1, title)
            self.tableWidget.setItem(i, 2, duration)

            audio_combobox = QComboBox()
            self.tableWidget.setCellWidget(i, 3, audio_combobox)
            video_combobox = QComboBox()
            video_combobox.currentIndexChanged.connect(
                self.currentIndexChangedEventHandle)
            self.tableWidget.setCellWidget(i, 4, video_combobox)

            code_combobox = QComboBox()
            self.tableWidget.setCellWidget(i, 5, code_combobox)


    def currentIndexChangedEventHandle(self,index):
        if self.videoParsing:
            return

        if self.tableWidget.currentIndex().row() == -1:
            return

        # self.video_data_quality
        code_combobox = self.tableWidget.cellWidget(self.tableWidget.currentIndex().row(),5)
        code_combobox.clear()
        # self.video_data_quality
        video_quality = {v:k for k,v in Bilibili.video_quality.items()}[self.tableWidget.cellWidget(self.tableWidget.currentIndex().row(), 4).currentText()]

        # codecs = self.video_data_quality[int(self.tableWidget.currentIndex().row())]["video_codes"][str(video_quality)]
        codecs = self.parseInfo[int(self.tableWidget.currentIndex().row())]["video_codes"][int(video_quality)]
        for c in codecs:
            self.tableWidget.cellWidget(int(self.tableWidget.currentIndex().row()), 5).addItem(str(c))

        # code_combobox.addItem(BilibiliVideoDownloader.audio_quality[str(a)])
        # self.tableWidget.cellWidget(index, 3).addItem(BilibiliVideoDownloader.video_quality[str(b)])


        print(self.tableWidget.currentIndex().row())
        print(index)


    def addProcessHandle(self,data):
        self.videoInfo = data
        self.label_9.setPixmap(data["pic"])
        self.label_9.setMaximumSize(80, 80)
        self.label_9.setScaledContents(True)

        self.label_10.setText("{0}".format(data["title"]))
        self.label_11.setText("{0}".format(data["desc"]))
        # 投币
        self.label_3.setText("投币:{0}".format(data["coin"]))
        self.label_5.setText("点赞:{0}".format(data["like"]))
        self.label_4.setText("分享:{0}".format(data["share"]))
        self.label_6.setText("收藏:{0}".format(data["favorite"]))


        self.label_8.setPixmap(data["owner_face"])
        self.label_8.setMaximumSize(80, 80)
        self.label_8.setScaledContents(True)
        self.label_7.setText("{0}".format(data["owner_name"]))

        if data["videos"] == 1:
            data["pages"][0]["part"] = data["title"]

        self.insertTableItem(data["pages"])


        self.home.switchWindow[1] = True
        self.home.detailButton.click()


    def checkBoxChangeEventHandle(self):
        if self.checkBox.isChecked():
            self.tableWidget.selectAll()
        else:
            self.tableWidget.clearSelection()

    def parseVideoEventHandle(self):
        t =  threading.Thread(target=self.parseVideoProcess)
        t.start()


    def parseVideoProcess(self):
        pages = self.videoInfo["pages"]

        self.videoParsing = True
        for i,_ in enumerate(pages):
            item = self.home.downloader.signalVideoParse(i)
            result = {}
            result["index"] = i
            result["data"] = item
            self.parseSignal.emit(result)

        self.videoParsing = False
