import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk
from tkinter import ttk
import sqlite3
style.use("ggplot")

class Graph:
	def __init__ (self, monitor):
		self.monitor = monitor
		self.f = Figure(figsize=(5,5), dpi=100)
		self.a = self.f.add_subplot(111)

		self.currentConnection = '192.168.1.97'
		self.currentField = 'voltage_2'

	def run(self):
		canvas = FigureCanvasTkAgg(self.f, self.monitor.dataFrame)
		canvas.draw()
		canvas.get_tk_widget().place(relx=0, rely=0.4, relwidth=1, relheight=0.6)

		# toolbar = NavigationToolbar2Tk(canvas, self)
		# toolbar.update()
		# canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		canvas._tkcanvas.place(relx=0, rely=0.4, relwidth=1, relheight=0.6)

	def animate(self, i):
		dataList = self.getData()
		xList = []
		yList = []
		for i in dataList:
			x = i[0]
			y = i[1]
			xList.append(x)
			yList.append(y)

		self.a.clear()
		self.a.plot(xList, yList)

	def getData(self):
		conn = sqlite3.connect('solarPanel.db')
		cursor = conn.cursor()	
		cursor.execute("SELECT timeRecorded, ({0}) FROM voltages WHERE (:ip)".format(self.currentField),
		{
			'ip': self.currentConnection,
		})
		values = cursor.fetchall()
		conn.commit()
		return values

	def convertTime(self, seconds): 
		seconds = seconds % (24 * 3600) 
		hour = seconds // 3600
		seconds %= 3600
		minutes = seconds // 60
		seconds %= 60
		return "%d:%02d:%02d" % (hour, minutes, seconds)
