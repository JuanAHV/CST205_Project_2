import sys
import os
import time
import thread
import subprocess
import pyaudio
import wave
from pyo import *
from pylab import *
from PyQt4 import * #QtGui, QtCore
from Engine import *

class Track(QtGui.QWidget):
	def __init__( self, name, path, parent=None):
		super(Track, self).__init__(parent)
                
		self.state = 'active'
		self.tempName = "Untitled_Track_"+name
		self.recordingPath = path+"/audio"

		# temporary spectrogram placeholder
		self.pushButton = QtGui.QPushButton("Spectrogram")
		self.pushButton.setMaximumSize(2000,240)

		# Sets the layout for the track object
		self.layout = QtGui.QHBoxLayout()
		# Left panel displays control buttons 
		self.leftControlsPanel = QtGui.QVBoxLayout()
		# Left panel displays control buttons 
		self.leftPanel = QtGui.QHBoxLayout()
		# Displays delete track button and track name in one row
		self.nameLayout = QtGui.QHBoxLayout()
		# Effects layout panel
		self.effectsLayout = QtGui.QVBoxLayout()
		# Right panel displays audio editing module
		self.rightPanel = QtGui.QVBoxLayout()
		# Displays editing buttons
		self.editBoxLayout = QtGui.QVBoxLayout()
		self.editFirstRow = QtGui.QHBoxLayout()
		self.editSecondRow = QtGui.QHBoxLayout()
		
		# Chorus effect buttons and dialog
		self.chorusRow = QtGui.QHBoxLayout()
		self.chorusDialog = startFXSetupGUI(self)
		self.chorusDialog.setNames("Chorus", "wet", "dry", "balance")
		self.chorusState = 'inactive'

		self.chorus = QtGui.QPushButton("Chorus")
		self.chorus.setMaximumSize(80,40)

		self.chorusToggle = QtGui.QPushButton("OFF")
		self.chorusToggle.setMaximumSize(40,40)
                self.chorus.setStyleSheet("background-color: grey; border-radius:3;color:#ffffff;")
		self.chorusRow.addWidget(self.chorus)
		self.chorusRow.addWidget(self.chorusToggle)

		self.effectsLayout.addLayout(self.chorusRow)
		self.connect(self.chorus,QtCore.SIGNAL('clicked()'), self.showChorusDialog)
		self.chorusToggle.setStyleSheet("background-color: #770000; border-radius:3;color:#ffffff;")
		self.connect(self.chorusToggle, QtCore.SIGNAL('clicked()'), self.chorusOn)

		
		# *******************************************
		# Delay effect buttons
		self.delayRow = QtGui.QHBoxLayout()
		self.delayDialog = startFXSetupGUI(self)
		self.delayState = 'inactive'

		self.delay = QtGui.QPushButton("Delay")
		self.delay.setMaximumSize(80,40)
		self.delay.setStyleSheet("background-color: grey; border-radius:3;color:#ffffff;")

		self.delayToggle = QtGui.QPushButton("OFF")
		self.delayToggle.setMaximumSize(40,40)

		self.delayRow.addWidget(self.delay)
		self.delayRow.addWidget(self.delayToggle)

		self.effectsLayout.addLayout(self.delayRow)
		self.connect(self.delay,QtCore.SIGNAL('clicked()'), self.showDelayDialog)
		self.delayToggle.setStyleSheet("background-color: #770000; border-radius:3;color:#ffffff;")
		self.connect(self.delayToggle, QtCore.SIGNAL('clicked()'), self.delayOn)
		# *******************************************
		# Flanger effect buttons
		self.flangerRow = QtGui.QHBoxLayout()
		self.flangerDialog = startFXSetupGUI(self)
		self.flangerState = 'inactive'


		self.flanger = QtGui.QPushButton("Flanger")
		self.flanger.setMaximumSize(80,40)
		self.flanger.setStyleSheet("background-color: grey; border-radius:3;color:#ffffff;")

		self.flangerToggle = QtGui.QPushButton("OFF")
		self.flangerToggle.setMaximumSize(40,40)

		self.flangerRow.addWidget(self.flanger)
		self.flangerRow.addWidget(self.flangerToggle)

		self.effectsLayout.addLayout(self.flangerRow)
		self.connect(self.flanger,QtCore.SIGNAL('clicked()'), self.showFlangerDialog)
		self.flangerToggle.setStyleSheet("background-color: #770000; border-radius:3;color:#ffffff;")
		self.connect(self.flangerToggle, QtCore.SIGNAL('clicked()'), self.flangerOn)
		# *******************************************
		# Phaser effect buttons
		self.phaserRow = QtGui.QHBoxLayout()
		self.phaserDialog = startFXSetupGUI(self)
		self.phaserState = 'inactive'

		self.phaser = QtGui.QPushButton("Phaser")
		self.phaser.setMaximumSize(80,40)
		self.phaser.setStyleSheet("background-color: grey; border-radius:3;color:#ffffff;")

		self.phaserToggle = QtGui.QPushButton("OFF")
		self.phaserToggle.setMaximumSize(40,40)

		self.phaserRow.addWidget(self.phaser)
		self.phaserRow.addWidget(self.phaserToggle)

		self.effectsLayout.addLayout(self.phaserRow)
		self.connect(self.phaser,QtCore.SIGNAL('clicked()'), self.showPhaserDialog)
		self.phaserToggle.setStyleSheet("background-color: #770000; border-radius:3;color:#ffffff;")
		self.connect(self.phaserToggle, QtCore.SIGNAL('clicked()'), self.phaserOn)
		# *******************************************
		# Reverb effect buttons
		self.reverbRow = QtGui.QHBoxLayout()
		self.reverbDialog = startFXSetupGUI(self)
		self.reverbState = 'inactive'

		self.reverb = QtGui.QPushButton("Reverb")
		self.reverb.setMaximumSize(80,40)
		self.reverb.setStyleSheet("background-color: grey; border-radius:3;color:#ffffff;")

		self.reverbToggle = QtGui.QPushButton("OFF")
		self.reverbToggle.setMaximumSize(40,40)

		self.reverbRow.addWidget(self.reverb)
		self.reverbRow.addWidget(self.reverbToggle)

		self.effectsLayout.addLayout(self.reverbRow)
		self.connect(self.reverb,QtCore.SIGNAL('clicked()'), self.showReverbDialog)
		self.reverbToggle.setStyleSheet("background-color: #770000; border-radius:3;color:#ffffff;")
		self.connect(self.reverbToggle, QtCore.SIGNAL('clicked()'), self.reverbOn)
		# *******************************************

		self.closeButton = QtGui.QPushButton("X")
		self.closeButton.setMaximumSize(40,120)
		self.closeButton.setStyleSheet("background-color: #771111; border-radius:1;color:#ffffff;")
		self.closeButton.clicked.connect(self.deleteLater)
		self.closeButton.clicked.connect(self.setState)
		self.trackName = QtGui.QPushButton(self.tempName)
		#self.trackName = QtGui.QLabel(" Untitled Track "+name)
		self.trackName.setMaximumSize(160,100)
		self.trackName.setStyleSheet("background-color: #ffffff")
		self.trackName.clicked.connect(self.renameDialog)
		#self.trackName.mouseReleaseEvent(self.renameDialog)
		#self.trackName.mouseDoubleClickEvent(self.renameDialog)

		self.nameLayout.addWidget(self.closeButton)
		self.nameLayout.addWidget(self.trackName)

		self.recordButton = QtGui.QPushButton("Record")
		self.recordButton.setMaximumSize(200,100)
		self.recordButton.setStyleSheet("background-color: #554444; border-radius:3;color:#ffffff;")
		self.muteButton = QtGui.QPushButton("Mute")
		self.muteButton.setMaximumSize(200,100)
		self.muteButton.setStyleSheet("background-color: #555544; border-radius:3;color:#ffffff;")
		self.stopButton = QtGui.QPushButton("Stop")
		self.stopButton.setMaximumSize(200,100)
		self.stopButton.setStyleSheet("background-color: #555544; border-radius:3;color:#ffffff;")
		self.mixButton = QtGui.QPushButton("Mix")
		self.mixButton.setMaximumSize(200,100)
		self.mixButton.setStyleSheet("background-color: #445544; border-radius:3;color:#ffffff;")

		self.connect(self.muteButton, QtCore.SIGNAL('clicked()'), self.muteClicked)
		#self.connect(self.stopButton, QtCore.SIGNAL('clicked()'), self.stopClicked)
		self.connect(self.recordButton, QtCore.SIGNAL('clicked()'), self.recordClicked)
		#self.connect(self.VolumeButton, SIGNAL('clicked()'), self.volumeClicked)

		self.leftControlsPanel.addLayout(self.nameLayout)
		self.leftControlsPanel.addWidget(self.recordButton)
		self.leftControlsPanel.addWidget(self.muteButton)
		#self.leftControlsPanel.addWidget(self.stopButton)
		self.leftControlsPanel.addWidget(self.mixButton)

		self.leftPanel.addLayout(self.leftControlsPanel)
		self.leftPanel.addLayout(self.effectsLayout)

		self.layout.addLayout(self.leftPanel)
		#self.layout.addLayout(self.effectsLayout)
		self.layout.addLayout(self.rightPanel)
		self.layout.addWidget(self.pushButton)
	

		self.setLayout(self.layout)

		#self.spectrogram = Spectrogram("Untitled_Track_1")
		#self.spectrogram.start()
		#self.spectrogram.stuff()

	def setState(self, state):
		self.state = state

	def getState(self):
		return str(self.state)
	  
	def renameDialog(self):
		text, ok = QtGui.QInputDialog.getText(self, 'Rename', '')
		
		if ok:
			self.tempName = str(text)
			self.trackName.setText(self.tempName)


	def getTrackName(self):
		return self.tempName

	def setTrackName(self, name):
		self.tempName = str(name)
		self.trackName.setText(self.tempName)

	def muteClicked(self):
		if(self.getState() == 'active'):
			self.setState('mute')
			self.muteButton.setText('Unmute')
			self.muteButton.setStyleSheet("background-color: #888800; border-radius:3;color:#ffffff;")
		else:
			if(self.getState() == 'record'):
				QtGui.QMessageBox.question(self, 'Warning!',"Cannot mute track while recording is active.", QtGui.QMessageBox.Ok)
			else:
				self.setState('active')
				self.muteButton.setText('Mute')
				self.muteButton.setStyleSheet("background-color: #555544; border-radius:3;color:#ffffff;")

		#start playback thread
		#self.play.start()

	def stopClicked(self):


		#self.StopButton.setPixmap(QPixmap(self.STOP_BUTTON))
		print('Stop Button Clicked')
		# Kill arecord subprocess and terminate threads
		#self.record.terminate()
		#self.play.terminate()
		# change playback button to original state

	def recordClicked(self):

		if(self.getState() == 'active'):
			self.setState('record')
			self.recordButton.setStyleSheet("background-color: #771111; border-radius:3;color:#ffffff;")
		else:
			self.setState('active')
			self.recordButton.setStyleSheet("background-color: #554444; border-radius:3;color:#ffffff;")
		# Start recording thread
		#self.record.start()
		# Displays a wave form of track recorded

	def track_name():
		return str(self.tempName)

	def showChorusDialog(self):
		self.chorusDialog.show()

	def showFlangerDialog(self):
		self.flangerDialog.show()

	def showDelayDialog(self):
		self.delayDialog.show()

	def showPhaserDialog(self):
		self.phaserDialog.show()

	def showReverbDialog(self):
		self.reverbDialog.show()

	def chorusOn(self):
		if(self.chorusState == 'inactive'):
			self.chorusState = 'active'
			self.chorusToggle.setText('ON')
			self.chorusToggle.setStyleSheet("background-color: #00aa00; border-radius:3;color:white;")
		else:
			self.chorusState = 'inactive'
			self.chorusToggle.setText('OFF')
			self.chorusToggle.setStyleSheet("background-color: #770000; border-radius:3;color:white;")

	def delayOn(self):
		if(self.delayState == 'inactive'):
			self.delayState = 'active'
			self.delayToggle.setText('ON')
			self.delayToggle.setStyleSheet("background-color: #00aa00; border-radius:3;color:white;")
		else:
			self.delayState = 'inactive'
			self.delayToggle.setText('OFF')
			self.delayToggle.setStyleSheet("background-color: #770000; border-radius:3;color:white;")                

	def flangerOn(self):
		if(self.flangerState == 'inactive'):
			self.flangerState = 'active'
			self.flangerToggle.setText('ON')
			self.flangerToggle.setStyleSheet("background-color: #00aa00; border-radius:3;color:white;")
		else:
			self.flangerState = 'inactive'
			self.flangerToggle.setText('OFF')
			self.flangerToggle.setStyleSheet("background-color: #770000; border-radius:3;color:white;")

	def phaserOn(self):
		if(self.phaserState == 'inactive'):
			self.phaserState = 'active'
			self.phaserToggle.setText('ON')
			self.phaserToggle.setStyleSheet("background-color: #00aa00; border-radius:3;color:white;")
		else:
			self.phaserState = 'inactive'
			self.phaserToggle.setText('OFF')
			self.phaserToggle.setStyleSheet("background-color: #770000; border-radius:3;color:white;")
	def reverbOn(self):
		if(self.reverbState == 'inactive'):
			self.reverbState = 'active'
			self.reverbToggle.setText('ON')
			self.reverbToggle.setStyleSheet("background-color: #00aa00; border-radius:3;color:white;")
		else:
			self.reverbState = 'inactive'
			self.reverbToggle.setText('OFF')
			self.reverbToggle.setStyleSheet("background-color: #770000; border-radius:3;color:white;")

