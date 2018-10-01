import tkinter as tk
import time 
import sys

class visualizer():
	def __init__(self):
		self.root = tk.Tk()
		self.canvas = tk.Canvas(self.root, width=1280, height=600, borderwidth=0, highlightthickness=0, bg="white")
		self.canvas.grid()
		tk.Canvas.create_circle = self._create_circle

		self.canvas.create_rectangle(0, 0, 1280, 50, fill='black')
		self.canvas.create_rectangle(0, 100, 1280, 150, fill='black')
		self.canvas.create_rectangle(0, 200, 1280, 250, fill='black')
		self.canvas.create_rectangle(0, 300, 1280, 350, fill='black')
		self.canvas.create_rectangle(0, 400, 1280, 450, fill='black')
		self.canvas.create_rectangle(0, 500, 1280, 550, fill='black')
		self.root.wm_title("LED visualizer")


		e1,e2,e3,e4,e5,e6 = [],[],[],[],[],[]
		for i in range(100):
			e1.append(self.canvas.create_circle(i*15, 25, 5, fill="grey", outline="#DDD", width=1))
			e2.append(self.canvas.create_circle(i*15, 125, 5, fill="grey", outline="#DDD", width=1))
			e3.append(self.canvas.create_circle(i*15, 225, 5, fill="grey", outline="#DDD", width=1))
			e4.append(self.canvas.create_circle(i*15, 325, 5, fill="grey", outline="#DDD", width=1))
			e5.append(self.canvas.create_circle(i*15, 425, 5, fill="grey", outline="#DDD", width=1))
			e6.append(self.canvas.create_circle(i*15, 525, 5, fill="grey", outline="#DDD", width=1))

		# canvas.create_circle(150, 40, 20, fill="#BBB", outline="")
		self.LED = e1+e2+e3+e4+e5+e6

		self.colorSet = ["red","green","blue","purple","orange","yellow","pink","navy"]

	def _create_circle(self, x, y, r, **kwargs):
	    return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)
	

	def flash(self,commands):
		for i,x in enumerate(commands):
			color = ord(x)//32
			self.canvas.itemconfigure(self.LED[i],fill = self.colorSet[color])


v = visualizer()	
while True:
	commands = input()
	v.flash(commands)
	v.root.update_idletasks()
	v.root.update()
