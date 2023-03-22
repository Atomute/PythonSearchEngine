import sys
import sqlite3
import timeit
from PyQt5.QtWidgets import QListWidget,QTabWidget,QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QTableWidget, QTableWidgetItem, QProgressBar
from PyQt5.QtGui import QFont, QDesktopServices
from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal
from PyQt5 import QtCore, QtWidgets
from time import sleep
from urllib.parse import urlparse
sys.path.insert(1,"./")
from indexer.index_Country import Getcountry
from spider.spider import spider
from indexer.index_inverter import InvertedIndex
from indexer.index_Country import Getcountry
from database.DB_sqlite3 import DB
from search.searcher import searcher

database_name = "testt.sqlite3"

class deleteworker(QThread):
    pass

class tfidfWorker(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        print("TFIDF Thread Working")
        self.is_pause = False
        self.indexer=InvertedIndex()
        for progression in self.indexer.calculate_tfidf():
            while self.is_pause:
                sleep(0)
            self.progress.emit(int(progression))

        self.finished.emit()

    def start_stop(self):
        self.is_pause = not self.is_pause

# class spiderworker(QThread):
#     finished = pyqtSignal()
#     progress = pyqtSignal(str)
#     uporin = pyqtSignal(str)

#     def __init__(self, url,depth,insert,parent=None):
#         super().__init__(parent)
#         self.url = url
#         self.max_depth = depth
#         self.is_update = insert

#     def run(self):
#         self.spider2 = spider()
#         self.db = DB("testt.sqlite3")
#         if self.url in self.db.get_column("websites","URL"):
#             self.uporin.emit("Update")
#             self.spider2.updateone(self.url)
#         else:
#             self.uporin.emit("insert")
#             for i in self.spider2.new_run(self.url,self.max_depth,0,self.is_update):
#                 self.db.cursor.execute("SELECT URL FROM websites ORDER BY websiteID DESC LIMIT 1")
#                 status = self.db.cursor.fetchone()[0]
#                 self.progress.emit(status)

#         self.finished.emit()
  
class spiderworker(QThread):
    finished = pyqtSignal()
    uporin = pyqtSignal(str)
    progress = pyqtSignal(str)
    Upload_status = pyqtSignal(str)
    updatepbar = pyqtSignal(int)

    def __init__(self,urls,*depth,parent=None):
        super().__init__(parent)
        self.urls = urls
        self.is_pause = False
        self.is_kill = False
        if not depth: depth = [None]
        self.depth = depth[0]

    def run(self):
        self.is_kill = False
        self.spider = spider()
        self.get_country = Getcountry()
        self.indexer = InvertedIndex()
        self.db = DB(database_name)
        self.spider.db = self.db
    
        existURLs = self.db.get_column("websites","URL")

        urls = self.urls.split(",")
        count = 0
        while urls:
            url = urls.pop(0)
            
            while self.is_pause:
                sleep(0)

            if url in existURLs: 
                # this will update that link
                self.uporin.emit("Update")
                self.spider.updateone(url)
                self.progress.emit(url)
            else:
                # this will insert that link
                self.uporin.emit("insert")

                for cururl in self.spider.run(url,self.depth):
                    self.progress.emit("Crawled "+cururl)
                    self.indexer.indexOneWebsite(cururl)
                    self.get_country.find_c_websites_one(cururl)

                    self.progress.emit("Indexed "+cururl)
                    if len(urls) != 0:
                        self.updatepbar.emit(int(count*100/len(urls)))

            if self.is_kill:
                if self.spider.urltovisit != []:
                    urls = self.spider.urltovisit
                self.spider.push_log(urls,self.spider.withDepth)
                break

            self.spider.counter()

        self.finished.emit()

    def start_stop(self):
        self.spider.start_stop()
        self.is_pause = not self.is_pause
        if self.spider.is_pause:
            self.Upload_status.emit("Pause")
        else:
            self.Upload_status.emit("Continue")

    def kill(self):
        self.spider.kill()
        self.is_kill = True

class SearchEngine(QMainWindow):
    def __init__(self):
        super().__init__()
        # Connect to database
        self.db = DB(database_name)
        self.index=InvertedIndex()
        self.country = Getcountry()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Search Engine')
        self.setGeometry(100,100,1000,700)
#---------------------------------
# Create a Country tab
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

        # Create the search tab and add it to the tab widget

#---------------------------------  
# Create the uplink tab 
        self.uplinkTab = QWidget(self)
        self.tabWidget.addTab(self.uplinkTab, 'Uplink')

        # ProgressBar
        self.pbar = QProgressBar(self.uplinkTab)

        # Uplink input text
        self.uplinkLabel = QLabel('Enter a URL:', self.uplinkTab)
        self.uplinkLabel.setFont(QFont('Arial', 14))
        self.uplinkBox = QLineEdit(self.uplinkTab)
        self.uplinkBox.setFont(QFont('Arial', 14))
        self.uplinkBox.returnPressed.connect(self.uploadlink)
        # submit button
        self.uplinkButton = QPushButton('Submit', self.uplinkTab)
        self.uplinkButton.setFont(QFont('Arial', 14))
        self.uplinkButton.clicked.connect(self.uploadlink)

        #Delete button
        self.deleteButton = QPushButton('Delete', self.uplinkTab)
        self.deleteButton.setFont(QFont('Arial', 14))
        self.deleteButton.clicked.connect(self.delete_btn)
        
        # List widget
        self.urlList = QListWidget(self.uplinkTab)

        self.urlList2 = QListWidget(self.uplinkTab)
        self.urlList2.itemClicked.connect(self.logging)
        
        #kill button
        self.killbtn = QPushButton('Kill', self.uplinkTab)
        self.killbtn.setEnabled(False)
        self.killbtn.setFont(QFont('Arial', 14))
        self.killbtn.clicked.connect(self.kill_btn)

        #Pause button 
        self.pausebtn = QPushButton('Start/Stop', self.uplinkTab)
        self.pausebtn.setEnabled(False)
        self.pausebtn.setFont(QFont('Arial', 14))
        self.pausebtn.clicked.connect(self.start_stop_btn)

        #Update_all button 
        self.Update_all = QPushButton('Update all website',self.uplinkTab)
        self.Update_all.setFont(QFont('Arial', 14))
        self.Update_all.clicked.connect(self.updateAll_btn)

        #Update_all button 
        self.caltfidf = QPushButton('Calculate TFIDF',self.uplinkTab)
        self.caltfidf.setFont(QFont('Arial', 14))
        self.caltfidf.clicked.connect(self.TFIDF)

        self.deptLabel = QLabel('Dept:', self.uplinkTab)
        self.deptLabel.setFont(QFont('Arial', 10))
        self.deptBox = QLineEdit(self.uplinkTab)
        self.deptBox.setFont(QFont('Arial', 14))

        # Add widgets to a grid layout
        grid = QGridLayout(self.uplinkTab)
        grid.addWidget(self.uplinkLabel, 0, 0)
        grid.addWidget(self.uplinkBox, 0, 1)
        grid.addWidget(self.uplinkButton, 0, 4)
        grid.addWidget(self.deptLabel, 0, 2,)
        grid.addWidget(self.deptBox,0,3)
        grid.addWidget(self.deleteButton, 0, 5)
        grid.addWidget(self.pausebtn, 5, 5)
        grid.addWidget(self.Update_all,6,5)
        grid.addWidget(self.urlList, 2, 0, 8, 3)
        grid.addWidget(self.killbtn, 4, 5)
        grid.addWidget(self.caltfidf, 7, 5)
        grid.addWidget(self.urlList2, 2,3,1,3)
        grid.addWidget(self.pbar, 3,4,1,2)

        self.updateLOG()

        if None in self.db.get_column("website_inverted_index","tfidf"):
            self.searchButton.setEnabled(False)

    def updateLOG(self):
        # add item in logging list
        items = []
        for index in range(self.urlList2.count()):
            items.append(self.urlList2.item(index).text())
        unfinish = self.db.get_column("log","root")
        if unfinish != []:
            for url in unfinish:
                if url in items:
                    continue
                else:
                    self.urlList2.addItem(url)

    def search(self):
        start = timeit.default_timer()
        searchTable = []
        query = self.searchBox.text()
        if query.strip() == '': return
        self.Mysearcher = searcher()
        results = self.Mysearcher.search(query)

        if not results:
            self.updateResultTable([])
            return

        for id in results[0]:
            webID = id
            score = results[0][id]
            self.db.cursor.execute("SELECT title, URL FROM websites WHERE websiteID={}".format(webID))
            title, url = self.db.cursor.fetchone()
            searchTable.append((title,url,score))

        stop = timeit.default_timer()
        print(stop-start)

        self.updateResultTable(searchTable)

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
        conn = sqlite3.connect(database_name)
        c = conn.cursor()

        # Get the content column for the specified website name
        c.execute("SELECT content FROM websites WHERE URL=?", (website_name,))
        content = c.fetchone()[0]

        # Close the database connection
        conn.close()
        return content

    def logging(self,url):
        self.urlList.addItem("Continue scraping "+url.text())
        urls = self.db.get_column_specific("log","remaining",url.text(),"root")
        urls = "".join(urls)
        withDepth = self.db.get_column_specific("log","withDepth",url.text(),"root")
        if withDepth == "True":
            self.worker = spiderworker(urls)
        else:
            self.worker = spiderworker(urls,0)

        self.worker.progress.connect(self.reportProgress)
        self.worker.Upload_status.connect(self.pauseORcontinue)
        self.worker.finished.connect(self.thread_finish)

        self.worker.start()
        self.killbtn.setEnabled(True)  # enable the kill button
        self.pausebtn.setEnabled(True)  # enable the pause button
        self.uplinkButton.setEnabled(False)
        self.deleteButton.setEnabled(False)

    def uploadlink(self):
        url = self.uplinkBox.text()
        if url.endswith("/"):
            url = url[:-1]
        depth = self.deptBox.text()
        if depth != '':
            depth = int(depth)
        else:
            depth = None

        if urlparse(url).scheme and urlparse(url).netloc:
            # The input is a valid URL
            self.worker = spiderworker(url,depth)
            self.worker.progress.connect(self.reportProgress)
            self.worker.uporin.connect(self.uporintype)
            self.worker.Upload_status.connect(self.pauseORcontinue)
            self.worker.updatepbar.connect(self.progressBar)
            self.worker.finished.connect(self.thread_finish)

            self.worker.start()

            self.killbtn.setEnabled(True)  # enable the kill button
            self.pausebtn.setEnabled(True)  # enable the pause button
            self.uplinkButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
            self.Update_all.setEnabled(False)
            self.caltfidf.setEnabled(False)
            self.urlList2.setEnabled(False)
        else:
            # The input is not a valid URL
            self.urlList.addItem("Invalid URL")
            
    def TFIDF(self):
        self.urlList.addItem("Calculating TF-IDF")
        self.tfidfworker = tfidfWorker()
        self.tfidfworker.progress.connect(self.progressBar)
        self.tfidfworker.finished.connect(self.tfidf_finish)

        self.tfidfworker.start()

        self.uplinkButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        self.Update_all.setEnabled(False)
        self.caltfidf.setEnabled(False)
        self.urlList2.setEnabled(False)

    def tfidf_finish(self):
        self.searchButton.setEnabled(True)

        self.urlList.addItem("Done")
        self.uplinkButton.setEnabled(True)
        self.deleteButton.setEnabled(True)
        self.Update_all.setEnabled(True)
        self.caltfidf.setEnabled(True)
        self.urlList2.setEnabled(True)

    def updateAll_btn(self):
        db = DB(database_name)
        spiderman = spider()
        spiderman.db = db
        urls = db.get_column("websites","URL")
        urls = str(urls).replace("[","").replace("]","").replace("'","").replace(" ","")
        if urls == "":
            self.urlList.addItem("No websites In this database yet")
            return
        self.urlList.addItem("Updating all the link")
        
        db.dump_table()
        spiderman.counter()
        db.close_conn()

        self.worker = spiderworker(urls,0)

        self.worker.progress.connect(self.reportProgress)
        self.worker.Upload_status.connect(self.pauseORcontinue)
        self.worker.finished.connect(self.thread_finish)
        self.worker.updatepbar.connect(self.progressBar)
        self.worker.start()

        self.killbtn.setEnabled(True)  # enable the kill button
        self.pausebtn.setEnabled(True)  # enable the pause button
        self.uplinkButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        self.Update_all.setEnabled(False)
        self.caltfidf.setEnabled(False)
        self.urlList2.setEnabled(False)

    def delete_btn(self):
        urls = self.uplinkBox.text()
        sp = spider()
        for url in urls.split(","):
            sp.removeone(url)
            self.urlList.addItem("Removed "+url)
        sp.db.close_conn()

    def kill_btn(self):
        self.worker.kill()
        self.updateLOG()
        self.urlList.clear()
        self.uplinkBox.clear()

        self.killbtn.setEnabled(False)
        self.pausebtn.setEnabled(False)
        self.searchButton.setEnabled(False)
        self.uplinkButton.setEnabled(True)
        self.deleteButton.setEnabled(True)
        self.urlList2.setEnabled(True)
        self.caltfidf.setEnabled(True)
        self.Update_all.setEnabled(True)

    def start_stop_btn(self):
        self.worker.start_stop()  
    
    def start_stop_tfidf(self):
        self.tfidfworker.start_stop()

    def progressBar(self,progress):
        progress = int(progress)
        self.pbar.setValue(progress)

    def pauseORcontinue(self,status):
        self.urlList.addItem(status)  

    def uporintype(self,uporin):
        self.urlList.addItem(uporin)

    def reportProgress(self,result):
        self.urlList.addItem(result)

    def thread_finish(self):
        self.urlList.addItem("Done")
        self.uplinkButton.setEnabled(True)
        self.deleteButton.setEnabled(True)
        self.urlList2.setEnabled(True)
        self.Update_all.setEnabled(True)
        self.caltfidf.setEnabled(True)

#----------------------------
#Sub widget
class WebsiteDetailsWindow(QtWidgets.QWidget):
    def __init__(self, title, url, content):
        super().__init__()

        self.setWindowTitle(title)
        self.setGeometry(100, 100, 705, 503)

        # Create the tab widget
        self.tabWidget = QtWidgets.QTabWidget(self)

        # Create the content tab
        self.content_tab = QtWidgets.QWidget(self)
        self.content_tab_layout = QtWidgets.QVBoxLayout(self.content_tab)
        self.content_tab.setLayout(self.content_tab_layout)
        self.tabWidget.addTab(self.content_tab, 'Content')

        # title label
        self.titleLabel = QtWidgets.QLabel(self.content_tab)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setText("Title: {}".format(title))
        self.content_tab_layout.addWidget(self.titleLabel)

        # URL label
        self.urlLabel = QtWidgets.QLabel(self.content_tab)
        self.urlLabel.setObjectName("urlLabel")
        self.urlLabel.setText("URL: {}".format(url))
        self.content_tab_layout.addWidget(self.urlLabel)

        # content text edit
        self.contentTextEdit = QtWidgets.QPlainTextEdit(self.content_tab)
        self.contentTextEdit.setObjectName("contentTextEdit")
        self.contentTextEdit.setPlainText(content)
        self.content_tab_layout.addWidget(self.contentTextEdit)

        # spatial tab
        self.spatial_tab = QtWidgets.QWidget(self)
        self.spatial_tab_layout = QtWidgets.QVBoxLayout(self.spatial_tab)
        self.spatial_tab.setLayout(self.spatial_tab_layout)
        self.tabWidget.addTab(self.spatial_tab, 'Spatial')

        #spatial 
        self.spatialLabel = QtWidgets.QLabel(self.spatial_tab)
        self.spatialLabel.setObjectName("spatialLabel")
        self.spatialLabel.setText("plot spatial here !.")
        self.spatial_tab_layout.addWidget(self.spatialLabel)

        # Set the layout for the main widget
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.tabWidget)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", self.title))
        self.pushButton.setText(_translate("Form", "Close"))
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    searchEngine = SearchEngine()
    searchEngine.show()
    sys.exit(app.exec_())