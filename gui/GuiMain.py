import sys

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QMessageBox)

from gui.GuiWidget import Widget

from common.Wallet import EthGenerateWallet
from hubstudio.Api import Api


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("AirDrop")

        self.api = Api()
        # 禁止窗体调整大小
        self.setMinimumWidth(800)
        self.setMinimumHeight(900)
        self.setFixedSize(self.width(), self.height())

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("菜单")

        # Exit QAction
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)
        check_balance = QAction("检索eth(做着玩的)", self)
        check_balance.triggered.connect(self.checkBalance)
        # About
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.about_app)

        self.file_menu.addAction(about_action)
        self.file_menu.addAction(check_balance)
        self.file_menu.addAction(exit_action)

        self.tools = self.menu.addMenu("工具")
        create_env = QAction("批量新建环境(50个)", self)
        create_env.triggered.connect(lambda: self.createEnv(widget))
        create_wallet = QAction("批量创建小狐狸账户(50个)", self)
        create_wallet.triggered.connect(self.createWallet)
        clear_cache = QAction("清除hubstudio缓存", self)
        clear_cache.triggered.connect(self.clearCache)
        self.tools.addAction(create_env)
        self.tools.addAction(create_wallet)
        self.tools.addAction(clear_cache)

        self.setCentralWidget(widget)

    # 关闭触发事件
    def closeEvent(self, event):
        a = QMessageBox.question(self, '退出', '你确定要退出吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if a == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    @Slot()
    def exit_app(self):
        QApplication.quit()

    @Slot()
    def checkBalance(self):
        EthGenerateWallet.createAndGetBalance()

    @Slot()
    def about_app(self):
        QMessageBox.about(self, '关于', '\n\nversion: 2023.0.1701   '
                                      '\nwechat: autumn_rains2333   \n')

    @Slot()
    def createEnv(self, widget):
        self.api.createEnv()
        widget.initEnv()
        QMessageBox.about(self, '提示', '环境创建完成')

    @Slot()
    def createWallet(self):
        EthGenerateWallet.createMetaMastAccount()
        QMessageBox.about(self, '提示', '账户创建完成，请在应用根目录查看')

    @Slot()
    def clearCache(self):
        a = QMessageBox.question(self, '提示', '你确定要清空缓存吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if a == QMessageBox.Yes:
            self.api.clearEnvCache()
            QMessageBox.about(self, '提示', 'hubstudio缓存清除成功')

def initGui():
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    layout = QHBoxLayout()
    widget = Widget()
    widget.setLayout(layout)
    # QMainWindow using QWidget as central widget
    window = MainWindow(widget)
    window.show()
    # Execute application
    sys.exit(app.exec())
