from PyQt5.QtCore import pyqtSignal, QThread
from selenium import webdriver

class QueryThread(QThread):
    callback = pyqtSignal(object)
    def __init__(self,browser,song):
        super().__init__(None)
        self.browser = browser
        self.song = song

    def run(self):
        url = f"https://www.youtube.com/results?search_query={self.song}"
        self.browser.get(url)
        tags = self.browser.find_elements_by_tag_name('a')
        links = {}

        for tag in tags:
            href = tag.get_attribute('href')
            if "watch" in str(href):
                title = tag.get_attribute('title')
                if title == '':
                    try:
                        title = tag.find_elements_by_id('video-title').get_attribute('title')
                    except:
                        pass
                if title != '':
                    links[href]='{0} url={1}'.format(title,href)
        self.callback.emit(links)


    