class FXSetupGUI(object):
    def makeUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(380, 250)

        font = QtGui.QFont()
        font.setPointSize(12)

        self.name = 'Effect'

        #Effect variables
        self.param1 = 70
        self.param2 = 70
        self.param3 = 70

        self.p1Name = 'p1'
        self.p2Name = 'p2'
        self.p3Name = 'p3'


        #PARAMETER LABEL 1
        self.label1 = QtGui.QLabel(Dialog)
        self.label1.setGeometry(QtCore.QRect(20, 170, 150, 100))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label1.setFont(font)
        self.label1.setObjectName("param1")
        #PARAMETER LABEL 2
        self.label2 = QtGui.QLabel(Dialog)
        self.label2.setGeometry(QtCore.QRect(160, 170, 150, 100))
        self.label2.setFont(font)
        self.label2.setObjectName("param2")
        #PARAMETER LABEL 3
        self.label3 = QtGui.QLabel(Dialog)
        self.label3.setGeometry(QtCore.QRect(290, 170, 150, 100))
        self.label3.setFont(font)
        self.label3.setObjectName("param3")
        #slider 1
        self.slider1 = QtGui.QSlider(Dialog)
        self.slider1.setRange(0,100)
        self.slider1.setValue(self.param1)
        self.slider1.setGeometry(QtCore.QRect(20, 50, 40, 160))
        self.slider1.setOrientation(QtCore.Qt.Vertical)
        self.slider1.setObjectName("slider1")
        
        #slider 2
        self.slider2 = QtGui.QSlider(Dialog)
        self.slider2.setRange(0,100)
        self.slider2.setValue(self.param2)
        self.slider2.setGeometry(QtCore.QRect(160, 50, 40, 160))
        self.slider2.setOrientation(QtCore.Qt.Vertical)
        self.slider2.setObjectName("slider2")
        #slider 3
        self.slider3 = QtGui.QSlider(Dialog)
        self.slider3.setRange(0,100)
        self.slider3.setValue(self.param3)
        self.slider3.setGeometry(QtCore.QRect(290, 50, 40, 160))
        self.slider3.setOrientation(QtCore.Qt.Vertical)
        self.slider3.setObjectName("slider3")
        #valuebox 1
        self.value1 = QtGui.QLabel(Dialog)
        self.value1.setGeometry(QtCore.QRect(23, 10, 40, 40))
        self.value1.setFont(font)
        self.value1.setText(str(self.param1))
        self.value1.setObjectName("value1")
        #valuebox 2
        self.value2 = QtGui.QLabel(Dialog)
        self.value2.setGeometry(QtCore.QRect(163, 10, 40, 40))
        self.value2.setFont(font)
        self.value2.setText(str(self.param2))
        self.value2.setObjectName("value2")
        #valuebox 3
        self.value3 = QtGui.QLabel(Dialog)
        self.value3.setGeometry(QtCore.QRect(293, 10, 40, 40))
        self.value3.setFont(font)
        self.value3.setText(str(self.param3))
        self.value3.setObjectName("value3")

        #Strings in box title and other things
        self.retranslateUi(Dialog)

        #Linking sliders with value boxes
        self.slider1.valueChanged.connect(self.slider1Changed)
        self.slider2.valueChanged.connect(self.slider2Changed)
        self.slider3.valueChanged.connect(self.slider3Changed)

    def getParam1(self):
    	return float(self.value1.text())/100.0

    def getParam2(self):
    	return float(self.value2.text())/100.0

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", self.name , None, QtGui.QApplication.UnicodeUTF8))
        self.label1.setText(QtGui.QApplication.translate("Dialog", self.p1Name, None, QtGui.QApplication.UnicodeUTF8))
        self.label2.setText(QtGui.QApplication.translate("Dialog", self.p2Name, None, QtGui.QApplication.UnicodeUTF8))
        self.label3.setText(QtGui.QApplication.translate("Dialog", self.p3Name, None, QtGui.QApplication.UnicodeUTF8))

    def setDialogName(self, Dialog):
    	Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", self.name , None, QtGui.QApplication.UnicodeUTF8))

    def getName(self):
    	return self.name 

    def slider1Changed(self, val):
        self.value1.setText(str(val))

    def slider2Changed(self, val):
        self.value2.setText(str(val))

    def slider3Changed(self, val):
        self.value3.setText(str(val))  

    def setNames(self, name, p1, p2, p3):
    	#self.name = name
    	self.label1.setText(QtGui.QApplication.translate("Dialog", p1, None, QtGui.QApplication.UnicodeUTF8))
        self.label2.setText(QtGui.QApplication.translate("Dialog", p2, None, QtGui.QApplication.UnicodeUTF8))
        self.label3.setText(QtGui.QApplication.translate("Dialog", p3, None, QtGui.QApplication.UnicodeUTF8))


class startFXSetupGUI(QtGui.QDialog, FXSetupGUI):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        #self.setDialogName(self.getName())
        self.makeUi(self)




