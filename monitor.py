import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Graph import *
from Globs import *

import matplotlib.animation as animation

HEIGHT = 540
WIDTH = 710 #670

class Monitor():
	def __init__ (self, application):
		self.root = tk.Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.close_window)
		self.root.winfo_toplevel().title("Solar Panel Monitor")
		self.root.geometry('{}x{}'.format(WIDTH, HEIGHT))
		self.root.configure(bg=MID_GRAY_2)
		self.root.resizable(0,0)

		self.application = application
		self.graph = None
		self.widgetFrames = []
		self.selected = 0
		self.vars = []

	# ------------- #

	def setupFrames(self):
		# Spacing
		spacingFrame = tk.Frame(self.root, bg=MID_GRAY_2, width=25)
		spacingFrame.pack(side="left")

		# Connection frame
		self.connFrame = tk.Frame(self.root, bg=DARK_GRAY, highlightbackground="black", highlightcolor="black", highlightthickness=2)
		self.connFrame.pack(side="left", fill="y", pady="25")

		# Data frame
		self.dataFrame = tk.Frame(self.root, bg=LIGHT_GRAY, highlightbackground="black", highlightcolor="black", highlightthickness=2)
		self.dataFrame.pack(side="left", fill="both", padx="25", pady="25")

	def setupThresholds(self):
		thresholdFrame = tk.Frame(self.topFrame, bg=LIGHT_GRAY)
		thresholdFrame.pack(side="left")

		# Threshold Title
		thresholdFrame_1 = tk.Frame(thresholdFrame, bg=LIGHT_GRAY)
		thresholdFrame_1.pack(side="top", padx=30, pady=2.5, fill="x")
		thresholdTitle = tk.Label(thresholdFrame_1, text="Thresholds:", bg=LIGHT_GRAY, font='Helvetica_Neue 13 bold')
		thresholdTitle.pack(side="left")

		# Voltage Threshold Label and Entry
		thresholdFrame_2 = tk.Frame(thresholdFrame, bg=LIGHT_GRAY)
		thresholdFrame_2.pack(side="top", padx=43, pady=2.5, fill="x")
		voltageEntryThreshold = tk.Label(thresholdFrame_2, text="Voltage: ", bg=LIGHT_GRAY)
		voltageEntryThreshold.pack(side="left")
		self.voltageEntry = tk.Entry(thresholdFrame_2, highlightbackground=LIGHT_GRAY, bg=DARK_GRAY, font=40, width=5)
		self.voltageEntry.insert(0, DEFAULT_VOLTAGE_THRES)
		self.voltageEntry.bind('<FocusIn>', lambda event, i=0: self.on_entry_click(event, i))
		self.voltageEntry.bind('<FocusOut>', lambda event, i=0: self.on_focusout(event, i))
		self.voltageEntry.config(fg = 'grey')
		self.voltageEntry.pack(side="left")
		voltageUnit = tk.Label(thresholdFrame_2, text="V", bg=LIGHT_GRAY)
		voltageUnit.pack(side="left")

		# Current Threshold Label and Entry
		self.thresholdFrame_3 = tk.Frame(thresholdFrame, bg=LIGHT_GRAY)
		self.thresholdFrame_3.pack(side="top", padx=43, pady=2.5, fill="x")
		currentEntryThreshold = tk.Label(self.thresholdFrame_3, text="Current: ", bg=LIGHT_GRAY)
		currentEntryThreshold.pack(side="left")
		self.currentEntry = tk.Entry(self.thresholdFrame_3, highlightbackground=LIGHT_GRAY, bg=DARK_GRAY, font=40, width=5)
		self.currentEntry.insert(0, DEFAULT_CURRENT_THRES)
		self.currentEntry.bind('<FocusIn>', lambda event, i=1: self.on_entry_click(event, i))
		self.currentEntry.bind('<FocusOut>', lambda event, i=1: self.on_focusout(event, i))
		self.currentEntry.config(fg = 'grey')
		self.currentEntry.pack(side="left")
		currentUnit = tk.Label(self.thresholdFrame_3, text="A", bg=LIGHT_GRAY)
		currentUnit.pack(side="left")

		# Temperature Threshold Label and Entry
		thresholdFrame_4 = tk.Frame(thresholdFrame, bg=LIGHT_GRAY)
		thresholdFrame_4.pack(side="top", padx=10, pady=2.5, fill="x")
		temperatureEntryThreshold = tk.Label(thresholdFrame_4, text="Temperature: ", bg=LIGHT_GRAY)
		temperatureEntryThreshold.pack(side="left")
		self.temperatureEntry = tk.Entry(thresholdFrame_4, highlightbackground=LIGHT_GRAY, bg=DARK_GRAY, font=40, width=5)
		self.temperatureEntry.insert(0, DEFAULT_TEMPERATURE_THRES)
		self.temperatureEntry.bind('<FocusIn>', lambda event, i=2: self.on_entry_click(event, i))
		self.temperatureEntry.bind('<FocusOut>', lambda event, i=2: self.on_focusout(event, i))
		self.temperatureEntry.config(fg = 'grey')
		self.temperatureEntry.pack(side="left")
		temperatureUnit = tk.Label(thresholdFrame_4, text="C", bg=LIGHT_GRAY)
		temperatureUnit.pack(side="left")

	def setupCheckboxes(self):
		self.configFrame = tk.Frame(self.topFrame, bg=LIGHT_GRAY)
		self.configFrame.pack(side="right", padx=10)

		configFrame = tk.Frame(self.configFrame, bg=LIGHT_GRAY)
		configFrame.pack(side="bottom", pady=2.5)

		configFrame1 = tk.Frame(configFrame, bg=LIGHT_GRAY)
		configFrame1.pack(side="left", pady=2.5)
		configFrame2 = tk.Frame(configFrame, bg=LIGHT_GRAY)
		configFrame2.pack(side="left", pady=2.5)
		# Output Configuration
		var4 = tk.IntVar()
		checkboxD = tk.Checkbutton(configFrame2, text="AD", background=LIGHT_GRAY, variable=var4, command=lambda: self.updateCheckbox(3))
		checkboxD.pack(side="bottom", pady=2.5)
		var3 = tk.IntVar()
		checkboxC = tk.Checkbutton(configFrame2, text="BC", background=LIGHT_GRAY, variable=var3, command=lambda: self.updateCheckbox(2))
		checkboxC.pack(side="bottom", pady=2.5)
		var2 = tk.IntVar()
		checkboxB = tk.Checkbutton(configFrame2, text="CD", background=LIGHT_GRAY, variable=var2, command=lambda: self.updateCheckbox(1))
		checkboxB.pack(side="bottom", pady=2.5)
		var1 = tk.IntVar()
		checkboxA = tk.Checkbutton(configFrame2, text="XX", background=LIGHT_GRAY, variable=var1, command=lambda: self.updateCheckbox(0))
		checkboxA.pack(side="bottom", pady=2.5)
		configLabel = tk.Label(configFrame1, text="Config Switch: ", bg=LIGHT_GRAY)
		configLabel.pack(side="bottom")
		self.vars = [var1, var2, var3, var4]

	def setupSyncButton(self):
		# SYNC Label
		self.syncFrame = tk.Frame(self.connFrame, bg=MID_GRAY_1)
		self.syncFrame.pack(side="bottom", fill="x")		

	def setupButtons(self):
		# self.syncButton = tk.Button(self.syncFrame, text='sync', highlightbackground=MID_GRAY_1, font=20, command=lambda: self.application.inputting('sync'))
		# self.syncButton.pack(side="bottom", padx=40)

		thresholdEntryButton = tk.Button(self.thresholdFrame_3, text="OK", highlightbackground=LIGHT_GRAY, font=40, command=lambda: self.application.thresholdInputting(self.voltageEntry.get(), self.currentEntry.get(), self.temperatureEntry.get(), self.selected))
		thresholdEntryButton.pack(side="left", padx=5)

		manualConfigFrame = tk.Frame(self.configFrame, bg=LIGHT_GRAY)
		manualConfigFrame.pack(side="top", pady=2.5)
		self.toggleManualSwitchButton = tk.Button(manualConfigFrame, text="ON", highlightbackground=LIGHT_GRAY, font=40, command=lambda: self.application.manualSwitchInputting(self.selected))
		self.toggleManualSwitchButton.pack(side="right", pady=2.5)
		manualConfigLabel = tk.Label(manualConfigFrame, text="Manual Switch: ", bg=LIGHT_GRAY)
		manualConfigLabel.pack(side="right")

	def setupQueryButtons(self):
		queryButtonFrame = tk.Frame(self.dataFrame, bg=LIGHT_GRAY)
		queryButtonFrame.pack(side="bottom")
		v1Button = tk.Button(queryButtonFrame, text="V1", highlightbackground=LIGHT_GRAY, font=30, command=lambda: self.graph.setField('voltage_1'))
		v1Button.pack(side="left")
		v2Button = tk.Button(queryButtonFrame, text="V2", highlightbackground=LIGHT_GRAY, font=30, command=lambda: self.graph.setField('voltage_2'))
		v2Button.pack(side="left")
		v3Button = tk.Button(queryButtonFrame, text="V3", highlightbackground=LIGHT_GRAY, font=30, command=lambda: self.graph.setField('voltage_3'))
		v3Button.pack(side="left")
		c1Button = tk.Button(queryButtonFrame, text="C1", highlightbackground=LIGHT_GRAY, font=30, command=lambda: self.graph.setField('current_1'))
		c1Button.pack(side="left")
		t1Button = tk.Button(queryButtonFrame, text="T1", highlightbackground=LIGHT_GRAY, font=30, command=lambda: self.graph.setField('temperature_1'))
		t1Button.pack(side="left")
		t2Button = tk.Button(queryButtonFrame, text="T2", highlightbackground=LIGHT_GRAY, font=30, command=lambda: self.graph.setField('temperature_2'))
		t2Button.pack(side="left")
		t3Button = tk.Button(queryButtonFrame, text="T3", highlightbackground=LIGHT_GRAY, font=30, command=lambda: self.graph.setField('temperature_3'))
		t3Button.pack(side="left")
		t4Button = tk.Button(queryButtonFrame, text="T4", highlightbackground=LIGHT_GRAY, font=30, command=lambda: self.graph.setField('temperature_4'))
		t4Button.pack(side="left")
		t5Button = tk.Button(queryButtonFrame, text="T5", highlightbackground=LIGHT_GRAY, font=30, command=lambda: self.graph.setField('temperature_5'))
		t5Button.pack(side="left")
		t6Button = tk.Button(queryButtonFrame, text="T6", highlightbackground=LIGHT_GRAY, font=30, command=lambda: self.graph.setField('temperature_6'))
		t6Button.pack(side="left")

	def setup(self):			
		self.setupFrames()
		self.topFrame = tk.Frame(self.dataFrame, bg=LIGHT_GRAY)
		self.topFrame.pack(side="top", fill="x", pady=10)
		self.setupThresholds()
		self.setupCheckboxes()
		self.setupSyncButton()
		self.setupQueryButtons()

	def updateWidgets(self):
		connLength = len(self.application.c.connections)

		for i in range(0, connLength):
			BACKGROUND = MID_GRAY_1 if i == 0 else DARK_GRAY
			# Frame for Widget
			widgetFrame = tk.Frame(self.connFrame, bg=BACKGROUND)
			widgetFrame.pack(side="top", fill="x")

			# IP Label
			ipLabel = tk.Label(widgetFrame, text='IP: ' + self.application.c.connections[i].ip, bg=BACKGROUND, font='TkDefaultFont 10')
			ipLabel.pack(side="top", fill="x", padx=10, pady=5)
			ipLabel.config(fg=LIGHT_GRAY)
			# IP Status
			ipStatus = tk.Label(widgetFrame, text="Status: Connected", bg=BACKGROUND, font='TkDefaultFont 10')
			ipStatus.pack(side="bottom", fill="x", padx=10, pady=5)
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
		self.updateStatus()

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
			self.voltageEntry.config(fg = 'grey')
		if i == 1:
			self.currentEntry.delete(0, "end")
			self.currentEntry.insert(0, '')
			self.currentEntry.config(fg = 'grey')
		if i == 2:
			self.temperatureEntry.delete(0, "end")
			self.temperatureEntry.insert(0, '')
			self.temperatureEntry.config(fg = 'grey')

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

	def updateEntries(self):
		self.voltageEntry.delete(0, "end")
		self.voltageEntry.insert(0, self.application.c.connections[self.selected].voltageValue)
		self.voltageEntry.config(fg = 'grey')

		self.currentEntry.delete(0, "end")
		self.currentEntry.insert(0, self.application.c.connections[self.selected].currentValue)
		self.currentEntry.config(fg = 'grey')

		self.temperatureEntry.delete(0, "end")
		self.temperatureEntry.insert(0, self.application.c.connections[self.selected].temperatureValue)
		self.temperatureEntry.config(fg = 'grey')

	def updateStatus(self):
		if len(self.application.c.connections) == 0:
			return

		self.widgetFrames[self.selected][2]['fg'] = GREEN
		self.widgetFrames[self.selected][2]['text'] = 'Status: Connected'
		self.application.c.connections[self.selected].currentAck = 0

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
		self.setupButtons()

		# Button Images
		sync_button = Image.open('sync.png')
		sync_image_for_button = ImageTk.PhotoImage(sync_button)
		self.syncButton = tk.Button(self.syncFrame, image=sync_image_for_button, highlightbackground=MID_GRAY_1, highlightcolor=MID_GRAY_1, command=lambda: self.application.inputting('sync'))
		self.syncButton.config(width="20", height="20")
		self.syncButton.pack(side="bottom", padx=50)
		self.syncButton.config(image=sync_image_for_button) 

		self.graph = Graph(self)
		self.graph.run()
		ani = animation.FuncAnimation(self.graph.f, self.graph.animate, interval=1000)
		self.root.mainloop()

