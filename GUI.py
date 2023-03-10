import sys
import sqlite3
from PyQt5.QtWidgets import QListWidget,QTabWidget,QMainWindow,QMessageBox, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont, QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QUrl, QObject, QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from time import sleep

sys.path.insert(1,"./")
from indexer.index_cleaner import Cleaning
from spider.spider import spider
from runner import Runner
from indexer.index_inverter import InvertedIndex
from indexer.index_Country import Getcountry
from database.DB_sqlite3 import DB

class spiderworker(QThread):
    finished = pyqtSignal()
    uporin = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self,urls,parent=None):
        super().__init__(parent)
        self.urls = urls
        self.is_pause = False
        self.is_kill = False

    def run(self):
        self.spider = spider()
        self.db = DB("testt.sqlite3")
        self.spider.db = self.db
    
        existURLs = self.db.get_column("websites","URL")

        for url in self.urls.split(","):
            while self.is_pause:
                sleep(1)

            if self.is_kill:
                break

            if url in existURLs: 
                self.uporin.emit("Update")
                self.spider.updateone(url)
                self.progress.emit(url)
            else:
                self.uporin.emit("insert")
                for cururl in self.spider.run(url,1):
                    self.progress.emit(cururl)

        self.finished.emit()

    def pause(self):
        self.spider.pauserun()
        self.is_pause = True

    def kill(self):
        self.is_kill = True

class SearchEngine(QMainWindow):
    def __init__(self):
        super().__init__()
        # Connect to database
        self.conn = sqlite3.connect('testt.sqlite3')
        self.cursor = self.conn.cursor()
        self.spider = spider()
        self.index=InvertedIndex()
        self.country = Getcountry()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Search Engine')
        self.setGeometry(100,100,1000,700)

        # Create a QTabWidget and add it to the central widget
        self.tabWidget = QTabWidget(self)
        self.setCentralWidget(self.tabWidget)

        # Create the search tab and add it to the tab widget
        self.searchTab = QWidget(self)
        self.tabWidget.addTab(self.searchTab, 'Search')

        # Search bar
        self.searchLabel = QLabel('Search:', self.searchTab)
        self.searchLabel.setFont(QFont('Arial', 14))
        self.searchBox = QLineEdit(self.searchTab)
        self.searchBox.setFont(QFont('Arial', 14))
        self.searchBox.returnPressed.connect(self.search)

        # Search button
        self.searchButton = QPushButton('Search', self.searchTab)
        self.searchButton.setFont(QFont('Arial', 14))
        self.searchButton.clicked.connect(self.search)

        # Result count
        self.resultCountLabel = QLabel('Result found: 0', self.searchTab)
        self.resultCountLabel.setFont(QFont('Arial', 14))

        # Search results
        self.resultTable = QTableWidget(self.searchTab)
        self.resultTable.setColumnCount(3)
        self.resultTable.setHorizontalHeaderLabels(['Title', 'URL', 'Score'])
        self.resultTable.setColumnWidth(0, 333)
        self.resultTable.setColumnWidth(1, 333)
        self.resultTable.setColumnWidth(2, 333)
        self.resultTable.cellDoubleClicked.connect(self.openUrl)

        # Add widgets to a grid layout
        grid = QGridLayout(self.searchTab)
        grid.addWidget(self.searchLabel, 0, 0)
        grid.addWidget(self.searchBox, 0, 1)
        grid.addWidget(self.searchButton, 0, 2)
        grid.addWidget(self.resultCountLabel , 1, 0)
        grid.addWidget(self.resultTable, 2, 0, 1, 3)

        # Create the uplink tab and add it to the tab widget
        self.uplinkTab = QWidget(self)
        self.tabWidget.addTab(self.uplinkTab, 'Uplink')

        # Uplink input text
        self.uplinkLabel = QLabel('Enter a URL:', self.uplinkTab)
        self.uplinkLabel.setFont(QFont('Arial', 14))
        self.uplinkBox = QLineEdit(self.uplinkTab)
        self.uplinkBox.setFont(QFont('Arial', 14))

        # Uplink button
        self.uplinkButton = QPushButton('Submit', self.uplinkTab)
        self.uplinkButton.setFont(QFont('Arial', 14))
        self.uplinkButton.clicked.connect(self.uploadlink)

        # Delete button
        # self.deleteButton = QPushButton('Submit', self.uplinkTab)
        # self.uplinkButton.setFont(QFont('Arial', 14))
        # self.uplinkButton.clicked.connect(self.uploadlink)
        
        # List widget
        self.urlList = QListWidget(self.uplinkTab)
        
        self.pausebtn = QPushButton('pause', self.uplinkTab)
        self.pausebtn.setFont(QFont('Arial', 14))
        self.pausebtn.clicked.connect(self.pause_update)

        # Add widgets to a grid layout
        grid = QGridLayout(self.uplinkTab)
        grid.addWidget(self.uplinkLabel, 0, 0)
        grid.addWidget(self.uplinkBox, 0, 1)
        grid.addWidget(self.uplinkButton, 0, 2)
        grid.addWidget(self.urlList, 1, 0, 1, 3)
        grid.addWidget(self.pausebtn,4,0)

    def search(self):
        sentence = self.searchBox.text()
        words = Cleaning().process_text(sentence)
        index_ids = []
        for word in words:
            self.cursor.execute("SELECT index_id FROM keyword WHERE word=?", (word,))
            result = self.cursor.fetchone()
            if result is not None:
                index_ids.append(result[0])
        if len(index_ids) == 0:
            return []
        self.cursor.execute("SELECT websiteID, SUM(frequency) FROM website_inverted_index WHERE index_id IN ({}) GROUP BY websiteID ORDER BY SUM(frequency) DESC".format(",".join(str(i) for i in index_ids)))
        results = self.cursor.fetchall()
        websites = []
        for result in results:
            website_id = result[0]
            frequency_sum = result[1]
            self.cursor.execute("SELECT title, URL FROM websites WHERE websiteID=?", (website_id,))
            title, url = self.cursor.fetchone()
            websites.append((title, url, frequency_sum))
        self.updateResultTable(websites)

    def updateResultTable(self,websites):
        self.resultTable.setRowCount(len(websites))
        for i, website in enumerate(websites):
            title = website[0]
            url = website[1]
            frequency_sum = website[2]
            titleItem = QTableWidgetItem(title)
            titleItem.setFlags(Qt.ItemIsEnabled)
            urlItem = QTableWidgetItem(url)
            urlItem.setFlags(Qt.ItemIsEnabled)
            freqSumItem = QTableWidgetItem(str(frequency_sum))
            freqSumItem.setFlags(Qt.ItemIsEnabled)
            self.resultTable.setItem(i, 0, titleItem)
            self.resultTable.setItem(i, 1, urlItem)
            self.resultTable.setItem(i, 2, freqSumItem)
        
        # Update search result count label
        count = len(websites)
        self.resultCountLabel.setText(f'Result found: {count}')

    def openUrl(self, row, column):
        if column == 1:
            url = self.resultTable.item(row, column).text()
            QDesktopServices.openUrl(QUrl(url))
        elif column==0:
            title = self.resultTable.item(row, 0).text()
            url = self.resultTable.item(row, 1).text()
            self.resultWindow = WebsiteDetailsWindow(title, url , self.get_content(url))
            self.resultWindow.show()

    def get_content(self,website_name):
        conn = sqlite3.connect('testt.sqlite3')
        c = conn.cursor()

        # Get the content column for the specified website name
        c.execute("SELECT content FROM websites WHERE URL=?", (website_name,))
        content = c.fetchone()[0]

        # Close the database connection
        conn.close()
        return content
