import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

try:
    font = open('keys/f').read()
except Exception as e:
    print(e)
    exit()

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.engine = QTabWidget()
        self.engine.setDocumentMode(True)
        self.engine.setTabsClosable(True)
        self.engine.setFont(QFont(font, 12))
        self.engine.tabCloseRequested.connect(self.closeTab)
        self.setCentralWidget(self.engine)

        self.newTab()
        self.menubar()
        self.toolbar()
        self.engine.currentChanged.connect(self.updateUrlBar)

    def newTab(self):
        self.tab = QWebEngineView()
        self.tab.setUrl(QUrl('https://www.google.com'))
        self.tab.page().profile().downloadRequested.connect(self.downloader)
        self.index = self.engine.addTab(self.tab, 'FastBrowse')
        self.engine.setCurrentIndex(self.index)

        self.tab.loadFinished.connect(self.identification)


    def toolbar(self):
        toolbar = QToolBar('FastBrowse Toolbar', self)

        newTab = QAction(QIcon('icons/new-tab.png'), 'New Tab', self)
        newTab.triggered.connect(self.newTab)
        toolbar.addAction(newTab)

        toolbar.addSeparator()

        back = QAction(QIcon('icons/back.png'), 'Back', self)
        back.triggered.connect(self.go_back)

        forward = QAction(QIcon('icons/forward.png'), 'Forward', self)
        forward.triggered.connect(self.go_forward)

        toolbar.addActions([back, forward])

        toolbar.addSeparator()

        self.url_bar = QLineEdit()
        self.url_bar.setFont(QFont(font, 12))
        self.url_bar.returnPressed.connect(self.load_web_page)
        toolbar.addWidget(self.url_bar)

        toolbar.addSeparator()

        reload = QAction(QIcon('icons/reload.png'), 'Reload', self)
        reload.triggered.connect(self.reload_page)

        home = QAction(QIcon('icons/home.png'), 'Home', self)
        home.triggered.connect(self.main_website)

        stop = QAction(QIcon('icons/stop.png'), 'Stop', self)
        stop.triggered.connect(self.stop_loading)

        toolbar.addActions([reload, home, stop])

        position = open('keys/toolbar_position').read().lower()

        try:
            if position == 'top':
                self.addToolBar(Qt.TopToolBarArea, toolbar)
            elif position == 'bottom':
                self.addToolBar(Qt.BottomToolBarArea, toolbar)
            elif position == 'left':
                self.addToolBar(Qt.LeftToolBarArea, toolbar)
            elif position == 'right':
                self.addToolBar(Qt.RightToolBarArea, toolbar)
            else:
                self.addToolBar(Qt.TopToolBarArea, toolbar)
        except Exception as e:
            print(e)
            exit()

    def identification(self):
        self.engine.setTabText(self.index, self.tab.page().title())
        self.url_bar.setText(self.tab.page().url().toString())

    def closeTab(self, i):
        self.engine.removeTab(i)

    def downloader(self, item: QWebEngineDownloadItem):
        messagebox = QMessageBox()
        messagebox.setWindowTitle('FastBrowse')
        messagebox.setText('Your Download was accepted by the servers.')
        messagebox.exec_()

        item.setDownloadDirectory('fast_browse-downloads/')
        item.setDownloadFileName(item.downloadFileName())
        item.accept()
        item.finished.connect(self.completed)

        self.download_name = item.downloadFileName()

        action = QAction(self.download_name, self)
        self.new_downloads.addAction(action)

    def menubar(self):
        menubar = QMenuBar()
        menubar.setFont(QFont(font, 12))

        self.access_downloads = str(os.listdir('fast_browse-downloads'))

        total_downloads = QMenu('Total Downloads', self)
        total_downloads.setFont(QFont(font, 12))

        downloads = QAction(self)
        downloads.setText(str(self.access_downloads))
        total_downloads.addAction(downloads)

        show_in_folder = QAction('Show In Folder', self)
        show_in_folder.triggered.connect(self.downloads)
        total_downloads.addAction(show_in_folder)

        menubar.addMenu(total_downloads)

        self.new_downloads = QMenu('Recent Downloads', self)
        self.new_downloads.setFont(QFont(font, 12))
        menubar.addMenu(self.new_downloads)

        menubar.addSeparator()

        self.setMenuBar(menubar)

    def downloads(self):
        try: os.startfile('fast_browse-downloads')
        except: pass

    def completed(self):
        messagebox = QMessageBox()
        messagebox.setWindowTitle('FastBrowse')
        messagebox.setText('Your Download was completed by the servers.')
        messagebox.exec_()
        os.startfile('fast_browse-downloads')

    def load_web_page(self):
        try:
            url = self.url_bar.text()

            if 'subtitleseeker.com' in url:
                self.engine.currentWidget().setHtml(open('keys/virus.html').read())
            elif 'financereports.co' in url:
                self.engine.currentWidget().setHtml(open('keys/virus.html').read())
            elif 'creativebookmark.com' in url:
                self.engine.currentWidget().setHtml(open('keys/virus.html').read())
            elif 'ffupdate.org' in url:
                self.engine.currentWidget().setHtml(open('keys/virus.html').read())
            elif 'vegweb.com' in url:
                self.engine.currentWidget().setHtml(open('keys/virus.html').read())
            elif 'delgets.com' in url:
                self.engine.currentWidget().setHtml(open('keys/virus.html').read())
            elif 'kvfan.net' in url:
                self.engine.currentWidget().setHtml(open('keys/virus.html').read())
            elif 'totalpad.com' in url:
                self.engine.currentWidget().setHtml(open('keys/virus.html').read())
            elif 'hgk.biz' in url:
                self.engine.currentWidget().setHtml(open('keys/virus.html').read())
            elif 'metro-ads.co.in' in url:
                self.engine.currentWidget().setHtml(open('keys/virus.html').read())
            elif 'salescript.info' in url:
                self.engine.currentWidget().setHtml(open('keys/virus.html').read())
            elif 'http://' in url:
                self.engine.currentWidget().setHtml(open('keys/old_website.html').read())
            elif 'https://' not in url:
                self.engine.currentWidget().setUrl(QUrl('https://'+url))
            elif 'https://' in url:
                self.engine.currentWidget().setUrl(QUrl(url))

            self.identification()

        except: pass

    def go_back(self):
        try: self.engine.currentWidget().back()
        except: pass

    def go_forward(self):
        try: self.engine.currentWidget().forward()
        except: pass

    def reload_page(self):
        try: self.engine.currentWidget().reload()
        except: pass

    def main_website(self):
        try: self.engine.currentWidget().setUrl(QUrl('https://www.google.com/'))
        except: pass

    def stop_loading(self):
        try: self.engine.currentWidget().stop()
        except: pass

    def change_to_top_toolbar_position(self):
        try: open('keys/toolbar_position', 'w').write('TOP')
        except Exception as e: print(e)

    def change_to_bottom_toolbar_position(self):
        try: open('keys/toolbar_position', 'w').write('BOTTOM')
        except: pass

    def change_to_left_toolbar_position(self):
        try: open('keys/toolbar_position', 'w').write('LEFT')
        except: pass

    def change_to_right_toolbar_position(self):
        try: open('keys/toolbar_position', 'w').write('RIGHT')
        except: pass

    def updateUrlBar(self):
        self.url_bar.setText(self.engine.currentWidget().url().toString())


app = QApplication(sys.argv)
app.setApplicationName('FastBrowse')
app.setApplicationVersion('1.0')
app.setWindowIcon(QIcon('icons/main.png'))
window = MainWindow()
window.setGeometry(100, 100, 1000, 600)
window.show()
sys.exit(app.exec_())
