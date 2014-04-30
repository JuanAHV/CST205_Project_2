import sys
import time
import thread
import subprocess
import pyaudio
import wave
import numpy
from pylab import *
from PyQt4 import *

class Record(QtCore.QThread,QtGui.QWidget):
	def __init__(self, name):
		QtCore.QThread.__init__(self) 
		self.name = str(name)
	def run(self):

		CHUNK = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 2
		RATE = 44100
		RECORD_SECONDS = 10
		WAVE_OUTPUT_FILENAME = self.name

		if sys.platform == 'darwin':
		    CHANNELS = 1

		p = pyaudio.PyAudio()

		stream = p.open(format=FORMAT,
		                channels=CHANNELS,
		                rate=RATE,
		                input=True,
		                frames_per_buffer=CHUNK)

		print("* recording")

		frames = []
		
		#self.spaceKeyPressed = SpaceKeyPress()
		#self.spaceKeyPressed.start()
		
		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		#while (self.spaceKeypressed != True):
		    data = stream.read(CHUNK)
		    frames.append(data)

		print("* done recording")
		#self.spaceKeyPressed.terminate()

		#stream.stop_stream()
		stream.close()
		p.terminate()

		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()

class SpaceKeyPress(QtCore.QThread,QtGui.QWidget):
	def __init__(self):
		QtCore.QThread.__init__(self)

	def run(self):
		print "Running space key detect event."


	def keyPressEvent(self, event):    
		print "key press event"  
		self.key = event.key()  
		if self.key == QtCore.Qt.Key_Space:
			#self.spaceKeypressed = True
			print "Space Key Pressed"
			self.terminate()

###class Play(QtCore.QThread):
##	def __init__(self, name):
##		QtCore.QThread.__init__(self)
##		self.name = str(name)
##		self.volume = 1
##	def run(self):
##		print('Play Button Clicked')
##		#initialize  buffer size
##		buffer_size = 1024
##		# open the file for reading.
##		wave_file = wave.open(self.name, 'rb')
##		# create an audio object
##		playback = pyaudio.PyAudio()
##		# open stream based on the wave object which has been input.
##		stream = playback.open(format =
##		playback.get_format_from_width(wave_file.getsampwidth()),
##		channels = wave_file.getnchannels(),
##		rate = wave_file.getframerate(),
##		output = True)
##		# read data (based on the buffer size)
##		data = wave_file.readframes(buffer_size)
##		# play stream (looping from beginning of file to the end)
##		while data != '':
##		# writing to the stream is what *actually* plays the sound.
##			decodeddata = numpy.fromstring(data, numpy.int16)
##			newdata = (decodeddata *self.volume).astype(numpy.int16)
##			stream.write(newdata.tostring())
##			data = wave_file.readframes(buffer_size)
##		# cleanup stuff.
##		stream.close()    
##		playback.terminate()
##
##	def setVolume(self, vol):
##		self.volume = vol





