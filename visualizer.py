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
		self.root.wm_title("LED visualizer")


		e1,e2,e3,e4,e5= [],[],[],[],[]
		for i in range(100):
			e1.append(self.canvas.create_circle(i*15, 25, 5, fill="grey", outline="#DDD", width=1))
			e2.append(self.canvas.create_circle(i*15, 125, 5, fill="grey", outline="#DDD", width=1))
			e3.append(self.canvas.create_circle(i*15, 225, 5, fill="grey", outline="#DDD", width=1))
			e4.append(self.canvas.create_circle(i*15, 325, 5, fill="grey", outline="#DDD", width=1))
			e5.append(self.canvas.create_circle(i*15, 425, 5, fill="grey", outline="#DDD", width=1))

		# canvas.create_circle(150, 40, 20, fill="#BBB", outline="")
		self.LED = e1+e2+e3+e4+e5

		self.colorSet = ["red","green","blue","purple","orange","yellow","pink","navy"]

	def _create_circle(self, x, y, r, **kwargs):
	    return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)
	
	def dim(self, start, end, brightness):
		(r1,g1,b1) = self.root.winfo_rgb(start)
		(r2,g2,b2) = self.root.winfo_rgb(end)
		r_ratio = float(r2-r1) / 255
		g_ratio = float(g2-g1) / 255
		b_ratio = float(b2-b1) / 255
		nr = int(r1 + (r_ratio * brightness))
		ng = int(g1 + (g_ratio * brightness))
		nb = int(b1 + (b_ratio * brightness))
		color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
		return color


	def flash(self,commands,brightness):
		commands = commands[0:60]
		for i,x in enumerate(commands):
			color = ord(x)//32
			c = self.colorSet[color] if color >0 else "grey"
			fc = self.dim(c,"grey",brightness[i])
			self.canvas.itemconfigure(self.LED[i],fill = fc)
		self.root.update_idletasks()
		self.root.update()

	
