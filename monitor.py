import tkinter as tk
from tkinter import ttk

HEIGHT = 500
WIDTH = 600

LIGHT_GRAY = '#ababab'
MID_GRAY_1 = '#464646'
MID_GRAY_2 = '#383735'
DARK_GRAY = '#262523'
RED = '#cd5c5c'
GREEN = '#32cd32'

class Monitor:
	def __init__ (self, application):
		self.root = tk.Tk()
		self.application = application
		self.widgetFrames = []

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
		dataFrame = tk.Frame(self.root, bg=LIGHT_GRAY)
		dataFrame.place(relx=0.67, rely=0.2, relwidth=0.525, relheight=0.7, anchor='n')

		# Threshold Title
		thresholdTitle = tk.Label(dataFrame, text="Thresholds:", bg=LIGHT_GRAY, font='TkDefaultFont 14 bold')
		thresholdTitle.place(relx=0, rely=0, relwidth=0.5, relheight=0.1)
		# Voltage Threshold Label and Entry
		voltageEntryThreshold = tk.Label(dataFrame, text="Voltage: ", bg=LIGHT_GRAY)
		voltageEntryThreshold.place(relx=0, rely=0.1, relwidth=0.25, relheight=0.1)
		voltageEntry = tk.Entry(dataFrame, font=40)
		voltageEntry.place(relx=0.25, rely=0.1, relwidth=0.25, relheight=0.1)
		# Current Threshold Label and Entry
		currentEntryThreshold = tk.Label(dataFrame, text="Current: ", bg=LIGHT_GRAY)
		currentEntryThreshold.place(relx=0, rely=0.2, relwidth=0.25, relheight=0.1)
		currentEntry = tk.Entry(dataFrame, font=40)
		currentEntry.place(relx=0.25, rely=0.2, relwidth=0.25, relheight=0.1)
		# Entry button submission
		thresholdEntryButton = tk.Button(dataFrame, text="OK", font=40, command=lambda: self.application.thresholdInputting(voltageEntry.get(), currentEntry.get()))
		thresholdEntryButton.place(relx=0.5, rely=0.15, relwidth=0.2, relheight=0.1)

		# OFF/ON Button
		self.togglePowerButton = tk.Button(dataFrame, text="OFF", font=40, command=lambda: self.application.powerInputting())
		self.togglePowerButton.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.1)

		# SYNC Button
		self.syncButton = tk.Button(self.root, text="SYNC", font=40, command=lambda: self.application.inputting('sync'))
		self.syncButton.place(relx=0.05, rely=0.9, relwidth=0.1, relheight=0.05)

		# Labels
		self.label = tk.Label(dataFrame, bg=LIGHT_GRAY)
		self.label.place(relx=0, rely=0.3, relwidth=1, relheight=0.8)

		self.connectedLabel = tk.Label(dataFrame, bg=LIGHT_GRAY)
		self.connectedLabel.place(relx=0, rely=0.3, relwidth=1, relheight=0.2)	

	def updateWidgets(self):
		j = 0
		for i in self.application.c.connections:
			BACKGROUND = MID_GRAY_1 if j == 0 else DARK_GRAY
			# Frame for Widget
			widgetFrame = tk.Frame(self.connFrame, bg=BACKGROUND)
			widgetFrame.place(relx=0.5, rely= j * 0.15, relwidth=1.0, relheight=0.15, anchor='n')

			# IP Label
			ipLabel = tk.Label(widgetFrame, text='IP: ' + i.ip, bg=BACKGROUND, font='TkDefaultFont 10')
			ipLabel.place(relx=0, rely= 0.20, relwidth=1.0, relheight=0.2)
			ipLabel.config(fg=LIGHT_GRAY)
			# IP Status
			ipStatus = tk.Label(widgetFrame, text="Status: Connected", bg=BACKGROUND, font='TkDefaultFont 10')
			ipStatus.place(relx=0, rely= 0.50, relwidth=1.0, relheight=0.2)
			ipStatus.config(fg=GREEN)

			l = [widgetFrame, ipLabel, ipStatus]
			widgetFrame.bind('<Button-1>', lambda event, h=widgetFrame: self.frameInteraction(event, l, BACKGROUND))
			ipLabel.bind('<Button-1>', lambda event, h=ipLabel: self.labelInteraction(event, l))
			ipStatus.bind('<Button-1>', lambda event, h=ipStatus: self.labelInteraction(event, l))
			widgetFrame.bind("<Enter>", lambda event, h=widgetFrame: self.frameInteraction(event, l, BACKGROUND))
			widgetFrame.bind("<Leave>", lambda event, h=widgetFrame: self.frameInteraction(event, l, BACKGROUND))

			self.widgetFrames.append(widgetFrame)
			j += 1

	# ------------- #

	def labelInteraction(self, event, l):
		if event.type is '4': color = MID_GRAY_1	# Clicked
		for i in l: i.configure(bg=color)

	def frameInteraction(self, event, l, bg):
		if event.type is '4': color = MID_GRAY_1	# Clicked
		if event.type is '7': color = MID_GRAY_2	# Entered
		if event.type is '8': color = bg	# Exited
		for i in l: i.configure(bg=color)

	# ------------- #

	def clearWidgets(self):
		for i in self.widgetFrames:
			i.destroy()

	def run(self):
		self.setup()
		self.root.mainloop()

