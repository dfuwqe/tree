import serial
import pandas as pd 
import time
import datetime
import numpy as np
from random import shuffle



class engine():
	def __init__(self,filename):
		#define parameters here
		self.playSpeed = 1 
		self.timeUnitBase = 1 #seconds
		self.fps = 2
		self.numLED = 60
		self.animations=[self.animation1]
		self.tableStartTime = datetime.timedelta(0,40) #day, seconds
		# Comment serial port out if not connected to Arduino
		# self.serialPort = serial.Serial('/dev/cu.usbserial-DN02B86I', 250000)

		#variables
		self.currentTime = 0
		self.tableEndTime = 0
		self.numAS = self.numLED
		self.timeUnit = self.playSpeed * self.timeUnitBase
		self.table = None
		self.ASmap = dict() #dictionary -- key: AS number, val: LED number
		self.maxTime = 0 
		self.frameInterval = 1/(self.fps)
		self.frames = [([0]* self.numLED) for i in range(self.timeUnit*self.fps)]
		self.timer = 0

		self.set_up_step(filename)
		self.init_run()
		

	def set_up_step(self,filename):
		#set up related goes here
		time.sleep(3)	#wait for setup in Arduino
		self.table = self.read_table(filename)
		self.currentTime = self.tableStartTime

	def init_run(self):
		#this step is to process the table to perform:
		#AS - LED position matching
		ASlist = self.table["AS"].value_counts().index.tolist()
		print(ASlist)
		if(len(ASlist) >= self.numLED):
			ASlist = ASlist[:self.numLED]
		else:
			ASlist = ASlist + [0] * (self.numLED - len(ASlist))

		shuffle(ASlist)
		
		#Map AS number to LED number
		for i in range(self.numLED):
			self.ASmap[ASlist[i]] = i

		#Convert timestamp to timedelta for extraction
		self.table["time"] = pd.to_timedelta(self.table['time'].str.split().str[1])
		self.tableEndTime = self.table["time"].iloc[-1]


	def read_table(self,filename):
		col_names = ["H","time","action","from","AS","content"]
		return pd.read_csv(filename, sep = "|", names=col_names, header=None)


	def show(self):
		# startTime = self.currentTime
		# self.currentTime += datetime.timedelta(seconds=self.timeUnit)
		# endTime = self.currentTime
		# print(startTime)
		# print(endTime)
		# data = self.table[(self.table["time"]>= startTime) & (self.table["time"] < endTime)]

		while self.currentTime <= self.tableEndTime:
			#extract a section of the table
			self.timer = time.time()
			data = self.extract_data_for_one_time_unit()
			#pass to processing -- animation modules 
			for f in self.animations:
				f(data)
			###
			###
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
		strList = [chr(x) for x in strList]
		self.write_to_serial("".join(strList)+"\n")
		timeElapsed = time.time() - self.timer
		self.wait_for_one_full_frame(timeElapsed)
		self.timer = time.time()

	def wait_for_one_full_frame(self,timeElapsed):
		# print(timeElapsed)
		time.sleep(self.frameInterval - timeElapsed)
		# pass


	def write_to_serial(self,frame):
		#middle-ware
		self.serialPort.write(frame.encode())
		print(frame)
		# print(self.serialPort.readline())
			


	#control 0 - 255. 
	#Visualization no.2
	def animation1(self,data):
		#ASes that have updates
		ASlist = data["AS"].unique().tolist()
		#blink at 2Hz
		for x in ASlist:
			if x in self.ASmap:
				led = self.ASmap[x]
				self.frames[0][led] = 0	#blink
				#check if this is annouce
				test = data[(data["AS"]==x) & (data["action"] == "A")]
				if not test.empty:
					self.frames[1][led] = int(test["content"].iloc[-1].split('.')[0])








def main():
	e = engine("output.txt")
	# e.show()


if __name__ == '__main__':
	main()