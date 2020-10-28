from PyQt5.QtCore import pyqtSignal, QThread
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


class BrowserThread(QThread):
    callback = pyqtSignal(object)

    def __init__(self, path):
        super().__init__(None)
        self.browser = None
        self.path = path

    def run(self):
        ops = Options()
        ops.add_argument('--headless')
        ops.add_argument('--disable-gpu')
        ops.add_experimental_option('excludeSwitches', ['enable-logging'])
        prefs = {'profile.default_content_settings_popups': 0, 'download.default_directory': self.path}
        ops.add_experimental_option('prefs', prefs)
        browser = webdriver.Chrome('Chromedriver.exe', options=ops)
        self.callback.emit(browser)
