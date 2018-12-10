import serial
import pandas as pd 
import time
import datetime
import numpy as np
from random import shuffle
import visualizer
import signal



class engine():
	def __init__(self,filename):
		#define parameters here
		self.playSpeed = 1 
		self.timeUnitBase = 1 #seconds
		self.fps = 2
		self.numLED = 600
		self.animations=[self.animation1]
		self.tableStartTime = datetime.timedelta(0,40) #day, seconds
		# Comment serial port out if not connected to Arduino
		self.serialPort1 = serial.Serial('/dev/cu.usbserial-DN02B86I', 250000)
		# self.serialPort2 = serial.Serial('/dev/cu.usbmodem1411', 250000)
		# self.serialPort3 = serial.Serial('/dev/cu.usbserial-DA01R2KF', 250000)
		

		#variables
		self.currentTime = 0
		self.tableEndTime = 0
		self.numAS = self.numLED
		self.timeUnit = self.playSpeed * self.timeUnitBase
		self.table = None
		self.ASmap = dict() #dictionary -- key: AS number, val: LED number
		self.maxTime = 0 
		self.frameInterval = 1/(self.fps)
		self.frames = [([0]* self.numLED*2) for i in range(self.timeUnit*self.fps)] #2 bytes for each light, one for color, one for state
		# self.brightness = [0]*self.numLED
		self.timer = 0
		#visualizer for debug purposes
		self.v = visualizer.visualizer()

		self.set_up_step(filename)
		self.init_run()
		

	def set_up_step(self,filename):
		#set up related goes here
		time.sleep(5)	#wait for setup in Arduino
		self.table = self.read_table(filename)
		self.currentTime = self.tableStartTime

	def init_run(self):
		#this step is to process the table to perform:
		#AS - LED position matching
		ASlist = self.table["AS"].value_counts().index.tolist()
		# print(len(ASlist))
		# print(ASlist)
		if(len(ASlist) >= self.numLED):
			ASlist = ASlist[:self.numLED]
		else:
			ASlist = ASlist + [0] * (self.numLED - len(ASlist))

		shuffle(ASlist)
		# print(ASlist)

		
		#Map AS number to LED number
		for i in range(self.numLED):
			self.ASmap[ASlist[i]] = i

		#Convert timestamp to timedelta for extraction
		self.table["time"] = pd.to_timedelta(self.table['time'].str.split().str[1])
		self.tableEndTime = self.table["time"].iloc[-1]


	def read_table(self,filename):
		col_names = ["H","time","action","from","AS","content","e1","e2"]
		return pd.read_csv(filename, sep = "|", names=col_names, header=None)


	def show(self):
		# startTime = self.currentTime
		# self.currentTime += datetime.timedelta(seconds=self.timeUnit)
		# endTime = self.currentTime
		# print(startTime)
		# print(endTime)
		# data = self.table[(self.table["time"]>= startTime) & (self.table["time"] < endTime)]

		# while self.currentTime <= self.tableEndTime:
		while True:
			#extract a section of the table
			self.timer = time.time()
			data = self.extract_data_for_one_time_unit()
			#pass to processing -- animation modules 
			for f in self.animations:
				f(data)
			#current design - draw out the full frames for the whole duration, then move on to next phase to draw each frame
			self.draw_frames()

			

	def extract_data_for_one_time_unit(self):
		print(self.currentTime)
		startTime = self.currentTime
		self.currentTime += datetime.timedelta(seconds=self.timeUnit)
		endTime = self.currentTime
		return self.table[(self.table["time"]>= startTime) & (self.table["time"] < endTime)]

	def draw_frames(self):
		for i in range(len(self.frames)):
			self.draw_frame(i)

	def draw_frame(self,index):
		#Note: since it's singled-threaded right now. I'll just let the thread wait until the next frame after it finishes processing
		strList = self.frames[index]
		# print(strList)
		strList = [chr(x) for x in strList]
		self.write_to_serial("".join(strList))
		timeElapsed = time.time() - self.timer
		self.wait_for_one_full_frame(timeElapsed)
		self.timer = time.time()

	def wait_for_one_full_frame(self,timeElapsed):
		# print(timeElapsed)
		if (self.frameInterval - timeElapsed) > 0:
			time.sleep(self.frameInterval - timeElapsed)
		# pass


	def write_to_serial(self,frame):
		#middle-ware
		self.serialPort1.write(frame[:600].encode("latin-1"))
		# self.serialPort2.write(frame[600:1200].encode("latin-1"))
		# self.serialPort3.write(frame[1200:].encode("latin-1"))
		# pass
		

	def onExit(self):
		st = [chr(255) for _ in range(2*self.numLED)]
		time.sleep(1)
		# self.write_to_serial("".join(st))
		
		# self.write_to_serial("".join(st))
		# time.sleep(1)
			

	#control 0 - 255. 
	#Visualization no.2
	def animation1(self,data):
		#ASes that have updates
		ASlist = data["AS"].unique().tolist()
		# print(len(ASlist))
		#blink at 2Hz
		#change later
		needUpdate = [1]*self.numLED
		# for x,led in self.ASmap.items():

		for x in ASlist:
			led = self.ASmap[x]
			# if x in ASlist:
			self.frames[0][2*led] = 0	#blink
			self.frames[1][2*led] = 64
			needUpdate[led] = 0
			#check if this is annouce
			test = data[(data["AS"]==x) & (data["action"] == "A")]
			if not test.empty:
				if ":" not in test["content"].iloc[-1]:
					self.frames[1][2*led+1] = int(test["content"].iloc[-1].split('.')[0])
					self.frames[0][2*led+1] = self.frames[1][2*led+1]
						
			# else:
		for led in range(self.numLED):
			if needUpdate[led] == 1:
				self.frames[0][2*led] = self.frames[1][2*led] -1 if self.frames[1][2*led] >=36 else 32
				self.frames[0][2*led+1] = self.frames[1][2*led+1]
				self.frames[1][2*led] = self.frames[0][2*led] -1 if self.frames[0][2*led] >=36 else 32




def main():
	e = engine("output.txt")
	def signal_handler(sig, frame):
		e.onExit()
		quit()
	signal.signal(signal.SIGINT, signal_handler)
	e.show()



if __name__ == '__main__':
	main()