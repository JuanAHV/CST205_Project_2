from PyQt4 import QtGui, QtCore
from pyo import *
#import ExtendedQLabel
import sys, os, shutil
from Track import *
from Engine import *

class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)

        # main buttons
        self.addButton = QtGui.QPushButton('ADD NEW TRACK')
        self.addButton.setStyleSheet("background-color: #333377; border-radius:3;height:30;color:#ffffff;")
        self.stopButton = QtGui.QPushButton('STOP')
        self.stopButton.setMaximumSize(200,160)
        self.stopButton.setStyleSheet("background-color: #555544; border-radius:3;color:#ffffff;")
        self.playButton = QtGui.QPushButton('PLAY')
        self.playButton.setMaximumSize(200,160)
        self.playButton.setStyleSheet("background-color: #445544; border-radius:3;color:#ffffff;")
        self.recordButton = QtGui.QPushButton('RECORD')
        self.recordButton.setMaximumSize(200,160)
        self.recordButton.setStyleSheet("background-color: #554444; border-radius:3;color:#ffffff;")

        # connect buttons to corresponding function
        self.addButton.clicked.connect(self.addTrackWidget)
        self.connect(self.recordButton, QtCore.SIGNAL('clicked()'), self.recordClicked)
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
        self.topSubLayout.addWidget(self.recordButton)
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
        


        self.trackArray = {}
        self.playArray = {} 
        self.recordArray = {}

        # Dialog for creating project at start up
        self.projectPath = self.createProject()

        self.play = Server().boot()
        
        self.setGeometry(100,100,1000,600)
        self.showMaximized()

        
   
		
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

        self.playButton.setStyleSheet("background-color: #118811; border-radius:3;color:#ffffff;")
        self.playButton.setText('PLAYING')
        print "play clicked"
        self.play.start()
        
        for track in self.trackArray:
                
            if self.trackArray[track].getState() == 'active':
                
                print self.trackArray[track].getTrackName() + " is playing"

                self.playback = SfPlayer(self.trackArray[track].getTrackName()).out()

    def stopClicked(self):

        self.playButton.setStyleSheet("background-color: #445544; border-radius:3;color:#ffffff;")
        self.playButton.setText('PLAY')
        self.recordButton.setStyleSheet("background-color: #554444; border-radius:3;color:#ffffff;")
        self.recordButton.setText('RECORD')
        
        print "stop clicked"
        self.play.stop()
##        for track in self.playArray:
##            self.playArray[track].terminate()
##        for track in self.recordArray:
##            self.recordArray[track].terminate()

    def recordClicked(self):

        if(len(self.trackArray) !=0):
            self.recordButton.setStyleSheet("background-color: #881111; border-radius:3;color:#ffffff;")
            self.recordButton.setText('RECORDING')
            #print "play clicked"
            self.playIndex = 0
            self.recordIndex = 0
            self.play.start()

            for track in self.trackArray:
                if self.trackArray[track].getState() == 'active':
                    print self.trackArray[track].getTrackName() + " is playing"
                    self.playArray[self.playIndex] = SfPlayer(self.trackArray[track].getTrackName()).out()
                    self.playIndex+=1
                if self.trackArray[track].getState() == 'record':
                    print "recording on track "+self.trackArray[track].getTrackName() 
                    self.recordArray[self.recordIndex] = Record(self.trackArray[track].getTrackName())
                    self.recordIndex+=1

            for track in self.recordArray:
                self.recordArray[track].start()
        else:
            QtGui.QMessageBox.question(self, 'Warning!',"No tracks have been added.", QtGui.QMessageBox.Ok)


    def closeEvent(self, event):
        # remove temp files
        if(self.projectPath == 'temp'):
            shutil.rmtree('temp')
        # let the window close
        event.accept() 
        

app = QtGui.QApplication(sys.argv)
myWidget = Main()

p = myWidget.palette()
p.setColor(QtGui.QPalette.Background,QtCore.Qt.black)
myWidget.setPalette(p)

myWidget.show()
app.exec_()

