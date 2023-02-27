from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QTableWidget, QHBoxLayout, QAbstractItemView


class DetailedTableQWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        # 设置布局
        # layout = QHBoxLayout()
        # self.tableWidget = QTableWidget()
        # layout.addWidget(self.tableWidget)

        # # 设置列数
        # self.tableWidget.setColumnCount(6)
        # # 设置标题框
        # self.tableWidget.setHorizontalHeaderLabels(['序号', '名称', '时长','音质', '画质', '视频编码'])
        # self.tableWidget.horizontalHeader().setStyleSheet("color: rgb(0, 83, 128);border:1px solid rgb(210, 210, 210);")
        # self.tableWidget.setColumnWidth(1, 300)
        #
        # #隐藏序号
        # self.tableWidget.verticalHeader().hide()
        # # 设置水平铺满
        # self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # # 设置一行选中
        # self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # # self.tableWidget.setSelectionBehavior(QAbstractItemView.SingleSelection)
        # # 设置一行的事件
        # self.tableWidget.doubleClicked.connect(self.doubleClickEventHandle)
        # # 设置不可编辑触发
        # self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置列数
        self.setColumnCount(6)
        # 设置标题框
        self.setHorizontalHeaderLabels(['序号', '名称', '时长','音质', '画质', '视频编码'])
        self.horizontalHeader().setStyleSheet("color: rgb(0, 83, 128);border:1px solid rgb(210, 210, 210);")
        self.setColumnWidth(1, 300)

        #隐藏序号
        self.verticalHeader().hide()
        # 设置水平铺满
        self.horizontalHeader().setStretchLastSection(True)
        # 设置一行选中
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.tableWidget.setSelectionBehavior(QAbstractItemView.SingleSelection)
        # 设置一行的事件
        self.doubleClicked.connect(self.doubleClickEventHandle)
        # 设置不可编辑触发
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # self.setLayout(layout)



    def doubleClickEventHandle(self,index):
        # print(self.tableWidget)
        print(self.item(index.row(), 0).text())
        print(self.item(index.row(), 1).text())
        print(self.item(index.row(), 2).text())
        print(self.cellWidget(index.row(), 3).currentText())
        print(self.cellWidget(index.row(),4).currentText())
        print(self.cellWidget(index.row(), 5).currentText())