# -------------------------------------------------------------------------------------------------------------------
    def uploadlink(self):
        urls = self.uplinkBox.text()
        self.worker = spiderworker(urls)

        self.worker.progress.connect(self.reportProgress)
        self.worker.uporin.connect(self.uporintype)
        self.worker.finished.connect(self.thread_finish)

        self.worker.start()

    def uporintype(self,uporin):
        self.urlList.addItem(uporin)

    def reportProgress(self,result):
        # QMessageBox.information(self,"Result",result)
        self.urlList.addItem(result)

    def thread_finish(self):
        self.urlList.addItem("Done")

    def pause_update(self):
        self.urlList.addItem('Pasue.....')
        self.worker.pause()

class WebsiteDetailsWindow(QtWidgets.QWidget):
    def __init__(self, title, url, content):
        super().__init__()

        self.setWindowTitle(title)
        self.setGeometry(100, 100, 705, 503)

        # Create and position the title label
        self.titleLabel = QtWidgets.QLabel(self)
        self.titleLabel.setGeometry(QtCore.QRect(20, 10, 400, 20))
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setText("Title :"+title)

        # Create and position the URL label
        self.urlLabel = QtWidgets.QLabel(self)
        self.urlLabel.setGeometry(QtCore.QRect(20, 40, 400, 20))
        self.urlLabel.setObjectName("urlLabel")
        self.urlLabel.setText("URL :"+url)

         # Create and position the content text edit
        self.contentTextEdit = QtWidgets.QPlainTextEdit(self)
        self.contentTextEdit.setGeometry(QtCore.QRect(20, 60, 500, 420))
        self.contentTextEdit.setObjectName("contentTextEdit")
        self.contentTextEdit.setPlainText(content)

        
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(590, 460, 100, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Close")
        self.pushButton.clicked.connect(self.close)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", self.title))
        self.pushButton.setText(_translate("Form", "Close"))
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    searchEngine = SearchEngine()
    searchEngine.show()
    sys.exit(app.exec_())
