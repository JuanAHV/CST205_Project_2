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
		
		# Chorus effect buttons
		self.chorusRow = QtGui.QHBoxLayout()

		self.chorus = QtGui.QPushButton("Chours")
		self.chorus.setMaximumSize(80,40)

		self.chorusToggle = QtGui.QPushButton("OFF")
		self.chorusToggle.setMaximumSize(40,40)
                self.chorus.setStyleSheet("background-color: grey; border-radius:3;color:#ffffff;")
		self.chorusRow.addWidget(self.chorus)
		self.chorusRow.addWidget(self.chorusToggle)

		self.effectsLayout.addLayout(self.chorusRow)
		self.chorus.clicked.connect(self.fxSettings)
		self.chorusToggle.setStyleSheet("background-color: red; border-radius:3;color:#ffffff;")
		self.connect(self.chorusToggle, QtCore.SIGNAL('clicked()'), self.chorusOn)
		# *******************************************
		# Delay effect buttons
		self.delayRow = QtGui.QHBoxLayout()

		self.delay = QtGui.QPushButton("Delay")
		self.delay.setMaximumSize(80,40)
		self.delay.setStyleSheet("background-color: grey; border-radius:3;color:#ffffff;")

		self.delayToggle = QtGui.QPushButton("OFF")
		self.delayToggle.setMaximumSize(40,40)

		self.delayRow.addWidget(self.delay)
		self.delayRow.addWidget(self.delayToggle)

		self.effectsLayout.addLayout(self.delayRow)
		self.delay.clicked.connect(self.fxSettings)
		self.delayToggle.setStyleSheet("background-color: red; border-radius:3;color:#ffffff;")
		self.connect(self.delayToggle, QtCore.SIGNAL('clicked()'), self.delayOn)
		# *******************************************
		# Flanger effect buttons
		self.flangerRow = QtGui.QHBoxLayout()

		self.flanger = QtGui.QPushButton("Flanger")
		self.flanger.setMaximumSize(80,40)
		self.flanger.setStyleSheet("background-color: grey; border-radius:3;color:#ffffff;")

		self.flangerToggle = QtGui.QPushButton("OFF")
		self.flangerToggle.setMaximumSize(40,40)

		self.flangerRow.addWidget(self.flanger)
		self.flangerRow.addWidget(self.flangerToggle)

		self.effectsLayout.addLayout(self.flangerRow)
		self.flanger.clicked.connect(self.fxSettings)
		self.flangerToggle.setStyleSheet("background-color: red; border-radius:3;color:#ffffff;")
		self.connect(self.flangerToggle, QtCore.SIGNAL('clicked()'), self.flangerOn)
		# *******************************************
		# Phaser effect buttons
		self.phaserRow = QtGui.QHBoxLayout()

		self.phaser = QtGui.QPushButton("Phaser")
		self.phaser.setMaximumSize(80,40)
		self.phaser.setStyleSheet("background-color: grey; border-radius:3;color:#ffffff;")

		self.phaserToggle = QtGui.QPushButton("OFF")
		self.phaserToggle.setMaximumSize(40,40)

		self.phaserRow.addWidget(self.phaser)
		self.phaserRow.addWidget(self.phaserToggle)

		self.effectsLayout.addLayout(self.phaserRow)
		self.phaser.clicked.connect(self.fxSettings)
		self.phaserToggle.setStyleSheet("background-color: red; border-radius:3;color:#ffffff;")
		self.connect(self.phaserToggle, QtCore.SIGNAL('clicked()'), self.phaserOn)
		# *******************************************
		# Reverb effect buttons
		self.reverbRow = QtGui.QHBoxLayout()

		self.reverb = QtGui.QPushButton("Reverb")
		self.reverb.setMaximumSize(80,40)
		self.reverb.setStyleSheet("background-color: grey; border-radius:3;color:#ffffff;")

		self.reverbToggle = QtGui.QPushButton("OFF")
		self.reverbToggle.setMaximumSize(40,40)

		self.reverbRow.addWidget(self.reverb)
		self.reverbRow.addWidget(self.reverbToggle)

		self.effectsLayout.addLayout(self.reverbRow)
		self.reverb.clicked.connect(self.fxSettings)
		self.reverbToggle.setStyleSheet("background-color: red; border-radius:3;color:#ffffff;")
		self.connect(self.reverbToggle, QtCore.SIGNAL('clicked()'), self.reverbOn)
		# *******************************************

		'''
		self.b1 = QtGui.QPushButton("<< 5 seconds")
		self.b1.setMaximumSize(120,40)

		self.editFirstRow.addWidget(self.b1)

		self.b2 = QtGui.QPushButton(">> 5 seconds")
		self.b2.setMaximumSize(120,40)

		self.editSecondRow.addWidget(self.b2)

		self.editBoxLayout.addLayout(self.editFirstRow)
		self.editBoxLayout.addLayout(self.editSecondRow)

		#editBoxLayout.addWidget(self.pushButton)
		self.rightPanel.addLayout(self.editBoxLayout)

		'''

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

		'''
		self.leftPanel.addLayout(self.nameLayout)
		self.leftPanel.addWidget(self.recordButton)
		self.leftPanel.addWidget(self.muteButton)
		self.leftPanel.addWidget(self.stopButton)
		self.leftPanel.addWidget(self.mixButton)
		self.leftPanel.addLayout(self.effectsLayout)
		'''

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

	def fxSettings(self):
		dialog = startFXSetupGUI(self)
		run = dialog.exec_()

	def chorusOn(self):
                if(self.getState() == 'active'):
			self.setState('chorus')
			self.chorusToggle.setText('ON')
			self.chorusToggle.setStyleSheet("background-color: green; border-radius:3;color:white;")
		else:
			self.setState('active')
			self.chorusToggle.setText('OFF')
			self.chorusToggle.setStyleSheet("background-color: red; border-radius:3;color:white;")

	def delayOn(self):
                if(self.getState() == 'active'):
			self.setState('delay')
			self.delayToggle.setText('ON')
			self.delayToggle.setStyleSheet("background-color: green; border-radius:3;color:white;")
		else:
			self.setState('active')
			self.delayToggle.setText('OFF')
			self.delayToggle.setStyleSheet("background-color: red; border-radius:3;color:white;")                

	def flangerOn(self):
                if(self.getState() == 'active'):
			self.setState('flanger')
			self.flangerToggle.setText('ON')
			self.flangerToggle.setStyleSheet("background-color: green; border-radius:3;color:white;")
		else:
			self.setState('active')
			self.flangerToggle.setText('OFF')
			self.flangerToggle.setStyleSheet("background-color: red; border-radius:3;color:white;")

	def phaserOn(self):
                if(self.getState() == 'active'):
			self.setState('phaser')
			self.phaserToggle.setText('ON')
			self.phaserToggle.setStyleSheet("background-color: green; border-radius:3;color:white;")
		else:
			self.setState('active')
			self.phaserToggle.setText('OFF')
			self.phaserToggle.setStyleSheet("background-color: red; border-radius:3;color:white;")
	def reverbOn(self):
                if(self.getState() == 'active'):
			self.setState('reverb')
			self.reverbToggle.setText('ON')
			self.reverbToggle.setStyleSheet("background-color: green; border-radius:3;color:white;")
		else:
			self.setState('active')
			self.reverbToggle.setText('OFF')
			self.reverbToggle.setStyleSheet("background-color: red; border-radius:3;color:white;")

