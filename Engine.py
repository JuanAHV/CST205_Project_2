import sys
import time
import thread
import subprocess
import pyaudio
import wave
import numpy
from pyo import *
#from pylab import *
from PyQt4 import QtGui, QtCore

class Record(QtCore.QThread,QtGui.QWidget):
	def __init__(self, name):
		QtCore.QThread.__init__(self) 
		self.name = str(name)

	def run(self):
		if sys.platform == 'linux2':
			rec = ['arecord','-f','dat','-d','10', self.name]
			subprocess.Popen(rec , stdout=subprocess.PIPE)
		else:
			CHUNK = 1024
			FORMAT = pyaudio.paInt16
			CHANNELS = 2
			RATE = 44100
			RECORD_SECONDS = 60
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
			QtGui.QMessageBox.question(self, 'Warning!',"Done recording...", QtGui.QMessageBox.Ok)

	def add_silence(self, snd_data, seconds):
	    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
	    r = array('h', [0 for i in xrange(int(seconds*RATE))])
	    r.extend(snd_data)
	    r.extend([0 for i in xrange(int(seconds*RATE))])
	    return r

	def record(self):
	    """
	    Record a word or words from the microphone and 
	    return the data as an array of signed shorts.

	    Normalizes the audio, trims silence from the 
	    start and end, and pads with 0.5 seconds of 
	    blank sound to make sure VLC et al can play 
	    it without getting chopped off.
	    """
	    p = pyaudio.PyAudio()
	    stream = p.open(format=FORMAT, channels=1, rate=RATE,
	        input=True, output=True,
	        frames_per_buffer=CHUNK_SIZE)

	    num_silent = 0
	    snd_started = False

	    r = array('h')

	    while 1:
	        # little endian, signed short
	        snd_data = array('h', stream.read(CHUNK_SIZE))
	        if byteorder == 'big':
	            snd_data.byteswap()
	        r.extend(snd_data)

	        silent = is_silent(snd_data)

	        if silent and snd_started:
	            num_silent += 1
	        elif not silent and not snd_started:
	            snd_started = True

	        if snd_started and num_silent > 30:
	            break

	    sample_width = p.get_sample_size(FORMAT)
	    stream.stop_stream()
	    stream.close()
	    p.terminate()

	    r = normalize(r)
	    r = trim(r)
	    r = add_silence(r, 0.5)
	    return sample_width, r

	def record_to_file(self, path):
	    "Records from the microphone and outputs the resulting data to 'path'"
	    sample_width, data = record(self)
	    data = pack('<' + ('h'*len(data)), *data)

	    wf = wave.open(path, 'wb')
	    wf.setnchannels(1)
	    wf.setsampwidth(sample_width)
	    wf.setframerate(RATE)
	    wf.writeframes(data)
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



