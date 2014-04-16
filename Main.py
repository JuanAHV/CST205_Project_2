'''
 Juan Hernandez
 CST205 
 Project 3
 '''

from PyQt4 import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
#import ExtendedQLabel
import sys, os, shutil
from Track import *
from Engine import *

class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)

        # main button
        self.addButton = QtGui.QPushButton('ADD NEW TRACK')
        self.addButton.clicked.connect(self.addTrackWidget)
        self.stopButton = QtGui.QPushButton('STOP')
        self.stopButton.setMaximumSize(250,100)
        self.playButton = QtGui.QPushButton('PLAY')
        self.playButton.setMaximumSize(250,100)

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

        self.trackArray = {}

        # Dialog for creating project at start up
        self.projectPath = self.createProject()
   
		
    def addTrackWidget(self):
        self.index = self.count
        self.count += 1
        self.trackArray[self.index] = Track(str(self.count),str(self.projectPath))

        self.scrollLayout.addRow(self.trackArray[self.index])
		#self.scrollLayout.addRow(self.track)

    def createProject(self):
        projectPath, ok = QtGui.QInputDialog.getText(self, 'Create Project', "Project Name: ")
        if ok:
            projectPath = str(projectPath)

            self.createProjectDirs(projectPath)
            return projectPath
        else:
            QtGui.QMessageBox.question(self, 'Warning!',"Nothing will be saved unless you create a project.", QtGui.QMessageBox.Ok)
            self.createProjectDirs('temp')
            return 'temp'

    def createProjectDirs(self, dirName):

        if not os.path.exists(dirName):
            os.makedirs(dirName)
        if not os.path.exists(dirName+"/audio"):
            os.makedirs(dirName+"/audio")

    def playClicked(self):

        print "play clicked"
        self.playIndex = 0
        self.playArray = {} 

        for track in self.trackArray:
            if self.trackArray[track].getState() == 'active':
                print self.trackArray[track].getTrackName() + " is playing"
                self.playArray[self.playIndex] = Play(self.trackArray[track].getTrackName())
                self.playIndex+=1

        for track in self.playArray:
            self.playArray[track].start()

    def stopClicked(self):

        print "stop clicked"

        for track in self.playArray:
            self.playArray[track].terminate()

    def stop_playback(self):
        #subprocess.call(["killall","arecord"])  
        self.play.terminate()
        #self.show_wave_n_spec("test.wav")

    def closeEvent(self, event):
        #remove temp files
        if(self.projectPath == 'temp'):
            shutil.rmtree('temp')
        # let the window close
        event.accept() 
        

app = QtGui.QApplication(sys.argv)
myWidget = Main()
myWidget.show()
app.exec_()

