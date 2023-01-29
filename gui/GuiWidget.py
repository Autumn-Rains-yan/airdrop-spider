import asyncio
import json
import os.path
import time
from threading import Thread
from time import sleep

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QTableWidget, QCheckBox, QHBoxLayout, QTableWidgetItem,
                               QAbstractItemView, QPushButton, QMessageBox)

from hubstudio.Api import Api


from hubstudio.BrowserSettings import BrowserSettings

from script.MetaMaskScript import MetaMaskScript
from settings.ProjectSettings import BASE_DIR


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.ck = {}
        self.api = Api()
        self.threadNames = {}
        self.allCheckType = False

        # button功能
        self.btn_1 = QPushButton("全选/反选", self)
        self.btn_1.setGeometry(10, 10, 80, 30)
        self.btn_1.clicked.connect(lambda: self.checkedAllData(not self.allCheckType))
        self.btn_4 = QPushButton("删除环境", self)
        self.btn_4.setGeometry(100, 10, 80, 30)
        self.btn_4.clicked.connect(self.deleteEnv)
        self.btn_5 = QPushButton("小狐狸绑定", self)
        self.btn_5.setGeometry(190, 10, 80, 30)
        self.btn_5.clicked.connect(self.bandEnv)
        self.btn_3 = QPushButton("启动", self)
        self.btn_3.setGeometry(700, 10, 80, 30)
        self.btn_3.clicked.connect(self.start)

        self.table = QTableWidget(self)
        self.table.setGeometry(10, 50, 800, 800)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(6)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setStretchLastSection(True)
        self.table.setHorizontalHeaderLabels(
            ['选择', '环境名称', '代理类型', '上次使用ip', '上次使用地址', '最后开启时间', '']
        )

        self.initEnv()

    def add_line(self, index, containerName, proxyTypeName, lastUsedIp, location, allOpenTime):
        row = self.table.rowCount()
        self.table.setRowCount(row + 1)
        # 生成居中的checkbox
        self.ck[index] = QCheckBox()
        h = QHBoxLayout()
        h.setAlignment(Qt.AlignCenter)
        h.addWidget(self.ck[index])
        w = QWidget()
        w.setLayout(h)
        self.ck[index].clicked.connect(lambda: self.checkboxChecked(index))
        # ---
        self.table.setCellWidget(row, 0, w)
        self.table.setItem(row, 1, QTableWidgetItem(containerName))
        self.table.setItem(row, 2, QTableWidgetItem(proxyTypeName))
        self.table.setItem(row, 3, QTableWidgetItem(lastUsedIp))
        self.table.setItem(row, 4, QTableWidgetItem(location))
        self.table.setItem(row, 5, QTableWidgetItem(allOpenTime))

    def checkedAllData(self, checked):
        self.allCheckType = checked
        for index in range(len(self.envList)):
            self.envList[index]['checked'] = checked
            self.ck[index].setChecked(checked)

    def checkboxChecked(self, index):
        self.envList[index]['checked'] = self.ck[index].isChecked()

    # 初始化环境
    def initEnv(self):
        # 初始化数据
        self.envList = self.api.getEnvList()['list']
        # 比较数据和本地数据进行替换
        for index in range(len(self.envList)):
            self.envList[index]['checked'] = False
            self.add_line(index,
                          self.envList[index]['containerName'],
                          self.envList[index]['proxyTypeName'],
                          self.envList[index]['lastUsedIp'] if 'lastUsedIp' in self.envList[index] else '',
                          self.envList[index]['lastCountry'] if 'lastCountry' in self.envList[index] else '' + '  ' + self.envList[index]['lastRegion'] if 'lastRegion' in self.envList[index] else '',
                          self.envList[index]['allOpenTime'] if 'allOpenTime' in self.envList[index] else '')

    # 删除环境
    def deleteEnv(self):
        a = QMessageBox.question(self, '提示', '你确定要删除环境吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if a == QMessageBox.Yes:
            # 由于接口最多同时删除100个环境，环境数量超过50个时执行一次删除
            deleteCodeArr = []
            hasCheck = False
            for index in range(len(self.envList)):
                if self.envList[index]['checked']:
                    hasCheck = True
                    deleteCodeArr.append(self.envList[index]['containerCode'])
                    if len(deleteCodeArr) >= 50:
                        self.api.deleteEnv(deleteCodeArr)
                        deleteCodeArr = []
            if len(deleteCodeArr) > 0:
                self.api.deleteEnv(deleteCodeArr)
            if not hasCheck:
                QMessageBox.about(self, '提示', '没有选中任何账户')
                print('脚本终止')
                return

            QMessageBox.about(self, '提示', '删除环境完毕')
            self.table.setRowCount(0)
            self.initEnv()

    # 环境绑定
    def bandEnv(self):
        print('开始执行脚本')
        file = open(BASE_DIR + '/account.txt', 'r')
        accountList = file.readlines()
        # 打开环境
        hasCheck = False
        for index in range(len(self.envList)):
            if self.envList[index]['checked']:
                hasCheck = True
                self.threadNames[self.envList[index]['containerCode']] =\
                    Thread(target=self.bandEnvScript, args=(self.envList[index], index, accountList[index].split(';')[0]))
                self.threadNames[self.envList[index]['containerCode']].start()
        if not hasCheck:
            QMessageBox.about(self, '提示', '没有选中任何账户')
            print('脚本终止')
            self.btn_3.setDisabled(False)

    # 环境绑定线程
    def bandEnvScript(self, env, index, mnemo):
        sleep(40 * index)
        res = self.api.openEnv(containerCode=env['containerCode'])
        browser = BrowserSettings.get_browser(res['debuggingPort'])
        # 执行脚本
        MetaMaskScript.initMetaMask(browser, mnemo, index)
        # 关闭环境
        self.api.closeEnv(containerCode=env['containerCode'])
        print(f"第{str(index)}执行完毕")

    def start(self):
        QMessageBox.about(self, '提示', '没有可用脚本')


