''' Juan Hernandez
	CST205 Project 2
'''

from PyQt4 import QtGui, QtCore
#import ExtendedQLabel
import sys

class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)

        # main button
        self.addButton = QtGui.QPushButton('ADD NEW TRACK')
        self.stopButton = QtGui.QPushButton('STOP')
        self.stopButton.setMaximumSize(250,100)
        self.playButton = QtGui.QPushButton('PLAY')
        self.playButton.setMaximumSize(250,100)
        self.addButton.clicked.connect(self.addWidget)

        # scroll area widget contents - layout
        self.scrollLayout = QtGui.QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QtGui.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        # main layout
        self.mainLayout = QtGui.QVBoxLayout()
        
        # Creat Top Sub Layout
        self.topSubLayout = QtGui.QHBoxLayout()

        #Top Layout Buttons 
        self.topSubLayout.addWidget(self.stopButton)
        self.topSubLayout.addWidget(self.playButton)
        self.topSubLayout.addWidget(self.addButton)
        
        self.mainLayout.addLayout(self.topSubLayout)

        # add all main to the main vLayout
        #self.mainLayout.addWidget(self.topSubLayout)
        self.mainLayout.addWidget(self.scrollArea)

        # central widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)
        self.count = 0;
        
        self.setGeometry(100,100,1000,600)
        self.showMaximized()
		
    def addWidget(self):
		self.count += 1
		self.scrollLayout.addRow(Track(str(self.count)))
		
class Track(QtGui.QWidget):
	def __init__( self, name, parent=None):
		super(Track, self).__init__(parent)

		self.pushButton = QtGui.QPushButton("stuff")

		# self.pushButton2.clicked.connect(self.deleteLater)

		layout = QtGui.QHBoxLayout()

		leftPanel = QtGui.QVBoxLayout()

		nameLayout = QtGui.QHBoxLayout()

		self.closeButton = QtGui.QPushButton("X")
		self.closeButton.setMaximumSize(40,120)
		self.closeButton.setStyleSheet("background-color: #ffaaaa; border-radius:5;")
		self.closeButton.clicked.connect(self.deleteLater)
		self.trackName = QtGui.QPushButton(" Untitled Track "+name)
		#self.trackName = QtGui.QLabel(" Untitled Track "+name)
		self.trackName.setMaximumSize(160,100)
		self.trackName.setStyleSheet("background-color: #ffffff")
		self.trackName.clicked.connect(self.renameDialog)
		#self.trackName.mouseReleaseEvent(self.renameDialog)
		#self.trackName.mouseDoubleClickEvent(self.renameDialog)

		nameLayout.addWidget(self.closeButton)
		nameLayout.addWidget(self.trackName)

		self.recordButton = QtGui.QPushButton("Record")
		self.recordButton.setMaximumSize(200,100)

		self.playButton = QtGui.QPushButton("Play")
		self.playButton.setMaximumSize(200,100)
		self.stopButton = QtGui.QPushButton("Stop")
		self.stopButton.setMaximumSize(200,100)
		self.mixButton = QtGui.QPushButton("Mix")
		self.mixButton.setMaximumSize(200,100)


		leftPanel.addLayout(nameLayout)
		leftPanel.addWidget(self.recordButton)
		leftPanel.addWidget(self.playButton)
		leftPanel.addWidget(self.stopButton)
		leftPanel.addWidget(self.mixButton)


		layout.addLayout(leftPanel)

		layout.addWidget(self.pushButton)


		self.setLayout(layout)
	  
	def renameDialog(self):
		text, ok = QtGui.QInputDialog.getText(self, 'Rename', '')
		
		if ok:
			self.trackName.setText(str(text))
			self.setSelected(False)
			#self.trackName.setStyleSheet("background-color: #ffffff")




app = QtGui.QApplication(sys.argv)
myWidget = Main()
myWidget.show()
app.exec_()
