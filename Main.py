'''
Juan Hernandez
 CST205 
 Project 2
 '''

from PyQt4 import QtGui, QtCore
#import ExtendedQLabel
import sys
from Track import *
from Engine import *

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

        self.connect(self.playButton, QtCore.SIGNAL('clicked()'), self.playClicked)
        self.connect(self.stopButton, QtCore.SIGNAL('clicked()'), self.stopClicked)

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

        self.tracks = {}
   
		
    def addWidget(self):
		self.count += 1
		self.track = Track(str(self.count))

        #self.tracks[self.count: self.track]

		self.scrollLayout.addRow(self.track)
		#self.scrollLayout.addRow(Track(str(self.count)))

    def playClicked(self):
        #start playback thread
        self.merge = PlayAll(self.tracks)
        self.merge.start()
        #self.merge.terminate()
        self.play = Play("Untitled_Track_3")
        self.play.start()



    def stopClicked(self):
        #self.StopButton.setPixmap(QPixmap(self.STOP_BUTTON))
        print('Stop Button Clicked')
        # Kill arecord subprocess and terminate threads
        self.stop_playback()
        #self.record.terminate()
        self.play.terminate()
        # change playback button to original state

    def stop_playback(self):
        #subprocess.call(["killall","arecord"])  
        self.play.terminate()
        #self.show_wave_n_spec("test.wav")

app = QtGui.QApplication(sys.argv)
myWidget = Main()
myWidget.show()
app.exec_()
