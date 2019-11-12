import tkinter as tk
from tkinter import ttk

HEIGHT = 500
WIDTH = 600

BACKGROUND_COLOR = '#383735'
CONNFRAME_COLOR = '#262523'
DATAFRAME_COLOR = '#464646'

class Monitor:
	def __init__ (self):
		self.root = tk.Tk()

	def setup(self):
		# Main window
		self.root.winfo_toplevel().title("Solar Panel Monitor")
		self.root.geometry('{}x{}'.format(WIDTH, HEIGHT))
		self.root.configure(bg=BACKGROUND_COLOR)

		# Top frame - Debug for commands
		frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
		frame.place(relx=0.5, rely=0.05, relwidth=0.75, relheight=0.1, anchor='n')
		entry = tk.Entry(frame, font=40)
		entry.place(relwidth=0.65, relheight=0.5)
		button = tk.Button(frame, text="Command", font=40, command=lambda: self.inputting(entry.get()))
		button.place(relx=0.7, relwidth=0.3, relheight=0.5)

		# Connection frame
		connFrame = tk.Frame(self.root, bg=CONNFRAME_COLOR)
		connFrame.place(relx=0.2, rely=0.2, relwidth=0.3, relheight=0.7, anchor='n')

		# Frame for Widget -- TODO
		widgetFrame = tk.Frame(connFrame, bg=DATAFRAME_COLOR)
		widgetFrame.place(relx=0.5, rely=0, relwidth=1.0, relheight=0.15, anchor='n')
		# IP Label
		self.ipLabel = tk.Label(widgetFrame, text="IP: XXX.XXX.X.X", bg=DATAFRAME_COLOR, font='TkDefaultFont 10')
		self.ipLabel.place(relx=0, rely=0.15, relwidth=1.0, relheight=0.2)
		self.ipLabel.config(fg="#ababab")
		# IP Status
		self.ipStatus = tk.Label(widgetFrame, text="Status: Not Connected", bg=DATAFRAME_COLOR, font='TkDefaultFont 10')
		self.ipStatus.place(relx=0, rely=0.55, relwidth=1.0, relheight=0.2)
		self.ipStatus.config(fg="#cd5c5c")

		# Data frame
		dataFrame = tk.Frame(self.root, bg='#ababab')
		dataFrame.place(relx=0.67, rely=0.2, relwidth=0.525, relheight=0.7, anchor='n')

		# Threshold Title
		thresholdTitle = tk.Label(dataFrame, text="Thresholds:", bg='#ababab', font='TkDefaultFont 14 bold')
		thresholdTitle.place(relx=0, rely=0, relwidth=0.5, relheight=0.1)
		# Voltage Threshold Label and Entry
		voltageEntryThreshold = tk.Label(dataFrame, text="Voltage: ", bg='#ababab')
		voltageEntryThreshold.place(relx=0, rely=0.1, relwidth=0.25, relheight=0.1)
		voltageEntry = tk.Entry(dataFrame, font=40)
		voltageEntry.place(relx=0.25, rely=0.1, relwidth=0.25, relheight=0.1)
		# Current Threshold Label and Entry
		currentEntryThreshold = tk.Label(dataFrame, text="Current: ", bg='#ababab')
		currentEntryThreshold.place(relx=0, rely=0.2, relwidth=0.25, relheight=0.1)
		currentEntry = tk.Entry(dataFrame, font=40)
		currentEntry.place(relx=0.25, rely=0.2, relwidth=0.25, relheight=0.1)
		# Entry button submission
		thresholdEntryButton = tk.Button(dataFrame, text="OK", font=40, command=lambda: self.thresholdInputting(voltageEntry.get(), currentEntry.get()))
		thresholdEntryButton.place(relx=0.5, rely=0.15, relwidth=0.2, relheight=0.1)

		# OFF/ON Button
		self.togglePowerButton = tk.Button(dataFrame, text="OFF", font=40, command=lambda: self.powerInputting())
		self.togglePowerButton.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.1)

		# SYNC Button
		self.syncButton = tk.Button(self.root, text="SYNC", font=40, command=lambda: self.inputting('sync'))
		self.syncButton.place(relx=0.05, rely=0.9, relwidth=0.1, relheight=0.05)

		# Labels
		self.label = tk.Label(dataFrame, bg='#ababab')
		self.label.place(relx=0, rely=0.3, relwidth=1, relheight=0.8)

		self.connectedLabel = tk.Label(dataFrame, bg='#ababab')
		self.connectedLabel.place(relx=0, rely=0.3, relwidth=1, relheight=0.2)

		# Main loop
		self.root.mainloop()

