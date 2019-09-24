import serial
import pandas as pd 
import time
import datetime
import numpy as np
from random import shuffle
import visualizer
import signal

col_names = ["H","time","action","from","AS","content","e1","e2"]
table = pd.read_csv("output1.txt", sep = "|", names=col_names, header=None)

table["timedelta"] = pd.to_timedelta(table['time'].str.split().str[1])
tableEndTime = table["timedelta"].iloc[-1]
tablestartTime = table["timedelta"].iloc[0]

df = pd.DataFrame(columns=col_names)

cur_time = tablestartTime
while cur_time < tableEndTime:
	print(cur_time, "  ", tableEndTime)
	onesec = table[(table["timedelta"]>= cur_time) & (table["timedelta"] < (cur_time+datetime.timedelta(seconds=1)))]
	ASlist = onesec["AS"].unique().tolist()
	for a in ASlist:
		d = onesec[(onesec["AS"] == a) & (onesec["action"] == "A") & (":" not in onesec["content"])]
		# print(d)
		# print(d["timedelta"])
		if not d.empty:
			d = d.drop("timedelta", 1).iloc[-1]
			df = df.append(d, ignore_index = True)
		else:
			d2 = onesec[(onesec["AS"] == a)]
			d2 = d2.drop("timedelta", 1).iloc[-1]
			df = df.append(d2, ignore_index = True)
	cur_time += datetime.timedelta(seconds=1)


df = df[col_names]
df.to_csv("test.txt", sep='|', index=False, header=False)

