'''
Juan Hernandez
 CST205 
 Project 2
 '''

import sys
import time
import thread
import subprocess
import pyaudio
import wave
from pylab import *
from PyQt4 import QtGui, QtCore

class Record(QtCore.QThread):

	def __init__(self, name):
		QtCore.QThread.__init__(self) 
		self.name = str(name)
	def run(self):
		
		rec = ['arecord','-f','dat','-d','10',self.name]
		subprocess.Popen(rec , stdout=subprocess.PIPE)
		#print "Recording done"

class Play(QtCore.QThread):
	def __init__(self, name):
		QtCore.QThread.__init__(self)
		self.name = str(name)
	def run(self):
		print('Play Button Clicked')
		#initialize  buffer size
		buffer_size = 1024
		# open the file for reading.
		wave_file = wave.open(self.name, 'rb')
		# create an audio object
		playback = pyaudio.PyAudio()
		# open stream based on the wave object which has been input.
		stream = playback.open(format =
		playback.get_format_from_width(wave_file.getsampwidth()),
		channels = wave_file.getnchannels(),
		rate = wave_file.getframerate(),
		output = True)
		# read data (based on the buffer size)
		data = wave_file.readframes(buffer_size)
		# play stream (looping from beginning of file to the end)
		while data != '':
		# writing to the stream is what *actually* plays the sound.
			stream.write(data)
			data = wave_file.readframes(buffer_size)
		# cleanup stuff.
		stream.close()    
		playback.terminate()


# Mix the audio files for play back

class PlayAll(QtCore.QThread):
	def __init__(self, tracks):
		QtCore.QThread.__init__(self)
		self.tracks = tracks
	def run(self):

		infiles = ["Untitled_Track_1", "Untitled_Track_2"]
		outfile = "Untitled_Track_3"

		data= []
		for infile in infiles:
			w = wave.open(infile, 'rb')
			data.append( [w.getparams(), w.readframes(w.getnframes())] )
			w.close()

		output = wave.open(outfile, 'wb')
		output.setparams(data[0][0])
		output.writeframes(data[0][1])
		output.writeframes(data[1][1])
		output.close()


		print('PlayAll clicked!')

		



