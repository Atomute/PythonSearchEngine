# you can copy paste and run this code for test
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
class window(QMainWindow):
	def __init__(self):
		super(window, self).__init__()
		listWidget = QListWidget()
		listWidget.resize(300,120)

		listWidget.addItem("Item 1")
		listWidget.addItem("Item 2")
		listWidget.addItem("Item 3")
		listWidget.addItem("Item 4")

		listWidget.itemClicked.connect(self.Clicked) # connect itemClicked to Clicked method

		self.setCentralWidget(listWidget)
        
	def Clicked(self,item):
		a = QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())

def main(): 
	app = QApplication(sys.argv)
	w = window()
	w.show()
	sys.exit(app.exec_())
if __name__ == '__main__':
	main()