class Spectrogram(QtCore.QThread,QtGui.QWidget):
	def __init__(self, name):
		QtCore.QThread.__init__(self) 
		self.name = str(name)

	def run(self):
	#def show_wave_n_spec(self,speech):
		spf = wave.open(self.name,'r')
		sound_info = spf.readframes(-1)
		sound_info = fromstring(sound_info, 'Int16')

		f = spf.getframerate()
		subplot(211)
		plot(sound_info)
		xlim(0, 2000000)        
		ylim(-40000, 40000)        
		title('Wave form and spectrogram of test.wav') #%s' % sys.argv[1])
		subplot(212)
		spectrogram = specgram(sound_info, Fs = f, scale_by_freq=True,sides='default')
		#self.addWidget(show())
		savefig(self.name+".png", bbox_inches='tight')
		show()
		spf.close()

		self.stuff()
		self.terminate()

	def stuff(self):
		print "function in thread"




class FXSetupGUI(object):
    def makeUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(380, 250)
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
        self.slider1.setValue(0)
        self.slider1.setGeometry(QtCore.QRect(20, 50, 40, 160))
        self.slider1.setOrientation(QtCore.Qt.Vertical)
        self.slider1.setObjectName("slider1")
        
        #slider 2
        self.slider2 = QtGui.QSlider(Dialog)
        self.slider2.setRange(0,100)
        self.slider2.setValue(0)
        self.slider2.setGeometry(QtCore.QRect(160, 50, 40, 160))
        self.slider2.setOrientation(QtCore.Qt.Vertical)
        self.slider2.setObjectName("slider2")
        #slider 3
        self.slider3 = QtGui.QSlider(Dialog)
        self.slider3.setRange(0,100)
        self.slider3.setValue(0)
        self.slider3.setGeometry(QtCore.QRect(290, 50, 40, 160))
        self.slider3.setOrientation(QtCore.Qt.Vertical)
        self.slider3.setObjectName("slider3")
        #valuebox 1
        self.value1 = QtGui.QLineEdit(Dialog)
        self.value1.setGeometry(QtCore.QRect(23,7, 31, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.value1.setFont(font)
        self.value1.setObjectName("value1")
        #valuebox 2
        self.value2 = QtGui.QLineEdit(Dialog)
        self.value2.setGeometry(QtCore.QRect(163, 7, 31, 30))
        self.value2.setFont(font)
        self.value2.setObjectName("value2")
        #valuebox 3
        self.value3 = QtGui.QLineEdit(Dialog)
        self.value3.setGeometry(QtCore.QRect(293, 7, 31, 30))
        self.value3.setFont(font)
        self.value3.setObjectName("value3")

        #Strings in box title and other things
        self.retranslateUi(Dialog)

        #Linking sliders with value boxes
        self.slider1.valueChanged.connect(self.slider1Changed)
        self.slider2.valueChanged.connect(self.slider2Changed)
        self.slider3.valueChanged.connect(self.slider3Changed)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "FX Setting", None, QtGui.QApplication.UnicodeUTF8))
        self.label1.setText(QtGui.QApplication.translate("Dialog", "PARAMETER1", None, QtGui.QApplication.UnicodeUTF8))
        self.label2.setText(QtGui.QApplication.translate("Dialog", "PARAMETER2", None, QtGui.QApplication.UnicodeUTF8))
        self.label3.setText(QtGui.QApplication.translate("Dialog", "PARAMETER3", None, QtGui.QApplication.UnicodeUTF8))

    def slider1Changed(self, val):
        self.value1.setText(str(val))

    def slider2Changed(self, val):
        self.value2.setText(str(val))

    def slider3Changed(self, val):
        self.value3.setText(str(val))        

class startFXSetupGUI(QtGui.QDialog, FXSetupGUI):
        def __init__(self, parent = None):
                QtGui.QDialog.__init__(self,parent)
                self.makeUi(self)
        def getValues(self):
                return params


