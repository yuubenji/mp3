import os
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox,QCheckBox,QWidgetItem,QListWidgetItem

from DownloadThread import DownloadThread
from MessageBox import MessageBox
from ui.ui_mainwindow import Ui_MainWindow
from BrowserThread import BrowserThread
from QueryThread import QueryThread


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # 設定btn連結
        # 設定按鈕為disable

        self.btnQuery.clicked.connect(self.btnQuery_click)
        self.btnDownload.clicked.connect(self.btnDownload_click)
        self.btnPath.clicked.connect(self.btnPath_click)
        self.path = 'c:\\tmp'  # 不可用'/'
        self.lblPath.setText(self.path)
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        self.btnQuery.setEnabled(False)
        self.btnDownload.setEnabled(False)
        self.btnPath.setEnabled(False)
        self.browserThread = BrowserThread(self.path)
        self.browserThread.callback.connect(self.browserThreadcallback)
        self.browserThread.start()


    def browserThreadcallback(self, browser):
        self.browser = browser
        self.btnDownload.setEnabled(True)
        self.btnQuery.setEnabled(True)

    def btnQuery_click(self):
        # MessageBox.show('查詢被按了', 'mp3', (QMessageBox.Ok, QMessageBox.Cancel))
        self.listWidget.clear()
        self.song = self.txtSong.text()
        if self.song == '':
            MessageBox.show('請輸入歌曲')
            return
        self.lblStatus.setText('搜尋中.....')
        self.btnQuery.setEnabled(True)
        self.btnDownload.setEnabled(True)
        self.queryThread = QueryThread(self.browser, self.song)
        self.queryThread.callback.connect(self.queryThreadCallback)
        self.queryThread.start()

    def queryThreadCallback(self, links):
        self.btnDownload.setEnabled(True)
        self.btnQuery.setEnabled(True)
        self.lblStatus.setText('')
        for key in links.keys():
            box = QCheckBox(links[key])
            item = QListWidgetItem()
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item,box)





    def btnDownload_click(self):
        # MessageBox.show('下載被按了', 'mp3', (QMessageBox.Ok, QMessageBox.Cancel))
        count = self.listWidget.count()
        boxs = [self.listWidget.itemWidget(self.listWidget.item(i))for i in range(count)]
        chks = []
        for box in boxs:
        
            if box.isChecked():
                chks.append(box.text())
                self.btnDownload.setEnabled(False)
                self.btnQuery.setEnabled(False)
                #for chk in chks:
                 #   print(chk.split(' url=')[0],chk.split(' url=')[1])
                self.downloadThread = DownloadThread(self.browser,chks)
                self.downloadThread.callback.connect(self.downloadThreadCallback)
                self.downloadThread.finished.connect(self.downloadFinished)
                self.downloadThread.start()

    def downloadThreadCallback(self, msg):
        self.lblStatus.setText(msg)

    def downloadFinished(self):
        self.btnDownload.setEnabled(True)
        self.btnPath.setEnabled(True)
        self.btnQuery.setEnabled(True)
        self.lblStatus.setText('下載完成')

    #
    def btnPath_click(self):
        #MessageBox.show('變更被按了', 'mp3', (QMessageBox.Ok, QMessageBox.Cancel))
        self.path = QFileDialog.getExistingDirectory()
        if self.path !='':
            self.path = sel.path.replace('/','\\')
            if not os.path.isdir(self.path):
                os.mkdir(self.path)
            self.btnQuery.setEnabled(False)
            self.btnDownload.setEnabled(False)
            self.lblPath.setText(self.path)
            self.browser.close()
            self.browserThread = BrowserThread(self.path)
            self.browserThread.callback.connect(self.browserThreadcallback)
            self.browserThread.start()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec()
