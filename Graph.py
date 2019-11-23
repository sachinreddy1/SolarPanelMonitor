import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

LARGE_FONT= ("TkDefaultFont", 8)
style.use("ggplot")

class Graph:
	def __init__ (self, monitor):
		self.monitor = monitor
		self.f = Figure(figsize=(2,2), dpi=100)
		self.a = self.f.add_subplot(111)

	def run(self):
		canvas = FigureCanvasTkAgg(self.f, self.monitor.dataFrame)
		canvas.draw()
		canvas.get_tk_widget().place(relx=0, rely=0.4, relwidth=1, relheight=0.6)

		# toolbar = NavigationToolbar2Tk(canvas, self)
		# toolbar.update()
		# canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		canvas._tkcanvas.place(relx=0, rely=0.4, relwidth=1, relheight=0.6)

	def animate(self, i):
	    pullData = open("sampleText.txt","r").read()
	    dataList = pullData.split('\n')
	    xList = []
	    yList = []
	    for eachLine in dataList:
	        if len(eachLine) > 1:
	            x, y = eachLine.split(',')
	            xList.append(int(x))
	            yList.append(int(y))

	    self.a.clear()
	    self.a.plot(xList, yList)