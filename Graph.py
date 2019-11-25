import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk
from tkinter import ttk
import sqlite3
from Globs import *
style.use("ggplot")

import matplotlib.dates as mdates
import numpy as np
import datetime
import time

units = ["V", "V", "V", "A", "C", "C", "C", "C", "C", "C"]
title = ["Voltage #1 vs. Time (Minutes)", "Voltage #2 vs. Time (Minutes)", "Voltage #3 vs. Time (Minutes)", "Current #1 vs. Time (Minutes)", "Temperature #1 vs. Time (Minutes)", "Temperature #2 vs. Time (Minutes)",
		 "Temperature #3 vs. Time (Minutes)", "Temperature #4 vs. Time (Minutes)", "Temperature #5 vs. Time (Minutes)", "Temperature #6 vs. Time (Minutes)"]

class Graph:
	def __init__ (self, monitor):
		self.monitor = monitor
		self.f = Figure(figsize=(5,5), dpi=100)
		self.f.patch.set_facecolor(LIGHT_GRAY)
		self.a = self.f.add_subplot(111)
		self.a.set_facecolor(DARK_GRAY)
		self.a.tick_params(axis='x', colors="black")
		self.a.tick_params(axis='y', colors="black")
		self.field = 'voltage_1'
		self.f.suptitle(title[self.getFieldIndex()], fontsize=10, color="black")
		self.t = self.f.text(0.915, 0.5, "X.X", fontweight="medium", transform=self.a.transAxes)

	def run(self):
		canvas = FigureCanvasTkAgg(self.f, self.monitor.dataFrame)
		canvas.draw()
		canvas.get_tk_widget().pack(side="bottom", fill="x", pady=5)
		canvas._tkcanvas.pack(side="bottom", fill="x")

	def animate(self, i):
		if len(self.monitor.application.c.connections) > 0:
			dataList = self.getData(self.monitor.application.c.connections[self.monitor.selected].ip)
			xList = []
			yList = []
			for i in dataList:
				x = i[0]
				y = i[1]
				xList.append(datetime.datetime.fromtimestamp(x))
				yList.append(y)

			self.a.clear()
			self.a.plot_date(xList, yList, color=GREEN, fmt='-r')
			self.a.xaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))
			self.a.tick_params(axis='x', which='major', labelsize=8)

			self.t.remove()
			labelValue = "X.X"
			if len(yList) > 0:
				labelValue = yList[-1]
			self.t = self.f.text(0.915, 0.5, str(labelValue) + units[self.getFieldIndex()], fontweight="medium", transform=self.a.transAxes)

	def getData(self, ip):
		conn = sqlite3.connect('solarPanel.db')
		cursor = conn.cursor()	
		cursor.execute("SELECT timeRecorded, ({0}) FROM voltages WHERE (:ip)".format(self.field),
		{
			'ip': ip,
		})
		values = cursor.fetchall()
		conn.commit()
		return values

	# ------------- #

	def setField(self, field):
		self.field = field
		self.f.suptitle(title[self.getFieldIndex()], fontsize=10)

	def getFieldIndex(self):
		if self.field == 'voltage_1':
			return 0
		elif self.field == 'voltage_2':
			return 1
		elif self.field == 'voltage_3':
			return 2
		elif self.field == 'current_1':
			return 3
		elif self.field == 'temperature_1':
			return 4
		elif self.field == 'temperature_2':
			return 5
		elif self.field == 'temperature_3':
			return 6
		elif self.field == 'temperature_4':
			return 7
		elif self.field == 'temperature_5':
			return 8
		elif self.field == 'temperature_6':
			return 9
		else:
			return 0
