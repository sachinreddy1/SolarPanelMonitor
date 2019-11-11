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

		# Frame for Widget
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

