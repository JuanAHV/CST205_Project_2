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

		self.chorus = QtGui.QPushButton("Chorus")
		self.chorus.setMaximumSize(80,40)

		self.chorusToggle = QtGui.QPushButton("off")
		self.chorusToggle.setMaximumSize(40,40)

		self.chorusRow.addWidget(self.chorus)
		self.chorusRow.addWidget(self.chorusToggle)

		self.effectsLayout.addLayout(self.chorusRow)
		# *******************************************
		# Delay effect buttons
		self.delayRow = QtGui.QHBoxLayout()

		self.delay = QtGui.QPushButton("Delay")
		self.delay.setMaximumSize(80,40)

		self.delayToggle = QtGui.QPushButton("off")
		self.delayToggle.setMaximumSize(40,40)

		self.delayRow.addWidget(self.delay)
		self.delayRow.addWidget(self.delayToggle)

		self.effectsLayout.addLayout(self.delayRow)
		# *******************************************
		# Flanger effect buttons
		self.flangerRow = QtGui.QHBoxLayout()

		self.flanger = QtGui.QPushButton("Flanger")
		self.flanger.setMaximumSize(80,40)

		self.flangerToggle = QtGui.QPushButton("off")
		self.flangerToggle.setMaximumSize(40,40)

		self.flangerRow.addWidget(self.flanger)
		self.flangerRow.addWidget(self.flangerToggle)

		self.effectsLayout.addLayout(self.flangerRow)
		# *******************************************
		# Phaser effect buttons
		self.phaserRow = QtGui.QHBoxLayout()

		self.phaser = QtGui.QPushButton("Phaser")
		self.phaser.setMaximumSize(80,40)

		self.phaserToggle = QtGui.QPushButton("off")
		self.phaserToggle.setMaximumSize(40,40)

		self.phaserRow.addWidget(self.phaser)
		self.phaserRow.addWidget(self.phaserToggle)

		self.effectsLayout.addLayout(self.phaserRow)
		# *******************************************
		# Reverb effect buttons
		self.reverbRow = QtGui.QHBoxLayout()

		self.reverb = QtGui.QPushButton("Reverb")
		self.reverb.setMaximumSize(80,40)

		self.reverbToggle = QtGui.QPushButton("off")
		self.reverbToggle.setMaximumSize(40,40)

		self.reverbRow.addWidget(self.reverb)
		self.reverbRow.addWidget(self.reverbToggle)

		self.effectsLayout.addLayout(self.reverbRow)
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



