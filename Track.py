'''
Juan Hernandez
 CST205 
 Project 2
 '''

import sys
import os
import time
import thread
import subprocess
import pyaudio
import wave
from pylab import *
from PyQt4 import QtGui, QtCore
from Engine import *

class Track(QtGui.QWidget):
	def __init__( self, name, parent=None):
		super(Track, self).__init__(parent)

		self.tempName = "Untitled_Track_"+name

		self.pushButton = QtGui.QPushButton("stuff")
		self.pushButton.setMaximumSize(1200,240)

		# self.pushButton2.clicked.connect(self.deleteLater)

		# Sets the layout for the track object
		self.layout = QtGui.QHBoxLayout()
		# Left panel displays control buttons 
		self.leftPanel = QtGui.QVBoxLayout()
		# Displays delete track button and track name in one row
		self.nameLayout = QtGui.QHBoxLayout()
		# Right panel displays audio editing module
		self.rightPanel = QtGui.QVBoxLayout()
		# Displays editing buttons
		self.editBoxLayout = QtGui.QVBoxLayout()
		self.editFirstRow = QtGui.QHBoxLayout()
		self.editSecondRow = QtGui.QHBoxLayout()


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

		self.closeButton = QtGui.QPushButton("X")
		self.closeButton.setMaximumSize(40,120)
		self.closeButton.setStyleSheet("background-color: #ffaaaa; border-radius:5;")
		self.closeButton.clicked.connect(self.deleteLater)
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

		self.playButton = QtGui.QPushButton("Play")
		self.playButton.setMaximumSize(200,100)
		self.stopButton = QtGui.QPushButton("Stop")
		self.stopButton.setMaximumSize(200,100)
		self.mixButton = QtGui.QPushButton("Mix")
		self.mixButton.setMaximumSize(200,100)

		self.connect(self.playButton, QtCore.SIGNAL('clicked()'), self.playClicked)
		self.connect(self.stopButton, QtCore.SIGNAL('clicked()'), self.stopClicked)
		self.connect(self.recordButton, QtCore.SIGNAL('clicked()'), self.recordClicked)
		#self.connect(self.VolumeButton, SIGNAL('clicked()'), self.volumeClicked)

		self.leftPanel.addLayout(self.nameLayout)
		self.leftPanel.addWidget(self.recordButton)
		self.leftPanel.addWidget(self.playButton)
		self.leftPanel.addWidget(self.stopButton)
		self.leftPanel.addWidget(self.mixButton)

		self.layout.addLayout(self.leftPanel)
		self.layout.addLayout(self.rightPanel)
		self.layout.addWidget(self.pushButton)
	

		self.setLayout(self.layout)

		#create thread for recording
		self.record = Record(self.tempName)

		#create thread for playback
		self.play = Play(self.tempName)

	  
	def renameDialog(self):
		text, ok = QtGui.QInputDialog.getText(self, 'Rename', '')
		
		if ok:
			self.trackName.setText(str(text))
			#self.trackName.setStyleSheet("background-color: #ffffff")
		#self.layout.addWidget(self.pushButton)

		subprocess.Popen(str('cp '+'/home/juan/CSUMB/CST205/Project_Two/'+self.tempName+'.wav'+ ' '+'/home/juan/CSUMB/CST205/Project_Two/'+text+'.wav'))


		#os.system(str('cp '+self.tempName+'.wav'+ ' '+text+'.wav'))
		#os.system(str('rm '+ self.tempName+'.wav'))

		self.tempName = text

	def playClicked(self):

		#start playback thread
		self.play.start()

	def stopClicked(self):
		#self.StopButton.setPixmap(QPixmap(self.STOP_BUTTON))
		print('Stop Button Clicked')
		# Kill arecord subprocess and terminate threads
		self.stop_recording()
		self.record.terminate()
		self.play.terminate()
		# change playback button to original state

	def stop_recording(self):
		subprocess.call(["killall","arecord"])	
		self.play.terminate()
		self.show_wave_n_spec("Untitled_Track_1")

	def recordClicked(self):

		print('Record Button Clicked')
		# Start recording thread
		self.record.start()
		# Displays a wave form of track recorded

	def show_wave_n_spec(self,speech):
		spf = wave.open(speech,'r')
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
		savefig('test.png', bbox_inches='tight')
		show()
		spf.close()

	def track_name():
		return str(self.tempName)