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
		
		CHUNK = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 2
		RATE = 44100
		RECORD_SECONDS = 20
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

		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		    data = stream.read(CHUNK)
		    frames.append(data)

		print("* done recording")

		stream.stop_stream()
		stream.close()
		p.terminate()

		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()

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
'''
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
		'''
		



