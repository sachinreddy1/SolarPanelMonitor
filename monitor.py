import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Graph import *
from Globs import *

import matplotlib.animation as animation

HEIGHT = 500
WIDTH = 600

LIGHT_GRAY = '#ababab'
MID_GRAY_1 = '#464646'
MID_GRAY_2 = '#383735'
MID_GRAY_3 = '#31302F'
DARK_GRAY = '#262523'
RED = '#cd5c5c'
GREEN = '#32cd32'

class Monitor():
	def __init__ (self, application):
		self.root = tk.Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.close_window)
		self.root.winfo_toplevel().title("Solar Panel Monitor")
		self.root.geometry('{}x{}'.format(WIDTH, HEIGHT))
		self.root.configure(bg=MID_GRAY_2)

		self.application = application
		self.graph = None
		self.widgetFrames = []
		self.selected = 0
		self.vars = []

	# ------------- #

	def setupFrames(self):
		# Connection frame
		self.connFrame = tk.Frame(self.root, bg=DARK_GRAY)
		self.connFrame.place(x=110, y=30, width=170, relheight=0.87, anchor='n')

		# Data frame
		self.dataFrame = tk.Frame(self.root, bg=LIGHT_GRAY)
		self.dataFrame.place(x=395, y=30, width=350, relheight=0.87, anchor='n')

	def setupThresholds(self):
		# Threshold Title
		thresholdTitle = tk.Label(self.dataFrame, text="Thresholds:", bg=LIGHT_GRAY, font='TkDefaultFont 14 bold')
		thresholdTitle.place(x=10, y=5, width=120, height=25)

		# Voltage Threshold Label and Entry
		voltageEntryThreshold = tk.Label(self.dataFrame, text="Voltage: ", bg=LIGHT_GRAY)
		voltageEntryThreshold.place(x=10, y=35, width=60, height=25)
		self.voltageEntry = tk.Entry(self.dataFrame, font=40)
		self.voltageEntry.insert(0, DEFAULT_VOLTAGE_THRES)
		self.voltageEntry.bind('<FocusIn>', lambda event, i=0: self.on_entry_click(event, i))
		self.voltageEntry.bind('<FocusOut>', lambda event, i=0: self.on_focusout(event, i))
		self.voltageEntry.config(fg = 'grey')
		self.voltageEntry.place(x=70, y=35, width=60, height=30)

		# Current Threshold Label and Entry
		currentEntryThreshold = tk.Label(self.dataFrame, text="Current: ", bg=LIGHT_GRAY)
		currentEntryThreshold.place(x=10, y=70, width=60, height=25)
		self.currentEntry = tk.Entry(self.dataFrame, font=40)
		self.currentEntry.insert(0, DEFAULT_CURRENT_THRES)
		self.currentEntry.bind('<FocusIn>', lambda event, i=1: self.on_entry_click(event, i))
		self.currentEntry.bind('<FocusOut>', lambda event, i=1: self.on_focusout(event, i))
		self.currentEntry.config(fg = 'grey')
		self.currentEntry.place(x=70, y=70, width=60, height=30)

		# Temperature Threshold Label and Entry
		temperatureEntryThreshold = tk.Label(self.dataFrame, text="Heat: ", bg=LIGHT_GRAY)
		temperatureEntryThreshold.place(x=10, y=105, width=60, height=25)
		self.temperatureEntry = tk.Entry(self.dataFrame, font=40)
		self.temperatureEntry.insert(0, DEFAULT_TEMPERATURE_THRES)
		self.temperatureEntry.bind('<FocusIn>', lambda event, i=2: self.on_entry_click(event, i))
		self.temperatureEntry.bind('<FocusOut>', lambda event, i=2: self.on_focusout(event, i))
		self.temperatureEntry.config(fg = 'grey')
		self.temperatureEntry.place(x=70, y=105, width=60, height=30)

		# Entry button submission
		thresholdEntryButton = tk.Button(self.dataFrame, text="OK", font=40, command=lambda: self.application.thresholdInputting(self.voltageEntry.get(), self.currentEntry.get(), self.temperatureEntry.get(), self.selected))
		thresholdEntryButton.place(x=135, y=70, width=40, height=30)

	def setupCheckboxes(self):
		# Output Configuration
		var1 = tk.IntVar()
		checkboxA = tk.Checkbutton(self.dataFrame, text="X", variable=var1, command=lambda: self.updateCheckbox(0))
		checkboxA.place(relx=0.97, y=60, width=50, height=20, anchor=tk.E)
		var2 = tk.IntVar()
		checkboxB = tk.Checkbutton(self.dataFrame, text="CD", variable=var2, command=lambda: self.updateCheckbox(1))
		checkboxB.place(relx=0.97, y=85, width=50, height=20, anchor=tk.E)
		var3 = tk.IntVar()
		checkboxC = tk.Checkbutton(self.dataFrame, text="BC", variable=var3, command=lambda: self.updateCheckbox(2))
		checkboxC.place(relx=0.97, y=110, width=50, height=20, anchor=tk.E)
		var4 = tk.IntVar()
		checkboxD = tk.Checkbutton(self.dataFrame, text="AD", variable=var4, command=lambda: self.updateCheckbox(3))
		checkboxD.place(relx=0.97, y=135, width=50, height=20, anchor=tk.E)
		self.vars = [var1, var2, var3, var4]

	def setupSyncButton(self):
		# SYNC Label
		self.syncFrame = tk.Frame(self.connFrame, bg=MID_GRAY_1)
		self.syncFrame.pack(side="bottom", fill="x")
		# SYNC Button
		self.syncButton = tk.Button(self.syncFrame, text='sync', font=20, command=lambda: self.application.inputting('sync'))
		self.syncButton.pack(side="left")

	def setupQueryButtons(self):
		queryButtonFrame = tk.Frame(self.dataFrame)
		queryButtonFrame.pack(side="bottom", fill="x")
		v1Button = tk.Button(queryButtonFrame, text="V1", font=30, command=lambda: self.graph.setField('voltage_1'))
		v1Button.pack(side="left")
		v2Button = tk.Button(queryButtonFrame, text="V2", font=30, command=lambda: self.graph.setField('voltage_2'))
		v2Button.pack(side="left")
		v3Button = tk.Button(queryButtonFrame, text="V3", font=30, command=lambda: self.graph.setField('voltage_3'))
		v3Button.pack(side="left")
		c1Button = tk.Button(queryButtonFrame, text="C1", font=30, command=lambda: self.graph.setField('current_1'))
		c1Button.pack(side="left")
		t1Button = tk.Button(queryButtonFrame, text="T1", font=30, command=lambda: self.graph.setField('temperature_1'))
		t1Button.pack(side="left")
		t2Button = tk.Button(queryButtonFrame, text="T2", font=30, command=lambda: self.graph.setField('temperature_2'))
		t2Button.pack(side="left")
		t3Button = tk.Button(queryButtonFrame, text="T3", font=30, command=lambda: self.graph.setField('temperature_3'))
		t3Button.pack(side="left")
		t4Button = tk.Button(queryButtonFrame, text="T4", font=30, command=lambda: self.graph.setField('temperature_4'))
		t4Button.pack(side="left")
		t5Button = tk.Button(queryButtonFrame, text="T5", font=30, command=lambda: self.graph.setField('temperature_5'))
		t5Button.pack(side="left")
		t6Button = tk.Button(queryButtonFrame, text="T6", font=30, command=lambda: self.graph.setField('temperature_6'))
		t6Button.pack(side="left")

	def setup(self):			
		self.setupFrames()
		self.setupThresholds()
		self.setupCheckboxes()
		self.setupSyncButton()
		self.setupQueryButtons()

		# Manual Switch Button
		self.toggleManualSwitchButton = tk.Button(self.dataFrame, text="ON", font=40, command=lambda: self.application.manualSwitchInputting(self.selected))
		self.toggleManualSwitchButton.place(relx=0.85, y=10, width=40, height=30)

	def updateWidgets(self):
		connLength = len(self.application.c.connections)

		for i in range(0, connLength):
			BACKGROUND = MID_GRAY_1 if i == 0 else DARK_GRAY
			# Frame for Widget
			widgetFrame = tk.Frame(self.connFrame, bg=BACKGROUND)
			widgetFrame.pack(side="top", fill="x")

			# IP Label
			ipLabel = tk.Label(widgetFrame, text='IP: ' + self.application.c.connections[i].ip, bg=BACKGROUND, font='TkDefaultFont 10')
			ipLabel.pack(side="top", fill="x", pady=5)
			ipLabel.config(fg=LIGHT_GRAY)
			# IP Status
			ipStatus = tk.Label(widgetFrame, text="Status: Connected", bg=BACKGROUND, font='TkDefaultFont 10')
			ipStatus.pack(side="bottom", fill="x", pady=5)
			ipStatus.config(fg=GREEN)

			self.widgetFrames.append([widgetFrame, ipLabel, ipStatus])
			index = len(self.widgetFrames) - 1
			widgetFrame.bind('<Button-1>', lambda event, i=index: self.frameInteraction(event, i, BACKGROUND))
			ipLabel.bind('<Button-1>', lambda event, i=index: self.labelInteraction(event, i))
			ipStatus.bind('<Button-1>', lambda event, i=index: self.labelInteraction(event, i))
			widgetFrame.bind("<Enter>", lambda event, i=index: self.frameInteraction(event, i, BACKGROUND))
			widgetFrame.bind("<Leave>", lambda event, i=index: self.frameInteraction(event, i, BACKGROUND))

	# ------------- #

	def switchConnections(self, i):
		# Change checkbox
		self.updateCheckbox(self.application.c.connections[i].configSwitch)

		# Change threshold values
		self.voltageEntry.delete(0, "end")
		self.voltageEntry.insert(0, self.application.c.connections[i].voltageValue)
		self.voltageEntry.config(fg = 'grey')
		self.currentEntry.delete(0, "end")
		self.currentEntry.insert(0, self.application.c.connections[i].currentValue)
		self.currentEntry.config(fg = 'grey')
		self.temperatureEntry.delete(0, "end")
		self.temperatureEntry.insert(0, self.application.c.connections[i].temperatureValue)
		self.temperatureEntry.config(fg = 'grey')

	def updateCheckbox(self, i):
		for var in self.vars:
			var.set(0)
		for j in range(0, len(self.vars)):
			if j == i:
				self.vars[j].set(1)
		self.application.configSwitchInputting(self.selected, i)

	def labelInteraction(self, event, index):
		color = MID_GRAY_1

		if event.type is '4':	# Clicked
			self.clearWidgetColors()
			color = MID_GRAY_1	
			self.selected = index
			self.switchConnections(self.selected)
			self.graph.a.clear()

		for i in self.widgetFrames[index]: i.configure(bg=color)

	def frameInteraction(self, event, index, bg):
		color = MID_GRAY_1

		if event.type is '4':	# Clicked
			self.clearWidgetColors()
			color = MID_GRAY_1	
			self.selected = index
			self.switchConnections(self.selected)
			self.graph.a.clear()

		if event.type is '7':	# Entered
			color = MID_GRAY_1 if self.selected == index else MID_GRAY_3

		if event.type is '8':	# Exited
			color = MID_GRAY_1 if self.selected == index else DARK_GRAY

		for i in self.widgetFrames[index]: i.configure(bg=color)

	def clearWidgetColors(self):
		for i in self.widgetFrames:
			for j in i:
				j.configure(bg=DARK_GRAY)

	# ------------- #

	def on_entry_click(self, event, i):
		if i == 0:
			self.voltageEntry.delete(0, "end")
			self.voltageEntry.insert(0, '')
			self.voltageEntry.config(fg = 'black')
		if i == 1:
			self.currentEntry.delete(0, "end")
			self.currentEntry.insert(0, '')
			self.currentEntry.config(fg = 'black')
		if i == 2:
			self.temperatureEntry.delete(0, "end")
			self.temperatureEntry.insert(0, '')
			self.temperatureEntry.config(fg = 'black')

	def on_focusout(self, event, i):
		if len(self.application.c.connections) == 0:
			if i == 0:
				if self.voltageEntry.get() == '':
					self.voltageEntry.insert(0, DEFAULT_VOLTAGE_THRES)
					self.voltageEntry.config(fg = 'grey')
			if i == 1:
				if self.currentEntry.get() == '':
					self.currentEntry.insert(0, DEFAULT_CURRENT_THRES)
					self.currentEntry.config(fg = 'grey')
			if i == 2:
				if self.temperatureEntry.get() == '':
					self.temperatureEntry.insert(0, DEFAULT_TEMPERATURE_THRES)
					self.temperatureEntry.config(fg = 'grey')
		else:
			if i == 0:
				if self.voltageEntry.get() == '':
					self.voltageEntry.insert(0, self.application.c.connections[self.selected].voltageValue)
					self.voltageEntry.config(fg = 'grey')
			if i == 1:
				if self.currentEntry.get() == '':
					self.currentEntry.insert(0, self.application.c.connections[self.selected].currentValue)
					self.currentEntry.config(fg = 'grey')
			if i == 2:
				if self.temperatureEntry.get() == '':
					self.temperatureEntry.insert(0, self.application.c.connections[self.selected].temperatureValue)
					self.temperatureEntry.config(fg = 'grey')

	# ------------- #

	def clearWidgets(self):
		for i in self.widgetFrames:
			for j in i:
				j.destroy()

		self.widgetFrames = []
		self.selected = 0

	def runSetup(self):
		self.setup()
		self.updateCheckbox(0)

	def close_window(self):
		self.application.command = 'quit'

	# ------------- #

	def run(self):
		#TESTING
		# sync_button = Image.open('images/sync.png')
		# sync_image_for_button = ImageTk.PhotoImage(sync_button)
		# self.syncButton = tk.Button(self.syncFrame, image=sync_image_for_button, command=lambda: self.application.inputting('sync'))
		# self.syncButton.config(width="20", height="20")
		# self.syncButton.place(relx=0, rely=0)
		# self.syncButton.config(image=sync_image_for_button) 

		# go_button = Image.open('images/go.png')
		# go_image_for_button = ImageTk.PhotoImage(go_button)
		# self.syncButton = tk.Button(self.dataFrame, image=go_image_for_button, command=lambda: self.application.thresholdInputting(voltageEntry.get(), currentEntry.get(), temperatureEntry.get(), self.selected))
		# self.syncButton.config(width="30", height="30")
		# self.syncButton.place(relx=0.5, rely=0.15, relwidth=0.15, relheight=0.1)
		# self.syncButton.config(image=go_image_for_button) 

		self.graph = Graph(self)
		self.graph.run()
		ani = animation.FuncAnimation(self.graph.f, self.graph.animate, interval=1000)
		self.root.mainloop()

