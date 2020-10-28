
from PyQt5.QtCore import pyqtSignal, QThread
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DownloadThread(QThread):
    callback = pyqtSignal(object)
    finished = pyqtSignal()
    def __init__(self,browser,chks):
        super().__init__(None)
        self.browser = browser
        self.chks = chks
    #def run(self):
    #    pass
    def run(self):

        for chk in self.chks:
            title = chk.split(' url=')[0]
            url = chk.split(' url=')[1].replace('youtube','youtubeto')
            self.callback.emit(f'正在下載{title}....')
            self.browser.get(url)
        self.finished.emit()
        try:
            self.browser.switch_to.frame('IframeChooseDefault')
            try:
                WebDriverWait(self.browser,3,0.1).until(EC.presence_of_element_located(By.ID,'MP3Format'))
            except:
                pass
            btn = self.browser.find_element_by_id('MP3Format')
            btn.click()
        except:
            pass
