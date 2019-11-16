import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

HEIGHT = 500
WIDTH = 600

LIGHT_GRAY = '#ababab'
MID_GRAY_1 = '#464646'
MID_GRAY_2 = '#383735'
MID_GRAY_3 = '#31302F'
DARK_GRAY = '#262523'
RED = '#cd5c5c'
GREEN = '#32cd32'

class Monitor:
	def __init__ (self, application):
		self.root = tk.Tk()
		self.application = application
		self.widgetFrames = []
		self.selected = 0

		self.vars = []

	def setup(self):		
		# Main window
		self.root.winfo_toplevel().title("Solar Panel Monitor")
		self.root.geometry('{}x{}'.format(WIDTH, HEIGHT))
		self.root.configure(bg=MID_GRAY_2)

		# Top frame - Debug for commands
		frame = tk.Frame(self.root, bg=MID_GRAY_2)
		frame.place(relx=0.5, rely=0.05, relwidth=0.75, relheight=0.1, anchor='n')

		entry = tk.Entry(frame, font=40)
		entry.place(relwidth=0.65, relheight=0.5)

		button = tk.Button(frame, text="Command", font=40, command=lambda: self.application.inputting(entry.get()))
		button.place(relx=0.7, relwidth=0.3, relheight=0.5)

		# Connection frame
		self.connFrame = tk.Frame(self.root, bg=DARK_GRAY)
		self.connFrame.place(relx=0.2, rely=0.2, relwidth=0.3, relheight=0.7, anchor='n')

		# Data frame
		self.dataFrame = tk.Frame(self.root, bg=LIGHT_GRAY)
		self.dataFrame.place(relx=0.67, rely=0.2, relwidth=0.525, relheight=0.7, anchor='n')

		# Threshold Title
		thresholdTitle = tk.Label(self.dataFrame, text="Thresholds:", bg=LIGHT_GRAY, font='TkDefaultFont 14 bold')
		thresholdTitle.place(relx=0, rely=0, relwidth=0.5, relheight=0.1)

		# Voltage Threshold Label and Entry
		voltageEntryThreshold = tk.Label(self.dataFrame, text="Voltage: ", bg=LIGHT_GRAY)
		voltageEntryThreshold.place(relx=0, rely=0.1, relwidth=0.3, relheight=0.1)
		voltageEntry = tk.Entry(self.dataFrame, font=40)
		voltageEntry.place(relx=0.3, rely=0.1, relwidth=0.2, relheight=0.1)
		# Current Threshold Label and Entry
		currentEntryThreshold = tk.Label(self.dataFrame, text="Current: ", bg=LIGHT_GRAY)
		currentEntryThreshold.place(relx=0, rely=0.2, relwidth=0.3, relheight=0.1)
		currentEntry = tk.Entry(self.dataFrame, font=40)
		currentEntry.place(relx=0.3, rely=0.2, relwidth=0.2, relheight=0.1)
		# Temperature Threshold Label and Entry
		temperatureEntryThreshold = tk.Label(self.dataFrame, text="Temperature: ", bg=LIGHT_GRAY)
		temperatureEntryThreshold.place(relx=0, rely=0.3, relwidth=0.3, relheight=0.1)
		temperatureEntry = tk.Entry(self.dataFrame, font=40)
		temperatureEntry.place(relx=0.3, rely=0.3, relwidth=0.2, relheight=0.1)

		# Output Configuration
		var1 = tk.IntVar()
		checkboxA = tk.Checkbutton(self.dataFrame, text="X", variable=var1, command=lambda: self.updateCheckbox(0))
		checkboxA.place(relx=0.85, rely=0.08, relwidth=0.15, relheight=0.08)
		var2 = tk.IntVar()
		checkboxB = tk.Checkbutton(self.dataFrame, text="CD", variable=var2, command=lambda: self.updateCheckbox(1))
		checkboxB.place(relx=0.85, rely=0.16, relwidth=0.15, relheight=0.08)
		var3 = tk.IntVar()
		checkboxC = tk.Checkbutton(self.dataFrame, text="BC", variable=var3, command=lambda: self.updateCheckbox(2))
		checkboxC.place(relx=0.85, rely=0.24, relwidth=0.15, relheight=0.08)
		var4 = tk.IntVar()
		checkboxD = tk.Checkbutton(self.dataFrame, text="AD", variable=var3, command=lambda: self.updateCheckbox(3))
		checkboxD.place(relx=0.85, rely=0.32, relwidth=0.15, relheight=0.08)

		self.vars = [var1, var2, var3]

		# Entry button submission
		thresholdEntryButton = tk.Button(self.dataFrame, text="OK", font=40, command=lambda: self.application.thresholdInputting(voltageEntry.get(), currentEntry.get(), temperatureEntry.get(), self.selected))
		thresholdEntryButton.place(relx=0.5, rely=0.15, relwidth=0.15, relheight=0.1)

		# OFF/ON Button
		self.togglePowerButton = tk.Button(self.dataFrame, text="OFF", font=40, command=lambda: self.application.powerInputting(self.selected))
		self.togglePowerButton.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.1)

		# SYNC Label
		self.syncFrame = tk.Frame(self.connFrame, bg=MID_GRAY_1)
		self.syncFrame.place(relx=0.5, rely=0.92, relwidth=1.0, relheight=0.08, anchor='n')
		# SYNC Button
		self.syncButton = tk.Button(self.syncFrame, text='sync', font=20, command=lambda: self.application.inputting('sync'))
		self.syncButton.place(relx=0, rely=0, relwidth=0.28, relheight=1.0)

		# Labels
		self.label = tk.Label(self.dataFrame, bg=LIGHT_GRAY)
		self.label.place(relx=0, rely=0.4, relwidth=1, relheight=0.8)

	def updateWidgets(self):
		connLength = len(self.application.c.connections)

		for i in range(0, connLength):
			BACKGROUND = MID_GRAY_1 if i == 0 else DARK_GRAY
			# Frame for Widget
			widgetFrame = tk.Frame(self.connFrame, bg=BACKGROUND)
			widgetFrame.place(relx=0.5, rely= i * 0.15, relwidth=1.0, relheight=0.15, anchor='n')

			# IP Label
			ipLabel = tk.Label(widgetFrame, text='IP: ' + self.application.c.connections[i].ip, bg=BACKGROUND, font='TkDefaultFont 10')
			ipLabel.place(relx=0, rely= 0.20, relwidth=1.0, relheight=0.2)
			ipLabel.config(fg=LIGHT_GRAY)
			# IP Status
			ipStatus = tk.Label(widgetFrame, text="Status: Connected", bg=BACKGROUND, font='TkDefaultFont 10')
			ipStatus.place(relx=0, rely= 0.50, relwidth=1.0, relheight=0.2)
			ipStatus.config(fg=GREEN)

			self.widgetFrames.append([widgetFrame, ipLabel, ipStatus])
			index = len(self.widgetFrames) - 1

			widgetFrame.bind('<Button-1>', lambda event, i=index: self.frameInteraction(event, i, BACKGROUND))
			ipLabel.bind('<Button-1>', lambda event, i=index: self.labelInteraction(event, i))
			ipStatus.bind('<Button-1>', lambda event, i=index: self.labelInteraction(event, i))
			widgetFrame.bind("<Enter>", lambda event, i=index: self.frameInteraction(event, i, BACKGROUND))
			widgetFrame.bind("<Leave>", lambda event, i=index: self.frameInteraction(event, i, BACKGROUND))

	# ------------- #

	def updateCheckbox(self, i):
		for var in self.vars:
			var.set(0)

		for j in range(0, len(self.vars)):
			if j == i:
				self.vars[j].set(1)

		self.application.configSwitchInputting(self.selected, i)

	def labelInteraction(self, event, index):
		if event.type is '4':	# Clicked
			self.clearWidgetColors()
			color = MID_GRAY_1	
			self.selected = index

		for i in self.widgetFrames[index]: i.configure(bg=color)

	def frameInteraction(self, event, index, bg):
		if event.type is '4':	# Clicked
			self.clearWidgetColors()
			color = MID_GRAY_1	
			self.selected = index

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

	def clearWidgets(self):
		for i in self.widgetFrames:
			for j in i:
				j.destroy()

	def run(self):
		self.setup()
		self.updateCheckbox(0)

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

		self.root.mainloop()

